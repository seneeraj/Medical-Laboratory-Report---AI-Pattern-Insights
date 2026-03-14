import pandas as pd
import plotly.express as px
import streamlit as st


# ---------------------------------------------------
# BIOMARKER TABLE
# ---------------------------------------------------

def show_biomarker_table(reference_results):

    if not reference_results:
        st.info("No biomarker data available.")
        return

    rows = []

    for marker, data in reference_results.items():

        rows.append({
            "Biomarker": marker,
            "Value": data.get("value"),
            "Status": data.get("status"),
            "Range": f"{data.get('min')} - {data.get('max')}"
        })

    df = pd.DataFrame(rows)

    st.dataframe(df, use_container_width=True)


# ---------------------------------------------------
# BIOMARKER CHART
# ---------------------------------------------------

import plotly.graph_objects as go


def show_biomarker_chart(lab_data, reference_results=None):
    """
    Clinical range chart:
    - Grey bar = reference (normal) range
    - Vertical marker = patient value
    - Marker color = Low / Normal / High
    """

    if not lab_data or not reference_results:
        return

    rows = []

    for marker, value in lab_data.items():

        if marker not in reference_results:
            continue

        ref = reference_results[marker]

        min_val = ref.get("min")
        max_val = ref.get("max")

        if min_val is None or max_val is None:
            continue

        # determine status
        if value < min_val:
            status = "Low"
        elif value > max_val:
            status = "High"
        else:
            status = "Normal"

        rows.append({
            "marker": marker,
            "value": value,
            "min": min_val,
            "max": max_val,
            "status": status
        })

    if not rows:
        return

    df = pd.DataFrame(rows)

    color_map = {
        "Normal": "#2ecc71",  # green
        "High": "#e74c3c",    # red
        "Low": "#f39c12"      # orange
    }

    fig = go.Figure()

    for i, row in df.iterrows():

        # grey reference range bar
        fig.add_trace(
            go.Bar(
                x=[row["max"] - row["min"]],
                y=[row["marker"]],
                base=row["min"],
                orientation="h",
                marker_color="#E5E7EB",
                hoverinfo="skip",
                showlegend=False
            )
        )

        # patient marker line
        fig.add_shape(
            type="line",
            x0=row["value"],
            x1=row["value"],
            y0=i - 0.35,
            y1=i + 0.35,
            line=dict(
                color=color_map[row["status"]],
                width=4
            )
        )

        # value label
        fig.add_annotation(
            x=row["value"],
            y=row["marker"],
            text=str(row["value"]),
            showarrow=False,
            xanchor="left",
            yanchor="middle",
            font=dict(size=12)
        )

    fig.update_layout(
        height=140 + len(df) * 28,
        margin=dict(l=0, r=0, t=0, b=0),
        barmode="overlay",
        xaxis_title=None,
        yaxis_title=None
    )

    st.plotly_chart(fig, use_container_width=True)
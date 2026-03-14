import streamlit as st
import pandas as pd

from modules.parser import parse_report
from modules.biomarker_mapper import map_biomarkers
from modules.reference_engine import check_reference_ranges
from modules.pattern_engine import detect_patterns
from modules.risk_engine import calculate_risk
from modules.biomarker_filter import filter_biomarkers
from modules.biomarker_derivations import compute_derived_biomarkers
from modules.biomarker_alias_engine import apply_biomarker_aliases
from modules.clinical_patterns import detect_clinical_clusters
from modules.knowledge_graph import detect_graph_patterns
from modules.pattern_aggregator import aggregate_patterns
from modules.pattern_normalizer import normalize_patterns
from modules.clinical_summary import generate_clinical_summary

from modules.visualization import (
    show_biomarker_table,
    show_biomarker_chart
)

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Medical Laboratory Report - AI Patterns Insights",
    layout="wide"
)

st.title("Medical Laboratory Report - AI Patterns Insights")

# ---------------------------------------------------
# SESSION STATE INITIALIZATION
# ---------------------------------------------------

defaults = {
    "analysis_done": False,
    "patterns": [],
    "lab_data": {},
    "reference_results": {},
    "risk_scores": {},
    "health_score": 0,
    "selected_condition": None
}

for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ---------------------------------------------------
# SIDEBAR UPLOAD
# ---------------------------------------------------

with st.sidebar:

    st.header("Upload Lab Report")

    uploaded_file = st.file_uploader(
        "Choose report",
        type=["csv", "xlsx", "xls", "pdf"]
    )

    if uploaded_file:
        st.success("File uploaded successfully")

    analyze_button = st.button("Analyze Report")


# ---------------------------------------------------
# RUN ANALYSIS
# ---------------------------------------------------

if uploaded_file and analyze_button:

    lab_data = parse_report(uploaded_file)

    lab_data = apply_biomarker_aliases(lab_data)
    lab_data = map_biomarkers(lab_data)
    lab_data = filter_biomarkers(lab_data)

    derived = compute_derived_biomarkers(lab_data)
    lab_data.update(derived)

    reference_results = check_reference_ranges(lab_data)

    patterns = detect_patterns(lab_data)
    patterns.extend(detect_clinical_clusters(lab_data))
    patterns.extend(detect_graph_patterns(lab_data))

    patterns = normalize_patterns(patterns)
    patterns = aggregate_patterns(patterns)

    risk_scores = calculate_risk(lab_data)

    health_score = 100 - int(
        (
            risk_scores["metabolic_risk"]
            + risk_scores["cardiovascular_risk"]
            + risk_scores["inflammation_risk"]
        ) / 3
    )

    st.session_state.analysis_done = True
    st.session_state.patterns = patterns
    st.session_state.lab_data = lab_data
    st.session_state.reference_results = reference_results
    st.session_state.risk_scores = risk_scores
    st.session_state.health_score = health_score


# ---------------------------------------------------
# DASHBOARD
# ---------------------------------------------------

if st.session_state.analysis_done:

    patterns = st.session_state.patterns
    lab_data = st.session_state.lab_data
    reference_results = st.session_state.reference_results
    risk_scores = st.session_state.risk_scores
    health_score = st.session_state.health_score

    # ---------------------------------------------------
    # CLINICAL SUMMARY
    # ---------------------------------------------------

    summary = generate_clinical_summary(patterns, lab_data)

    st.subheader("Clinical Summary")

    colA, colB, colC = st.columns(3)

    with colA:
        st.markdown("**Primary Concern**")
        if summary["primary"]:
            for s in summary["primary"]:
                st.write("•", s)
        else:
            st.write("No major primary concern detected")

    with colB:
        st.markdown("**Secondary Findings**")
        if summary["secondary"]:
            for s in summary["secondary"]:
                st.write("•", s)
        else:
            st.write("No secondary findings")

    with colC:
        st.markdown("**Nutritional Issues**")
        if summary["nutrition"]:
            for s in summary["nutrition"]:
                st.write("•", s)
        else:
            st.write("No nutritional deficiencies detected")

    st.divider()

    # ---------------------------------------------------
    # RISK METRICS
    # ---------------------------------------------------

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Health Score", health_score)
    c2.metric("Metabolic Risk", f"{risk_scores['metabolic_risk']}%")
    c3.metric("Cardiovascular Risk", f"{risk_scores['cardiovascular_risk']}%")
    c4.metric("Inflammation Risk", f"{risk_scores['inflammation_risk']}%")

    st.divider()

    # ---------------------------------------------------
    # CONDITIONS PANEL
    # ---------------------------------------------------

    left_panel, right_panel = st.columns([1, 2])

    with left_panel:

        st.subheader("Detected Conditions")

        for p in patterns:

            condition = p["pattern"].replace("_", " ").title()
            evidence = len(p["reasons"])

            col1, col2 = st.columns([4, 1])

            with col1:
                st.write(condition)

            with col2:
                if st.button(str(evidence), key=condition):
                    st.session_state.selected_condition = p

    # ---------------------------------------------------
    # CONDITION DETAILS
    # ---------------------------------------------------

    with right_panel:

        selected = st.session_state.selected_condition

        if selected:

            condition_name = selected["pattern"].replace("_", " ").title()

            st.subheader(condition_name)

            for r in selected["reasons"]:
                st.write("•", r)

            related = []

            for biomarker in lab_data.keys():
                if biomarker.lower() in str(selected["reasons"]).lower():
                    related.append(biomarker)

            if related:

                biomarker_rows = []

                for biomarker in related:

                    if biomarker in reference_results:

                        ref = reference_results[biomarker]

                        biomarker_rows.append({
                            "Biomarker": biomarker,
                            "Value": ref.get("value"),
                            "Status": ref.get("status"),
                            "Range": f"{ref.get('min')} - {ref.get('max')}"
                        })

                if biomarker_rows:

                    df = pd.DataFrame(biomarker_rows)

                    col_table, col_graph = st.columns(2)

                    with col_table:
                        st.dataframe(df, use_container_width=True)

                    with col_graph:
                        show_biomarker_chart(
                            {k: lab_data[k] for k in related if k in lab_data},
                            reference_results
                        )

        else:
            st.info("Click an evidence number to view details.")

    st.divider()

    # ---------------------------------------------------
    # BIOMARKER OVERVIEW
    # ---------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:
        show_biomarker_table(reference_results)

    with col2:
        show_biomarker_chart(lab_data, reference_results)

else:

    st.info("Upload a lab report and click **Analyze Report** to start.")
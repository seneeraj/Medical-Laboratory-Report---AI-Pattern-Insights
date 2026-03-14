import pandas as pd


# Load biomarker reference ranges
def load_reference_ranges():

    df = pd.read_csv("data/biomarker_reference.csv")

    reference_dict = {}

    for i,row in df.iterrows():

        marker = str(row["marker"]).strip()

        reference_dict[marker] = {
            "min": row["min"],
            "max": row["max"],
            "unit": row["unit"]
        }

    return reference_dict


# Check biomarker status
def check_reference_ranges(lab_data):

    reference = load_reference_ranges()

    results = {}

    for marker,value in lab_data.items():

        if marker not in reference:
            continue

        min_val = reference[marker]["min"]
        max_val = reference[marker]["max"]

        if value < min_val:
            status = "Low"

        elif value > max_val:
            status = "High"

        else:
            status = "Normal"

        results[marker] = {
            "value": value,
            "status": status,
            "min": min_val,
            "max": max_val
        }

    return results
import pandas as pd


def normalize(name):
    """
    Convert biomarker names to comparable format
    """
    return name.lower().replace("_", "").replace(" ", "")


def filter_biomarkers(lab_data):

    df = pd.read_csv("data/biomarker_reference.csv")

    valid_markers = df["marker"].tolist()

    # normalize reference markers
    normalized_reference = {normalize(m): m for m in valid_markers}

    filtered = {}

    for marker, value in lab_data.items():

        n_marker = normalize(marker)

        # special alias handling
        if n_marker == "hscrp":
            n_marker = "crp"

        if n_marker in normalized_reference:

            real_name = normalized_reference[n_marker]

            filtered[real_name] = value

    return filtered
import pandas as pd
import os

def apply_biomarker_aliases(lab_data):

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(BASE_DIR, "data", "biomarker_synonyms.csv")

    df = pd.read_csv(path)

    # normalize column names
    df.columns = df.columns.str.lower().str.strip()

    alias_map = {}

    for _, row in df.iterrows():
        alias_map[str(row["synonym"]).lower()] = row["standard"]

    standardized = {}

    for marker, value in lab_data.items():

        key = marker.lower().strip()

        if key in alias_map:
            standardized[alias_map[key]] = value
        else:
            standardized[marker] = value

    return standardized
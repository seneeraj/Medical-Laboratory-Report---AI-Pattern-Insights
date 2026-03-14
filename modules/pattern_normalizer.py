NORMALIZATION_MAP = {

    "diabetes": "diabetes",
    "severe_diabetes": "diabetes",

    "kidney_stress": "kidney_function_risk",
    "kidney_dysfunction": "kidney_function_risk",
    "early_kidney_decline": "kidney_function_risk",

    "chronic_inflammation": "chronic_inflammation",
    "inflammation_risk": "chronic_inflammation",

    "insulin_resistance": "metabolic_risk",
    "metabolic_syndrome": "metabolic_risk",

    "cardiovascular_risk": "cardiovascular_risk",

    "vitamin_d_deficiency": "vitamin_deficiency"
}


def normalize_patterns(patterns):

    normalized = []

    for p in patterns:

        pattern = p["pattern"]

        # normalize incoming name
        key = pattern.lower().replace(" ", "_").strip()

        normalized_name = NORMALIZATION_MAP.get(key, key)

        normalized.append({
            "pattern": normalized_name,
            "description": p["description"]
        })

    return normalized
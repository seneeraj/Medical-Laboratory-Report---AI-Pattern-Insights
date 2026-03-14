import json
import os


def detect_patterns(data):

    patterns = []

    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    path = os.path.join(BASE_DIR, "data", "pattern_rules.json")

    with open(path) as f:
        rules = json.load(f)

    for rule in rules:

        conditions_met = True

        for biomarker, condition in rule["conditions"].items():

            value = data.get(biomarker)

            if value is None:
                conditions_met = False
                break

            if ">" in condition and not value > condition[">"]:
                conditions_met = False

            if "<" in condition and not value < condition["<"]:
                conditions_met = False

        if conditions_met:
            patterns.append({
                "pattern": rule["pattern"],
                "description": rule["description"]
            })

    return patterns
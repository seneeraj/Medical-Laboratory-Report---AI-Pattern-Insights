import re


import re

def normalize(text):

    text = text.lower()

    # remove punctuation
    text = re.sub(r'[^a-z0-9\s]', ' ', text)

    # collapse spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def map_biomarkers(lab_data):

    print("Mapper running Initialize...")

    mapped = {}

    for marker, value in lab_data.items():

        name = normalize(marker)

        print("Checking:", name)

        if "glycosylated hemoglobin" in name or "hba1c" in name or "a1c" in name:
            mapped["HbA1c"] = value
            print("Mapped HbA1c")

        elif "glucose fasting" in name:
            mapped["Glucose_Fasting"] = value
            print("Mapped Glucose Fasting")

        elif "glucose post prandial" in name:
            mapped["Glucose_PP"] = value
            print("Mapped Glucose PP")

        elif "hdl cholesterol" in name:
            mapped["HDL"] = value
            print("Mapped HDL")

        elif "ldl cholesterol" in name:
            mapped["LDL"] = value
            print("Mapped LDL")

        elif "triglycerides" in name:
            mapped["Triglycerides"] = value
            print("Mapped Triglycerides")

        elif "creatinine" in name:
            mapped["Creatinine"] = value
            print("Mapped Creatinine")

        elif "egfr" in name:
            mapped["eGFR"] = value
            print("Mapped eGFR")

        elif "vitamin d" in name:
            mapped["Vitamin_D"] = value
            print("Mapped Vitamin D")

        elif "c reactive protein" in name:
            mapped["hsCRP"] = value
            print("Mapped hsCRP")

        elif "thyroid stimulating hormone" in name or name == "tsh":
            mapped["TSH"] = value
            print("Mapped TSH")

    return mapped
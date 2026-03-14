import pdfplumber
import pandas as pd
import re


# ----------------------------------------------------
# MAIN PARSER ROUTER
# ----------------------------------------------------

def parse_report(file):

    filename = file.name.lower()

    if filename.endswith(".csv"):
        return parse_csv(file)

    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        return parse_excel(file)

    elif filename.endswith(".pdf"):
        return parse_pdf(file)

    else:
        raise ValueError("Unsupported file format")


# ----------------------------------------------------
# CSV PARSER
# ----------------------------------------------------

def parse_csv(file):

    df = pd.read_csv(file)

    lab_data = {}

    for _, row in df.iterrows():

        try:
            marker = str(row[0]).strip()
            value = float(row[1])
            lab_data[marker] = value
        except:
            continue

    return lab_data


# ----------------------------------------------------
# EXCEL PARSER
# ----------------------------------------------------

def parse_excel(file):

    df = pd.read_excel(file)

    lab_data = {}

    for _, row in df.iterrows():

        try:
            marker = str(row[0]).strip()
            value = float(row[1])
            lab_data[marker] = value
        except:
            continue

    return lab_data


# ----------------------------------------------------
# HELPER: CLEAN MARKER NAME
# ----------------------------------------------------

def clean_marker(marker):

    if marker is None:
        return None

    marker = str(marker)

    # remove newline characters
    marker = marker.replace("\n", " ")

    # remove extra spaces
    marker = re.sub(r"\s+", " ", marker)

    # remove method names in brackets
    marker = re.sub(r"\(.*?\)", "", marker)

    # remove trailing method descriptions
    marker = marker.split("  ")[0]

    marker = marker.strip()

    return marker


# ----------------------------------------------------
# HELPER: INVALID ROW FILTER
# ----------------------------------------------------

def is_valid_marker(marker):

    if marker is None:
        return False

    marker = str(marker).strip()

    if marker == "":
        return False

    invalid_keywords = [
        "reference",
        "interpretation",
        "comment",
        "note",
        "category",
        "optimal",
        "borderline",
        "risk",
        "therapy",
        "goal",
        "status",
        "table",
        "range"
    ]

    marker_lower = marker.lower()

    for word in invalid_keywords:
        if word in marker_lower:
            return False

    # reject numeric-only markers
    if re.fullmatch(r"\d+\.?\d*", marker):
        return False

    return True


# ----------------------------------------------------
# PDF PARSER
# ----------------------------------------------------

def parse_pdf(file):

    lab_data = {}

    with pdfplumber.open(file) as pdf:

        for page in pdf.pages:

            tables = page.extract_tables()

            if not tables:
                continue

            for table in tables:

                for row in table:

                    # safety checks
                    if not row:
                        continue

                    if len(row) < 2:
                        continue

                    raw_marker = row[0]
                    raw_value = row[1]

                    if raw_marker is None or raw_value is None:
                        continue

                    marker = clean_marker(raw_marker)
                    value = str(raw_value).strip()

                    if marker is None or marker == "":
                        continue

                    # skip obvious non-test rows
                    invalid_words = [
                        "reference",
                        "interpretation",
                        "comment",
                        "note",
                        "range",
                        "risk",
                        "status",
                        "category",
                        "optimal",
                        "borderline",
                        "therapy",
                        "goal"
                    ]

                    marker_lower = marker.lower()

                    if any(word in marker_lower for word in invalid_words):
                        continue

                    # remove flags like H*, L*
                    value = value.replace("H*", "")
                    value = value.replace("L*", "")
                    value = value.replace("*", "")

                    # extract numeric value
                    match = re.search(r"\d+\.?\d*", value)

                    if not match:
                        continue

                    try:
                        numeric_value = float(match.group())
                    except:
                        continue

                    # remove duplicate spaces
                    marker = re.sub(r"\s+", " ", marker).strip()

                    # store biomarker
                    lab_data[marker] = numeric_value

    return lab_data
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
            value = extract_numeric(row[1])

            if marker and value is not None:
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
            value = extract_numeric(row[1])

            if marker and value is not None:
                lab_data[marker] = value

        except:
            continue

    return lab_data


# ----------------------------------------------------
# CLEAN MARKER NAME
# ----------------------------------------------------

def clean_marker(marker):

    if marker is None:
        return None

    marker = str(marker)

    marker = marker.replace("\n", " ")
    marker = re.sub(r"\(.*?\)", "", marker)
    marker = re.sub(r"\s+", " ", marker)

    return marker.strip()


# ----------------------------------------------------
# INVALID ROW FILTER
# ----------------------------------------------------

def is_valid_marker(marker):

    if marker is None:
        return False

    marker = marker.lower()

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
        "range",
        "ratio",
        "index",
        "calculated",
        "method"
    ]

    for word in invalid_keywords:
        if word in marker:
            return False

    if re.fullmatch(r"\d+\.?\d*", marker):
        return False

    return True


# ----------------------------------------------------
# EXTRACT NUMERIC VALUE
# ----------------------------------------------------

def extract_numeric(value):

    if value is None:
        return None

    value = str(value)

    value = value.replace("H*", "")
    value = value.replace("L*", "")
    value = value.replace("*", "")

    numbers = re.findall(r"\d+\.\d+|\d+", value)

    if numbers:
        try:
            return float(numbers[0])
        except:
            return None

    return None


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

                    if not row or len(row) < 2:
                        continue

                    raw_marker = row[0]
                    raw_value = row[1]

                    if raw_marker is None or raw_value is None:
                        continue

                    marker = clean_marker(raw_marker)

                    if not is_valid_marker(marker):
                        continue

                    numeric_value = extract_numeric(raw_value)

                    if numeric_value is None:
                        continue

                    lab_data[marker] = numeric_value

    return lab_data

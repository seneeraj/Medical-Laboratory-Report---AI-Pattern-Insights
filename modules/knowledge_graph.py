import networkx as nx


def build_medical_graph():

    G = nx.Graph()

    # biomarker nodes
    biomarkers = [
        "HbA1c", "Glucose", "Triglycerides", "HDL",
        "LDL", "CRP", "Vitamin D", "Creatinine", "eGFR"
    ]

    # disease nodes
    diseases = [
        "Diabetes",
        "Insulin Resistance",
        "Metabolic Syndrome",
        "Cardiovascular Risk",
        "Chronic Inflammation",
        "Kidney Dysfunction"
    ]

    for b in biomarkers:
        G.add_node(b, type="biomarker")

    for d in diseases:
        G.add_node(d, type="disease")

    # relationships
    edges = [

        ("HbA1c", "Diabetes"),
        ("Glucose", "Diabetes"),

        ("Triglycerides", "Insulin Resistance"),
        ("HDL", "Insulin Resistance"),

        ("Triglycerides", "Metabolic Syndrome"),
        ("HDL", "Metabolic Syndrome"),
        ("Glucose", "Metabolic Syndrome"),

        ("LDL", "Cardiovascular Risk"),
        ("HDL", "Cardiovascular Risk"),

        ("CRP", "Chronic Inflammation"),
        ("Vitamin D", "Chronic Inflammation"),

        ("Creatinine", "Kidney Dysfunction"),
        ("eGFR", "Kidney Dysfunction"),
    ]

    for e in edges:
        G.add_edge(*e)

    return G


def detect_graph_patterns(data):

    G = build_medical_graph()

    detected = []

    for biomarker, value in data.items():

        if value is None:
            continue

        if biomarker not in G:
            continue

        neighbors = G.neighbors(biomarker)

        for disease in neighbors:

            detected.append({
                "pattern": disease,
                "description": f"{biomarker} is associated with {disease} risk."
            })

    return detected
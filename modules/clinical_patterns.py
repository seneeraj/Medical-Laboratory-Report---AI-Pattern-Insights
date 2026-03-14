def detect_clinical_clusters(data):

    clusters = []

    glucose = data.get("Glucose")
    HbA1c = data.get("HbA1c")
    triglycerides = data.get("Triglycerides")
    HDL = data.get("HDL")
    LDL = data.get("LDL")
    crp = data.get("CRP")
    vitamin_d = data.get("Vitamin D")
    egfr = data.get("eGFR")

    # -----------------------
    # INSULIN RESISTANCE
    # -----------------------

    if triglycerides and HDL:

        tg_hdl = triglycerides / HDL

        if tg_hdl > 3:

            clusters.append({
                "pattern": "insulin_resistance",
                "description": "Triglyceride/HDL ratio suggests insulin resistance."
            })

    # -----------------------
    # METABOLIC SYNDROME
    # -----------------------

    if triglycerides and HDL and glucose:

        if triglycerides > 150 and HDL < 40 and glucose > 100:

            clusters.append({
                "pattern": "metabolic_syndrome",
                "description": "Combination of triglycerides, HDL and glucose indicates metabolic syndrome."
            })

    # -----------------------
    # CARDIOMETABOLIC RISK
    # -----------------------

    if LDL and HDL:

        if LDL > 120 and HDL < 40:

            clusters.append({
                "pattern": "cardiometabolic_risk",
                "description": "Cholesterol imbalance indicates cardiometabolic risk."
            })

    # -----------------------
    # CHRONIC INFLAMMATION
    # -----------------------

    if crp and vitamin_d:

        if crp > 1 and vitamin_d < 30:

            clusters.append({
                "pattern": "chronic_inflammation",
                "description": "CRP elevation combined with Vitamin D deficiency suggests chronic inflammation."
            })

    # -----------------------
    # EARLY KIDNEY DECLINE
    # -----------------------

    if egfr and egfr < 90:

        clusters.append({
            "pattern": "early_kidney_decline",
            "description": "Reduced filtration rate may indicate early kidney decline."
        })

    return clusters
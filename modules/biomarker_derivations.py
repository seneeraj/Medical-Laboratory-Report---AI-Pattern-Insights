def compute_derived_biomarkers(data):

    derived = {}

    triglycerides = data.get("Triglycerides")
    hdl = data.get("HDL")
    ldl = data.get("LDL")
    total_chol = data.get("Total Cholesterol")
    bun = data.get("Urea/BUN")
    creatinine = data.get("Creatinine")

    # -------------------------
    # TRIGLYCERIDE / HDL RATIO
    # -------------------------

    if triglycerides and hdl and hdl != 0:

        derived["TG_HDL_Ratio"] = triglycerides / hdl

    # -------------------------
    # LDL / HDL RATIO
    # -------------------------

    if ldl and hdl and hdl != 0:

        derived["LDL_HDL_Ratio"] = ldl / hdl

    # -------------------------
    # TOTAL CHOLESTEROL / HDL
    # -------------------------

    if total_chol and hdl and hdl != 0:

        derived["Chol_HDL_Ratio"] = total_chol / hdl

    # -------------------------
    # BUN / CREATININE RATIO
    # -------------------------

    if bun and creatinine and creatinine != 0:

        derived["BUN_Creatinine_Ratio"] = bun / creatinine

    return derived
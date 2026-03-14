def calculate_risk(data):

    metabolic = 0
    cardio = 0
    inflammation = 0

    HbA1c = data.get("HbA1c")
    triglycerides = data.get("Triglycerides")
    HDL = data.get("HDL")
    LDL = data.get("LDL")
    crp = data.get("CRP")
    egfr = data.get("eGFR")
    vitamin_d = data.get("Vitamin D")

    # -----------------------
    # METABOLIC RISK
    # -----------------------

    if HbA1c:

        if HbA1c > 9:
            metabolic += 70
        elif HbA1c > 6.5:
            metabolic += 50
        elif HbA1c > 5.7:
            metabolic += 25

    if triglycerides and triglycerides > 150:
        metabolic += 10

    if HDL and HDL < 40:
        metabolic += 10

    if vitamin_d and vitamin_d < 20:
        metabolic += 10

    # -----------------------
    # CARDIOVASCULAR RISK
    # -----------------------

    if LDL and LDL > 130:
        cardio += 40

    if HDL and HDL < 40:
        cardio += 20

    if triglycerides and triglycerides > 150:
        cardio += 20

    if egfr and egfr < 90:
        cardio += 10

    # -----------------------
    # INFLAMMATION RISK
    # -----------------------

    if crp:

        if crp > 3:
            inflammation += 60
        elif crp > 1:
            inflammation += 30

    # cap risks
    metabolic = min(metabolic, 100)
    cardio = min(cardio, 100)
    inflammation = min(inflammation, 100)

    return {
        "metabolic_risk": metabolic,
        "cardiovascular_risk": cardio,
        "inflammation_risk": inflammation
    }
def generate_clinical_summary(patterns, lab_data):
    """
    Generate a structured clinical summary grouped by organ systems.
    Removes duplicate findings and produces doctor-style sentences.
    """

    summary = {
        "primary": set(),
        "secondary": set(),
        "nutrition": set()
    }

    for p in patterns:

        pattern = p.get("pattern", "").lower()

        # -------------------------
        # DIABETES / METABOLIC
        # -------------------------

        if "diabetes" in pattern:

            hba1c = lab_data.get("HbA1c")

            if hba1c:
                summary["primary"].add(
                    f"Severe glycemic dysregulation detected (HbA1c {hba1c}%)"
                )

        # -------------------------
        # KIDNEY FUNCTION
        # -------------------------

        if "kidney" in pattern:

            egfr = lab_data.get("eGFR")

            if egfr:
                summary["secondary"].add(
                    f"Reduced kidney filtration capacity observed (eGFR {egfr})"
                )

        # -------------------------
        # CARDIOVASCULAR
        # -------------------------

        if "cardiovascular" in pattern:

            ldl = lab_data.get("LDL")
            hdl = lab_data.get("HDL")

            if ldl or hdl:
                summary["secondary"].add(
                    "Lipid profile imbalance suggests elevated cardiovascular risk"
                )

        # -------------------------
        # INFLAMMATION
        # -------------------------

        if "inflammation" in pattern:

            crp = lab_data.get("CRP")

            if crp:
                summary["secondary"].add(
                    f"Systemic inflammatory activity indicated by CRP level ({crp})"
                )

        # -------------------------
        # VITAMIN DEFICIENCY
        # -------------------------

        if "vitamin" in pattern:

            vitd = lab_data.get("Vitamin D")

            if vitd:
                summary["nutrition"].add(
                    f"Vitamin D deficiency detected (Vitamin D {vitd})"
                )

    # convert sets → lists
    return {
        "primary": list(summary["primary"]),
        "secondary": list(summary["secondary"]),
        "nutrition": list(summary["nutrition"])
    }
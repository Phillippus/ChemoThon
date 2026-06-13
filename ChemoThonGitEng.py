import streamlit as st
import json

def load_chemotherapy_data():
    """Loads all chemotherapy data from a JSON file."""
    try:
        with open('data/chemotherapyGITENG.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Chemotherapy data file not found. Please ensure the JSON file is in the 'data' directory.")
        return None
    except json.JSONDecodeError:
        st.error("Error decoding JSON. Please check the file format.")
        return None

def calculate_bsa(weight, height):
    """Calculates body surface area using the DuBois formula."""
    return round((weight ** 0.425) * (height ** 0.725) * 0.007184, 2)

def calculate_cisplatin_doses(total_dose):
    """Calculates the infusion breakdown for cisplatin when the dose exceeds 50 mg."""
    dose_split = []
    while total_dose > 0:
        infusion_dose = min(50, total_dose)
        dose_split.append(infusion_dose)
        total_dose -= infusion_dose
    return dose_split

def display_chemotherapy_details(protocol, bsa, weight, crcl=None, auc=None):
    """Displays details of the selected chemotherapy protocol."""
    st.write(f"### Protocol: {protocol['name']}")

    # Display chemotherapy drugs with calculated doses
    st.write("#### Chemotherapy Drugs")
    calculated_doses = {}
    for drug in protocol.get("Chemo", []):
        if drug["Name"].lower() == "carboplatin":
            # Calculate carboplatin dose if AUC and CrCl are provided
            if auc and crcl:
                dose = round((crcl + 25) * auc, 2)
            else:
                dose = "requires AUC and CrCl"
        elif drug["Name"].lower() == "cisplatin":
            # Calculate cisplatin dose
            dose = round(drug["Dosage"] * (weight if "mg/kg" in drug["DosageMetric"] else bsa), 2)
        elif drug["Name"].lower() == "mitomycin":
            # Calculate mitomycin dose and enforce the cap
            dose = round(drug["Dosage"] * bsa, 2)
            if dose > 20:  # Apply the cap for all Mitomycin regimens
                st.error("⚠️ Dose of Mitomycin must not exceed 20 mg!")
                dose = 20
        else:
            # Calculate dose for other drugs using BSA or weight
            dose = round(drug["Dosage"] * (weight if "mg/kg" in drug["DosageMetric"] else bsa), 2)
        
        calculated_doses[drug["Name"].lower()] = dose
        st.write(f"{drug['Name']} {drug['Dosage']} {drug['DosageMetric']} ......... {dose if isinstance(dose, (int, float)) else dose} mg D{drug['Day']}")

    st.write(f"**Next Cycle:** {protocol.get('NextCycle', 'Unknown')} days")

    # Premedication
    premed_note = protocol.get("Day1", {}).get("Premed", {}).get("Note", "")
    if premed_note:
        st.write("#### Day 1 - Premedication")
        st.write(premed_note)

    # Day 1 Chemotherapy Instructions
    st.write("#### Day 1 - Chemotherapy Instructions")
    for instruction in protocol.get("Day1", {}).get("Instructions", []):
        drug_name = instruction.get("Name", "Unknown").lower()
        calculated_dose = calculated_doses.get(drug_name, "dose unavailable")

        # Display carboplatin dose dynamically
        if drug_name == "carboplatin" and isinstance(calculated_dose, (int, float)):
            st.write(f"{instruction['Name']} - {calculated_dose} mg, {instruction.get('Instruction', 'No instructions available.')}")
        elif drug_name == "carboplatin":
            st.write(f"{instruction['Name']} - requires AUC and CrCl, {instruction.get('Instruction', 'No instructions available.')}")
        
        # Handle cisplatin dose splitting
        elif drug_name == "cisplatin" and isinstance(calculated_dose, (int, float)):
            if calculated_dose > 50:
                cisplatin_split = calculate_cisplatin_doses(calculated_dose)
                for i, dose_split in enumerate(cisplatin_split, start=1):
                    st.write(f"{instruction['Name']} - {dose_split} mg in 500ml normal saline (NS), infusion {i}. {instruction.get('Instruction', '')}")
                # Add Mannitol after the last Cisplatin infusion
                st.write("Mannitol 10% 250 ml IV infusion - Administer after the last Cisplatin infusion.")
            else:
                st.write(f"{instruction['Name']} - {calculated_dose} mg in 500ml normal saline (NS), {instruction.get('Instruction', '')}")
                # Add Mannitol after a single Cisplatin infusion
                st.write("Mannitol 10% 250 ml IV infusion - Administer after the Cisplatin infusion.")
        
        # Handle other drugs
        else:
            st.write(f"{instruction['Name']} - {calculated_dose} mg, {instruction.get('Instruction', 'No instructions available.')}")


def display_simple_json(filename, bsa, weight=None):
    """Display regimen from individual JSON file (flat-dose / BSA / weight-based)."""
    try:
        with open(f'data/{filename}', 'r') as f:
            reg = json.load(f)
    except Exception as e:
        st.error(f"Error loading {filename}: {e}")
        return
    st.write("#### Chemotherapy Drugs")
    for drug in reg.get("Chemo", []):
        metric = drug.get("DosageMetric", "")
        dosage = drug.get("Dosage", 0)
        if "mg/kg" in metric and weight:
            calculated = round(dosage * weight, 2)
            st.write(f"{drug['Name']} {dosage} {metric} ......... {calculated} mg D{drug['Day']}")
        elif "mg/m2" in metric:
            calculated = round(dosage * bsa, 2)
            st.write(f"{drug['Name']} {dosage} {metric} ......... {calculated} mg D{drug['Day']}")
        else:
            st.write(f"{drug['Name']} {dosage} {metric} D{drug['Day']}")
    st.write(f"**Next Cycle:** {reg.get('NC', '?' )} days")
    premed = reg.get("Day1", {}).get("Premed", {}).get("Note", "")
    if premed:
        st.write("#### D1 - Premedication")
        st.write(premed)
    instructions = reg.get("Day1", {}).get("Instructions", [])
    if instructions:
        st.write("#### D1 - Chemotherapy Instructions")
        chemo_list = reg.get("Chemo", [])
        for inst in instructions:
            drug_name = inst.get("Name", "")
            inst_text = inst.get("Inst", "")
            drug = next((d for d in chemo_list if d["Name"] == drug_name), None)
            if drug:
                metric = drug.get("DosageMetric", "")
                dosage = drug.get("Dosage", 0)
                if "mg/kg" in metric and weight:
                    calc_dose = round(dosage * weight, 2)
                elif "mg/m2" in metric:
                    calc_dose = round(dosage * bsa, 2)
                else:
                    calc_dose = dosage
                st.write(f"{drug_name} - {calc_dose} mg, {inst_text}")
            else:
                st.write(f"{drug_name} - {inst_text}")

def main():
    st.title("ChemoThon Gastrointestinal (Except CRC) v 3.2 ENG")
    st.write("""Welcome to ChemoThon!
This application provides assistance in prescribing chemotherapy regimens based on body surface area (BSA), weight, or AUC for carboplatin-based treatments.
Please ensure that doses are adjusted to align with the packaging and protocols available in your country. Users bear full responsibility for applying this tool in clinical practice.

We welcome your feedback to improve this app further. Feel free to reach out at filip.kohutek@fntn.sk.""")


    # Load chemotherapy data
    data = load_chemotherapy_data()
    if not data:
        return

    # User input for weight and height
    weight = st.number_input("Enter weight (kg):", min_value=1, max_value=200, step=1, value=None, format="%d")
    height = st.number_input("Enter height (cm):", min_value=1, max_value=250, step=1, value=None, format="%d")

    # Calculate BSA
    if st.button("Calculate BSA") and weight and height:
        bsa_val = calculate_bsa(weight, height)
        st.session_state['bsa'] = bsa_val
        st.session_state['weight'] = weight

    # Show chemotherapy regimen options after BSA is calculated
    if st.session_state.get("bsa"):
        st.write(f"**Body Surface Area (BSA):** {st.session_state['bsa']:.2f} m²")
        weight_val = st.session_state.get('weight', weight) or weight

        chemo_names = [protocol["name"] for protocol in data["chemotherapies"]]
        # New regimens (added 2026-06)
        extra_new = [
            "Nivolumab 360 mg flat + FOLFOX/CAPOX (gastric/GEJ CPS≥5, CheckMate-649)",
            "Trastuzumab-deruxtecan 6.4 mg/kg (HER2+ gastric 2L, DESTINY-Gastric01)",
            "Ramucirumab 8 mg/kg q2w (gastric 2L, REGARD)",
            "Ramucirumab + Paclitaxel weekly (gastric 2L, RAINBOW)",
        ]
        selected_protocol_name = st.selectbox("Select a chemotherapy regimen:", chemo_names + extra_new)

        # Input CrCl and AUC for carboplatin-based regimens
        crcl = None
        auc = None
        protocol = None
        if selected_protocol_name not in extra_new:
            protocol = next((p for p in data["chemotherapies"] if p["name"] == selected_protocol_name), None)
            if protocol and any("carboplatin" in drug["Name"].lower() for drug in protocol.get("Chemo", [])):
                crcl = st.number_input("Enter Creatinine Clearance (CrCl in mL/min):", min_value=1, max_value=200, step=1, value=None, format="%d")
                if crcl is not None and crcl < 30:
                    st.error("⚠️ Your patient seems to be platinum-ineligible!")
                auc = st.number_input("Enter Area Under Curve (AUC, 2-6):", min_value=2, max_value=6, step=1, value=None, format="%d")
                if selected_protocol_name.lower() == "cross regimen" and auc != 2:
                    st.warning("⚠️ For the CROSS regimen, the AUC value must be set to 2!")

        if st.button("Display Protocol"):
            if selected_protocol_name == "Nivolumab 360 mg flat + FOLFOX/CAPOX (gastric/GEJ CPS≥5, CheckMate-649)":
                display_simple_json("nivolumab_gastric.json", st.session_state["bsa"], weight_val)
            elif selected_protocol_name == "Trastuzumab-deruxtecan 6.4 mg/kg (HER2+ gastric 2L, DESTINY-Gastric01)":
                display_simple_json("tdx_gastric.json", st.session_state["bsa"], weight_val)
            elif selected_protocol_name == "Ramucirumab 8 mg/kg q2w (gastric 2L, REGARD)":
                display_simple_json("ramucirumab.json", st.session_state["bsa"], weight_val)
            elif selected_protocol_name == "Ramucirumab + Paclitaxel weekly (gastric 2L, RAINBOW)":
                display_simple_json("ramucirumab_paclitaxel.json", st.session_state["bsa"], weight_val)
            elif protocol:
                display_chemotherapy_details(protocol, st.session_state["bsa"], weight_val, crcl, auc)
            else:
                st.error("Selected protocol not found in the data.")

if __name__ == "__main__":
    main()



# ===== Zdroje / Sources (pridané 2026-06, aditívne) =====
with st.expander("📚 Zdroje k režimom / Sources"):
    st.markdown("""**Key references – GI cancers (excl. CRC)**

Guidelines: [ESMO](https://www.esmo.org/guidelines/esmo-clinical-practice-guidelines-gastrointestinal-cancers) · [NCCN](https://www.nccn.org/guidelines/category_1). Always verify against the current guideline version and available drug vial sizes. As of: June 2026.

- **FLOT (perioperačne)** — FLOT4 – Al-Batran et al., Lancet 2019.
- **EOX / ECX** — REAL-2 – Cunningham et al., NEJM 2008.
- **Paklitaxel weekly (gastrický, 2. línia)** — +ramucirumab RAINBOW – Wilke et al., Lancet Oncol 2014.
- **CROSS (karboplatina/paklitaxel + RT)** — van Hagen et al., NEJM 2012 (CROSS).
- **FOLFIRINOX (pankreas)** — Conroy et al., NEJM 2011 (PRODIGE 4/ACCORD 11).
- **Gemcitabín / kapecitabín** — Cunningham et al., J Clin Oncol 2009.
- **Gemcitabín / nab-paklitaxel** — MPACT – Von Hoff et al., NEJM 2013.
- **NALIRI / 5-FU (lipozomálny irinotekan)** — NAPOLI-1 – Wang-Gillam et al., Lancet 2016.
- **NALIRIFOX** — NAPOLI-3 – Wainberg et al., Lancet 2023.
- **Gemcitabín (monoterapia)** — Burris et al., J Clin Oncol 1997.
- **Mitomycín / 5-FU (anál)** — Nigro / RTOG 98-11 – Ajani et al., JAMA 2008.

**Current standards to consider (not yet in tool):**
- **Nivolumab + chemoterapia (CPS≥5) gastrický** — CheckMate-649, Lancet 2021 → teraz v nástroji.
- Pembrolizumab + trastuzumab + chemo pri HER2+ gastrickom – KEYNOTE-811, Nature 2024.
- **T-DXd 6.4 mg/kg gastric** — DESTINY-Gastric01, NEJM 2020 → teraz v nástroji.
- **Ramucirumab ± paklitaxel (gastric 2L)** — REGARD/RAINBOW → teraz v nástroji.
- Zolbetuximab + chemo pri CLDN18.2+ – SPOTLIGHT/GLOW, Lancet 2023.""")

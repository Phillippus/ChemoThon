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
        if drug["Name"] == "carboplatin":
            if auc and crcl:
                dose = (crcl + 25) * auc
            else:
                dose = "requires AUC and CrCl"
        else:
            dose = round(drug["Dosage"] * (weight if "mg/kg" in drug["DosageMetric"] else bsa), 2)
        
        calculated_doses[drug["Name"]] = dose
        st.write(f"{drug['Name']} {drug['Dosage']} {drug['DosageMetric']} ......... {dose} mg D{drug['Day']}")

    st.write(f"**Next Cycle:** {protocol.get('NextCycle', 'Unknown')} days")

    # Premedication
    premed_note = protocol.get("Day1", {}).get("Premed", {}).get("Note", "")
    if premed_note:
        st.write("#### Day 1 - Premedication")
        st.write(premed_note)

    # Day 1 Chemotherapy Instructions
    st.write("#### Day 1 - Chemotherapy Instructions")
    for instruction in protocol.get("Day1", {}).get("Instructions", []):
        drug_name = instruction.get("Name", "Unknown")
        calculated_dose = calculated_doses.get(drug_name, "dose unavailable")
        if drug_name == "cisplatin" and isinstance(calculated_dose, (int, float)) and calculated_dose > 50:
            cisplatin_split = calculate_cisplatin_doses(calculated_dose)
            for i, dose_split in enumerate(cisplatin_split, start=1):
                st.write(f"{drug_name} - {dose_split} mg in 500ml normal saline (NS), infusion {i}. {instruction.get('Instruction', '')}")
        elif drug_name == "carboplatin" and isinstance(calculated_dose, (int, float)):
            st.write(f"{drug_name} - {calculated_dose} mg, {instruction.get('Instruction', 'No instructions available.')}")
        else:
            st.write(f"{drug_name} - {calculated_dose} mg, {instruction.get('Instruction', 'No instructions available.')}")


def calculate_bsa(weight, height):
    """Calculates body surface area using the DuBois formula."""
    return round((weight ** 0.425) * (height ** 0.725) * 0.007184, 2)

def main():
    st.title("ChemoThon Gastrointestinal (Except CRC) v 3.0 ENG")
    st.write("This program prescribes chemotherapy regimens based on body surface area (BSA), weight, or AUC for carboplatin-based regimens.")

    # Load chemotherapy data
    data = load_chemotherapy_data()
    if not data:
        return

    # User input for weight and height without default values
    weight = st.number_input("Enter weight (kg):", min_value=1, max_value=200, step=1, value=None, format="%d")
    height = st.number_input("Enter height (cm):", min_value=1, max_value=250, step=1, value=None, format="%d")

    # Ensure inputs are provided before proceeding
    if not weight or not height:
        st.warning("Please enter valid weight and height to proceed.")
        return

    # Calculate BSA
    if "bsa" not in st.session_state:
        st.session_state["bsa"] = None

    if st.button("Calculate BSA"):
        bsa = calculate_bsa(weight, height)
        st.session_state['bsa'] = bsa
        st.success(f"Calculated Body Surface Area (BSA): {bsa:.2f} m²")

    # Show chemotherapy regimen options after BSA is calculated
    if st.session_state["bsa"]:
        st.write(f"**Current BSA:** {st.session_state['bsa']:.2f} m²")
        chemo_names = [protocol["name"] for protocol in data["chemotherapies"]]
        selected_protocol_name = st.selectbox("Select a chemotherapy regimen:", chemo_names)

        # Carboplatin inputs only for carboplatin-based regimens
        crcl = None
        auc = None
        if selected_protocol_name and "carboplatin" in selected_protocol_name.lower():
            crcl = st.number_input("Enter CrCl (ml/min) for carboplatin (if applicable):", min_value=1, max_value=200, step=1, value=None, format="%d")
            auc = st.number_input("Enter AUC for carboplatin (if applicable):", min_value=2, max_value=6, step=1, value=None, format="%d")

        if st.button("Display Protocol"):
            protocol = next((p for p in data["chemotherapies"] if p["name"] == selected_protocol_name), None)
            if protocol:
                display_chemotherapy_details(protocol, st.session_state["bsa"], weight, crcl, auc)
            else:
                st.error("Selected protocol not found in the data.")

if __name__ == "__main__":
    main()
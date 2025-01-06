import streamlit as st
import json

def load_chemotherapy_data():
    """Loads all chemotherapy data from the consolidated JSON file."""
    try:
        with open('data/chemotherapyBRSENG.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error("Chemotherapy data file not found. Please ensure 'chemotherapyBRSENG.json' is in the 'data' directory.")
        return None
    except json.JSONDecodeError:
        st.error("Error decoding JSON. Please check the file format.")
        return None

def display_chemotherapy_details(protocol, bsa, weight):
    """Displays details of the selected chemotherapy protocol."""
    st.write(f"### Protocol: {protocol['name']}")
    
    if "Chemo" in protocol and protocol["Chemo"]:
        for drug in protocol["Chemo"]:
            if "mg/kg" in drug["DosageMetric"]:
                dosage = round(drug["Dosage"] * weight, 2)
            else:
                dosage = round(drug["Dosage"] * bsa, 2)
            st.write(f"{drug['Name']} {drug['Dosage']} {drug['DosageMetric']} ......... {dosage} mg D {drug['Day']}")
    else:
        st.warning("No chemotherapy drugs found for this protocol.")

    # Use a default value if "NextCycle" is missing
    next_cycle = protocol.get("NextCycle", "Unknown")
    st.write(f"Next Cycle: {next_cycle} days")

    if "Day1" in protocol and "Premed" in protocol["Day1"]:
        st.write("D1 - Premedication")
        premed_note = protocol["Day1"]["Premed"].get("Note", "No premedication details available.")
        st.write(premed_note.replace("Degan", "metoclopramide"))  # Adjust Degan to metoclopramide
        
        if "Instructions" in protocol["Day1"] and protocol["Day1"]["Instructions"]:
            for instruction in protocol["Day1"]["Instructions"]:
                instruction_text = instruction.get("Instruction", "No instructions available.").replace("tablet", "pill")
                st.write(f"{instruction.get('Name', 'Unknown')} {instruction_text}")
        else:
            st.warning("No instructions available for Day 1.")
    else:
        st.warning("No details found for Day 1 instructions.")
        
def calculate_bsa(weight, height):
    """Calculates body surface area using the DuBois formula."""
    return round((weight**0.425) * (height**0.725) * 0.007184, 2)

def main():
    st.title("ChemoThon Breast v. 3.0 ENG")
    st.write("This program prescribes chemotherapy regimens based on body surface area (BSA) or weight.")

    # Load chemotherapy data
    data = load_chemotherapy_data()
    if not data:
        return

    # User input for weight and height
    weight = st.number_input("Enter weight (kg):", min_value=1, max_value=250, step=1, value=None)
    height = st.number_input("Enter height (cm):", min_value=1, max_value=250, step=1, value=None)

    # Calculate BSA
    if st.button("Calculate BSA") and weight and height:
        bsa = calculate_bsa(weight, height)
        st.session_state['bsa'] = bsa
        st.write(f"Body Surface Area: {bsa} m²")

    # Select chemotherapy regimen
    if 'bsa' in st.session_state:
        bsa = st.session_state['bsa']
        chemo_names = [protocol["name"] for protocol in data["chemotherapies"]]
        selected_protocol_name = st.selectbox("Select a chemotherapy regimen:", chemo_names)

        if st.button("Display Protocol") and weight:
            protocol = next((p for p in data["chemotherapies"] if p["name"] == selected_protocol_name), None)
            if protocol:
                display_chemotherapy_details(protocol, bsa, weight)
            else:
                st.error("Selected protocol not found in the data.")
        elif not weight:
            st.error("Please enter a weight to calculate the chemotherapy protocol.")

if __name__ == "__main__":
    main()
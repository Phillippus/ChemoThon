import streamlit as st
import json

def load_json(filename):
    try:
        with open('data/chemotherapyBRSENG.json', 'r') as file:
            data = json.load(file)
            return next((c for c in data['chemotherapies'] if c['name'] == filename), None)
    except FileNotFoundError:
        st.error(f"File not found: {filename}")
        return None
    except json.JSONDecodeError:
        st.error("Error decoding JSON. Check file format.")
        return None

def display_chemotherapy_details(bsa, chemo_name, weight):
    data = load_json(chemo_name)
    if not data:
        return

    st.write(f"### Protocol: {chemo_name}")
    for chemo in data['Chemo']:
        if data.get("FixedDose", False):
            dosage = chemo['Dosage']
        elif chemo['DosageMetric'] == "mg/kg":
            dosage = round(chemo['Dosage'] * weight, 2)
        else:
            dosage = round(chemo['Dosage'] * bsa, 2)

        st.write(f"{chemo['Name']}: {chemo['Dosage']} {chemo['DosageMetric']} ......... {dosage} mg D{chemo['Day']}")

    st.write(f"Next cycle: day {data['nc']}")
    st.write("### Day 1")
    st.write(data['Day1']['Premed']['Note'])

    for inst in data['Day1']['Instructions']:
        name = inst.get("Name")
        if name:
            chemo_entry = next((c for c in data['Chemo'] if c['Name'] == name), None)
            if chemo_entry:
                if data.get("FixedDose", False):
                    dosage = chemo_entry['Dosage']
                elif chemo_entry['DosageMetric'] == "mg/kg":
                    dosage = round(chemo_entry['Dosage'] * weight, 2)
                else:
                    dosage = round(chemo_entry['Dosage'] * bsa, 2)
                st.write(f"{name}: {dosage} mg {inst['Instruction']}")
        else:
            st.write(inst['Instruction'])

def calculate_bsa(weight, height):
    return round((weight**0.425) * (height**0.725) * 0.007184, 2)

def main():
    st.title("ChemoThon - English Edition")

    weight = st.number_input("Enter weight (kg):", min_value=1)
    height = st.number_input("Enter height (cm):", min_value=1)

    if st.button("Calculate BSA") and weight and height:
        bsa = calculate_bsa(weight, height)
        st.session_state['bsa'] = bsa
        st.write(f"Body Surface Area (BSA): {bsa} m²")

    if 'bsa' in st.session_state:
        bsa = st.session_state['bsa']

        chemo_options = {
            # Chemo first
            "AC": "AC",
            "capecitabine": "capecitabine",
            "dd-AC + G-CSF": "dd-AC + G-CSF",
            "docetaxel + G-CSF": "docetaxel + G-CSF",
            "EC": "EC",
            "eribulin": "eribulin",
            "gemcitabine": "gemcitabine",
            "paclitaxel": "paclitaxel",
            "peg- doxorubicin": "peg- doxorubicin",
            "TD-M1": "TD-M1",
            "vinorelbin p.o. weekly": "vinorelbin p.o. weekly",

            # Biologics
            "Pertuzumab": None,
            "Trastuzumab iv": None,
            "Trastuzumab/pertuzumab SC": None,
            "Trastuzumab-deruxtecan": "Trastuzumab-deruxtecan",
            "Sacituzumab govitecan": "Sacituzumab govitecan"
        }

        chemo_name = st.selectbox("Select chemotherapy protocol:", list(chemo_options.keys()))

        if chemo_name in ["Pertuzumab", "Trastuzumab iv", "Trastuzumab/pertuzumab SC"]:
            subtype = st.radio("Select administration type:", ["First administration", "Subsequent administrations"])
            if chemo_name == "Pertuzumab":
                selected_name = "Pertuzumab (first adm.)" if subtype == "First administration" else "Pertuzumab (subseq. adm.)"
            elif chemo_name == "Trastuzumab iv":
                selected_name = "Trastuzumab iv (first adm.)" if subtype == "First administration" else "Trastuzumab iv (subseq. adm.)"
            elif chemo_name == "Trastuzumab/pertuzumab SC":
                selected_name = "Trastuzumab/pertuzumab SC (first adm.)" if subtype == "First administration" else "Trastuzumab/pertuzumab SC (subseq. adm.)"
        else:
            selected_name = chemo_options[chemo_name]

        if st.button("Show protocol"):
            display_chemotherapy_details(bsa, selected_name, weight)

if __name__ == "__main__":
    main()
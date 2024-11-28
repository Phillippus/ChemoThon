import streamlit as st
import json

def load_json(filename):
    """Loads JSON data from a specified file with error handling."""
    try:
        with open(f'data/{filename}', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"Súbor nenájdený: {filename}. Uistite sa, že je v adresári 'data'.")
        return None
    except json.JSONDecodeError:
        st.error("Chyba pri dekódovaní JSON. Skontrolujte formát súboru.")
        return None

def display_chemotherapy_details(rbodysurf, chemoType, weight):
    """Displays detailed information about the chemotherapy regimen using body surface area or weight."""
    chemoJson = load_json(chemoType)
    if chemoJson:
        st.write(f"### Protokol {chemoType.replace('.json', '')}")
        for chemo in chemoJson["Chemo"]:
            # Handle dosage calculation based on BSA or weight
            if chemoType == "TDM1.json":
                dosage = round(chemo["Dosage"] * weight, 2)  # TD-M1 is calculated using weight
            else:
                dosage = round(chemo["Dosage"] * rbodysurf, 2)  # Others use BSA
            
            st.write(f"{chemo['Name']} {round(chemo['Dosage'], 2)} {chemo['DosageMetric']} ......... {dosage} mg D {chemo['Day']}")

        st.write(f"""         
                       NC {chemoJson["NC"]} . deň
                                            """)
    
        st.write("                                     D1")
        st.write(chemoJson["Day1"]["Premed"]["Note"])
    
        for i in range(len(chemoJson["Chemo"])):
            drug_name = chemoJson["Day1"]["Instructions"][i]["Name"]
            if chemoType == "TDM1.json":
                dosage = round(chemoJson["Chemo"][i]["Dosage"] * weight, 2)  # TD-M1
            else:
                dosage = round(chemoJson["Chemo"][i]["Dosage"] * rbodysurf, 2)  # Others
            
            instruction = chemoJson["Day1"]["Instructions"][i]["Inst"]
            st.write(f"{drug_name} {dosage} mg {instruction}")

def calculate_bsa(weight, height):
    """Calculates body surface area using the DuBois formula."""
    bodysurf = (weight**0.425) * (height**0.725) * 0.007184
    return round(bodysurf, 2)

def main():
    st.title("ChemoThon - BreastSK v. 2.0")
    st.write("Vitajte v programe ChemoThon!")
    st.write("""Program rozpisuje najbežnejšie chemoterapie podľa povrchu alebo hmotnosti. 
    Najskôr si vypočítajte BSA a potom sa Vám sprístupní tlačidlo pre výpočet chemoterapie.
    Dávky je nutné upraviť podľa aktuálne dostupných balení liečiv.
    Autor nezodpovedá za prípadné škody spôsobené jeho použitím!
    Pripomienky a požiadavky na úpravu posielajte na filip.kohutek@fntn.sk""")

    weight = st.number_input("Zadajte hmotnosť (kg):", min_value=1, max_value=250, step=1, value=None)
    height = st.number_input("Zadajte výšku (cm):", min_value=1, max_value=250, step=1, value=None)
    
    if st.button("Vypočítať BSA") and weight is not None and height is not None:
        rbodysurf = calculate_bsa(weight, height)
        st.session_state['rbodysurf'] = rbodysurf
        st.write(f"Telesný povrch je: {rbodysurf} m²")

    if 'rbodysurf' in st.session_state:
        st.write(f"Telesný povrch (BSA): {st.session_state['rbodysurf']} m²")

        chemo_options = {
            "EC": "EC.json",
            "AC": "AC.json",
            "dd-AC + G-CSF": "dd-AC.json",
            "docetaxel + G-CSF": "docetaxelbreast.json",
            "paclitaxel": "paclitaxelweekly.json",
            "kapecitabin": "capecitabine.json",
            "gemcitabin": "gemcitabine.json",
            "vinorelbin p.o. weekly": "vinorelbinweekly.json",
            "eribulin": "eribulin.json",
            "peg- doxorubicin": "pegdoxo.json",
            "TD-M1": "TDM1.json"
        }

        chemo_name = st.selectbox("Vyberte chemoterapeutický režim:", list(chemo_options.keys()))

        if st.button('Zobraziť protokol chemoterapie'):
            selected_filename = chemo_options[chemo_name]
            display_chemotherapy_details(st.session_state['rbodysurf'], selected_filename, weight)

if __name__ == "__main__":
    main()

import streamlit as st
import json

def load_json(filename):
    """ Loads JSON data from a specified file with error handling. """
    try:
        with open(f'data/{filename}', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        st.error(f"Súbor nenájdený: {filename}. Uistite sa, že je v adresári 'data'.")
        return None
    except json.JSONDecodeError:
        st.error("Chyba pri dekódovaní JSON. Skontrolujte formát súboru.")
        return None

def display_chemotherapy_details(rbodysurf, filename):
    """ Displays detailed information about the chemotherapy regimen using body surface area. """
    chemo_json = load_json(filename)
    if chemo_json:
        regimen_name = filename.replace('.json', '')
        st.write(f"### Protokol {regimen_name}")
        for chemo in chemo_json['Chemo']:
            dosage = round(chemo['Dosage'] * rbodysurf, 2)
            st.write(f"{chemo['Name']} {chemo['Dosage']} mg/m2 ......... {dosage} mg D {chemo['Day']}")

        st.write(f"                       NC {chemo_json.get('NC', 'Nie je určené')} . deň")
        st.write(" ")
        st.write("                                     D1")
        st.write(chemo_json['Day1']['Premed']['Note'])
        for instruction in chemo_json['Day1']['Instructions']:
            drug_name = instruction['Name']
            dosage = next((item['Dosage'] for item in chemo_json['Chemo'] if item['Name'] == drug_name), None)
            if dosage:
                adjusted_dosage = round(dosage * rbodysurf, 2)
                st.write(f"{drug_name} {adjusted_dosage} mg {instruction['Inst']}")

def calculate_bsa(weight, height):
    """ Calculates body surface area using the DuBois formula. """
    return round((weight**0.425) * (height**0.725) * 0.007184, 2)

def main():
    st.title("ChemoThon - BreastSK v. 2.0")
    st.write("         Vitajte v programe ChemoThon!")
    st.write("""Program rozpisuje najbežnejšie chemoterapie podľa povrchu alebo hmotnosti. 
    Najskôr si vypočítajte BSA a potom sa Vám sprístupní tlačidlo pre výpočet chemoterapie.
    Dávky je nutné upraviť podľa aktuálne dostupných balení liečiv.
    Autor nezodpovedá za prípadné škody spôsobené jeho použitím!
    Pripomienky a požiadavky na úpravu posielajte na filip.kohutek@fntn.sk""")

    weight = st.number_input("Zadajte hmotnosť (kg):", min_value=1, max_value=250, value=70, step=1)
    height = st.number_input("Zadajte výšku (cm):", min_value=1, max_value=250, value=170, step=1)
    
    if st.button("Vypočítať BSA"):
        rbodysurf = calculate_bsa(weight, height)
        st.session_state['rbodysurf'] = rbodysurf

    if 'rbodysurf' in st.session_state:
        st.write(f"Vypočítaný telesný povrch (BSA): {st.session_state['rbodysurf']} m²")

    chemo_options = {
        "EC": "EC.json",
        "AC": "AC.json",
        "Dose-dense AC": "dd-AC.json",
        "Docetaxel": "docetaxelbreast.json",
        "Weekly Paclitaxel": "paclitaxelweekly.json",
        "Capecitabine": "capecitabine.json",
        "Gemcitabine": "gemcitabine.json",
        "Weekly Vinorelbine": "vinorelbinweekly.json",
        "Eribulin": "eribulin.json",
        "Pegylated Liposomal Doxorubicin": "pegdoxo.json",
        "TDM-1": "TDM1.json"
    }

    chemo_name = st.selectbox("Vyberte chemoterapeutický režim:", list(chemo_options.keys()))

    if 'rbodysurf' in st.session_state and st.button('Zobraziť protokol chemoterapie'):
        selected_filename = chemo_options[chemo_name]
        display_chemotherapy_details(st.session_state['rbodysurf'], selected_filename)

if __name__ == "__main__":
    main()

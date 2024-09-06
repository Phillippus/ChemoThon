import streamlit as st
import json
import os

# Function for basic chemotherapy
def Chemo(rbodysurf, chemoType):
    """Táto funkcia rozpisuje jednoduché chemoterapie s priamou úmerou"""
    try:
        with open('data/' + chemoType, "r") as chemoFile:
            chemoJson = json.loads(chemoFile.read())
    except FileNotFoundError:
        st.error(f"File not found: data/{chemoType}")
        return
    except json.JSONDecodeError:
        st.error(f"Error parsing JSON file: {chemoType}")
        return
    
    st.write("Rozpis chemoterapie:")
    for i in chemoJson["Chemo"]:
        st.write(f"{i['Name']}  {round(i['Dosage'], 2)} {i['DosageMetric']}......... {round(i['Dosage'] * rbodysurf, 2)} mg D{i['Day']}")
    
    st.write(f"NC {chemoJson['NC']} . deň")
    
    Day1 = chemoJson["Day1"]["Instructions"]
    C1 = chemoJson["Chemo"]
    
    st.write("D1 - premedikácia:")
    st.write(chemoJson["Day1"]["Premed"]["Note"])
    
    st.write("D1 - chemoterapia:")
    for x in range(len(chemoJson["Chemo"])):
        st.write(f"{Day1[x]['Name']} {round(C1[x]['Dosage'] * rbodysurf, 2)} mg {Day1[x]['Inst']}")

# Function for chemotherapy with CBDCA
def ChemoCBDCA(rbodysurf, chemoType):
    try:
        with open('data/' + chemoType, "r") as chemoFile:
            chemoJson = json.loads(chemoFile.read())
    except FileNotFoundError:
        st.error(f"File not found: data/{chemoType}")
        return
    except json.JSONDecodeError:
        st.error(f"Error parsing JSON file: {chemoType}")
        return

    CrCl = st.number_input("Zadajte hodnotu clearance v ml/min", min_value=1, max_value=250, value=None)
    AUC = st.number_input("Zadajte hodnotu AUC 2-6 (CROSS režim: AUC=2)", min_value=2, max_value=6, value=None)

    if CrCl is not None and AUC is not None:
        st.write(f"CBDCA AUC {AUC}............ {(CrCl + 25) * AUC} mg  D1")
        for i in chemoJson["Chemo"]:
            st.write(f"{i['Name']} {i['Dosage']} {i['DosageMetric']} ..... {round(i['Dosage'] * rbodysurf, 2)} mg D{i['Day']}")

        st.write(f"NC {chemoJson['NC']} . deň")

        st.write("D1")
        st.write(chemoJson["Day1"]["Premed"]["Note"])
        st.write(f"CBDCA {(CrCl + 25) * AUC} mg v 500ml FR iv")
        for x in range(len(chemoJson["Chemo"])):
            st.write(f"{chemoJson['Day1']['Instructions'][x]['Name']} {round(chemoJson['Chemo'][x]['Dosage'] * rbodysurf, 2)} mg {chemoJson['Day1']['Instructions'][x]['Inst']}")

# Main function for gastrointestinal malignancies
def gastrointestinal(rbodysurf):
    """Táto funkcia rozpisuje chemoterapie používané v liečbe gastrointestinálnych malignít"""

    chemo_options = {
        " ": None,
        "Pt/5-FU": platinum5FU,
        "FLOT": "FLOT.json",
        "EOX": "EOX.json",
        "Paclitaxel weekly": "paclitaxelweekly.json",
        "CROSS režim": "paclitaxel50weekly.json",
        "FOLFIRINOX": "FOLFIRINOX.json",
        "Gemcitabin/ Capecitabine": "gemcap.json",
        "Gemcitabin/ Nab-Paclitaxel": "gemnabpcl.json",
        "NALIRI/ 5-FU": "peglipiri5FU.json",
        "NALIRIFOX": "NALIRIFOX.json",
        "Gemcitabin": "gemcitabin4w.json",
        "Mitomycin/ 5-FU": "mtc5FU.json"
    }
    
    chemo_choice = st.selectbox("Vyberte chemoterapiu:", list(chemo_options.keys()))

    if chemo_choice and chemo_choice != "Vyberte chemoterapiu":
        if chemo_choice == "Pt/5-FU":
            platinum5FU(rbodysurf)
        else:
            chemo_file = chemo_options[chemo_choice]
            if chemo_file:
                if chemo_choice in ["FLOT", "FOLFIRINOX", "NALIRI/ 5-FU", "NALIRIFOX", "Mitomycin/ 5-FU"]:
                    Chemo5FU(rbodysurf, chemo_file)
                elif chemo_choice in ["CROSS režim"]:
                    ChemoCBDCA(rbodysurf, chemo_file)
                else:
                    Chemo(rbodysurf, chemo_file)

# Function to calculate Body Surface Area (BSA)
def bsa(weight, height):
    bodysurf = (weight**0.425) * (height**0.725) * 0.007184
    return round(bodysurf, 2)

# Main input function for weight and height
def main():
    st.title("ChemoThon - GastrointestinalSK (excl. CrC) v2.0")
    st.write("""
       Program rozpisuje najbežnejšie chemoterapie podľa povrchu alebo hmotnosti.
    Dávky je nutné upraviť podľa aktuálne dostupných balení liečiv.
    Autor nezodpovedá za prípadné škody spôsobené jeho použitím!
    Pripomienky posielajte na filip.kohutek@fntn.sk
    Program kedykoľvek ukončíte zatvorením okna.
    """)

    # Step 1: Input weight and height
    weight = st.number_input("Zadajte hmotnosť (kg):", min_value=1, max_value=250, value=None)
    height = st.number_input("Zadajte výšku (cm):", min_value=1, max_value=250, value=None)

    if weight and height:
        rbodysurf = bsa(weight, height)
        st.session_state.rbodysurf = rbodysurf
        st.write(f"Telesný povrch je: {st.session_state.rbodysurf} m²")
        gastrointestinal(st.session_state.rbodysurf)

if __name__ == "__main__":
    main()
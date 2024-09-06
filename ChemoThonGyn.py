import streamlit as st
import json

# Function for calculating BSA (Body Surface Area)
def bsa(weight, height):
    bodysurf = (weight**0.425) * (height**0.725) * 0.007184
    rbodysurf = round(bodysurf, 2)
    return rbodysurf

# Function for chemotherapy with Carboplatin (CBDCA)
def ChemoCBDCA(rbodysurf, chemoType):
    """Táto funkcia slúži pre rozpis chemoterapie obsahujúcu karboplatinu"""
    with open('data/' + chemoType, "r") as chemoFile:
        chemoJson = json.loads(chemoFile.read())

    CrCl = st.number_input("Zadajte hodnotu clearance v ml/min", min_value=1, max_value=250, value=None)
    AUC = st.number_input("Zadajte hodnotu AUC 2-6 (INTERLACE: AUC=2)", min_value=2, max_value=6, value=None)

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

# Function for basic chemotherapy
def Chemo(rbodysurf, chemoType):
    """Táto funkcia rozpisuje jednoduché chemoterapie s priamou úmerou"""
    with open('data/' + chemoType, "r") as chemoFile:
        chemoJson = json.loads(chemoFile.read())

    st.write("Rozpis chemoterapie:")
    for i in chemoJson["Chemo"]:
        st.write(f"{i['Name']} {round(i['Dosage'], 2)} {i['DosageMetric']}......... {round(i['Dosage'] * rbodysurf, 2)} mg D{i['Day']}")

    st.write(f"NC {chemoJson['NC']} . deň")

    Day1 = chemoJson["Day1"]["Instructions"]
    C1 = chemoJson["Chemo"]

    st.write("D1 - premedikácia:")
    st.write(chemoJson["Day1"]["Premed"]["Note"])

    st.write("D1 - chemoterapia:")
    for x in range(len(chemoJson["Chemo"])):
        st.write(f"{Day1[x]['Name']} {round(C1[x]['Dosage'] * rbodysurf, 2)} mg {Day1[x]['Inst']}")

# Main function for gynecology chemotherapy
def gynecology(rbodysurf):
    """Táto funkcia rozpisuje chemoterapie gynekologických tumorov"""
    chemo_choice = st.selectbox("Akú chemoterapiu chcete podať?", ["  ", "CBDCA/ paclitaxel","INTERLACE CBDCA/paclitaxel", "Topotecan + G-CSF", "PEG-doxorubicin", "CBDCA/ PEG-doxorubicin", "CBDCA/ gemcitabin"])

    if chemo_choice == "CBDCA/ paclitaxel":
        ChemoCBDCA(rbodysurf, "paclitaxel3weekly.json")
    elif chemo_choice == "INTERLACE CBDCA/paclitaxel":
        ChemoCBDCA(rbodysurf, "paclitaxelweekly.json")
    elif chemo_choice == "Topotecan + G-CSF":
        Chemo(rbodysurf, "topotecan.json")
    elif chemo_choice == "PEG-doxorubicin":
        Chemo(rbodysurf, "pegdoxo.json")
    elif chemo_choice == "CBDCA/ PEG-doxorubicin":
        ChemoCBDCA(rbodysurf, "PEGdoxo30.json")
    elif chemo_choice == "CBDCA/ gemcitabin":
        ChemoCBDCA(rbodysurf, "gemcitabinCBDCA.json")

# Main input function for weight and height
def main():
    st.title("        ChemoThon Gynecology v2.0")
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

    if st.button("Vypočítať telesný povrch"):
        rbodysurf = bsa(weight, height)
        st.session_state.rbodysurf = rbodysurf

    # Always display the BSA if it has been calculated
    if 'rbodysurf' in st.session_state:
        st.write(f"Telesný povrch je: {st.session_state.rbodysurf} m²")

    # Step 2: Display chemotherapy options if BSA is calculated
    if 'rbodysurf' in st.session_state:
        st.write("Teraz vyberte chemoterapiu:")
        gynecology(st.session_state.rbodysurf)

if __name__ == "__main__":
    main()
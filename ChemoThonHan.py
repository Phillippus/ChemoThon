import streamlit as st
import json

# Function for platinum + 5FU chemotherapy
def platinum5FU(rbodysurf):
    """Táto chemoterapia slúži na rozpis chemoterapie s platinou a 5FU"""
    
    a = 80 * rbodysurf
    b = a // 50
    c = a % 50
    rng = int(b)
    
    whichPt = st.selectbox("Ktorá platina?", ["Vyberte platinu", "Cisplatina", "Karboplatina"])
    
    if whichPt == "Cisplatina":
        st.write(f"DDP 80mg/m2................ {80 * rbodysurf} mg  D1")
        st.write(f"5-fluoruracil 1000mg/m2......... {1000 * rbodysurf} mg D1-D4")
        st.write("""
                                             NC 21. deň
                                                          
                                             D1
        """)
        st.write("1. Dexametazón 8mg iv, Pantoprazol 40 mg p.o., Ondansetron 8mg v 250ml FR iv")
        for ordo in range(2, rng + 2):
            st.write(f"{ordo}. Cisplatina 50mg v 500ml RR iv")
        st.write(f"{ordo}. Cisplatina {int(c)} mg v 500ml RR iv")
        st.write(f"{ordo + 1}. Manitol 10% 250ml iv")
        st.write(f"{ordo + 2}. 5-fluoruracil {rbodysurf * 1000} mg na 24 hodín/kivi")
        
    elif whichPt == "Karboplatina":
        CrCl = st.number_input("Zadajte hodnotu clearance v ml/min", min_value=1, max_value=250, value=None, step=1)
        AUC = st.number_input("Zadajte hodnotu AUC 2-6", min_value=2, max_value=6, value=None, step=1)
        
        if CrCl is not None and AUC is not None:
            st.write(f"CBDCA AUC {AUC}............ {(CrCl + 25) * AUC} mg  D1")
            st.write(f"5-fluoruracil 1000mg/m2.............. {rbodysurf * 1000} mg  D1-D4")     
            st.write("""
                                                 NC 21. deň
                                                              
                                                 D1
            """)
            st.write("Dexametazón 8mg iv, Pantoprazol 40 mg p.o., Ondansetron 8mg v 250ml FR iv")
            st.write(f"CBDCA AUC {AUC}............ {(CrCl + 25) * AUC} mg  D1") 
            st.write(f"5-fluoruracil {rbodysurf * 1000} mg na 24 hodín/kivi")

# Function for basic chemotherapy
def Chemo(rbodysurf, chemoType):
    """Táto funkcia rozpisuje jednoduché chemoterapie s priamou úmerou"""
    with open('data/' + chemoType, "r") as chemoFile:
        chemoJson = json.loads(chemoFile.read())
    
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

# Function for head and neck cancer chemotherapy
def headandneck(rbodysurf): 
    """Táto funkcia rozpisuje chemoterapie používané v liečbe nádorov hlavy a krku"""
    chemo_choice = st.selectbox("Vyberte chemoterapiu:", ["Vyberte chemoterapiu", "Pt/5-FU", "Cetuximab", "Paclitaxel weekly", "Metotrexat"])
    
    if chemo_choice == "Pt/5-FU":
        platinum5FU(rbodysurf)
    elif chemo_choice == "Cetuximab":
        ctx_choice = st.selectbox("Prvé podanie cetuximabu?", ["Vyberte možnosť", "Áno", "Nie"])
        if ctx_choice == "Áno":
            Chemo(rbodysurf, "1cetuximab.json")
        elif ctx_choice == "Nie":
            Chemo(rbodysurf, "elsecetuximab.json")
    elif chemo_choice == "Paclitaxel weekly":
        Chemo(rbodysurf, "paclitaxelweekly.json")
    elif chemo_choice == "Metotrexat":
        Chemo(rbodysurf, "metotrexate.json")

# Function to calculate Body Surface Area (BSA)
def bsa(weight, height):
    bodysurf = (weight**0.425) * (height**0.725) * 0.007184
    rbodysurf = round(bodysurf, 2)
    return rbodysurf

# Main input function for weight and height
def main():
    st.title("ChemoThon Head and NeckSK v2.0")
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
        headandneck(st.session_state.rbodysurf)

if __name__ == "__main__":
    main()
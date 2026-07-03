import streamlit as st
import chemo_utils as _cu, importlib as _il
_il.reload(_cu)  # deploy-safe: vynúti čerstvý chemo_utils (Streamlit cachuje moduly)
from chemo_utils import load_json, show_evidence

def display_adc_details(chemoType, weight):
    """Zobrazuje podrobné informácie o ADC režime na základe hmotnosti pacienta."""
    chemo_json = load_json(chemoType)
    if chemo_json:
        regimen_name = chemoType.replace('.json', '')
        st.write(f"### Protokol {regimen_name}")

        for chemo in chemo_json['Chemo']:
            metric = chemo.get('DosageMetric', 'mg/kg')
            dosage = chemo.get('Dosage')
            if dosage is None:
                st.write(f"{chemo['Name']} — dávka zatiaľ nie je vyplnená v knowledge base ({regimen_name}.json)")
                continue
            if 'flat' in metric.lower():
                st.write(f"{chemo['Name']} {dosage} {metric} D {chemo['Day']}")
            elif 'mg/kg' in metric and weight:
                calc = round(dosage * weight, 2)
                st.write(f"{chemo['Name']} {dosage} {metric} ......... {calc} mg D {chemo['Day']}")
            else:
                st.write(f"{chemo['Name']} {dosage} {metric} D {chemo['Day']}")

        st.write(f"NC {chemo_json.get('NC', 'Nie je určené')} . deň")
        st.write(" ")
        st.write("D1")
        st.write(chemo_json['Day1']['Premed']['Note'])

        for instruction in chemo_json['Day1']['Instructions']:
            drug_name = instruction['Name']
            item = next((i for i in chemo_json['Chemo'] if i['Name'] == drug_name), None)
            if item and item.get('Dosage') is not None:
                metric = item.get('DosageMetric', 'mg/kg')
                if 'mg/kg' in metric and weight:
                    dosage = round(item['Dosage'] * weight, 2)
                    st.write(f"{drug_name} {dosage} mg {instruction['Inst']}")
                else:
                    st.write(f"{drug_name} {item['Dosage']} {metric} {instruction['Inst']}")
            else:
                st.write(f"{drug_name} {instruction['Inst']}")

        show_evidence(chemo_json)


def main():
    """Main function to run the Streamlit app."""
    st.title("ChemoThon - ADC v. 0.1 (template)")
    st.write(" ")
    st.write("         Vitajte v module ADC (antibody-drug conjugates)!")
    st.write("""Modul rozpisuje ADC lieky podľa hmotnosti pacienta.
    Dávky je nutné upraviť podľa aktuálne dostupných balení liečiv.
    Autor nezodpovedá za prípadné škody spôsobené jeho použitím!
    Pripomienky a požiadavky na úpravu posielajte na filip.kohutek@fntn.sk""")

    st.warning("⚠️ Knowledge base tohto modulu je zatiaľ ŠABLÓNA bez vyplnených dávok — obsah dopĺňa autor manuálne.")

    weight = st.number_input("Zadajte hmotnosť pacienta (kg):", min_value=1, max_value=250, step=1, value=None)

    adc_options = {
        "Trastuzumab deruxtecan (T-DXd)": "adc_tdxd.json",
        "Datopotamab deruxtecan (Dato-DXd)": "adc_datdxd.json",
        "Patritumab deruxtecan (HER3-DXd)": "adc_patdxd.json",
        "Sacituzumab govitecan": "adc_sacgov.json",
        "Enfortumab vedotin": "adc_ev.json",
        "Brentuximab vedotin": "adc_bv.json",
    }

    adc_name = st.selectbox("Vyberte ADC:", list(adc_options.keys()))
    selected_filename = adc_options[adc_name]

    if st.button('Zobraziť protokol') and weight is not None:
        display_adc_details(selected_filename, weight)
    else:
        if weight is None:
            st.info("Zadajte hmotnosť na výpočet dávky.")

if __name__ == "__main__":
    main()



# ===== Zdroje / Sources =====
with st.expander("📚 Zdroje k režimom / Sources"):
    st.markdown("""**Kľúčové referencie – ADC (šablóna, zatiaľ nevyplnené)**

Guidelines: [ESMO](https://www.esmo.org/guidelines) · [NCCN](https://www.nccn.org/guidelines/category_1). Vždy overte podľa aktuálnej verzie guidelines a dostupných balení liečiv.

TODO: doplniť referencie per liek v rovnakom formáte ako v ostatných moduloch
(štúdia – autor, časopis, rok), pri manuálnom vypĺňaní knowledge base.""")

"""ProstateRisk — NCCN riziková stratifikácia karcinómu prostaty.

Streamlit entry point. Spustenie lokálne:
    streamlit run app.py

ARCHITEKTÚRA PROTI HALUCINÁCII: aplikácia NEGENERUJE klinický obsah za behu.
Riziková skupina je odvodená čisto deterministickou funkciou (prostaterisk/risk.py)
z parametrov zadaných používateľom. Žiadny LLM pri runtime.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from prostaterisk.risk import (  # noqa: E402
    M_STAGE_DEFINITIONS,
    M_STAGES,
    N_STAGE_DEFINITIONS,
    N_STAGES,
    NCCN_SOURCE_LABEL,
    ProstateInputs,
    T_STAGE_DEFINITIONS,
    T_STAGES,
    TNM_SOURCE_LABEL,
    classify,
    grade_group,
)

DISCLAIMER = (
    "**ProstateRisk** je nástroj klinickej podpory rozhodovania **vo vývoji**. "
    "Rizikové kritériá sú rekonštruované z pamäte a **NEOVERENÉ** oproti primárnemu "
    "zdroju — pred klinickým použitím ich over oproti aktuálnej verzii NCCN guideline. "
    "Nenahrádza klinický úsudok ani multidisciplinárny tím."
)

RISK_COLORS = {
    "Veľmi nízke riziko": "green",
    "Nízke riziko": "green",
    "Stredné riziko": "orange",
    "Vysoké riziko": "red",
    "Veľmi vysoké riziko": "red",
    "Regionálne (N1)": "violet",
    "Metastatické (M1)": "violet",
    "Nezaradené": "gray",
}


def show_disclaimer() -> None:
    st.info(DISCLAIMER, icon="⚠️")


def page_classifier() -> None:
    st.title("🎯 ProstateRisk — NCCN riziková stratifikácia")
    show_disclaimer()

    st.subheader("1) Zadaj klinicko-patologické parametre")

    # Mimo formulára, aby popis zvoleného štádia reagoval hneď pri výbere
    # (widgety vo vnútri st.form prekreslia appku až po odoslaní formulára).
    tcol, ncol, mcol = st.columns(3)
    with tcol:
        t_stage = st.selectbox("Klinické T štádium (cT)", T_STAGES, index=T_STAGES.index("T1c"))
        st.caption(f"**{t_stage}** — {T_STAGE_DEFINITIONS[t_stage]}")
    with ncol:
        n_stage = st.radio("N štádium", N_STAGES, horizontal=True)
        st.caption(f"**{n_stage}** — {N_STAGE_DEFINITIONS[n_stage]}")
    with mcol:
        m_stage = st.radio("M štádium", M_STAGES, horizontal=True)
        st.caption(f"**{m_stage}** — {M_STAGE_DEFINITIONS[m_stage]}")
    st.caption(TNM_SOURCE_LABEL)

    with st.form("prostate_form"):
        col1, col2 = st.columns(2)
        with col1:
            psa = st.number_input("PSA (ng/mL)", min_value=0.0, max_value=1000.0, value=6.0, step=0.1)
        with col2:
            gleason_primary = st.selectbox("Gleason primárny pattern (histológia)", [3, 4, 5], index=0)
            gleason_secondary = st.selectbox("Gleason sekundárny pattern (histológia)", [3, 4, 5], index=0)

        st.markdown("**Voliteľné — spresnia veľmi nízke / nepriaznivé stredné / veľmi vysoké riziko:**")
        col3, col4, col5 = st.columns(3)
        with col3:
            use_cores = st.checkbox("Zadať počet bioptických jadier")
            cores_positive = None
            cores_total = None
            if use_cores:
                cores_positive = st.number_input("Počet pozitívnych jadier", min_value=0, max_value=100, value=1, step=1)
                cores_total = st.number_input("Celkový počet odobratých jadier", min_value=1, max_value=100, value=12, step=1)
        with col4:
            use_core_pct = st.checkbox("Zadať max. % nádoru v jadre")
            max_core_pct = None
            if use_core_pct:
                max_core_pct = st.number_input("Max. % nádoru v jednom pozitívnom jadre", min_value=0.0, max_value=100.0, value=30.0, step=1.0)
        with col5:
            use_density = st.checkbox("Zadať PSA denzitu")
            psa_density = None
            if use_density:
                psa_density = st.number_input("PSA denzita (ng/mL/g)", min_value=0.0, max_value=10.0, value=0.10, step=0.01, format="%.2f")
                st.caption("Objem prostaty najlepšie z mpMRI (presnejší než TRUS).")

        use_gg45_cores = st.checkbox("Zadať počet jadier s Grade Group 4–5 (pre veľmi vysoké riziko)")
        cores_gg45 = None
        if use_gg45_cores:
            cores_gg45 = st.number_input("Počet pozitívnych jadier s Grade Group 4–5", min_value=0, max_value=100, value=0, step=1)

        submitted = st.form_submit_button("Vyhodnotiť rizikovú skupinu", use_container_width=True)

    if not submitted:
        return

    gg = grade_group(gleason_primary, gleason_secondary)
    st.subheader("2) Odvodený Grade Group")
    st.markdown(f"Gleason **{gleason_primary}+{gleason_secondary} = {gleason_primary + gleason_secondary}** → **Grade Group {gg}**")

    inputs = ProstateInputs(
        t_stage=t_stage,
        n_stage=n_stage,
        m_stage=m_stage,
        gleason_primary=gleason_primary,
        gleason_secondary=gleason_secondary,
        psa=psa,
        cores_positive=cores_positive,
        cores_total=cores_total,
        max_core_involvement_pct=max_core_pct,
        psa_density=psa_density,
        cores_grade_group_4_5=cores_gg45,
    )
    result = classify(inputs)

    st.subheader("3) Výsledok")
    color = RISK_COLORS.get(result.risk_group, "gray")
    label = result.risk_group + (f" — {result.subgroup}" if result.subgroup else "")
    st.markdown(f"## :{color}[{label}]")

    if result.matched_criteria:
        st.markdown("**Splnené kritériá:**")
        for c in result.matched_criteria:
            st.markdown(f"- {c}")

    for caveat in result.caveats:
        st.warning(caveat, icon="⚠️")

    with st.expander(f"📚 Zdroj — {NCCN_SOURCE_LABEL}"):
        st.markdown(
            "Kategórie: Veľmi nízke / Nízke / Stredné (priaznivé, nepriaznivé) / Vysoké / "
            "Veľmi vysoké riziko + Regionálne (N1) / Metastatické (M1)."
        )
        st.markdown(
            ":red[Hraničné hodnoty NEBOLI manuálne overené oproti aktuálnemu PDF guideline. "
            "Over pred klinickým rozhodnutím.]"
        )


def page_about() -> None:
    st.title("ℹ️ O aplikácii")
    show_disclaimer()
    st.markdown(
        """
### Architektúra proti halucinácii

- Aplikácia **negeneruje** klinický obsah za behu pomocou LLM. Riziková skupina je
  čisto **deterministická funkcia** vstupných parametrov (`prostaterisk/risk.py`).
- Kritériá sú rekonštruované z pamäte modelu pri tvorbe appky a sú **explicitne
  označené ako NEOVERENÉ**, kým ich niekto manuálne neskontroluje oproti aktuálnej
  verzii NCCN guideline (verzia/rok sa menia niekoľkokrát ročne).
- Ak pre kombináciu parametrov nemožno jednoznačne potvrdiť podkritérium (napr.
  nezadaný podiel pozitívnych jadier), appka to **explicitne vypíše ako caveat**
  namiesto tichého predpokladu.
- Žiadne PHI/pacientske dáta sa neukladajú — appka pracuje len s abstraktnými
  klinickými parametrami zadanými v rámci session.

### Rozsah

Pokrýva stratifikáciu **klinicky lokalizovaného a lokálne pokročilého** karcinómu
prostaty (cT1a–T4, N0–N1, M0–M1) do NCCN rizikových skupín na základe histologických
(Gleason/Grade Group, biopsia jadier) a zobrazovacích (cT staging a PSA denzita
informované mpMRI) parametrov. Nepokrýva terapeutické odporúčania ani nomogramy
(napr. CAPRA, MSKCC) — len zaradenie do rizikovej skupiny.
"""
    )


def main() -> None:
    st.set_page_config(page_title="ProstateRisk", page_icon="🎯", layout="centered")
    pages = ["🎯 Klasifikátor", "ℹ️ O aplikácii"]
    choice = st.sidebar.radio("Navigácia", pages, key="nav")
    st.sidebar.divider()
    st.sidebar.caption("ProstateRisk · Fáza 1 (scaffold)")

    if choice == "🎯 Klasifikátor":
        page_classifier()
    elif choice == "ℹ️ O aplikácii":
        page_about()


if __name__ == "__main__":
    main()

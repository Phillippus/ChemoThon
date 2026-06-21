"""MDM Sarcoma & NET — nástroj klinickej podpory pre sarkómy a neuroendokrinné nádory.

Streamlit entry point. Spustenie lokálne:
    streamlit run app.py

ARCHITEKTÚRA PROTI HALUCINÁCII: aplikácia NEGENERUJE klinický obsah za behu. Všetky
odporúčania pochádzajú zo štruktúrovanej KB (kb/*.yaml), validovanej pydanticom, a sú
deterministicky párované s parametrami zadanými používateľom. Žiadny LLM pri runtime.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Zabezpeč import balíka `mdmsarcnet` nezávisle od pracovného adresára (Streamlit Cloud).
APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from mdmsarcnet import matching  # noqa: E402
from mdmsarcnet.entities import ENTITIES, UNKNOWN  # noqa: E402
from mdmsarcnet.kb_loader import KBError, load_kb  # noqa: E402
from mdmsarcnet.schema import UNVERIFIED_MARK, Entity, Society  # noqa: E402

DISCLAIMER = (
    "**MDM Sarcoma & NET** je nástroj klinickej podpory rozhodovania **vo vývoji**. Všetky "
    "odporúčania musia byť pred klinickým použitím overené oproti primárnym zdrojom. "
    "Nenahrádza klinický úsudok ani multidisciplinárny tím."
)

SOCIETY_ORDER = [Society.ESMO, Society.NCCN, Society.ENETS]


@st.cache_data(show_spinner=False)
def get_kb():
    return load_kb()


def show_disclaimer() -> None:
    st.info(DISCLAIMER, icon="⚠️")


def render_citation(rec) -> None:
    status = "✅ overené" if rec.reviewed else "⛔ NEOVERENÉ"
    with st.expander(f"📚 Citácia — {rec.society.value} · {rec.guideline_version} ({rec.year}) · {status}"):
        st.markdown(f"- **Spoločnosť:** {rec.society.value}")
        st.markdown(f"- **Verzia / rok:** {rec.guideline_version} ({rec.year})")
        st.markdown(f"- **Zdroj:** {rec.source_reference}")
        loc = rec.source_location
        if loc.strip() == UNVERIFIED_MARK:
            st.markdown(f"- **Lokácia v dokumente:** :red[{loc}]")
        else:
            st.markdown(f"- **Lokácia v dokumente:** {loc}")
        st.markdown(f"- **Stav kontroly:** {status}")
        if rec.reviewed:
            st.markdown(f"- **Overil/a:** {rec.reviewed_by} ({rec.reviewed_date})")
        st.caption(f"Audit: {rec.generated_by} · id={rec.id}")


def render_recommendation_card(rec) -> None:
    if not rec.reviewed:
        st.warning(
            "⚠️ AI-generovaný obsah, **NEOVERENÉ** — nepoužívať klinicky pred kontrolou.",
            icon="⚠️",
        )
    meta = []
    if rec.stage:
        meta.append(f"štádium {rec.stage}")
    if rec.risk_group:
        meta.append(f"skupina: {rec.risk_group}")
    if meta:
        st.caption(" · ".join(meta))
    st.markdown(rec.recommendation_text)
    render_citation(rec)


# --------------------------------------------------------------------------- #
# Stránky
# --------------------------------------------------------------------------- #
def page_home() -> None:
    st.title("MDM Sarcoma & NET")
    st.markdown(
        "Nástroj klinickej podpory rozhodovania pre **sarkómy a neuroendokrinné nádory** — "
        "riziková stratifikácia a odporúčaný postup podľa **ESMO, NCCN a ENETS**. "
        "Moduly: soft-tissue sarkóm, GIST, kostný sarkóm, GEP-NET."
    )
    show_disclaimer()
    st.subheader("Vyber modul")
    cols = st.columns(2)
    for i, entity in enumerate(ENTITIES):
        ed = ENTITIES[entity]
        with cols[i % 2]:
            if st.button(f"{ed.icon}  {ed.title}", use_container_width=True, key=f"home_{entity.value}"):
                st.session_state["nav"] = ed.title
                st.rerun()


def page_entity(entity: Entity) -> None:
    ed = ENTITIES[entity]
    st.title(f"{ed.icon} {ed.title}")
    show_disclaimer()

    st.subheader("1) Zadaj klinicko-patologické parametre")
    inputs: dict[str, str] = {}
    with st.form(key=f"form_{entity.value}"):
        for fld in ed.fields:
            choice = st.selectbox(fld.label, fld.labels(), help=fld.help or None, key=f"{entity.value}_{fld.key}")
            inputs[fld.key] = fld.value_for_label(choice)
        submitted = st.form_submit_button("Vyhodnotiť", use_container_width=True)

    if not submitted:
        return

    st.subheader("2) Výstup")

    try:
        kb = get_kb()
    except KBError as exc:
        st.error(f"Chyba pri načítaní databázy: {exc}")
        return

    hits = matching.match(kb, entity, inputs)

    if not hits:
        st.error(
            "Pre túto kombináciu parametrov nie je v databáze odporúčanie — "
            "**konzultuj primárny zdroj.**",
            icon="🚫",
        )
        return

    grouped = matching.group_by_society(hits)
    societies_present = [s for s in SOCIETY_ORDER if s in grouped] + [
        s for s in grouped if s not in SOCIETY_ORDER
    ]

    if len(societies_present) > 1:
        st.caption(
            "Odporúčania sa medzi spoločnosťami môžu líšiť — zobrazené sú oddelene, "
            "bez zlučovania."
        )

    for soc in societies_present:
        st.markdown(f"### {soc.value}")
        for rec in grouped[soc]:
            render_recommendation_card(rec)
            st.divider()


def page_sources() -> None:
    st.title("📚 Zdroje")
    st.markdown("Zoznam všetkých guidelines referencovaných v databáze.")
    try:
        kb = get_kb()
    except KBError as exc:
        st.error(f"Chyba pri načítaní databázy: {exc}")
        return

    seen = {}
    for rec in kb:
        key = (rec.society.value, rec.guideline_version, rec.year)
        seen.setdefault(key, rec.source_reference)

    for (soc, ver, year), ref in sorted(seen.items()):
        st.markdown(f"- **{soc}** · {ver} ({year}) — {ref}")


def page_review_status() -> None:
    st.title("🔍 Stav kontroly")
    st.markdown(
        "Prehľad overených (`reviewed: true`) a neoverených záznamov per modul a spoločnosť. "
        "Slúži na sledovanie priebehu klinickej kontroly pred prvým použitím (Fáza 3)."
    )
    try:
        kb = get_kb()
    except KBError as exc:
        st.error(f"Chyba pri načítaní databázy: {exc}")
        return

    total = len(kb)
    reviewed = sum(1 for r in kb if r.reviewed)
    c1, c2, c3 = st.columns(3)
    c1.metric("Záznamov spolu", total)
    c2.metric("Overené", reviewed)
    c3.metric("Neoverené", total - reviewed)
    if total:
        st.progress(reviewed / total, text=f"{reviewed}/{total} overených")

    st.subheader("Podľa modulu a spoločnosti")
    rows = []
    for entity in Entity:
        ed = ENTITIES[entity]
        for soc in Society:
            recs = [r for r in kb if r.entity == entity and r.society == soc]
            if not recs:
                continue
            rev = sum(1 for r in recs if r.reviewed)
            rows.append({
                "Modul": ed.title,
                "Spoločnosť": soc.value,
                "Spolu": len(recs),
                "Overené": rev,
                "Neoverené": len(recs) - rev,
            })
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.info("Databáza je prázdna.")


def page_about() -> None:
    st.title("ℹ️ O aplikácii")
    show_disclaimer()
    st.markdown(
        """
### Architektúra proti halucinácii

- Aplikácia **negeneruje** klinický obsah za behu pomocou LLM. Logika je čisto
  **deterministický matching engine** nad štruktúrovanou databázou (`kb/*.yaml`).
- Každý záznam má povinné polia vrátane `society`, `guideline_version`, `year`,
  `source_reference`, `source_location`, `reviewed` a `generated_by`.
- **`reviewed: false` = nepoužívať na klinické rozhodnutie.** Takéto záznamy sú
  zobrazené s výrazným bannerom.
- Ak pre kombináciu parametrov **neexistuje záznam**, appka to **explicitne oznámi**
  a odkáže na primárny zdroj — nikdy nedopĺňa odpoveď odhadom.
- Rizikové skupiny (FNCLCC grade, GIST riziko podľa Miettinen/AFIP) sa **nepočítajú** —
  zadávajú sa ako vstup.
- Schéma je validovaná pydanticom; `pytest` zlyhá, ak ktorémukoľvek záznamu chýba
  povinné pole.

Žiadne PHI/pacientske dáta sa neukladajú — appka pracuje len s abstraktnými
klinickými parametrami zadanými v rámci session.
"""
    )


# --------------------------------------------------------------------------- #
# Navigácia
# --------------------------------------------------------------------------- #
def main() -> None:
    st.set_page_config(page_title="MDM Sarcoma & NET", page_icon="🧩", layout="centered")

    pages = ["🏠 Domov"]
    entity_titles = {ENTITIES[e].title: e for e in ENTITIES}
    pages += list(entity_titles.keys())
    pages += ["📚 Zdroje", "🔍 Stav kontroly", "ℹ️ O aplikácii"]

    if st.session_state.get("nav") not in pages:
        st.session_state["nav"] = "🏠 Domov"
    choice = st.sidebar.radio("Navigácia", pages, key="nav")

    st.sidebar.divider()
    st.sidebar.caption("MDM Sarcoma & NET · Fáza 1 (scaffold)")

    if choice == "🏠 Domov":
        page_home()
    elif choice in entity_titles:
        page_entity(entity_titles[choice])
    elif choice == "📚 Zdroje":
        page_sources()
    elif choice == "🔍 Stav kontroly":
        page_review_status()
    elif choice == "ℹ️ O aplikácii":
        page_about()


if __name__ == "__main__":
    main()

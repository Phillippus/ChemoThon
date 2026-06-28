"""Rozpísaná AJCC 8 TNM klasifikácia pre sarkómy a neuroendokrinné nádory (NET).

⚠️  NEOVERENÉ — REKONŠTRUOVANÉ Z PAMÄTE (AJCC 8 štandard), NIE Z PRIMÁRNEHO MANUÁLU.
    Definície T/N/M (a grade) treba pred klinickým použitím overiť oproti AJCC Cancer
    Staging Manual 8. NET je TNM SILNE LOKALITNE ŠPECIFICKÝ — nižšie je reprezentatívny
    súhrn (pankreas / tenké črevo), pre ostatné lokality (žalúdok, apendix, rektum…)
    overiť samostatne. Filip označí reviewed.

Modul je referenčný (zobrazenie definícií); matching beží na `setting`/`grade`/… ako doteraz.
"""

from __future__ import annotations

from typing import Dict, List, Tuple

# --- Soft-tissue sarkóm (trup/končatiny, AJCC 8) ------------------------------
SOFT_TISSUE_T = {
    "T1": "Nádor ≤ 5 cm v najväčšom rozmere",
    "T2": "Nádor > 5–10 cm",
    "T3": "Nádor > 10–15 cm",
    "T4": "Nádor > 15 cm",
}
SOFT_TISSUE_N = {"N0": "Bez metastáz v regionálnych uzlinách", "N1": "Metastázy v regionálnych uzlinách"}
SOFT_TISSUE_M = {"M0": "Bez vzdialených metastáz", "M1": "Vzdialené metastázy"}
SOFT_TISSUE_NOTE = (
    "Grade (FNCLCC) je súčasťou stage groupingu: napr. IA = T1 G1; II–III = T1–4 G2–3; "
    "IV = N1 alebo M1."
)

# --- Kostný sarkóm (appendikulárny skelet/trup, AJCC 8) -----------------------
BONE_T = {
    "T1": "Nádor ≤ 8 cm v najväčšom rozmere",
    "T2": "Nádor > 8 cm",
    "T3": "Diskontinuálne nádory v primárnej kosti (skip metastázy)",
}
BONE_N = {"N0": "Bez metastáz v regionálnych uzlinách", "N1": "Metastázy v regionálnych uzlinách"}
BONE_M = {"M0": "Bez vzdialených metastáz", "M1a": "Metastázy v pľúcach", "M1b": "Iné vzdialené metastázy (vrátane iných kostí)"}
BONE_NOTE = "Grade (low/high) vstupuje do stage groupingu: napr. IA = T1 low; IVA = M1a; IVB = N1 alebo M1b."

# --- GIST (AJCC 8) ------------------------------------------------------------
GIST_T = {
    "T1": "Nádor ≤ 2 cm",
    "T2": "Nádor > 2–5 cm",
    "T3": "Nádor > 5–10 cm",
    "T4": "Nádor > 10 cm",
}
GIST_N = {"N0": "Bez metastáz v regionálnych uzlinách", "N1": "Metastázy v regionálnych uzlinách"}
GIST_M = {"M0": "Bez vzdialených metastáz", "M1": "Vzdialené metastázy"}
GIST_NOTE = (
    "Stage grouping závisí od mitotického indexu (≤ 5 vs > 5 / 5 mm²) a lokality "
    "(žalúdok vs tenké črevo). Riziko relapsu sa v praxi určuje podľa Miettinen/AFIP."
)

# --- NET (GEP) — reprezentatívne (pankreas / tenké črevo), AJCC 8/ENETS -------
NET_T = {
    "T1": "Pankreas: ≤ 2 cm  ·  tenké črevo: invázia do lamina propria/submukózy, ≤ 1 cm",
    "T2": "Pankreas: > 2–4 cm  ·  tenké črevo: invázia do muscularis propria alebo > 1 cm",
    "T3": "Pankreas: > 4 cm alebo invázia do duodena/žlčovodu  ·  tenké črevo: cez MP do subseróznej tkaniny",
    "T4": "Invázia do priľahlých orgánov/štruktúr alebo steny veľkých ciev (pankreas: truncus coeliacus/AMS)",
}
NET_N = {"N0": "Bez metastáz v regionálnych uzlinách", "N1": "Metastázy v regionálnych uzlinách"}
NET_M = {
    "M0": "Bez vzdialených metastáz",
    "M1a": "Metastázy obmedzené na pečeň",
    "M1b": "Extrahepatálne metastázy",
    "M1c": "Hepatálne aj extrahepatálne metastázy",
}
NET_NOTE = (
    "POZOR: TNM pre NET je SILNE lokalitne špecifický — vyššie je súhrn pre pankreas / "
    "tenké črevo. Pre žalúdok, apendix, kolon, rektum platia odlišné T definície. "
    "Grade (Ki-67 / mitózy: G1 < 3 %, G2 3–20 %, G3 > 20 %) je samostatný a kľúčový pre liečbu."
)

# entity_value -> (názov, [(sekcia, defs)...], poznámka)
BY_ENTITY: Dict[str, Tuple[str, List[Tuple[str, dict]], str]] = {
    "soft_tissue": ("Soft-tissue sarkóm (AJCC 8, trup/končatiny)",
                    [("T", SOFT_TISSUE_T), ("N", SOFT_TISSUE_N), ("M", SOFT_TISSUE_M)], SOFT_TISSUE_NOTE),
    "bone": ("Kostný sarkóm (AJCC 8)",
             [("T", BONE_T), ("N", BONE_N), ("M", BONE_M)], BONE_NOTE),
    "gist": ("GIST (AJCC 8)",
             [("T", GIST_T), ("N", GIST_N), ("M", GIST_M)], GIST_NOTE),
    "net": ("NET / GEP (AJCC 8 / ENETS — reprezentatívne)",
            [("T", NET_T), ("N", NET_N), ("M", NET_M)], NET_NOTE),
}


def legend(entity_value: str):
    """Vráti (názov, [(sekcia, defs)...], poznámka) pre danú entitu; ('', [], '') ak nie je."""
    return BY_ENTITY.get(entity_value, ("", [], ""))


def t_for_size(size_value: str) -> str:
    """Mapuje pole 'size' soft-tissue (≤5 / >5-10 / >10-15 / >15) na T kategóriu."""
    return {"le5": "T1", "5_10": "T2", "10_15": "T3", "gt15": "T4"}.get(size_value, "")

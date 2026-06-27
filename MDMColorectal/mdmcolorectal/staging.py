"""AJCC 8 TNM pre kolorektálny karcinóm — rozpísané kategórie T/N/M + odvodenie štádia.

⚠️  NEOVERENÉ — REKONŠTRUOVANÉ Z PAMÄTE (AJCC 8 štandard), NIE Z PRIMÁRNEHO MANUÁLU.
    Definície T/N/M aj stage grouping treba pred klinickým použitím overiť oproti
    AJCC Cancer Staging Manual, 8th ed. (colon and rectum). Filip označí reviewed.

Funkcie sú čisto deterministické (žiadny LLM za behu). KB matching beží na agregovanom
`stage` (colon) resp. `ct_stage`/`cn_stage` (rektum); tieto sa z rozpísaného TNM
deterministicky odvodia, takže KB ostáva nezmenená.
"""

from __future__ import annotations

from typing import Dict, List, Optional, Tuple

AJCC_REF = "AJCC Cancer Staging Manual, 8th ed. (colon/rectum) — NEOVERENÉ, overiť"

# --- Rozpísané definície kategórií (AJCC 8) -----------------------------------
# Každá položka: kód -> (krátky label, plná definícia v SK).
T_DEFS: Dict[str, str] = {
    "Tis": "Karcinóm in situ / intramukózny (lamina propria, bez prieniku cez muscularis mucosae)",
    "T1": "Nádor prerastá do submukózy (cez muscularis mucosae)",
    "T2": "Nádor prerastá do muscularis propria",
    "T3": "Nádor prerastá cez muscularis propria do perikolorektálneho tkaniva",
    "T4a": "Nádor preniká na povrch viscerálneho peritonea",
    "T4b": "Nádor priamo prerastá do/adheruje k priľahlým orgánom alebo štruktúram",
}
N_DEFS: Dict[str, str] = {
    "N0": "Bez metastáz v regionálnych uzlinách",
    "N1a": "Metastáza v 1 regionálnej uzline",
    "N1b": "Metastázy v 2–3 regionálnych uzlinách",
    "N1c": "Tumor deposits (subseróza/mezentérium/perikolické tkanivo) bez pozitívnych uzlín",
    "N2a": "Metastázy v 4–6 regionálnych uzlinách",
    "N2b": "Metastázy v ≥ 7 regionálnych uzlinách",
}
M_DEFS: Dict[str, str] = {
    "M0": "Bez vzdialených metastáz",
    "M1a": "Metastázy obmedzené na 1 orgán/miesto (pečeň, pľúca, ováriá, neregionálna uzlina), bez peritonea",
    "M1b": "Metastázy v ≥ 2 orgánoch/miestach, bez postihnutia peritonea",
    "M1c": "Metastázy na peritoneu (samostatne alebo s postihnutím iných orgánov)",
}

T_CATS = tuple(T_DEFS.keys())
N_CATS = tuple(N_DEFS.keys())
M_CATS = tuple(M_DEFS.keys())


def tnm_legend() -> List[Tuple[str, Dict[str, str]]]:
    """Vráti rozpísanú TNM klasifikáciu na zobrazenie v UI."""
    return [("T — primárny nádor", T_DEFS), ("N — regionálne uzliny", N_DEFS), ("M — vzdialené metastázy", M_DEFS)]


# --- Odvodenie anatomického štádia (AJCC 8) -----------------------------------
def anatomic_stage(t: str, n: str, m: str) -> Optional[str]:
    """Anatomické AJCC 8 stage grouping z rozpísaného T/N/M. Napr. 'IIIB'. None ak neúplné."""
    if not (t and n and m):
        return None
    if m == "M1a":
        return "IVA"
    if m == "M1b":
        return "IVB"
    if m == "M1c":
        return "IVC"
    if m != "M0":
        return None
    if t == "Tis":
        return "0"
    if t not in T_CATS or n not in N_CATS:
        return None

    n1 = n in ("N1a", "N1b", "N1c")
    n2a = n == "N2a"
    n2b = n == "N2b"

    if n == "N0":
        return {"T1": "I", "T2": "I", "T3": "IIA", "T4a": "IIB", "T4b": "IIC"}.get(t)

    if t in ("T1", "T2") and n1:
        return "IIIA"
    if t == "T1" and n2a:
        return "IIIA"
    if t in ("T3", "T4a") and n1:
        return "IIIB"
    if t in ("T2", "T3") and n2a:
        return "IIIB"
    if t in ("T1", "T2") and n2b:
        return "IIIB"
    if t == "T4a" and n2a:
        return "IIIC"
    if t in ("T3", "T4a") and n2b:
        return "IIIC"
    if t == "T4b" and (n1 or n2a or n2b):
        return "IIIC"
    return None


# --- Mapovanie rozpísaného TNM na agregované kľúče pre KB matching -------------
def coarse_ct(ct: str) -> Optional[str]:
    """cT (rozpísané) -> ct_stage kľúč v KB rekta (cT1_2 / cT3 / cT4)."""
    if ct in ("cT1", "cT2"):
        return "cT1_2"
    if ct == "cT3":
        return "cT3"
    if ct in ("cT4a", "cT4b"):
        return "cT4"
    return None


def coarse_cn(cn: str) -> Optional[str]:
    """cN (rozpísané) -> cn_stage kľúč v KB rekta (cN0 / cN_pos)."""
    if cn == "cN0":
        return "cN0"
    if cn in ("cN1", "cN1a", "cN1b", "cN1c", "cN2", "cN2a", "cN2b"):
        return "cN_pos"
    return None

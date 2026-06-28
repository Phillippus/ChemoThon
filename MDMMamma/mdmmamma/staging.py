"""AJCC 8 staging pre karcinóm prsníka — deterministické odvodenie štádia z T/N/M.

⚠️  NEOVERENÉ — REKONŠTRUOVANÉ Z PAMÄTE, NIE Z PRIMÁRNEHO AJCC MANUÁLU.
    Anatomické štádium (čisté T/N/M) je dobre definované a implementované úplne.
    Klinické PROGNOSTICKÉ štádium (AJCC 8, + grade + ER/PR/HER2) je rekonštruované
    z pamäte a aplikované LEN tam, kde existuje istota (kalibrované na 5 oficiálnych
    AJCC príkladov — viď tests/test_staging.py). Pre profily mimo istoty funkcia
    vráti anatomické štádium s poznámkou "prognostické neoverené".
    Pred klinickým použitím OVERIŤ KAŽDÉ PRAVIDLO oproti AJCC Cancer Staging Manual 8.

Funkcie sú čisto deterministické (žiadny LLM za behu).
"""

from __future__ import annotations

from typing import Optional, Tuple

# Akceptované hlavné kategórie (po normalizácii sub-kategórií).
T_CATS = ("Tis", "T1", "T2", "T3", "T4")
N_CATS = ("N0", "N1", "N2", "N3")
M_CATS = ("M0", "M1")
GRADES = ("G1", "G2", "G3")

AJCC_REF = "AJCC Cancer Staging Manual, 8th ed. (breast) — NEOVERENÉ, overiť"

# --- Rozpísané definície kategórií (AJCC 8, prsník) ---------------------------
T_DEFS = {
    "Tis": "Karcinóm in situ (DCIS) alebo Pagetova choroba bradavky bez invazívneho nádoru",
    "T1mi": "Mikroinvázia ≤ 1 mm",
    "T1a": "Nádor > 1–5 mm",
    "T1b": "Nádor > 5–10 mm",
    "T1c": "Nádor > 10–20 mm",
    "T2": "Nádor > 20–50 mm",
    "T3": "Nádor > 50 mm",
    "T4a": "Šírenie do hrudnej steny (bez m. pectoralis)",
    "T4b": "Edém/ulcerácia kože alebo satelitné kožné uzlíky",
    "T4c": "T4a aj T4b súčasne",
    "T4d": "Inflamatórny karcinóm",
}
N_DEFS = {
    "N0": "Bez metastáz v regionálnych uzlinách",
    "N1": "Pohyblivé ipsilaterálne axilárne uzliny I.–II. etáže (1–3 pri pN1)",
    "N2a": "Fixované/zhlukované axilárne uzliny I.–II. etáže (4–9 pri pN2)",
    "N2b": "Klinicky zjavné a. mammaria interna bez axilárnych",
    "N3a": "Infraklavikulárne uzliny (III. etáž) / ≥ 10 axilárnych",
    "N3b": "A. mammaria interna + axilárne uzliny",
    "N3c": "Supraklavikulárne uzliny",
}
M_DEFS = {
    "M0": "Bez vzdialených metastáz (cM0(i+) = izolované nádorové bunky bez klinických metastáz)",
    "M1": "Vzdialené metastázy",
}


def normalize_t(t: str) -> str:
    """Sub-kategórie T -> hlavná kategória pre stage grouping."""
    if t.startswith("T1"):
        return "T1"
    if t.startswith("T4"):
        return "T4"
    return t


def normalize_n(n: str) -> str:
    if n.startswith("N2"):
        return "N2"
    if n.startswith("N3"):
        return "N3"
    return n


def tnm_legend():
    """Rozpísaná TNM klasifikácia (AJCC 8) na zobrazenie v UI."""
    return [("T — primárny nádor", T_DEFS), ("N — regionálne uzliny", N_DEFS), ("M — vzdialené metastázy", M_DEFS)]


def anatomic_stage(t: str, n: str, m: str) -> Optional[str]:
    """Anatomické AJCC 8 stage grouping z T/N/M (sub-kategórie normalizované). Napr. 'IIA'."""
    if not (t and n and m):
        return None
    t, n = normalize_t(t), normalize_n(n)
    if m == "M1":
        return "IV"
    if t == "Tis":
        return "0"
    if t not in T_CATS or n not in N_CATS:
        return None
    if n == "N3":
        return "IIIC"
    if t == "T4":
        return "IIIB"  # T4 N0–N2 (T4N3 už zachytené vyššie)
    if n == "N2":
        return "IIIA"  # T1–T3 N2
    # N0 / N1:
    table = {
        ("T1", "N0"): "IA",
        ("T2", "N0"): "IIA",
        ("T3", "N0"): "IIB",
        ("T1", "N1"): "IIA",
        ("T2", "N1"): "IIB",
        ("T3", "N1"): "IIIA",
    }
    return table.get((t, n))


def clinical_prognostic_stage(
    t: str, n: str, m: str, grade: str, her2: str, er: str, pr: str
) -> Tuple[Optional[str], str]:
    """Klinické prognostické AJCC 8 štádium. Vráti (štádium, poznámka).

    Implementované s istotou: M1→IV, Tis→0, a HR+/HER2− priestor I–II (anchory),
    plus TNBC T3N0→IIIB. Mimo istoty vráti anatomické štádium s poznámkou.
    """
    anat = anatomic_stage(t, n, m)
    t, n = normalize_t(t), normalize_n(n)
    if m == "M1":
        return "IV", ""
    if t == "Tis":
        return "0", ""
    if anat is None:
        return None, ""

    hr_pos = er == "positive" or pr == "positive"
    her2_pos = her2 == "her2_positive"
    her2_neg = her2 in ("her2_low", "her2_zero")
    fallback = (anat, "prognostické pre tento profil NEOVERENÉ — zobrazené anatomické (overiť AJCC)")

    if not grade or not her2 or not er or not pr:
        return anat, "neúplné prognostické faktory (grade/ER/PR/HER2) — zobrazené anatomické"

    # --- HR+ / HER2− : grade-dependent downstaging (kalibrované na AJCC anchory) ---
    if hr_pos and her2_neg:
        key = (t, n)
        if key in (("T1", "N0"),):
            return "IA", ""
        if key == ("T2", "N0"):
            return ("IB", "") if grade in ("G1", "G2") else ("IIA", "")
        if key == ("T1", "N1"):
            return ("IB", "") if grade in ("G1", "G2") else ("IIA", "")
        if key == ("T2", "N1"):
            return ("IIA", "") if grade in ("G1", "G2") else ("IIB", "")
        return fallback

    # --- Triple-negatívny (ER−/PR−/HER2−) : len istý anchor, inak anatomické ---
    if (not hr_pos) and her2_neg:
        if (t, n) == ("T3", "N0"):
            return "IIIB", ""
        return (anat, "TNBC: prognostické CPS čiastočne NEOVERENÉ — zobrazené anatomické (overiť AJCC)")

    # --- HER2+ : CPS riadky nerekonštruované s istotou ---
    if her2_pos:
        return (anat, "HER2-pozitívne: prognostické CPS NEOVERENÉ — zobrazené anatomické (overiť AJCC)")

    return fallback

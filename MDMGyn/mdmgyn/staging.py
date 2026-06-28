"""Rozpísaná FIGO + TNM klasifikácia pre gynekologické malignity.

⚠️  NEOVERENÉ — REKONŠTRUOVANÉ Z PAMÄTE (FIGO/AJCC štandard), NIE Z PRIMÁRNEHO ZDROJA.
    Definície FIGO štádií aj TNM ekvivalenty treba pred klinickým použitím overiť oproti
    aktuálnym FIGO klasifikáciám (endometrium 2023, cervix 2018, vulva 2021, ovárium 2014)
    a AJCC 8. Filip označí reviewed.

Modul je len referenčný (zobrazenie definícií); matching beží na `figo_stage` ako doteraz.
Pre každú lokalitu: FIGO kód -> (definícia, TNM ekvivalent).
"""

from __future__ import annotations

from typing import Dict, Tuple

# (definícia, TNM ekvivalent)
ENDOMETRIUM: Dict[str, Tuple[str, str]] = {
    "IA": ("Obmedzený na telo maternice, < 50 % invázie myometria (nízkorizik. histológia)", "T1a N0 M0"),
    "IB": ("Invázia ≥ 50 % myometria", "T1b N0 M0"),
    "IC": ("Agresívna histológia obmedzená na endometrium/polyp (FIGO 2023)", "T1 N0 M0"),
    "IIA": ("Postihnutie strómy krčka maternice", "T2 N0 M0"),
    "IIB": ("Rozsiahla LVSI alebo agresívna histológia s inváziou myometria (FIGO 2023)", "T2 N0 M0"),
    "IIC": ("Agresívna histológia s inváziou myometria (FIGO 2023)", "T2 N0 M0"),
    "IIIA": ("Šírenie na seróza/adnexá", "T3a N0 M0"),
    "IIIB": ("Postihnutie vagíny a/alebo parametrií", "T3b N0 M0"),
    "IIIC1": ("Metastázy v panvových lymfatických uzlinách", "T(any) N1 M0"),
    "IIIC2": ("Metastázy v paraaortálnych uzlinách (± panvové)", "T(any) N2 M0"),
    "IVA": ("Invázia do sliznice močového mechúra a/alebo čreva", "T4 N(any) M0"),
    "IVB": ("Brušné metastázy a/alebo inguinálne uzliny", "T(any) N(any) M1"),
    "IVC": ("Vzdialené metastázy (vrátane pľúc, pečene, kostí)", "T(any) N(any) M1"),
}

CERVIX: Dict[str, Tuple[str, str]] = {
    "IA1": ("Mikroskopická invázia ≤ 3 mm do hĺbky", "T1a1 N0 M0"),
    "IA2": ("Invázia > 3–5 mm do hĺbky", "T1a2 N0 M0"),
    "IB1": ("Invázia > 5 mm, tumor ≤ 2 cm", "T1b1 N0 M0"),
    "IB2": ("Tumor > 2–4 cm", "T1b2 N0 M0"),
    "IB3": ("Tumor > 4 cm, obmedzený na krčok", "T1b3 N0 M0"),
    "IIA1": ("Šírenie na hornú 2/3 vagíny, ≤ 4 cm, bez parametrií", "T2a1 N0 M0"),
    "IIA2": ("Šírenie na vagínu > 4 cm, bez parametrií", "T2a2 N0 M0"),
    "IIB": ("Parametriálna invázia bez šírenia na panvovú stenu", "T2b N0 M0"),
    "IIIA": ("Šírenie na dolnú 1/3 vagíny, bez panvovej steny", "T3a N0 M0"),
    "IIIB": ("Šírenie na panvovú stenu / hydronefróza", "T3b N(any) M0"),
    "IIIC1": ("Metastázy v panvových uzlinách (bez ohľadu na rozsah tumoru)", "T(any) N1 M0 (panvové)"),
    "IIIC2": ("Metastázy v paraaortálnych uzlinách", "T(any) N1 M0 (paraaortálne)"),
    "IVA": ("Šírenie na sliznicu mechúra/rekta alebo mimo panvy", "T4 N(any) M0"),
    "IVB": ("Vzdialené metastázy", "T(any) N(any) M1"),
}

VULVA: Dict[str, Tuple[str, str]] = {
    "IA": ("Tumor ≤ 2 cm obmedzený na vulvu/perineum, stromálna invázia ≤ 1 mm", "T1a N0 M0"),
    "IB": ("Tumor > 2 cm alebo stromálna invázia > 1 mm, obmedzený na vulvu/perineum", "T1b N0 M0"),
    "II": ("Šírenie na priľahlé štruktúry (dolná uretra/vagína/anus), uzliny negatívne", "T2 N0 M0"),
    "IIIA": ("Metastázy v 1–2 uzlinách < 5 mm alebo 1 uzlina ≥ 5 mm", "T(any) N1 M0"),
    "IIIB": ("Metastázy v ≥ 2 uzlinách ≥ 5 mm alebo ≥ 3 uzliny < 5 mm", "T(any) N2 M0"),
    "IIIC": ("Uzliny s extrakapsulárnym šírením", "T(any) N2c M0"),
    "IVA": ("Fixované/ulcerované uzliny alebo invázia hornej uretry/vagíny/kosti", "T(any) N3 / T3 M0"),
    "IVB": ("Vzdialené metastázy (vrátane panvových uzlín)", "T(any) N(any) M1"),
}

OVARY: Dict[str, Tuple[str, str]] = {
    "IA": ("Obmedzený na 1 ováriu/tubu, kapsula intaktná, bez nádoru na povrchu/ascite", "T1a N0 M0"),
    "IB": ("Obmedzený na obe ováriá/tuby, kapsuly intaktné", "T1b N0 M0"),
    "IC": ("Obmedzený na ováriá s ruptúrou kapsuly / nádorom na povrchu / pozit. cytológiou", "T1c N0 M0"),
    "IIA": ("Šírenie na maternicu a/alebo tuby/ováriá", "T2a N0 M0"),
    "IIB": ("Šírenie na ostatné panvové tkanivá", "T2b N0 M0"),
    "IIIA": ("Mikroskopické peritoneálne metastázy mimo panvy / retroperitoneálne uzliny", "T3a / N1 M0"),
    "IIIB": ("Makroskopické peritoneálne metastázy ≤ 2 cm", "T3b N(any) M0"),
    "IIIC": ("Peritoneálne metastázy > 2 cm (± kapsula pečene/sleziny)", "T3c N(any) M0"),
    "IVA": ("Pleurálny výpotok s pozitívnou cytológiou", "T(any) N(any) M1a"),
    "IVB": ("Parenchýmové a extraabdominálne metastázy (vrátane inguinálnych uzlín)", "T(any) N(any) M1b"),
}

BY_ENTITY = {
    "endometrium": ("FIGO 2023", ENDOMETRIUM),
    "cervix": ("FIGO 2018", CERVIX),
    "vulva": ("FIGO 2021", VULVA),
    "ovary": ("FIGO 2014", OVARY),
}


def stage_info(entity_value: str, figo: str) -> Tuple[str, str]:
    """Vráti (definícia, TNM ekvivalent) pre dané FIGO štádium a lokalitu; ('','') ak nie je."""
    _, table = BY_ENTITY.get(entity_value, ("", {}))
    return table.get(figo, ("", ""))


def legend(entity_value: str):
    """Rozpísaná FIGO klasifikácia (+TNM) pre lokalitu na zobrazenie v UI."""
    version, table = BY_ENTITY.get(entity_value, ("", {}))
    return version, table

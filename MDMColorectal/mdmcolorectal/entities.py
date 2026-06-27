"""Definícia klinických scenárov (modulov) a polí wizardu pre kolorektálny karcinóm.

TOTO NIE JE KLINICKÝ OBSAH — je to len konfigurácia formulára: aké atribúty sa
pýtame a aké hodnoty sú prípustné. Mapovanie kombinácie atribútov na odporúčanie
prebieha výhradne cez KB (kb/*.yaml) a deterministický matching engine.

Každé pole má:
- key    : interný kľúč atribútu (musí sa zhodovať s kľúčmi v `criteria` v KB)
- label  : popis pre používateľa
- options: zoznam dvojíc (label, value); value="" znamená "nezadané/neznáme"
- help   : voliteľná nápoveda
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List, Tuple

from .schema import Entity

UNKNOWN = ""
UNKNOWN_LABEL = "— nezadané / neznáme —"


@dataclass(frozen=True)
class Field_:
    key: str
    label: str
    options: List[Tuple[str, str]]
    help: str = ""

    def labels(self) -> List[str]:
        return [UNKNOWN_LABEL] + [lbl for lbl, _ in self.options]

    def value_for_label(self, label: str) -> str:
        if label == UNKNOWN_LABEL:
            return UNKNOWN
        for lbl, val in self.options:
            if lbl == label:
                return val
        return UNKNOWN


@dataclass(frozen=True)
class EntityDef:
    key: Entity
    title: str
    icon: str
    fields: List[Field_] = field(default_factory=list)


def _opts(*pairs: Tuple[str, str]) -> List[Tuple[str, str]]:
    return list(pairs)


# Spoločné polia ---------------------------------------------------------------
_MMR = Field_("mmr_status", "MMR / MSI status", _opts(
    ("dMMR / MSI-high", "dmmr"),
    ("pMMR / MSS", "pmmr"),
), "Deficientná oprava mispárovania = dMMR/MSI-H; intaktná = pMMR/MSS.")
_RAS = Field_("ras", "RAS (KRAS/NRAS) status", _opts(
    ("Mutovaný", "mutated"), ("Wild-type", "wildtype"),
))
_BRAF = Field_("braf", "BRAF status", _opts(
    ("V600E mutovaný", "v600e"), ("Wild-type", "wildtype"),
))


# T/N/M kategórie (AJCC 8) — rozpísané; štádium sa odvodí v staging.py.
_T_CRC = Field_("t", "T kategória (AJCC 8)", _opts(
    ("Tis (in situ / intramukózny)", "Tis"),
    ("T1 (submukóza)", "T1"),
    ("T2 (muscularis propria)", "T2"),
    ("T3 (cez MP do perikolorektálneho tkaniva)", "T3"),
    ("T4a (viscerálne peritoneum)", "T4a"),
    ("T4b (priľahlé orgány/štruktúry)", "T4b"),
), "Hĺbka invázie steny. Definície sa rozpíšu vo výstupe.")
_N_CRC = Field_("n", "N kategória (AJCC 8)", _opts(
    ("N0 (bez uzlín)", "N0"),
    ("N1a (1 uzlina)", "N1a"),
    ("N1b (2–3 uzliny)", "N1b"),
    ("N1c (tumor deposits, bez poz. uzlín)", "N1c"),
    ("N2a (4–6 uzlín)", "N2a"),
    ("N2b (≥ 7 uzlín)", "N2b"),
))
_M_CRC = Field_("m", "M kategória (AJCC 8)", _opts(
    ("M0 (bez vzdialených)", "M0"),
    ("M1a (1 orgán/miesto, bez peritonea)", "M1a"),
    ("M1b (≥ 2 orgány, bez peritonea)", "M1b"),
    ("M1c (peritoneum ± iné)", "M1c"),
))


# --- Kolon (st. I–III) --------------------------------------------------------
COLON = EntityDef(
    key=Entity.COLON,
    title="Karcinóm kolon (st. I–III)",
    icon="🟤",
    fields=[
        _T_CRC, _N_CRC, _M_CRC,
        _MMR,
        Field_("high_risk_stage2", "Vysokorizikové znaky (st. II)", _opts(
            ("Prítomné", "present"), ("Neprítomné", "absent"),
        ), "T4, perforácia/obštrukcia, < 12 uzlín, low grade differentiation, LVI/PNI."),
        Field_("grade", "Grade", _opts(
            ("Nízky (G1–2)", "low"), ("Vysoký (G3)", "high"),
        )),
    ],
)

# --- Rektum -------------------------------------------------------------------
RECTUM = EntityDef(
    key=Entity.RECTUM,
    title="Karcinóm rekta (lokalizovaný)",
    icon="🟧",
    fields=[
        Field_("ct", "cT kategória (AJCC 8, klinické)", _opts(
            ("cT1 (submukóza)", "cT1"),
            ("cT2 (muscularis propria)", "cT2"),
            ("cT3 (cez MP do perirektálneho tkaniva)", "cT3"),
            ("cT4a (viscerálne peritoneum)", "cT4a"),
            ("cT4b (priľahlé orgány/štruktúry)", "cT4b"),
        ), "Hĺbka invázie. Definície sa rozpíšu vo výstupe."),
        Field_("cn", "cN kategória (AJCC 8, klinické)", _opts(
            ("cN0 (bez uzlín)", "cN0"),
            ("cN1 (1–3 uzliny / N1c deposits)", "cN1"),
            ("cN2 (≥ 4 uzliny)", "cN2"),
        )),
        Field_("cm", "M kategória (AJCC 8)", _opts(
            ("M0 (bez vzdialených)", "M0"),
            ("M1a (1 orgán/miesto)", "M1a"),
            ("M1b (≥ 2 orgány)", "M1b"),
            ("M1c (peritoneum ± iné)", "M1c"),
        )),
        Field_("mrf", "Mezorektálna fascia (MRF/CRM)", _opts(
            ("Voľná", "clear"), ("Ohrozená / postihnutá", "involved"),
        )),
        Field_("emvi", "EMVI (extramurálna vaskulárna invázia)", _opts(
            ("Pozitívna", "positive"), ("Negatívna", "negative"),
        )),
        Field_("distance", "Vzdialenosť od anu", _opts(
            ("Dolné rektum (< 5 cm)", "low"),
            ("Stredné rektum", "mid"),
            ("Horné rektum", "high"),
        )),
        _MMR,
    ],
)

# --- Metastatický (mCRC) ------------------------------------------------------
METASTATIC = EntityDef(
    key=Entity.METASTATIC,
    title="Metastatický kolorektálny karcinóm",
    icon="🔴",
    fields=[
        Field_("m", "M kategória (AJCC 8)", _opts(
            ("M1a (1 orgán/miesto, bez peritonea)", "M1a"),
            ("M1b (≥ 2 orgány, bez peritonea)", "M1b"),
            ("M1c (peritoneum ± iné)", "M1c"),
        ), "Metastatické ochorenie = M1; podkategória sa rozpíše vo výstupe."),
        Field_("sidedness", "Lateralita primárneho tumoru", _opts(
            ("Pravostranný kolon", "right"),
            ("Ľavostranný kolon", "left"),
            ("Rektum", "rectum"),
        ), "Pravý = od céka po lienálnu flexúru; ľavý = od lienálnej flexúry po rektum."),
        _RAS,
        _BRAF,
        _MMR,
        Field_("her2", "HER2 status", _opts(
            ("Amplifikovaný / pozitívny", "amplified"),
            ("Neamplifikovaný", "not_amplified"),
        )),
        Field_("resectability", "Resekabilita metastáz", _opts(
            ("Resekabilné", "resectable"),
            ("Potenciálne resekabilné (konverzia)", "potentially_resectable"),
            ("Neresekabilné", "unresectable"),
        )),
    ],
)


ENTITIES = {
    Entity.COLON: COLON,
    Entity.RECTUM: RECTUM,
    Entity.METASTATIC: METASTATIC,
}

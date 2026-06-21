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


# --- Kolon (st. I–III) --------------------------------------------------------
COLON = EntityDef(
    key=Entity.COLON,
    title="Karcinóm kolon (st. I–III)",
    icon="🟤",
    fields=[
        Field_("stage", "Štádium (AJCC TNM 8)", _opts(
            ("I", "I"), ("IIA", "IIA"), ("IIB", "IIB"), ("IIC", "IIC"),
            ("IIIA", "IIIA"), ("IIIB", "IIIB"), ("IIIC", "IIIC"),
        )),
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
        Field_("stage", "Štádium (AJCC TNM 8)", _opts(
            ("I", "I"), ("II", "II"), ("III", "III"),
        )),
        Field_("ct_stage", "cT (klinické)", _opts(
            ("cT1–2", "cT1_2"), ("cT3", "cT3"), ("cT4", "cT4"),
        )),
        Field_("cn_stage", "cN (klinické)", _opts(
            ("cN0", "cN0"), ("cN+", "cN_pos"),
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

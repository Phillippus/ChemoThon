"""Definícia klinických scenárov (modulov) a polí wizardu pre karcinóm prsníka.

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


# Spoločné biomarkerové polia ---------------------------------------------------
_ER = Field_("er", "ER (estrogénový receptor)", _opts(
    ("Pozitívny", "positive"), ("Negatívny", "negative"),
))
_PR = Field_("pr", "PR (progesterónový receptor)", _opts(
    ("Pozitívny", "positive"), ("Negatívny", "negative"),
))
_HER2 = Field_("her2", "HER2 status", _opts(
    ("Pozitívny (IHC 3+ / ISH+)", "her2_positive"),
    ("Low (IHC 1+ alebo 2+/ISH−)", "her2_low"),
    ("Nulový (IHC 0)", "her2_zero"),
), "HER2-negatívny zahŕňa 'low' aj 'zero'.")
_BRCA = Field_("brca", "BRCA1/2 (germinálne)", _opts(
    ("Mutovaný", "mutated"), ("Wild-type", "wildtype"),
))
_MENO = Field_("menopause", "Menopauzálny status", _opts(
    ("Premenopauzálny", "pre"), ("Postmenopauzálny", "post"),
))
# T/N/M kategórie (AJCC 8) — vstup pre deterministické odvodenie štádia (staging.py).
_T = Field_("t", "T kategória (AJCC 8)", _opts(
    ("Tis (in situ)", "Tis"), ("T1 (≤ 20 mm)", "T1"), ("T2 (> 20–50 mm)", "T2"),
    ("T3 (> 50 mm)", "T3"), ("T4 (stena/koža/inflamatórny)", "T4"),
))
_N = Field_("n", "N kategória (AJCC 8)", _opts(
    ("N0 (bez uzlín)", "N0"), ("N1 (1–3 axilárne)", "N1"),
    ("N2 (4–9 / fixované / a. mammaria int.)", "N2"),
    ("N3 (≥ 10 / infraklavik. / supraklavik.)", "N3"),
))
_M = Field_("m", "M kategória", _opts(
    ("M0 (bez vzdialených)", "M0"), ("M1 (vzdialené metastázy)", "M1"),
))


# --- DCIS ---------------------------------------------------------------------
DCIS = EntityDef(
    key=Entity.DCIS,
    title="Duktálny karcinóm in situ (DCIS)",
    icon="🟣",
    fields=[
        Field_("grade", "Grade", _opts(
            ("Nízky", "low"), ("Stredný", "intermediate"), ("Vysoký", "high"),
        )),
        _ER,
        Field_("margins", "Chirurgické okraje", _opts(
            ("Negatívne (≥ 2 mm)", "negative"),
            ("Pozitívne / tesné", "positive_close"),
        )),
    ],
)

# --- Skorý invazívny karcinóm -------------------------------------------------
# --- Invazívny karcinóm (zlúčený skorý + lokálne pokročilý) -------------------
# Jeden tok: zadáš T/N/M + biomarkery -> appka odvodí AJCC štádium (staging.py) a
# zobrazí odporúčania (skoré aj lokálne pokročilé) podľa biomarkerov. Modul „early"
# a „locally_advanced" zlúčené, aby štádium vyplývalo z TNM a nebolo ručne delené.
INVASIVE = EntityDef(
    key=Entity.INVASIVE,
    title="Invazívny karcinóm",
    icon="🟢",
    fields=[
        _T, _N, _M,
        Field_("histology", "Histologický typ", _opts(
            ("Invazívny NST (duktálny)", "nst"),
            ("Lobulárny", "lobular"),
            ("Špeciálny typ", "special"),
        )),
        Field_("grade", "Grade (Nottingham)", _opts(("G1", "G1"), ("G2", "G2"), ("G3", "G3"))),
        _ER, _PR, _HER2,
        Field_("ki67", "Ki-67", _opts(("Nízky (< 20 %)", "low"), ("Vysoký (≥ 20 %)", "high"))),
        Field_("subtype", "Surrogátny molekulárny podtyp", _opts(
            ("Luminálny A", "luminal_a"),
            ("Luminálny B (HER2−)", "luminal_b_her2neg"),
            ("Luminálny B (HER2+)", "luminal_b_her2pos"),
            ("HER2-enriched", "her2_enriched"),
            ("Triple-negatívny", "tnbc"),
        )),
        Field_("inflammatory", "Inflamatórny karcinóm", _opts(
            ("Áno", "yes"), ("Nie", "no"),
        )),
        _MENO,
        Field_("genomic_risk", "Genomické riziko (Oncotype DX / MammaPrint)", _opts(
            ("Nízke", "low"), ("Vysoké", "high"), ("Nerobené", "not_done"),
        )),
        _BRCA,
    ],
)

# --- Metastatický / pokročilý karcinóm ---------------------------------------
METASTATIC = EntityDef(
    key=Entity.METASTATIC,
    title="Metastatický / pokročilý karcinóm",
    icon="🔴",
    fields=[
        Field_("subtype", "Klinický podtyp", _opts(
            ("HR+ / HER2−", "hr_pos_her2_neg"),
            ("HER2+", "her2_pos"),
            ("Triple-negatívny", "tnbc"),
        )),
        _ER, _HER2, _BRCA, _MENO,
        Field_("visceral_crisis", "Viscerálna kríza", _opts(
            ("Áno", "yes"), ("Nie", "no"),
        )),
        Field_("endocrine_status", "Endokrinná senzitivita", _opts(
            ("Senzitívny", "sensitive"), ("Rezistentný", "resistant"),
        )),
        Field_("pik3ca", "PIK3CA status", _opts(
            ("Mutovaný", "mutated"), ("Wild-type", "wildtype"),
        )),
    ],
)


ENTITIES = {
    Entity.DCIS: DCIS,
    Entity.INVASIVE: INVASIVE,
    Entity.METASTATIC: METASTATIC,
}

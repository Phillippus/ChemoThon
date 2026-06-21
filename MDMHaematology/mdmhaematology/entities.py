"""Definícia entít (modulov) a polí wizardu pre lymfómy.

TOTO NIE JE KLINICKÝ OBSAH — je to len konfigurácia formulára: aké atribúty sa
pýtame a aké hodnoty sú prípustné. Mapovanie kombinácie atribútov na odporúčanie
prebieha výhradne cez KB (kb/*.yaml) a deterministický matching engine.

Prognostické indexy (IPI/FLIPI/MIPI/IPS, early favorable/unfavorable) sa NEPOČÍTAJÚ —
zadávajú sa ako vstup. Appka nič nevyhodnocuje za behu, len páruje so záznamami KB.
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
def _stage_field() -> Field_:
    return Field_("stage", "Štádium (Lugano / Ann Arbor)", _opts(
        ("I", "I"), ("II", "II"), ("III", "III"), ("IV", "IV"),
    ))


_BSYMP = Field_("b_symptoms", "B-symptómy", _opts(
    ("Prítomné", "present"), ("Neprítomné", "absent"),
), "Horúčka > 38 °C, nočné potenie, úbytok hmotnosti > 10 % za 6 mes.")
_BULKY = Field_("bulky", "Bulky ochorenie", _opts(
    ("Áno", "yes"), ("Nie", "no"),
))


# --- Hodgkinov lymfóm ---------------------------------------------------------
HL = EntityDef(
    key=Entity.HL,
    title="Hodgkinov lymfóm (klasický)",
    icon="🎗️",
    fields=[
        _stage_field(),
        Field_("risk_group", "Riziková skupina", _opts(
            ("Skoré štádium — favorable", "early_fav"),
            ("Skoré štádium — unfavorable", "early_unfav"),
            ("Pokročilé štádium", "advanced"),
        ), "Podľa kritérií GHSG/EORTC (rizikové faktory: bulky, ESR, počet oblastí, extranodálne)."),
        _BSYMP,
        _BULKY,
    ],
)

# --- DLBCL --------------------------------------------------------------------
DLBCL = EntityDef(
    key=Entity.DLBCL,
    title="Difúzny veľkobunkový B-lymfóm (DLBCL)",
    icon="🔵",
    fields=[
        Field_("line", "Línia liečby", _opts(
            ("Prvá línia", "first_line"),
            ("Relaps / refraktérne", "relapsed_refractory"),
        )),
        _stage_field(),
        Field_("ipi_risk", "IPI / NCCN-IPI riziko", _opts(
            ("Nízke", "low"),
            ("Nízke-stredné", "low_int"),
            ("Vysoké-stredné", "high_int"),
            ("Vysoké", "high"),
        )),
        _BULKY,
        Field_("double_hit", "Double/triple-hit (MYC + BCL2/BCL6)", _opts(
            ("Áno", "yes"), ("Nie", "no"),
        ), "High-grade B-cell lymphoma s MYC a BCL2 a/alebo BCL6 prestavbou."),
    ],
)

# --- Folikulárny lymfóm -------------------------------------------------------
FL = EntityDef(
    key=Entity.FL,
    title="Folikulárny lymfóm (FL)",
    icon="🟢",
    fields=[
        _stage_field(),
        Field_("grade", "Grade", _opts(
            ("1–2", "g1_2"), ("3A", "g3a"), ("3B", "g3b"),
        ), "Grade 3B sa lieči ako DLBCL."),
        Field_("tumor_burden", "Nálož ochorenia (GELF)", _opts(
            ("Nízka (GELF−)", "low"), ("Vysoká (GELF+)", "high"),
        )),
        Field_("flipi_risk", "FLIPI riziko", _opts(
            ("Nízke", "low"), ("Stredné", "intermediate"), ("Vysoké", "high"),
        )),
    ],
)

# --- Lymfóm z plášťových buniek (MCL) -----------------------------------------
MCL = EntityDef(
    key=Entity.MCL,
    title="Lymfóm z plášťových buniek (MCL)",
    icon="🟣",
    fields=[
        _stage_field(),
        Field_("mipi_risk", "MIPI riziko", _opts(
            ("Nízke", "low"), ("Stredné", "intermediate"), ("Vysoké", "high"),
        )),
        Field_("transplant_eligible", "Vhodný na ASCT (mladší/fit)", _opts(
            ("Áno", "yes"), ("Nie", "no"),
        )),
        Field_("blastoid", "Blastoidný / pleomorfný variant", _opts(
            ("Áno", "yes"), ("Nie", "no"),
        )),
    ],
)

# --- Marginálnozónový lymfóm (MZL) --------------------------------------------
MZL = EntityDef(
    key=Entity.MZL,
    title="Marginálnozónový lymfóm (MZL)",
    icon="🟡",
    fields=[
        Field_("subtype", "Podtyp", _opts(
            ("Gastrický MALT", "gastric_malt"),
            ("Negastrický MALT (extranodálny)", "nongastric_malt"),
            ("Nodálny", "nodal"),
            ("Splenický", "splenic"),
        )),
        Field_("h_pylori", "Helicobacter pylori (gastrický MALT)", _opts(
            ("Pozitívny", "positive"), ("Negatívny", "negative"),
        )),
        _stage_field(),
    ],
)

# --- Periférny T-bunkový lymfóm (PTCL) ----------------------------------------
PTCL = EntityDef(
    key=Entity.PTCL,
    title="Periférny T-bunkový lymfóm (PTCL)",
    icon="🔴",
    fields=[
        Field_("subtype", "Podtyp", _opts(
            ("PTCL-NOS", "ptcl_nos"),
            ("Angioimunoblastový (AITL)", "aitl"),
            ("ALCL, ALK-pozitívny", "alcl_alk_pos"),
            ("ALCL, ALK-negatívny", "alcl_alk_neg"),
        )),
        _stage_field(),
        Field_("ipi_risk", "IPI riziko", _opts(
            ("Nízke", "low"), ("Stredné", "intermediate"), ("Vysoké", "high"),
        )),
    ],
)


ENTITIES = {
    Entity.HL: HL,
    Entity.DLBCL: DLBCL,
    Entity.FL: FL,
    Entity.MCL: MCL,
    Entity.MZL: MZL,
    Entity.PTCL: PTCL,
}

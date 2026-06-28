"""Definícia modulov a polí wizardu pre sarkómy a NET.

TOTO NIE JE KLINICKÝ OBSAH — je to len konfigurácia formulára: aké atribúty sa
pýtame a aké hodnoty sú prípustné. Mapovanie kombinácie atribútov na odporúčanie
prebieha výhradne cez KB (kb/*.yaml) a deterministický matching engine.

Rizikové skupiny (napr. GIST risk podľa Miettinen/AFIP, FNCLCC grade) sa NEPOČÍTAJÚ —
zadávajú sa ako vstup.
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


# --- Soft-tissue sarkóm -------------------------------------------------------
SOFT_TISSUE = EntityDef(
    key=Entity.SOFT_TISSUE,
    title="Soft-tissue sarkóm",
    icon="🟦",
    fields=[
        Field_("setting", "Klinická situácia", _opts(
            ("Lokalizovaný", "localized"),
            ("Metastatický", "metastatic"),
        )),
        Field_("location", "Lokalita", _opts(
            ("Končatina / trup", "extremity_trunk"),
            ("Retroperitoneum", "retroperitoneal"),
        )),
        Field_("grade", "Grade (FNCLCC)", _opts(
            ("G1", "g1"), ("G2", "g2"), ("G3", "g3"),
        )),
        Field_("size", "Veľkosť tumoru (= T kategória AJCC 8)", _opts(
            ("≤ 5 cm (T1)", "le5"),
            ("> 5–10 cm (T2)", "5_10"),
            ("> 10–15 cm (T3)", "10_15"),
            ("> 15 cm (T4)", "gt15"),
        ), "Veľkosť určuje T kategóriu (AJCC 8) — rozpíše sa vo výstupe."),
    ],
)

# --- GIST ---------------------------------------------------------------------
GIST = EntityDef(
    key=Entity.GIST,
    title="GIST (gastrointestinálny stromálny tumor)",
    icon="🟩",
    fields=[
        Field_("setting", "Klinická situácia", _opts(
            ("Lokalizovaný", "localized"),
            ("Metastatický / neresekabilný", "metastatic"),
        )),
        Field_("risk_group", "Riziko relapsu (Miettinen/AFIP)", _opts(
            ("Veľmi nízke", "very_low"),
            ("Nízke", "low"),
            ("Stredné", "intermediate"),
            ("Vysoké", "high"),
        ), "Podľa veľkosti, mitotického indexu a lokalizácie."),
        Field_("mutation", "Mutačný status", _opts(
            ("KIT exón 11", "kit_ex11"),
            ("KIT exón 9", "kit_ex9"),
            ("PDGFRA D842V", "pdgfra_d842v"),
            ("Wild-type", "wildtype"),
        )),
    ],
)

# --- Kostný sarkóm ------------------------------------------------------------
BONE = EntityDef(
    key=Entity.BONE,
    title="Kostný sarkóm",
    icon="🦴",
    fields=[
        Field_("subtype", "Histologický typ", _opts(
            ("Osteosarkóm", "osteosarcoma"),
            ("Ewingov sarkóm", "ewing"),
            ("Chondrosarkóm", "chondrosarcoma"),
        )),
        Field_("setting", "Klinická situácia", _opts(
            ("Lokalizovaný", "localized"),
            ("Metastatický", "metastatic"),
        )),
    ],
)

# --- Neuroendokrinný nádor (GEP-NET) ------------------------------------------
NET = EntityDef(
    key=Entity.NET,
    title="Neuroendokrinný nádor (GEP-NET)",
    icon="🟪",
    fields=[
        Field_("primary_site", "Primárna lokalita", _opts(
            ("Pankreas", "pancreatic"),
            ("Tenké črevo (midgut)", "midgut"),
            ("Iný GEP", "other_gep"),
        )),
        Field_("grade", "Grade (Ki-67 / mitózy)", _opts(
            ("G1", "g1"), ("G2", "g2"),
            ("G3 (dobre diferencovaný NET)", "g3_net"),
            ("NEC (slabo diferencovaný)", "nec"),
        )),
        Field_("functionality", "Funkčnosť", _opts(
            ("Funkčný", "functioning"),
            ("Nefunkčný", "nonfunctioning"),
        )),
        Field_("sstr", "Somatostatínové receptory (SSTR / DOTATATE PET)", _opts(
            ("Pozitívne", "positive"), ("Negatívne", "negative"),
        )),
        Field_("setting", "Klinická situácia", _opts(
            ("Lokalizovaný", "localized"),
            ("Pokročilý / metastatický", "advanced"),
        )),
    ],
)


ENTITIES = {
    Entity.SOFT_TISSUE: SOFT_TISSUE,
    Entity.GIST: GIST,
    Entity.BONE: BONE,
    Entity.NET: NET,
}

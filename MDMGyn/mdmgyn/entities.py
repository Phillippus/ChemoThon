"""Definícia entít a polí wizardu.

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

# Sentinel pre "nezadané / neznáme" — pri matchingu sa ignoruje (nikdy nematchne).
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


# --- Karcinóm endometria (FIGO 2023) ---------------------------------------
ENDOMETRIUM = EntityDef(
    key=Entity.ENDOMETRIUM,
    title="Karcinóm endometria",
    icon="🔬",
    fields=[
        Field_("figo_stage", "FIGO štádium (2023)", _opts(
            ("IA", "IA"), ("IB", "IB"), ("IC", "IC"),
            ("IIA", "IIA"), ("IIB", "IIB"), ("IIC", "IIC"),
            ("IIIA", "IIIA"), ("IIIB", "IIIB"),
            ("IIIC1", "IIIC1"), ("IIIC2", "IIIC2"),
            ("IVA", "IVA"), ("IVB", "IVB"), ("IVC", "IVC"),
        ), "FIGO 2023 klasifikácia karcinómu endometria."),
        Field_("histology", "Histologický typ", _opts(
            ("Endometrioidný", "endometrioid"),
            ("Serózny", "serous"),
            ("Clear cell", "clear_cell"),
            ("Karcinosarkóm", "carcinosarcoma"),
            ("Nediferencovaný / dediferencovaný", "undifferentiated"),
            ("Zmiešaný", "mixed"),
        )),
        Field_("grade", "Grading", _opts(
            ("G1", "G1"), ("G2", "G2"), ("G3", "G3"),
        )),
        Field_("myometrial_invasion", "Hĺbka myometriálnej invázie", _opts(
            ("< 50 %", "lt50"), ("≥ 50 %", "ge50"),
        )),
        Field_("lvsi", "LVSI", _opts(
            ("Negatívna", "negative"),
            ("Fokálna", "focal"),
            ("Substanciálna / rozsiahla", "substantial"),
        ), "Lymfovaskulárna invázia."),
        Field_("molecular", "Molekulárna klasifikácia", _opts(
            ("POLE-mutovaný", "POLEmut"),
            ("MMR-deficientný / MSI-H", "MMRd"),
            ("p53-abnormálny", "p53abn"),
            ("NSMP (no specific molecular profile)", "NSMP"),
        )),
        Field_("node_status", "Uzlinový status", _opts(
            ("Negatívny (cN0/pN0)", "negative"),
            ("Pozitívny", "positive"),
        )),
    ],
)

# --- Karcinóm cervixu (FIGO 2018) ------------------------------------------
CERVIX = EntityDef(
    key=Entity.CERVIX,
    title="Karcinóm cervixu",
    icon="🧬",
    fields=[
        Field_("figo_stage", "FIGO štádium (2018)", _opts(
            ("IA1", "IA1"), ("IA2", "IA2"),
            ("IB1", "IB1"), ("IB2", "IB2"), ("IB3", "IB3"),
            ("IIA1", "IIA1"), ("IIA2", "IIA2"), ("IIB", "IIB"),
            ("IIIA", "IIIA"), ("IIIB", "IIIB"),
            ("IIIC1", "IIIC1"), ("IIIC2", "IIIC2"),
            ("IVA", "IVA"), ("IVB", "IVB"),
        )),
        Field_("histology", "Histológia", _opts(
            ("Skvamózny karcinóm", "squamous"),
            ("Adenokarcinóm", "adenocarcinoma"),
            ("Adenoskvamózny", "adenosquamous"),
            ("Iný / zriedkavý", "other"),
        )),
        Field_("tumor_size", "Veľkosť tumoru", _opts(
            ("≤ 2 cm", "le2"), ("> 2–4 cm", "2to4"), ("> 4 cm", "gt4"),
        )),
        Field_("stromal_invasion", "Hĺbka stromálnej invázie", _opts(
            ("≤ 3 mm", "le3mm"), ("> 3–5 mm", "3to5mm"), ("> 5 mm", "gt5mm"),
        )),
        Field_("lvsi", "LVSI", _opts(
            ("Negatívna", "negative"), ("Pozitívna", "positive"),
        )),
        Field_("parametria", "Parametriálna invázia", _opts(
            ("Negatívna", "negative"), ("Pozitívna", "positive"),
        )),
        Field_("node_status", "Uzlinový status", _opts(
            ("Negatívny", "negative"), ("Pozitívny", "positive"),
        )),
    ],
)

# --- Karcinóm vulvy --------------------------------------------------------
VULVA = EntityDef(
    key=Entity.VULVA,
    title="Karcinóm vulvy",
    icon="🩺",
    fields=[
        Field_("figo_stage", "FIGO štádium", _opts(
            ("IA", "IA"), ("IB", "IB"), ("II", "II"),
            ("IIIA", "IIIA"), ("IIIB", "IIIB"), ("IIIC", "IIIC"),
            ("IVA", "IVA"), ("IVB", "IVB"),
        )),
        Field_("tumor_size", "Veľkosť tumoru", _opts(
            ("≤ 2 cm", "le2"), ("> 2 cm", "gt2"),
        )),
        Field_("depth_invasion", "Hĺbka invázie", _opts(
            ("≤ 1 mm", "le1mm"), ("> 1 mm", "gt1mm"),
        )),
        Field_("inguinal_nodes", "Status inguinálnych uzlín", _opts(
            ("Negatívne", "negative"), ("Pozitívne", "positive"),
        )),
        Field_("hpv_p16", "HPV / p16 status", _opts(
            ("HPV-asociovaný (p16+)", "hpv_associated"),
            ("HPV-nezávislý (p16−)", "hpv_independent"),
        )),
    ],
)

# --- Nádory ovária / adnex -------------------------------------------------
OVARY = EntityDef(
    key=Entity.OVARY,
    title="Nádory ovária / adnex",
    icon="⚕️",
    fields=[
        Field_("figo_stage", "FIGO štádium", _opts(
            ("IA", "IA"), ("IB", "IB"), ("IC", "IC"),
            ("IIA", "IIA"), ("IIB", "IIB"),
            ("IIIA", "IIIA"), ("IIIB", "IIIB"), ("IIIC", "IIIC"),
            ("IVA", "IVA"), ("IVB", "IVB"),
        )),
        Field_("histology", "Histologický typ", _opts(
            ("High-grade serózny", "high_grade_serous"),
            ("Low-grade serózny", "low_grade_serous"),
            ("Endometrioidný", "endometrioid"),
            ("Clear cell", "clear_cell"),
            ("Mucinózny", "mucinous"),
            ("Karcinosarkóm", "carcinosarcoma"),
        )),
        Field_("brca_hrd", "BRCA / HRD status", _opts(
            ("BRCA1/2 mutovaný", "brca_mut"),
            ("HRD-pozitívny (BRCA wt)", "hrd_positive"),
            ("HRD-negatívny / HRP", "hrd_negative"),
        )),
        Field_("residual_disease", "Reziduálne ochorenie po operácii", _opts(
            ("R0 / bez makroskopického rezídua", "r0"),
            ("Reziduálne ochorenie prítomné", "residual"),
        )),
    ],
)


ENTITIES = {
    Entity.ENDOMETRIUM: ENDOMETRIUM,
    Entity.CERVIX: CERVIX,
    Entity.VULVA: VULVA,
    Entity.OVARY: OVARY,
}

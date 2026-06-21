"""Pydantic schéma znalostnej databázy (knowledge base, KB) pre kolorektálny karcinóm.

Každý záznam je jedno odporúčanie jednej odbornej spoločnosti pre jednu kombináciu
klinicko-patologických kritérií. Schéma vynucuje povinné polia vrátane audit-trailu
(`generated_by`) a kontrolného stavu (`reviewed`).

Ak v KB chýba čo i len jedno povinné pole, načítanie/validácia (a teda aj pytest a CI)
zlyhá — viď kb_loader.load_kb a tests/test_kb_validation.py.
"""

from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field, model_validator


class Society(str, Enum):
    ESMO = "ESMO"
    NCCN = "NCCN"
    ASCO = "ASCO"


class Entity(str, Enum):
    """Klinické scenáre (moduly) kolorektálneho karcinómu."""

    COLON = "colon"
    RECTUM = "rectum"
    METASTATIC = "metastatic"


# Hodnota, ktorou v KB označujeme neoverenú/nedoplnenú lokáciu v zdroji.
UNVERIFIED_MARK = "NEOVERENÉ - doplniť"


class Recommendation(BaseModel):
    """Jeden záznam KB.

    `criteria` je mapa: názov klinického atribútu -> zoznam akceptovaných hodnôt.
    Záznam sa pri matchingu uplatní len vtedy, ak používateľ zadal danú hodnotu
    a tá je v zozname. Prázdne `criteria` = záznam platí pre celý modul (všeobecný).
    Hodnoty atribútov musia zodpovedať `value` poliam v entities.py.
    """

    model_config = ConfigDict(extra="forbid")

    id: str = Field(..., min_length=1, description="Unikátny identifikátor záznamu")
    entity: Entity
    society: Society
    guideline_version: str = Field(..., min_length=1)
    year: int = Field(..., ge=1990, le=2100)
    source_reference: str = Field(..., min_length=1)
    source_location: str = Field(..., min_length=1)
    recommendation_text: str = Field(..., min_length=1)

    # Voliteľné popisné polia zobrazované vo výstupe.
    risk_group: Optional[str] = None
    stage: Optional[str] = None

    criteria: Dict[str, List[str]] = Field(default_factory=dict)

    # Audit / kontrola.
    reviewed: bool = False
    reviewed_by: Optional[str] = None
    reviewed_date: Optional[str] = None
    generated_by: str = Field(..., min_length=1)

    @model_validator(mode="after")
    def _check_review_consistency(self) -> "Recommendation":
        if self.reviewed:
            if not (self.reviewed_by and self.reviewed_by.strip()):
                raise ValueError(
                    f"Záznam '{self.id}': reviewed=true, ale chýba reviewed_by."
                )
            if not (self.reviewed_date and self.reviewed_date.strip()):
                raise ValueError(
                    f"Záznam '{self.id}': reviewed=true, ale chýba reviewed_date."
                )
        return self

    @model_validator(mode="after")
    def _check_criteria_values(self) -> "Recommendation":
        for key, allowed in self.criteria.items():
            if not isinstance(allowed, list) or not allowed:
                raise ValueError(
                    f"Záznam '{self.id}': criteria['{key}'] musí byť neprázdny zoznam hodnôt."
                )
        return self

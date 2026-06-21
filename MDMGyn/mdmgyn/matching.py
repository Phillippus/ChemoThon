"""Deterministický matching engine nad KB.

Žiadna generatívna logika. Záznam sa uplatní práve vtedy, keď KAŽDÉ jeho kritérium
je splnené zadanými vstupmi používateľa:
  pre každý (key, allowed) v rec.criteria platí inputs.get(key) in allowed.
Atribúty, ktoré používateľ nezadal (prázdna hodnota), nemôžu splniť kritérium —
záznam s takým kritériom sa neuplatní (bezpečný fallback namiesto odhadu).

Záznamy s prázdnym `criteria` platia pre celú entitu (všeobecné odporúčania).
"""

from __future__ import annotations

from typing import Dict, List

from .schema import Entity, Recommendation, Society


def _matches(rec: Recommendation, inputs: Dict[str, str]) -> bool:
    for key, allowed in rec.criteria.items():
        value = inputs.get(key, "")
        if not value or value not in allowed:
            return False
    return True


def specificity(rec: Recommendation) -> int:
    """Počet splnených kritérií = miera špecifickosti záznamu (vyššie = konkrétnejšie)."""
    return len(rec.criteria)


def match(records: List[Recommendation], entity: Entity, inputs: Dict[str, str]) -> List[Recommendation]:
    """Vráti zoznam zhodných záznamov pre danú entitu, zoradený od najšpecifickejších."""
    hits = [
        rec for rec in records
        if rec.entity == entity and _matches(rec, inputs)
    ]
    hits.sort(key=lambda r: (specificity(r), r.society.value, r.id), reverse=True)
    return hits


def group_by_society(records: List[Recommendation]) -> Dict[Society, List[Recommendation]]:
    """Zoskupí zhody podľa spoločnosti — pre prehľadné zobrazenie rozdielov medzi guidelines."""
    out: Dict[Society, List[Recommendation]] = {}
    for rec in records:
        out.setdefault(rec.society, []).append(rec)
    return out

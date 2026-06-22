"""Testy deterministického matching enginu."""

from __future__ import annotations

from mdmgyn import matching
from mdmgyn.kb_loader import load_kb
from mdmgyn.schema import Entity, Recommendation, Society


def _rec(rec_id, society, criteria, entity=Entity.ENDOMETRIUM):
    return Recommendation(
        id=rec_id, entity=entity, society=society,
        guideline_version="v1", year=2021, source_reference="ref",
        source_location="s1", recommendation_text="text",
        criteria=criteria, generated_by="test",
    )


def test_full_criteria_match():
    recs = [_rec("a", Society.ESGO, {"figo_stage": ["IA"], "grade": ["G1", "G2"]})]
    hits = matching.match(recs, Entity.ENDOMETRIUM, {"figo_stage": "IA", "grade": "G1"})
    assert [r.id for r in hits] == ["a"]


def test_partial_input_does_not_match():
    """Ak používateľ nezadá atribút požadovaný kritériom, záznam sa neuplatní (bezpečný fallback)."""
    recs = [_rec("a", Society.ESGO, {"figo_stage": ["IA"], "grade": ["G1"]})]
    hits = matching.match(recs, Entity.ENDOMETRIUM, {"figo_stage": "IA", "grade": ""})
    assert hits == []


def test_value_not_in_allowed_does_not_match():
    recs = [_rec("a", Society.ESGO, {"grade": ["G1", "G2"]})]
    hits = matching.match(recs, Entity.ENDOMETRIUM, {"grade": "G3"})
    assert hits == []


def test_empty_criteria_always_matches_entity():
    recs = [_rec("general", Society.ESGO, {})]
    hits = matching.match(recs, Entity.ENDOMETRIUM, {"grade": "G3"})
    assert [r.id for r in hits] == ["general"]


def test_entity_isolation():
    recs = [_rec("a", Society.ESGO, {}, entity=Entity.CERVIX)]
    hits = matching.match(recs, Entity.ENDOMETRIUM, {})
    assert hits == []


def test_specificity_ordering():
    recs = [
        _rec("general", Society.ESGO, {}),
        _rec("specific", Society.ESGO, {"figo_stage": ["IA"], "grade": ["G1"]}),
    ]
    hits = matching.match(recs, Entity.ENDOMETRIUM, {"figo_stage": "IA", "grade": "G1"})
    assert hits[0].id == "specific"  # špecifickejšie pred všeobecným


def test_group_by_society():
    recs = [
        _rec("a", Society.ESGO, {}),
        _rec("b", Society.NCCN, {}),
    ]
    hits = matching.match(recs, Entity.ENDOMETRIUM, {})
    grouped = matching.group_by_society(hits)
    assert set(grouped.keys()) == {Society.ESGO, Society.NCCN}


def test_kb_low_risk_endometrium_matches_esgo():
    """Nízke riziko endometria (IA, endometrioidný, G1, LVSI neg) -> ESGO low-risk záznam."""
    kb = load_kb()
    inputs = {
        "figo_stage": "IA", "histology": "endometrioid",
        "grade": "G1", "lvsi": "negative",
    }
    hits = matching.match(kb, Entity.ENDOMETRIUM, inputs)
    assert Society.ESGO in {r.society for r in hits}


def test_kb_advanced_dmmr_endometrium_matches_nccn():
    """Pokročilý dMMR karcinóm endometria -> NCCN chemoimunoterapia (viac spoločností/záznamov)."""
    kb = load_kb()
    inputs = {"figo_stage": "IVB", "molecular": "MMRd"}
    hits = matching.match(kb, Entity.ENDOMETRIUM, inputs)
    assert Society.NCCN in {r.society for r in hits}

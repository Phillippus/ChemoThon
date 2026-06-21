"""Testy deterministického matching enginu — kolorektálny karcinóm."""

from __future__ import annotations

from mdmcolorectal import matching
from mdmcolorectal.kb_loader import load_kb
from mdmcolorectal.schema import Entity, Recommendation, Society


def _rec(rec_id, society, criteria, entity=Entity.COLON):
    return Recommendation(
        id=rec_id, entity=entity, society=society,
        guideline_version="v1", year=2023, source_reference="ref",
        source_location="s1", recommendation_text="text",
        criteria=criteria, generated_by="test",
    )


def test_full_criteria_match():
    recs = [_rec("a", Society.ESMO, {"stage": ["IIIA", "IIIB", "IIIC"]})]
    hits = matching.match(recs, Entity.COLON, {"stage": "IIIB"})
    assert [r.id for r in hits] == ["a"]


def test_partial_input_does_not_match():
    recs = [_rec("a", Society.NCCN, {"stage": ["IIA"], "high_risk_stage2": ["present"]})]
    hits = matching.match(recs, Entity.COLON, {"stage": "IIA", "high_risk_stage2": ""})
    assert hits == []


def test_value_not_in_allowed_does_not_match():
    recs = [_rec("a", Society.ESMO, {"stage": ["IIIA"]})]
    hits = matching.match(recs, Entity.COLON, {"stage": "I"})
    assert hits == []


def test_empty_criteria_always_matches_module():
    recs = [_rec("general", Society.ESMO, {})]
    hits = matching.match(recs, Entity.COLON, {"stage": "I"})
    assert [r.id for r in hits] == ["general"]


def test_module_isolation():
    recs = [_rec("a", Society.ESMO, {}, entity=Entity.METASTATIC)]
    hits = matching.match(recs, Entity.COLON, {})
    assert hits == []


def test_specificity_ordering():
    recs = [
        _rec("general", Society.ESMO, {}),
        _rec("specific", Society.NCCN, {"stage": ["IIA"], "high_risk_stage2": ["present"]}),
    ]
    hits = matching.match(recs, Entity.COLON, {"stage": "IIA", "high_risk_stage2": "present"})
    assert hits[0].id == "specific"


def test_seed_kb_mcrc_left_raswt_matches_egfr():
    kb = load_kb()
    inputs = {"sidedness": "left", "ras": "wildtype", "braf": "wildtype"}
    hits = matching.match(kb, Entity.METASTATIC, inputs)
    assert any(r.id == "mcrc-esmo-left-raswt-egfr" for r in hits)


def test_seed_kb_mcrc_dmmr_immuno():
    kb = load_kb()
    hits = matching.match(kb, Entity.METASTATIC, {"mmr_status": "dmmr"})
    assert any(r.id == "mcrc-nccn-dmmr-immuno" for r in hits)

"""Testy deterministického matching enginu — lymfómy."""

from __future__ import annotations

from mdmhaematology import matching
from mdmhaematology.kb_loader import load_kb
from mdmhaematology.schema import Entity, Recommendation, Society


def _rec(rec_id, society, criteria, entity=Entity.DLBCL):
    return Recommendation(
        id=rec_id, entity=entity, society=society,
        guideline_version="v1", year=2020, source_reference="ref",
        source_location="s1", recommendation_text="text",
        criteria=criteria, generated_by="test",
    )


def test_full_criteria_match():
    recs = [_rec("a", Society.ESMO, {"line": ["first_line"], "stage": ["III", "IV"]})]
    hits = matching.match(recs, Entity.DLBCL, {"line": "first_line", "stage": "IV"})
    assert [r.id for r in hits] == ["a"]


def test_partial_input_does_not_match():
    recs = [_rec("a", Society.ESMO, {"line": ["first_line"], "stage": ["III", "IV"]})]
    hits = matching.match(recs, Entity.DLBCL, {"line": "first_line", "stage": ""})
    assert hits == []


def test_value_not_in_allowed_does_not_match():
    recs = [_rec("a", Society.ESMO, {"double_hit": ["yes"]})]
    hits = matching.match(recs, Entity.DLBCL, {"double_hit": "no"})
    assert hits == []


def test_empty_criteria_always_matches_module():
    recs = [_rec("general", Society.ESMO, {})]
    hits = matching.match(recs, Entity.DLBCL, {"stage": "I"})
    assert [r.id for r in hits] == ["general"]


def test_module_isolation():
    recs = [_rec("a", Society.ESMO, {}, entity=Entity.HL)]
    hits = matching.match(recs, Entity.DLBCL, {})
    assert hits == []


def test_specificity_ordering():
    recs = [
        _rec("general", Society.ESMO, {"line": ["first_line"]}),
        _rec("specific", Society.NCCN, {"line": ["first_line"], "double_hit": ["no"], "ipi_risk": ["high"]}),
    ]
    inputs = {"line": "first_line", "double_hit": "no", "ipi_risk": "high"}
    hits = matching.match(recs, Entity.DLBCL, inputs)
    assert hits[0].id == "specific"


def test_seed_kb_hl_advanced_two_societies():
    """Pokročilý HL -> ESMO (PET-adapted) aj NCCN (A+AVD) zobrazené oddelene."""
    kb = load_kb()
    hits = matching.match(kb, Entity.HL, {"risk_group": "advanced"})
    societies = {r.society for r in hits}
    assert Society.ESMO in societies
    assert Society.NCCN in societies


def test_seed_kb_dlbcl_relapse_cart_eha():
    kb = load_kb()
    hits = matching.match(kb, Entity.DLBCL, {"line": "relapsed_refractory"})
    assert any(r.id == "dlbcl-eha-cart-relapse" and r.society == Society.EHA for r in hits)


def test_seed_kb_mzl_gastric_hp_positive():
    kb = load_kb()
    hits = matching.match(kb, Entity.MZL, {"subtype": "gastric_malt", "h_pylori": "positive"})
    assert any(r.id == "mzl-esmo-gastric-malt-hp-pos" for r in hits)

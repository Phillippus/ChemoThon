"""Testy deterministického matching enginu — karcinóm prsníka."""

from __future__ import annotations

from mdmmamma import matching
from mdmmamma.kb_loader import load_kb
from mdmmamma.schema import Entity, Recommendation, Society


def _rec(rec_id, society, criteria, entity=Entity.INVASIVE):
    return Recommendation(
        id=rec_id, entity=entity, society=society,
        guideline_version="v1", year=2023, source_reference="ref",
        source_location="s1", recommendation_text="text",
        criteria=criteria, generated_by="test",
    )


def test_full_criteria_match():
    recs = [_rec("a", Society.ESMO, {"subtype": ["tnbc"]})]
    hits = matching.match(recs, Entity.INVASIVE, {"subtype": "tnbc"})
    assert [r.id for r in hits] == ["a"]


def test_partial_input_does_not_match():
    recs = [_rec("a", Society.ESMO, {"subtype": ["luminal_a"], "nodal": ["negative"]})]
    hits = matching.match(recs, Entity.INVASIVE, {"subtype": "luminal_a", "nodal": ""})
    assert hits == []


def test_value_not_in_allowed_does_not_match():
    recs = [_rec("a", Society.ESMO, {"subtype": ["tnbc"]})]
    hits = matching.match(recs, Entity.INVASIVE, {"subtype": "luminal_a"})
    assert hits == []


def test_empty_criteria_always_matches_module():
    recs = [_rec("general", Society.ESMO, {})]
    hits = matching.match(recs, Entity.INVASIVE, {"subtype": "tnbc"})
    assert [r.id for r in hits] == ["general"]


def test_module_isolation():
    recs = [_rec("a", Society.ESMO, {}, entity=Entity.METASTATIC)]
    hits = matching.match(recs, Entity.INVASIVE, {})
    assert hits == []


def test_specificity_ordering():
    recs = [
        _rec("general", Society.ESMO, {}),
        _rec("specific", Society.ESMO, {"subtype": ["luminal_a"], "nodal": ["negative"]}),
    ]
    hits = matching.match(recs, Entity.INVASIVE, {"subtype": "luminal_a", "nodal": "negative"})
    assert hits[0].id == "specific"


def test_seed_kb_early_tnbc_matches_esmo():
    # Stage-gating: skorý TNBC záznam vyžaduje aj odvodené štádium (I–II).
    kb = load_kb()
    hits = matching.match(kb, Entity.INVASIVE, {"subtype": "tnbc", "stage": "IIA"})
    assert Society.ESMO in {r.society for r in hits}


def test_seed_kb_invasive_stage_gating_separates_early_vs_la_tnbc():
    """Stage I–II TNBC -> skorý záznam; stage III TNBC -> lokálne pokročilý záznam."""
    kb = load_kb()
    early = matching.match(kb, Entity.INVASIVE, {"subtype": "tnbc", "stage": "IIA"})
    la = matching.match(kb, Entity.INVASIVE, {"subtype": "tnbc", "stage": "IIIB"})
    assert any(r.id == "early-esmo-tnbc-chemo-pembro" for r in early)
    assert not any(r.id == "la-nccn-tnbc-neoadj-pembro" for r in early)
    assert any(r.id == "la-nccn-tnbc-neoadj-pembro" for r in la)
    assert not any(r.id == "early-esmo-tnbc-chemo-pembro" for r in la)


def test_seed_kb_metastatic_her2_first_line():
    kb = load_kb()
    hits = matching.match(kb, Entity.METASTATIC, {"subtype": "her2_pos"})
    assert any(r.id == "mbc-nccn-her2-1L-thp" for r in hits)

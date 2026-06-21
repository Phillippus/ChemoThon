"""Testy deterministického matching enginu — sarkómy a NET."""

from __future__ import annotations

from mdmsarcnet import matching
from mdmsarcnet.kb_loader import load_kb
from mdmsarcnet.schema import Entity, Recommendation, Society


def _rec(rec_id, society, criteria, entity=Entity.GIST):
    return Recommendation(
        id=rec_id, entity=entity, society=society,
        guideline_version="v1", year=2022, source_reference="ref",
        source_location="s1", recommendation_text="text",
        criteria=criteria, generated_by="test",
    )


def test_full_criteria_match():
    recs = [_rec("a", Society.ESMO, {"setting": ["metastatic"], "mutation": ["kit_ex9"]})]
    hits = matching.match(recs, Entity.GIST, {"setting": "metastatic", "mutation": "kit_ex9"})
    assert [r.id for r in hits] == ["a"]


def test_partial_input_does_not_match():
    recs = [_rec("a", Society.ESMO, {"setting": ["localized"], "risk_group": ["high"]})]
    hits = matching.match(recs, Entity.GIST, {"setting": "localized", "risk_group": ""})
    assert hits == []


def test_value_not_in_allowed_does_not_match():
    recs = [_rec("a", Society.NCCN, {"mutation": ["pdgfra_d842v"]})]
    hits = matching.match(recs, Entity.GIST, {"mutation": "kit_ex11"})
    assert hits == []


def test_empty_criteria_always_matches_module():
    recs = [_rec("general", Society.ESMO, {})]
    hits = matching.match(recs, Entity.GIST, {"setting": "localized"})
    assert [r.id for r in hits] == ["general"]


def test_module_isolation():
    recs = [_rec("a", Society.ESMO, {}, entity=Entity.NET)]
    hits = matching.match(recs, Entity.GIST, {})
    assert hits == []


def test_specificity_ordering():
    recs = [
        _rec("general", Society.NCCN, {"setting": ["metastatic"]}),
        _rec("specific", Society.ESMO, {"setting": ["metastatic"], "mutation": ["kit_ex9"]}),
    ]
    hits = matching.match(recs, Entity.GIST, {"setting": "metastatic", "mutation": "kit_ex9"})
    assert hits[0].id == "specific"


def test_seed_kb_gist_d842v_avapritinib():
    kb = load_kb()
    hits = matching.match(kb, Entity.GIST, {"mutation": "pdgfra_d842v"})
    assert any(r.id == "gist-nccn-pdgfra-d842v-avapritinib" for r in hits)


def test_seed_kb_net_advanced_sstr_positive_three_paths():
    """Pokročilý SSTR+ NET (G1/G2) -> ENETS (SSA) aj ESMO (PRRT)."""
    kb = load_kb()
    inputs = {"setting": "advanced", "grade": "g1", "sstr": "positive"}
    hits = matching.match(kb, Entity.NET, inputs)
    societies = {r.society for r in hits}
    assert Society.ENETS in societies
    assert Society.ESMO in societies


def test_seed_kb_net_nec_platinum():
    kb = load_kb()
    hits = matching.match(kb, Entity.NET, {"grade": "nec"})
    assert any(r.id == "net-esmo-nec-platinum-etoposide" for r in hits)

"""Validačné testy znalostnej databázy (KB) — sarkómy a NET.

Jadro architektúry proti halucinácii: ak akýkoľvek záznam nemá vyplnené všetky povinné
polia (vrátane `reviewed`) alebo je nekonzistentný, build zlyhá.
"""

from __future__ import annotations

import pytest

from mdmsarcnet.entities import ENTITIES
from mdmsarcnet.kb_loader import load_kb
from mdmsarcnet.schema import UNVERIFIED_MARK, Recommendation

REQUIRED_FIELDS = [
    "id", "entity", "society", "guideline_version", "year",
    "source_reference", "source_location", "recommendation_text",
    "reviewed", "generated_by",
]


@pytest.fixture(scope="module")
def kb():
    return load_kb()


def test_kb_loads_without_error(kb):
    assert isinstance(kb, list)
    assert len(kb) > 0


def test_every_record_has_required_fields(kb):
    for rec in kb:
        data = rec.model_dump()
        for fld in REQUIRED_FIELDS:
            assert fld in data, f"{rec.id}: chýba pole {fld}"
            if fld != "reviewed":
                assert data[fld] not in (None, ""), f"{rec.id}: prázdne pole {fld}"


def test_reviewed_records_have_reviewer(kb):
    for rec in kb:
        if rec.reviewed:
            assert rec.reviewed_by, f"{rec.id}: reviewed=true bez reviewed_by"
            assert rec.reviewed_date, f"{rec.id}: reviewed=true bez reviewed_date"


def test_ids_are_unique(kb):
    ids = [r.id for r in kb]
    assert len(ids) == len(set(ids)), "Duplicitné id v KB"


def test_all_modules_have_seed_records(kb):
    present = {r.entity for r in kb}
    for entity in ENTITIES:
        assert entity in present, f"Modul {entity.value} nemá žiadny záznam"


def test_criteria_keys_are_known_fields(kb):
    for rec in kb:
        valid_keys = {f.key for f in ENTITIES[rec.entity].fields}
        for key in rec.criteria:
            assert key in valid_keys, (
                f"{rec.id}: criteria kľúč '{key}' nie je pole modulu {rec.entity.value}"
            )


def test_criteria_values_are_known_options(kb):
    for rec in kb:
        fields = {f.key: {v for _, v in f.options} for f in ENTITIES[rec.entity].fields}
        for key, allowed in rec.criteria.items():
            valid_values = fields.get(key, set())
            for val in allowed:
                assert val in valid_values, (
                    f"{rec.id}: criteria['{key}'] hodnota '{val}' nie je platná možnosť"
                )


def test_missing_required_field_fails_validation():
    with pytest.raises(Exception):
        Recommendation(**{"id": "x", "entity": "gist", "society": "ESMO"})


def test_reviewed_true_without_reviewer_fails():
    with pytest.raises(Exception):
        Recommendation(
            id="x", entity="gist", society="ESMO",
            guideline_version="v1", year=2022, source_reference="ref",
            source_location=UNVERIFIED_MARK, recommendation_text="t",
            reviewed=True, generated_by="test",
        )


def test_unknown_field_rejected():
    with pytest.raises(Exception):
        Recommendation(
            id="x", entity="gist", society="ESMO",
            guideline_version="v1", year=2022, source_reference="ref",
            source_location="s", recommendation_text="t",
            generated_by="test", reviewd=False,  # preklep
        )

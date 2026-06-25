"""Testy AJCC 8 stagingu (mdmmamma.staging).

Prognostické testy vychádzajú z 5 OFICIÁLNYCH príkladov z AJCC webinára
(facs.org 8th-edition-breast-staging.pdf) — slúžia ako kontrola rekonštrukcie.
"""

from __future__ import annotations

from mdmmamma.staging import anatomic_stage, clinical_prognostic_stage


# --- Anatomické (čisté T/N/M) ---
def test_anatomic_basic():
    assert anatomic_stage("Tis", "N0", "M0") == "0"
    assert anatomic_stage("T1", "N0", "M0") == "IA"
    assert anatomic_stage("T2", "N0", "M0") == "IIA"
    assert anatomic_stage("T3", "N0", "M0") == "IIB"
    assert anatomic_stage("T2", "N1", "M0") == "IIB"
    assert anatomic_stage("T3", "N1", "M0") == "IIIA"
    assert anatomic_stage("T1", "N2", "M0") == "IIIA"
    assert anatomic_stage("T4", "N0", "M0") == "IIIB"
    assert anatomic_stage("T2", "N3", "M0") == "IIIC"
    assert anatomic_stage("T1", "N0", "M1") == "IV"


def test_anatomic_incomplete():
    assert anatomic_stage("", "N0", "M0") is None


# --- Klinické prognostické: 5 oficiálnych AJCC anchorov ---
def _cps(t, n, m, g, her2, er, pr):
    return clinical_prognostic_stage(t, n, m, g, her2, er, pr)[0]


def test_cps_anchor_t2n0_g2_hrpos_her2neg_IB():
    assert _cps("T2", "N0", "M0", "G2", "her2_zero", "positive", "positive") == "IB"


def test_cps_anchor_t2n0_g3_hrpos_her2neg_IIA():
    assert _cps("T2", "N0", "M0", "G3", "her2_zero", "positive", "positive") == "IIA"


def test_cps_anchor_t3n0_g2_tnbc_IIIB():
    assert _cps("T3", "N0", "M0", "G2", "her2_zero", "negative", "negative") == "IIIB"


def test_cps_anchor_t1a_n0_g2_hrpos_her2neg_IA():
    assert _cps("T1", "N0", "M0", "G2", "her2_zero", "positive", "positive") == "IA"


def test_cps_anchor_t2n1_g2_hrpos_her2neg_IIA():
    assert _cps("T2", "N1", "M0", "G2", "her2_zero", "positive", "positive") == "IIA"


# --- Hraničné prípady ---
def test_cps_m1_is_IV():
    assert _cps("T2", "N1", "M1", "G2", "her2_positive", "positive", "negative") == "IV"


def test_cps_tis_is_0():
    assert _cps("Tis", "N0", "M0", "", "", "", "") == "0"


def test_cps_incomplete_biomarkers_falls_back_to_anatomic():
    stage, note = clinical_prognostic_stage("T2", "N0", "M0", "", "her2_zero", "positive", "positive")
    assert stage == "IIA"  # anatomické
    assert "neúpln" in note.lower() or "NEOVEREN" in note


def test_cps_her2pos_falls_back_with_note():
    stage, note = clinical_prognostic_stage("T2", "N0", "M0", "G2", "her2_positive", "positive", "positive")
    assert stage == "IIA"  # anatomické fallback
    assert "HER2" in note

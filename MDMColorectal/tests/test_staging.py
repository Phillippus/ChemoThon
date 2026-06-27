"""Kontrola deterministického odvodenia AJCC 8 štádia z rozpísaného TNM (kolorektál).

POZN.: tabuľka je NEOVERENÁ (rekonštruovaná z AJCC 8 štandardu) — tieto testy
fixujú očakávané správanie, Filip overí oproti AJCC manuálu.
"""

from mdmcolorectal import staging


def test_stage_node_negative():
    assert staging.anatomic_stage("Tis", "N0", "M0") == "0"
    assert staging.anatomic_stage("T1", "N0", "M0") == "I"
    assert staging.anatomic_stage("T2", "N0", "M0") == "I"
    assert staging.anatomic_stage("T3", "N0", "M0") == "IIA"
    assert staging.anatomic_stage("T4a", "N0", "M0") == "IIB"
    assert staging.anatomic_stage("T4b", "N0", "M0") == "IIC"


def test_stage_node_positive():
    assert staging.anatomic_stage("T1", "N1a", "M0") == "IIIA"
    assert staging.anatomic_stage("T1", "N2a", "M0") == "IIIA"
    assert staging.anatomic_stage("T1", "N2b", "M0") == "IIIB"
    assert staging.anatomic_stage("T3", "N1b", "M0") == "IIIB"
    assert staging.anatomic_stage("T3", "N2a", "M0") == "IIIB"
    assert staging.anatomic_stage("T3", "N2b", "M0") == "IIIC"
    assert staging.anatomic_stage("T4a", "N2a", "M0") == "IIIC"
    assert staging.anatomic_stage("T4b", "N1a", "M0") == "IIIC"


def test_stage_metastatic():
    assert staging.anatomic_stage("T3", "N1a", "M1a") == "IVA"
    assert staging.anatomic_stage("T3", "N1a", "M1b") == "IVB"
    assert staging.anatomic_stage("T3", "N1a", "M1c") == "IVC"


def test_incomplete_returns_none():
    assert staging.anatomic_stage("", "N0", "M0") is None
    assert staging.anatomic_stage("T1", "", "M0") is None


def test_coarse_mappings():
    assert staging.coarse_ct("cT1") == "cT1_2"
    assert staging.coarse_ct("cT2") == "cT1_2"
    assert staging.coarse_ct("cT3") == "cT3"
    assert staging.coarse_ct("cT4a") == "cT4"
    assert staging.coarse_ct("cT4b") == "cT4"
    assert staging.coarse_cn("cN0") == "cN0"
    assert staging.coarse_cn("cN1") == "cN_pos"
    assert staging.coarse_cn("cN2") == "cN_pos"

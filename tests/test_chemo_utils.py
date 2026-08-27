"""Testy pre centrálny dávkovací 'rules engine' ChemoThonu (chemo_utils.py).

Kryje: BSA vzorec (DuBois), Calvertov vzorec (karboplatina), a gating logiku
okolo tlačidla "Vypočítať chemoterapiu" v Gyn module (ChemoCBDCA s
predvyplnenými/chýbajúcimi CrCl/AUC).

Referenčné hodnoty pre BSA a Calvert boli prepočítané nezávisle od
implementácie (pozri komentáre pri jednotlivých testoch).
"""
import pytest

import chemo_utils


# ---------------------------------------------------------------------------
# BSA (DuBois formula)
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "weight_kg, height_cm, expected_m2",
    [
        (70, 170, 1.81),   # bežný dospelý pacient
        (60, 160, 1.62),
        (90, 180, 2.1),
        (50, 150, 1.43),   # nízka hmotnosť/výška
    ],
)
def test_bsa_dubois_formula(weight_kg, height_cm, expected_m2):
    assert chemo_utils.bsa(weight_kg, height_cm) == expected_m2


def test_bsa_rounds_to_two_decimals():
    result = chemo_utils.bsa(73, 168)
    assert result == round(result, 2)


# ---------------------------------------------------------------------------
# Calvertov vzorec (karboplatina): dávka = (CrCl + 25) * AUC
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    "crcl, auc, expected_mg",
    [
        (60, 5, 425),
        (100, 6, 750),
        (1, 2, 52),      # minimum povoleného rozsahu CrCl v UI (min_value=1)
        (250, 6, 1650),  # maximum povoleného rozsahu CrCl v UI (max_value=250)
    ],
)
def test_calvert_carboplatin_dose(crcl, auc, expected_mg):
    assert chemo_utils.calvert_carboplatin_dose(crcl, auc) == expected_mg


def test_calvert_carboplatin_dose_at_platinum_eligibility_boundary():
    """CrCl 30 ml/min je klinická hranica platina-eligibility (pozri
    ChemoThonGynEng.py: 'crcl < 30 → platinum-ineligible'). Samotný Calvertov
    vzorec dávku počíta rovnako na hranici aj tesne pod ňou — eligibilitu
    vyhodnocuje volajúci kód, nie tento vzorec."""
    assert chemo_utils.calvert_carboplatin_dose(30, 2) == 110
    assert chemo_utils.calvert_carboplatin_dose(29, 2) == 108


# ---------------------------------------------------------------------------
# Gating: tlačidlo "Vypočítať chemoterapiu" / ChemoCBDCA s chýbajúcimi
# voliteľnými poľami (CrCl, AUC)
# ---------------------------------------------------------------------------

class _FakeStreamlit:
    """Minimálna náhrada za `streamlit`, aby sa dal ChemoCBDCA testovať bez
    bežiacej Streamlit session. Zaznamenáva, či bol number_input zavolaný
    (čiže či appka žiadala CrCl/AUC znova, aj keď už boli zadané vopred)."""

    def __init__(self, number_input_return=None):
        self.number_input_calls = 0
        self._number_input_return = number_input_return
        self.written = []

    def number_input(self, *args, **kwargs):
        self.number_input_calls += 1
        return self._number_input_return

    def write(self, *args, **kwargs):
        self.written.append(args[0] if args else "")

    def error(self, *args, **kwargs):
        pass

    def markdown(self, *args, **kwargs):
        pass


@pytest.fixture
def fake_st(monkeypatch):
    fake = _FakeStreamlit()
    monkeypatch.setattr(chemo_utils, "st", fake)
    return fake


def test_chemo_cbdca_uses_precollected_crcl_auc_without_reasking(fake_st):
    """Keď volajúci (napr. gated tlačidlo v Gyn module) už CrCl/AUC vopred
    zozbieral, ChemoCBDCA ich nesmie žiadať znova (žiadna duplicitná logika/
    UI mimo toho, čo už bolo zadané)."""
    chemo_utils.ChemoCBDCA(1.81, "paclitaxel3weekly.json", crcl=60, auc=5)
    assert fake_st.number_input_calls == 0
    assert any("425" in str(w) for w in fake_st.written)


def test_chemo_cbdca_missing_optional_auc_does_not_compute_dose(fake_st):
    """Chýbajúce voliteľné pole (AUC nezadané) → žiadna dávka sa nesmie
    vypočítať/zobraziť; appka sa má spýtať cez number_input (vráti None,
    keďže pole nie je vyplnené)."""
    fake_st._number_input_return = None
    chemo_utils.ChemoCBDCA(1.81, "paclitaxel3weekly.json")
    assert fake_st.number_input_calls == 2  # CrCl aj AUC
    assert not any("CBDCA AUC" in str(w) for w in fake_st.written)


def test_chemo_cbdca_missing_crcl_only_does_not_compute_dose(fake_st):
    """Ak je vopred zadané len AUC, ale CrCl nie (voliteľné pole chýba),
    appka si CrCl dopýta a dávka sa nepočíta, kým nie je aj CrCl k dispozícii."""
    fake_st._number_input_return = None
    chemo_utils.ChemoCBDCA(1.81, "paclitaxel3weekly.json", auc=5)
    assert fake_st.number_input_calls == 1  # len CrCl, AUC bolo už zadané
    assert not any("CBDCA AUC" in str(w) for w in fake_st.written)

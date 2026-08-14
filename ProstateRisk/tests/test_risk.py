from prostaterisk.risk import ProstateInputs, classify, grade_group


def test_grade_group_mapping():
    assert grade_group(3, 3) == 1
    assert grade_group(3, 4) == 2
    assert grade_group(4, 3) == 3
    assert grade_group(4, 4) == 4
    assert grade_group(3, 5) == 4
    assert grade_group(5, 3) == 4
    assert grade_group(4, 5) == 5
    assert grade_group(5, 4) == 5
    assert grade_group(5, 5) == 5


def test_very_low_risk():
    inputs = ProstateInputs(
        t_stage="T1c", n_stage="N0", m_stage="M0",
        gleason_primary=3, gleason_secondary=3, psa=6.0,
        cores_positive=1, cores_total=12,
        max_core_involvement_pct=20.0, psa_density=0.10,
    )
    result = classify(inputs)
    assert result.risk_group == "Veľmi nízke riziko"


def test_low_risk_when_very_low_criteria_unset():
    inputs = ProstateInputs(
        t_stage="T2a", n_stage="N0", m_stage="M0",
        gleason_primary=3, gleason_secondary=3, psa=8.0,
    )
    result = classify(inputs)
    assert result.risk_group == "Nízke riziko"
    assert result.caveats  # missing very-low sub-criteria flagged


def test_low_risk_not_very_low_due_to_core_count():
    inputs = ProstateInputs(
        t_stage="T1c", n_stage="N0", m_stage="M0",
        gleason_primary=3, gleason_secondary=3, psa=6.0,
        cores_positive=5, cores_total=12,
        max_core_involvement_pct=20.0, psa_density=0.10,
    )
    result = classify(inputs)
    assert result.risk_group == "Nízke riziko"


def test_intermediate_favorable_single_irf():
    inputs = ProstateInputs(
        t_stage="T1c", n_stage="N0", m_stage="M0",
        gleason_primary=3, gleason_secondary=4, psa=6.0,
        cores_positive=3, cores_total=12,
    )
    result = classify(inputs)
    assert result.risk_group == "Stredné riziko"
    assert result.subgroup == "Priaznivé"


def test_intermediate_unfavorable_multiple_irf():
    inputs = ProstateInputs(
        t_stage="T2b", n_stage="N0", m_stage="M0",
        gleason_primary=3, gleason_secondary=4, psa=12.0,
    )
    result = classify(inputs)
    assert result.risk_group == "Stredné riziko"
    assert result.subgroup == "Nepriaznivé"


def test_intermediate_unfavorable_due_to_gg3():
    inputs = ProstateInputs(
        t_stage="T1c", n_stage="N0", m_stage="M0",
        gleason_primary=4, gleason_secondary=3, psa=6.0,
    )
    result = classify(inputs)
    assert result.risk_group == "Stredné riziko"
    assert result.subgroup == "Nepriaznivé"


def test_high_risk_via_t3a():
    inputs = ProstateInputs(
        t_stage="T3a", n_stage="N0", m_stage="M0",
        gleason_primary=3, gleason_secondary=3, psa=6.0,
    )
    result = classify(inputs)
    assert result.risk_group == "Vysoké riziko"


def test_high_risk_via_psa():
    inputs = ProstateInputs(
        t_stage="T1c", n_stage="N0", m_stage="M0",
        gleason_primary=3, gleason_secondary=3, psa=25.0,
    )
    result = classify(inputs)
    assert result.risk_group == "Vysoké riziko"


def test_very_high_risk_via_t3b():
    inputs = ProstateInputs(
        t_stage="T3b", n_stage="N0", m_stage="M0",
        gleason_primary=3, gleason_secondary=3, psa=6.0,
    )
    result = classify(inputs)
    assert result.risk_group == "Veľmi vysoké riziko"


def test_very_high_risk_via_primary_pattern_5():
    inputs = ProstateInputs(
        t_stage="T1c", n_stage="N0", m_stage="M0",
        gleason_primary=5, gleason_secondary=4, psa=6.0,
    )
    result = classify(inputs)
    assert result.risk_group == "Veľmi vysoké riziko"


def test_very_high_risk_via_two_high_features():
    inputs = ProstateInputs(
        t_stage="T3a", n_stage="N0", m_stage="M0",
        gleason_primary=4, gleason_secondary=4, psa=6.0,
    )
    result = classify(inputs)
    assert result.risk_group == "Veľmi vysoké riziko"


def test_regional_n1_overrides_everything():
    inputs = ProstateInputs(
        t_stage="T1c", n_stage="N1", m_stage="M0",
        gleason_primary=3, gleason_secondary=3, psa=6.0,
    )
    result = classify(inputs)
    assert result.risk_group == "Regionálne (N1)"


def test_metastatic_m1_overrides_everything():
    inputs = ProstateInputs(
        t_stage="T1c", n_stage="N1", m_stage="M1",
        gleason_primary=3, gleason_secondary=3, psa=6.0,
    )
    result = classify(inputs)
    assert result.risk_group == "Metastatické (M1)"

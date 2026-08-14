"""Deterministická riziková stratifikácia lokalizovaného/lokálne pokročilého
karcinómu prostaty podľa NCCN.

REKONŠTRUOVANÉ Z PAMÉTE — NEOVERENÉ. Kritériá nižšie zodpovedajú rizikovým
skupinám tak, ako ich NCCN Clinical Practice Guidelines in Oncology: Prostate
Cancer definuje v tabuľke "Risk Group and Nomogram Stratification for Clinically
Localized Prostate Cancer" (sekcia PROS-2 v printovej verzii guideline).
Pred klinickým použitím MUSIA byť hraničné hodnoty overené oproti aktuálnej
verzii guideline (číslo verzie a rok sa menia niekoľkokrát ročne).

Žiadny LLM sa pri behu tejto appky nepoužíva — klasifikácia je čisto
deterministická funkcia vstupných parametrov.
"""

from __future__ import annotations

from dataclasses import dataclass, field

NCCN_SOURCE_LABEL = "NCCN Guidelines: Prostate Cancer — NEOVERENÉ (doplniť presnú verziu/rok pri kontrole)"

T_STAGES = ["T1a", "T1b", "T1c", "T2a", "T2b", "T2c", "T3a", "T3b", "T4"]
N_STAGES = ["N0", "N1"]
M_STAGES = ["M0", "M1"]

RISK_ORDER = [
    "Veľmi nízke riziko",
    "Nízke riziko",
    "Stredné riziko",
    "Vysoké riziko",
    "Veľmi vysoké riziko",
    "Regionálne (N1)",
    "Metastatické (M1)",
]


def grade_group(primary: int, secondary: int) -> int:
    """Prevedie primárny + sekundárny Gleason pattern na ISUP Grade Group (1–5)."""
    if primary not in (3, 4, 5) or secondary not in (3, 4, 5):
        raise ValueError("Gleason pattern musí byť 3, 4 alebo 5")
    score = primary + secondary
    if score <= 6:
        return 1
    if primary == 3 and secondary == 4:
        return 2
    if primary == 4 and secondary == 3:
        return 3
    if score == 8:
        return 4
    return 5  # 9-10


@dataclass
class ProstateInputs:
    t_stage: str
    n_stage: str
    m_stage: str
    gleason_primary: int
    gleason_secondary: int
    psa: float
    cores_positive: int | None = None
    cores_total: int | None = None
    max_core_involvement_pct: float | None = None
    psa_density: float | None = None
    cores_grade_group_4_5: int | None = None

    @property
    def gg(self) -> int:
        return grade_group(self.gleason_primary, self.gleason_secondary)

    @property
    def gleason_score(self) -> int:
        return self.gleason_primary + self.gleason_secondary

    @property
    def pct_positive_cores(self) -> float | None:
        if self.cores_positive is None or not self.cores_total:
            return None
        return 100.0 * self.cores_positive / self.cores_total


@dataclass
class RiskResult:
    risk_group: str
    subgroup: str | None = None
    matched_criteria: list[str] = field(default_factory=list)
    caveats: list[str] = field(default_factory=list)


def classify(inputs: ProstateInputs) -> RiskResult:
    """Vráti NCCN rizikovú skupinu (a pri strednom riziku priaznivú/nepriaznivú
    subkategóriu) pre zadané klinicko-patologické parametre."""

    if inputs.m_stage == "M1":
        return RiskResult(
            risk_group="Metastatické (M1)",
            matched_criteria=["M1 — vzdialené metastázy"],
        )

    if inputs.n_stage == "N1":
        return RiskResult(
            risk_group="Regionálne (N1)",
            matched_criteria=["N1 — regionálne uzlinové postihnutie"],
        )

    gg = inputs.gg
    t = inputs.t_stage
    psa = inputs.psa
    caveats: list[str] = []

    # --- Vysokorizikové znaky (pre Vysoké aj Veľmi vysoké riziko) ---
    high_features: list[str] = []
    if t == "T3a":
        high_features.append("cT3a")
    if gg in (4, 5):
        high_features.append(f"Grade Group {gg} (Gleason {inputs.gleason_score})")
    if psa > 20:
        high_features.append("PSA > 20 ng/mL")

    # --- Znaky veľmi vysokého rizika ---
    very_high_features: list[str] = []
    if t in ("T3b", "T4"):
        very_high_features.append(f"c{t} (T3b–T4)")
    if inputs.gleason_primary == 5:
        very_high_features.append("primárny Gleason pattern 5")
    if len(high_features) >= 2:
        very_high_features.append(f"{len(high_features)} vysokorizikové znaky súčasne")
    if inputs.cores_grade_group_4_5 is not None and inputs.cores_grade_group_4_5 > 4:
        very_high_features.append(">4 pozitívne jadrá s Grade Group 4–5")
    elif inputs.cores_grade_group_4_5 is None and gg in (4, 5):
        caveats.append(
            "Nezadaný počet jadier s Grade Group 4–5 — kritérium '>4 jadrá GG4–5' pre "
            "veľmi vysoké riziko nemožno overiť."
        )

    if very_high_features:
        return RiskResult(
            risk_group="Veľmi vysoké riziko",
            matched_criteria=very_high_features,
            caveats=caveats,
        )

    if high_features:
        return RiskResult(
            risk_group="Vysoké riziko",
            matched_criteria=high_features,
            caveats=caveats,
        )

    # --- Intermediate risk factors (IRF) ---
    irf: list[str] = []
    if t in ("T2b", "T2c"):
        irf.append("cT2b–T2c")
    if gg in (2, 3):
        irf.append(f"Grade Group {gg} (Gleason {inputs.gleason_score})")
    if 10 <= psa <= 20:
        irf.append("PSA 10–20 ng/mL")

    if irf:
        unfav_reasons: list[str] = []
        if len(irf) >= 2:
            unfav_reasons.append(f"{len(irf)} IRF súčasne")
        if gg == 3:
            unfav_reasons.append("Grade Group 3 (Gleason 4+3=7)")
        pct = inputs.pct_positive_cores
        if pct is not None and pct >= 50:
            unfav_reasons.append("≥50 % pozitívnych bioptických jadier")
        elif pct is None:
            caveats.append(
                "Nezadaný podiel pozitívnych jadier — kritérium '≥50 % jadier' pre "
                "nepriaznivé stredné riziko nemožno overiť."
            )

        subgroup = "Nepriaznivé" if unfav_reasons else "Priaznivé"
        matched = irf + (unfav_reasons if subgroup == "Nepriaznivé" else [])
        return RiskResult(
            risk_group="Stredné riziko",
            subgroup=subgroup,
            matched_criteria=matched,
            caveats=caveats,
        )

    # --- Nízke / veľmi nízke riziko (T1-T2a, GG1, PSA < 10) ---
    base_low = t in ("T1a", "T1b", "T1c", "T2a") and gg == 1 and psa < 10
    if not base_low:
        # Nemalo by nastať pri korektne definovaných hraniciach vyššie, ale
        # radšej explicitne nahlásiť namiesto tichého nesprávneho zaradenia.
        return RiskResult(
            risk_group="Nezaradené",
            matched_criteria=[],
            caveats=[
                "Kombinácia parametrov nezodpovedá žiadnej NCCN kategórii podľa "
                "implementovanej logiky — over manuálne oproti guideline."
            ],
        )

    very_low_checks = {
        "cT1c": t == "T1c",
        "< 3 pozitívne jadrá": inputs.cores_positive is not None and inputs.cores_positive < 3,
        "≤ 50 % nádoru v každom pozitívnom jadre": (
            inputs.max_core_involvement_pct is not None and inputs.max_core_involvement_pct <= 50
        ),
        "PSA denzita < 0.15 ng/mL/g": (
            inputs.psa_density is not None and inputs.psa_density < 0.15
        ),
    }
    missing = [k for k, v in very_low_checks.items() if not v]
    # Chýbajúce (nezadané) hodnoty odlíšime od skutočne nesplnených.
    unset = []
    if inputs.cores_positive is None:
        unset.append("< 3 pozitívne jadrá")
    if inputs.max_core_involvement_pct is None:
        unset.append("≤ 50 % nádoru v každom pozitívnom jadre")
    if inputs.psa_density is None:
        unset.append("PSA denzita < 0.15 ng/mL/g")

    if all(very_low_checks.values()):
        return RiskResult(
            risk_group="Veľmi nízke riziko",
            matched_criteria=["cT1c", "Grade Group 1", "PSA < 10 ng/mL"] + list(very_low_checks.keys()),
            caveats=caveats,
        )

    if unset:
        caveats.append(
            "Nezadané parametre (" + ", ".join(unset) + ") — kritériá veľmi nízkeho "
            "rizika nemožno overiť, appka konzervatívne zaradila do 'Nízke riziko'."
        )

    return RiskResult(
        risk_group="Nízke riziko",
        matched_criteria=[t if t != "T1c" else "cT1-T2a", "Grade Group 1", "PSA < 10 ng/mL"],
        caveats=caveats,
    )

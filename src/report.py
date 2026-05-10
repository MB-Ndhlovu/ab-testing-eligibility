"""Generate a readable summary report from simulation results."""

from src.simulate import run_simulation


def generate_report(seed: int = 42) -> str:
    """Generate a human-readable summary report.

    Args:
        seed: Random seed used in data generation.

    Returns:
        Formatted string report.
    """
    results = run_simulation(seed=seed)
    metrics = results["metrics"]
    appr = results["approval_test"]
    defl = results["default_test"]

    lines = [
        "=" * 60,
        "     A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY REPORT",
        "=" * 60,
        "",
        "SAMPLE METRICS",
        "-" * 40,
        f"{'Metric':<22} {'Group A':>12} {'Group B':>12}",
        f"{'n':<22} {metrics['A']['n']:>12} {metrics['B']['n']:>12}",
        f"{'Approval Rate':<22} {metrics['A']['approval_rate']:>11.2%} {metrics['B']['approval_rate']:>11.2%}",
        f"{'Default Rate':<22} {metrics['A']['default_rate']:>11.2%} {metrics['B']['default_rate']:>11.2%}",
        f"{'Avg Loan Size':<22} {'$'+str(round(metrics['A']['avg_loan_size'],2)):>12} {'$'+str(round(metrics['B']['avg_loan_size'],2)):>12}",
        f"{'Avg Processing Days':<22} {metrics['A']['avg_processing_days']:>12.1f} {metrics['B']['avg_processing_days']:>12.1f}",
        "",
        "STATISTICAL RESULTS",
        "-" * 40,
        "1. APPROVAL RATE",
        f"   Observed:     A={appr['p_A']:.4f}  B={appr['p_B']:.4f}  Diff={appr['diff']:+.4f}",
        f"   Z-statistic:  {appr['z_statistic']:.4f}",
        f"   P-value:      {appr['p_value']:.6f}",
        f"   95% CI:       [{appr['ci_lower']:+.4f}, {appr['ci_upper']:+.4f}]",
        f"   Significant: {'YES' if appr['significant'] else 'NO'}  (alpha=0.05)",
        f"   MDE (80%):    {appr['mde']:.4f}",
        "",
        "2. DEFAULT RATE",
        f"   Observed:     A={defl['p_A']:.4f}  B={defl['p_B']:.4f}  Diff={defl['diff']:+.4f}",
        f"   Z-statistic:  {defl['z_statistic']:.4f}",
        f"   P-value:      {defl['p_value']:.6f}",
        f"   95% CI:       [{defl['ci_lower']:+.4f}, {defl['ci_upper']:+.4f}]",
        f"   Significant: {'YES' if defl['significant'] else 'NO'}  (alpha=0.05)",
        f"   MDE (80%):    {defl['mde']:.4f}",
        "",
        "CONCLUSION",
        "-" * 40,
        _conclusion(appr, defl),
        "=" * 60,
    ]
    return "\n".join(lines)


def _conclusion(apr: dict, dfl: dict) -> str:
    parts = []
    if apr["significant"]:
        direction = "higher" if apr["diff"] > 0 else "lower"
        parts.append(f"Approval rate is significantly {direction} under Group B (p={apr['p_value']:.4f}).")
    else:
        parts.append("Approval rate difference is NOT statistically significant.")

    if dfl["significant"]:
        direction = "lower" if dfl["diff"] < 0 else "higher"
        parts.append(f"Default rate is significantly {direction} under Group B (p={dfl['p_value']:.4f}).")
    else:
        parts.append("Default rate difference is NOT statistically significant.")

    if apr["significant"] and dfl["significant"]:
        if apr["diff"] > 0 and dfl["diff"] < 0:
            parts.append("The new model is BETTER — more approvals AND fewer defaults.")
        elif apr["diff"] < 0 and dfl["diff"] > 0:
            parts.append("The new model is WORSE — fewer approvals AND more defaults.")
        else:
            parts.append("Results are mixed — evaluate trade-offs carefully.")
    return " ".join(parts)
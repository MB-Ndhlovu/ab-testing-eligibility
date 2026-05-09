"""Generate a human-readable summary report from experiment results."""

from typing import Any


def format_rate(value: float) -> str:
    return f"{value:.2%}"


def generate_report(results: dict) -> str:
    """
    Build a plain-text summary report from the experiment results dict.
    """
    meta = results["_meta"]
    appr = results["approval_rate"]
    defr = results["default_rate"]

    a_sum = meta["group_a_summary"]
    b_sum = meta["group_b_summary"]

    # Pre-format values to avoid quote nesting hell
    loan_a = a_sum.get("avg_loan_size", 0)
    loan_b = b_sum.get("avg_loan_size", 0)
    proc_a = a_sum.get("avg_processing_time", 0)
    proc_b = b_sum.get("avg_processing_time", 0)

    lines = [
        "=" * 60,
        "  A/B TEST REPORT — Credit Eligibility Model",
        "=" * 60,
        "",
        "EXPERIMENT SETUP",
        f"  Sample size       : {meta['n_total']:,} applicants",
        f"  Allocation        : 50% control (A) / 50% treatment (B)",
        f"  Significance level: alpha = 0.05",
        "",
        "-" * 60,
        "GROUP SUMMARY",
        "-" * 60,
        f"  {'Metric':<22} {'Group A':>12} {'Group B':>12}",
        f"  {'-'*22} {'-'*12} {'-'*12}",
        f"  {'Approval Rate':<22} {format_rate(a_sum['approval_rate']):>12} {format_rate(b_sum['approval_rate']):>12}",
        f"  {'Default Rate':<22}  {format_rate(a_sum['default_rate']):>12} {format_rate(b_sum['default_rate']):>12}",
        f"  {'Avg Loan Size (ZAR)':<22} {'R' + f'{loan_a:,.0f}':>12} {'R' + f'{loan_b:,.0f}':>12}",
        f"  {'Avg Processing Time':<22} {f'{proc_a:.1f} min':>12} {f'{proc_b:.1f} min':>12}",
        "",
        "-" * 60,
        "STATISTICAL RESULTS",
        "-" * 60,
        "",
        "1. APPROVAL RATE",
        f"   Group A rate     : {format_rate(appr['group_A']['rate'])}",
        f"   Group B rate     : {format_rate(appr['group_B']['rate'])}",
        f"   Treatment effect : {appr['treatment_effect']:+.4f} ({appr['treatment_effect']*100:+.2f} pp)",
        f"   z-statistic      : {appr['z_statistic']:+.4f}",
        f"   p-value          : {appr['p_value']:.6f}",
        f"   95% CI           : [{appr['ci_lower']:+.4f}, {appr['ci_upper']:+.4f}]",
        f"   Significant?     : {'YES' if appr['significant'] else 'NO'}",
        "",
        "2. DEFAULT RATE",
        f"   Group A rate     : {format_rate(defr['group_A']['rate'])}",
        f"   Group B rate     : {format_rate(defr['group_B']['rate'])}",
        f"   Treatment effect : {defr['treatment_effect']:+.4f} ({defr['treatment_effect']*100:+.2f} pp)",
        f"   z-statistic      : {defr['z_statistic']:+.4f}",
        f"   p-value          : {defr['p_value']:.6f}",
        f"   95% CI           : [{defr['ci_lower']:+.4f}, {defr['ci_upper']:+.4f}]",
        f"   Significant?     : {'YES' if defr['significant'] else 'NO'}",
        "",
        "-" * 60,
        "POWER ANALYSIS",
        "-" * 60,
        f"   Observed MDE     : {meta['mde_observed']:.4f} ({meta['mde_observed']*100:.2f} pp)",
        f"   MDE for 80% power: {meta['mde_required_for_80_power']:.4f} ({meta['mde_required_for_80_power']*100:.2f} pp)",
        f"   Achieved power   : {meta['power_approval_test']:.2%}",
        "",
        "-" * 60,
        "RECOMMENDATION",
        "-" * 60,
    ]

    sig_appr = appr["significant"]
    sig_defr = defr["significant"]

    if sig_appr and sig_defr:
        verdict = (
            "ADOPT the new model (Group B).\n"
            "  -> Significantly higher approval rate (+approval)\n"
            "  -> Significantly lower default rate (-risk)\n"
            "  -> Rare win-win: more loans with less credit risk."
        )
    elif sig_appr:
        verdict = (
            "CAUTION — Approve with monitoring.\n"
            "  -> Significantly higher approval rate but default rate difference is not significant.\n"
            "  -> Ensure default rate does not worsen before full rollout."
        )
    elif sig_defr:
        verdict = (
            "REJECT the new model.\n"
            "  -> Lower default rate is not enough — approval rate is not significantly better.\n"
            "  -> The new model increases credit risk without sufficient business upside."
        )
    else:
        verdict = (
            "INCONCLUSIVE — Run a larger experiment.\n"
            "  -> Neither approval rate nor default rate shows a statistically significant difference.\n"
            "  -> Consider increasing sample size or revisiting the model."
        )

    lines.extend([verdict, "", "=" * 60])
    return "\n".join(lines)


if __name__ == "__main__":
    from src.simulate import run_experiment
    results = run_experiment()
    print(generate_report(results))
"""
Generate a human-readable summary report from experiment results.
"""

import json


def generate_report(results):
    """
    Pretty-print the experiment results.
    """
    alpha = results["alpha"]
    n_a = results["sample_sizes"]["group_a"]
    n_b = results["sample_sizes"]["group_b"]

    lines = []
    lines.append("=" * 60)
    lines.append("       A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    lines.append("=" * 60)
    lines.append(f"\nSample sizes  →  Group A (Control): {n_a}  |  Group B (Treatment): {n_b}")
    lines.append(f"Significance level (α): {alpha}")
    lines.append("")

    # Summary table
    s = results["summary"]
    lines.append("-" * 60)
    lines.append(f"{'Metric':<25} {'Group A':>12} {'Group B':>12}")
    lines.append("-" * 60)
    lines.append(f"{'Approval Rate':<25} {s['Group A (Control)']['approval_rate']:>12.2%} {s['Group B (Treatment)']['approval_rate']:>12.2%}")
    lines.append(f"{'Default Rate':<25} {s['Group A (Control)']['default_rate']:>12.2%} {s['Group B (Treatment)']['default_rate']:>12.2%}")
    lines.append(f"{'Avg Loan Size ($)':<25} {s['Group A (Control)']['avg_loan_size']:>12,.0f} {s['Group B (Treatment)']['avg_loan_size']:>12,.0f}")
    lines.append(f"{'Avg Processing Time (s)':<25} {s['Group A (Control)']['avg_processing_time']:>12.2f} {s['Group B (Treatment)']['avg_processing_time']:>12.2f}")
    lines.append("-" * 60)

    # Approval rate test
    ar = results["approval_rate"]
    lines.append("\n[APPROVAL RATE TEST]")
    lines.append(f"  Difference (B − A) : {ar['test']['diff']:+.4f}")
    lines.append(f"  z-statistic        : {ar['test']['z_stat']:.4f}")
    lines.append(f"  p-value            : {ar['test']['p_value']:.6f}")
    lines.append(f"  95% CI             : [{ar['ci'][0]:.4f}, {ar['ci'][1]:.4f}]")
    lines.append(f"  Statistical power  : {ar['power']:.4f}")
    lines.append(f"  Min detectable eff : {ar['mde']:.4f}")
    sig_word = "SIGNIFICANT" if ar["significant"] else "not significant"
    lines.append(f"  Conclusion         : {sig_word} at α={alpha}")

    # Default rate test
    dr = results["default_rate"]
    lines.append("\n[DEFAULT RATE TEST]")
    lines.append(f"  Difference (B − A) : {dr['test']['diff']:+.4f}")
    lines.append(f"  z-statistic        : {dr['test']['z_stat']:.4f}")
    lines.append(f"  p-value            : {dr['test']['p_value']:.6f}")
    lines.append(f"  95% CI             : [{dr['ci'][0]:.4f}, {dr['ci'][1]:.4f}]")
    lines.append(f"  Statistical power  : {dr['power']:.4f}")
    lines.append(f"  Min detectable eff : {dr['mde']:.4f}")
    sig_word = "SIGNIFICANT" if dr["significant"] else "not significant"
    lines.append(f"  Conclusion         : {sig_word} at α={alpha}")

    lines.append("\n" + "=" * 60)
    lines.append("  OVERALL RECOMMENDATION")
    lines.append("=" * 60)

    ar_sig = ar["significant"]
    dr_sig = dr["significant"]

    if ar_sig and dr_sig:
        lines.append("  ✓ New model (Group B) shows statistically significant improvement")
        lines.append("    in BOTH approval rate (higher) and default rate (lower).")
        lines.append("  → Recommend deploying the new credit eligibility model.")
    elif ar_sig and not dr_sig:
        lines.append("  ~ New model significantly increases approvals but default rate")
        lines.append("    difference is not statistically significant.")
        lines.append("  → Proceed with caution; evaluate default risk further.")
    elif not ar_sig and dr_sig:
        lines.append("  ~ New model significantly reduces defaults but approval rate")
        lines.append("    difference is not statistically significant.")
        lines.append("  → Investigate why approvals are not meaningfully higher.")
    else:
        lines.append("  ✗ Neither metric shows a statistically significant difference.")
        lines.append("  → Do not deploy; insufficient evidence to change model.")

    lines.append("=" * 60)

    return "\n".join(lines)


def results_to_json(results, path):
    """Save full results as JSON."""
    with open(path, "w") as f:
        json.dump(results, f, indent=2, default=float)
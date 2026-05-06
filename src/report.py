"""
Generate a human-readable summary report of the A/B test results.
"""
from src.statistical import run_analysis

ALPHA = 0.05

def format_metric_result(label, r):
    sig = "✅ SIGNIFICANT" if r["significant"] else "❌ NOT SIGNIFICANT"
    return (
        f"  {label}\n"
        f"    Group A: {r['group_A']:.2%}  |  Group B: {r['group_B']:.2%}\n"
        f"    Difference: {r['difference']:+.2%}\n"
        f"    Z-statistic: {r['z_statistic']:.4f}   P-value: {r['p_value']:.4f}\n"
        f"    95% CI for difference: [{r['ci_lower']:.2%}, {r['ci_upper']:.2%}]\n"
        f"    Power: {r['power']:.2%}   MDE: {r['mde']:.2%}\n"
        f"    Conclusion: {sig} (at α={ALPHA})\n"
    )

def generate_report(summary, analysis):
    lines = [
        "=" * 60,
        "   A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY",
        "   Experiment Report",
        "=" * 60,
        "",
        "▶ SAMPLE SUMMARY",
        "-" * 40,
    ]

    for group in ["A", "B"]:
        row = summary.loc[group]
        lines.append(f"  Group {group} ({int(row['applicants'])} applicants)")
        lines.append(f"    Approval Rate:      {row['approval_rate']:.2%}")
        lines.append(f"    Default Rate:       {row['default_rate']:.2%}")
        lines.append(f"    Avg Loan Size:      ${row['avg_loan_size']:,.2f}")
        lines.append(f"    Avg Processing:    {row['avg_processing_days']:.1f} days")
        lines.append("")

    lines += [
        "▶ STATISTICAL RESULTS",
        "-" * 40,
    ]

    lines.append(format_metric_result("Approval Rate", analysis["approval_rate"]))
    lines.append(format_metric_result("Default Rate",  analysis["default_rate"]))

    # Overall recommendation
    app_sig  = analysis["approval_rate"]["significant"]
    def_sig  = analysis["default_rate"]["significant"]
    app_diff = analysis["approval_rate"]["difference"]
    def_diff = analysis["default_rate"]["difference"]

    lines += [
        "▶ OVERALL RECOMMENDATION",
        "-" * 40,
    ]

    if app_sig and def_sig:
        if app_diff > 0 and def_diff < 0:
            lines.append("  ✅ Deploy the new model (Group B). It significantly")
            lines.append("     increases approvals AND reduces defaults.")
        elif app_diff > 0:
            lines.append("  ⚠️  Partial success. Approval rate improved significantly")
            lines.append("     but default rate change was not significant.")
        elif def_diff < 0:
            lines.append("  ⚠️  Partial success. Default rate improved significantly")
            lines.append("     but approval rate change was not significant.")
        else:
            lines.append("  ⚠️  Both metrics showed significant differences.")
            lines.append("     Review direction of changes before deploying.")
    elif app_sig:
        lines.append("  ⚠️  Approval rate improved significantly, but default")
        lines.append("     rate was not significantly different. Monitor risk.")
    elif def_sig:
        lines.append("  ⚠️  Default rate improved significantly, but approval")
        lines.append("     rate was not significantly different. Consider retest.")
    else:
        lines.append("  ❌ Neither metric showed a statistically significant")
        lines.append("     difference at α=0.05. Insufficient evidence to")
        lines.append("     justify deploying the new model.")

    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)
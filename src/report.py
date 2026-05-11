"""Generate readable summary reports for A/B test results."""

from typing import Dict


def format_pct(value: float, decimals: int = 2) -> str:
    """Format a decimal as percentage string."""
    return f"{value * 100:.{decimals}f}%"


def generate_report(results: Dict) -> str:
    """Generate a human-readable summary report."""
    ga = results["group_a"]
    gb = results["group_b"]
    at = results["approval_test"]
    dt = results["default_test"]

    lines = []
    lines.append("=" * 60)
    lines.append("      A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    lines.append("=" * 60)
    lines.append("")
    lines.append("EXECUTIVE SUMMARY")
    lines.append("-" * 40)

    approval_sig = "SIGNIFICANT" if at["significant"] else "NOT SIGNIFICANT"
    default_sig = "SIGNIFICANT" if dt["significant"] else "NOT SIGNIFICANT"

    lines.append(f"Approval Rate Lift: {format_pct(at['diff'])} ({approval_sig})")
    lines.append(f"Default Rate Change: {format_pct(dt['diff'])} ({default_sig})")
    lines.append("")

    lines.append("GROUP METRICS")
    lines.append("-" * 40)
    lines.append(f"{'Metric':<25} {'Group A (Control)':>18} {'Group B (Treatment)':>18}")
    lines.append("-" * 40)
    lines.append(f"{'Sample Size':<25} {ga['n']:>18} {gb['n']:>18}")
    lines.append(f"{'Approvals':<25} {ga['approvals']:>18} {gb['approvals']:>18}")
    lines.append(f"{'Approval Rate':<25} {format_pct(ga['approval_rate']):>18} {format_pct(gb['approval_rate']):>18}")
    lines.append(f"{'Defaults':<25} {ga['defaults']:>18} {gb['defaults']:>18}")
    lines.append(f"{'Default Rate':<25} {format_pct(ga['default_rate']):>18} {format_pct(gb['default_rate']):>18}")
    lines.append(f"{'Avg Loan Size':<25} {'${:,.2f}'.format(ga['avg_loan_size']):>18} {'${:,.2f}'.format(gb['avg_loan_size']):>18}")
    lines.append(f"{'Avg Processing Time':<25} {ga['avg_processing_time']:.2f} days{'':>9} {gb['avg_processing_time']:.2f} days{'':>9}")
    lines.append("")

    lines.append("APPROVAL RATE — TWO-PROPORTION Z-TEST")
    lines.append("-" * 40)
    lines.append(f"  Control rate (p1):     {format_pct(at['p1'])}")
    lines.append(f"  Treatment rate (p2):    {format_pct(at['p2'])}")
    lines.append(f"  Difference (p2 - p1):  {format_pct(at['diff'])}")
    lines.append(f"  95% CI:                [{format_pct(at['ci_lower'])}, {format_pct(at['ci_upper'])}]")
    lines.append(f"  Z-statistic:           {at['z_statistic']:.4f}")
    lines.append(f"  P-value:               {at['p_value']:.6f}")
    lines.append(f"  Result:                {'REJECT H0 — Significant difference' if at['significant'] else 'FAIL TO REJECT H0 — No significant difference'}")
    lines.append("")

    lines.append("DEFAULT RATE — TWO-PROPORTION Z-TEST")
    lines.append("-" * 40)
    lines.append(f"  Control rate (p1):     {format_pct(dt['p1'])}")
    lines.append(f"  Treatment rate (p2):    {format_pct(dt['p2'])}")
    lines.append(f"  Difference (p2 - p1):  {format_pct(dt['diff'])}")
    lines.append(f"  95% CI:                [{format_pct(dt['ci_lower'])}, {format_pct(dt['ci_upper'])}]")
    lines.append(f"  Z-statistic:           {dt['z_statistic']:.4f}")
    lines.append(f"  P-value:               {dt['p_value']:.6f}")
    lines.append(f"  Result:                {'REJECT H0 — Significant difference' if dt['significant'] else 'FAIL TO REJECT H0 — No significant difference'}")
    lines.append("")

    lines.append("POWER ANALYSIS")
    lines.append("-" * 40)
    lines.append(f"  Approval test power:  {results['power']['approval']:.1%}")
    lines.append(f"  Default test power:   {results['power']['default']:.1%}")
    lines.append(f"  Min detectable effect (approval): {format_pct(results['mde']['approval'])}")
    lines.append(f"  Min detectable effect (default):  {format_pct(results['mde']['default'])}")
    lines.append("")

    lines.append("CONCLUSION")
    lines.append("-" * 40)
    if at["significant"] and dt["significant"]:
        lines.append("  Both metrics show statistically significant improvement.")
        lines.append("  The new model (Group B) increases approval rate AND decreases")
        lines.append("  default rate. RECOMMEND adopting the new model.")
    elif at["significant"]:
        lines.append("  Only approval rate shows significant improvement.")
        lines.append("  Default rate change is not statistically significant.")
        lines.append("  Consider further testing before full deployment.")
    elif dt["significant"]:
        lines.append("  Only default rate shows significant improvement.")
        lines.append("  Approval rate change is not statistically significant.")
        lines.append("  Review if higher approvals are desired.")
    else:
        lines.append("  Neither metric shows statistically significant improvement.")
        lines.append("  The new model does not demonstrate clear advantage.")
        lines.append("  Recommend additional testing or model refinement.")
    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)
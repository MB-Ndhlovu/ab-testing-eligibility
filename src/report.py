"""Generate readable summary reports from A/B test results."""

import json
from datetime import datetime


def generate_report(results, output_path=None):
    """
    Generate a comprehensive text report from simulation results.

    Parameters
    ----------
    results : dict
        Results dictionary from run_simulation().
    output_path : str, optional
        Path to save the report as a text file.

    Returns
    -------
    str
        The formatted report string.
    """
    lines = []
    lines.append("=" * 65)
    lines.append("   A/B TESTING FRAMEWORK - CREDIT ELIGIBILITY MODEL")
    lines.append("=" * 65)
    lines.append(f"   Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("   Significance Level (α): 0.05")
    lines.append("=" * 65)
    lines.append("")

    lines.append("📋 BUSINESS CONTEXT")
    lines.append("-" * 65)
    lines.append("   A lender is evaluating a new credit eligibility model (Group B)")
    lines.append("   against their current model (Group A / Control).")
    lines.append("")
    lines.append("   Goals:")
    lines.append("     • Increase approval rate (target: ~71% vs ~62%)")
    lines.append("     • Decrease default rate (target: ~9% vs ~11%)")
    lines.append("")

    lines.append("📊 DATA SUMMARY")
    lines.append("-" * 65)
    ga = results["group_a"]
    gb = results["group_b"]
    lines.append(f"   {'Metric':<30} {'Control (A)':>15} {'Treatment (B)':>17}")
    lines.append(f"   {'-'*30} {'-'*15} {'-'*17}")
    lines.append(f"   {'Sample Size':<30} {ga['n']:>15,} {gb['n']:>17,}")
    lines.append(f"   {'Approved Applications':<30} {ga['approved_count']:>15,} {gb['approved_count']:>17,}")
    lines.append(f"   {'Approval Rate':<30} {ga['approval_rate']*100:>14.2f}% {gb['approval_rate']*100:>16.2f}%")
    lines.append(f"   {'Defaults':<30} {ga['defaulted_count']:>15,} {gb['defaulted_count']:>17,}")
    lines.append(f"   {'Default Rate':<30} {ga['default_rate']*100:>14.2f}% {gb['default_rate']*100:>16.2f}%")
    lines.append(f"   {'Avg Loan Size':<30} {'${:,.2f}'.format(ga['avg_loan_size']):>15} {'${:,.2f}'.format(gb['avg_loan_size']):>17}")
    lines.append(f"   {'Avg Processing Time':<30} {ga['avg_processing_time_hours']:>14.1f} hrs {gb['avg_processing_time_hours']:>16.1f} hrs")
    lines.append("")

    ar = results["approval_rate_test"]
    lines.append("🔬 TEST 1: APPROVAL RATE")
    lines.append("-" * 65)
    lines.append(f"   H₀: No difference in approval rates between groups")
    lines.append(f"   H₁: There is a difference in approval rates")
    lines.append("")
    lines.append(f"   Observed Rates:    Control = {ar['p1']:.4f}, Treatment = {ar['p2']:.4f}")
    lines.append(f"   Difference:        {ar['difference']:+.4f} ({ar['difference']*100:+.2f} percentage points)")
    lines.append(f"   95% CI:            [{ar['ci_95_lower']:+.4f}, {ar['ci_95_upper']:+.4f}]")
    lines.append(f"   Z-Statistic:       {ar['z_statistic']:.4f}")
    lines.append(f"   P-Value:          {ar['p_value']:.6f}")
    lines.append("")
    ar_verdict = "✅ STATISTICALLY SIGNIFICANT" if ar['significant'] else "❌ NOT SIGNIFICANT"
    lines.append(f"   Result: {ar_verdict} at α=0.05")
    if ar['significant']:
        direction_word = "increases" if ar['difference'] > 0 else "decreases"
        lines.append(f"   → New model {direction_word} approval rate by {abs(ar['difference'])*100:.2f} percentage points")
    lines.append("")

    dr = results["default_rate_test"]
    lines.append("🔬 TEST 2: DEFAULT RATE")
    lines.append("-" * 65)
    lines.append(f"   H₀: No difference in default rates between groups")
    lines.append(f"   H₁: There is a difference in default rates")
    lines.append("")
    lines.append(f"   Observed Rates:    Control = {dr['p1']:.4f}, Treatment = {dr['p2']:.4f}")
    lines.append(f"   Difference:        {dr['difference']:+.4f} ({dr['difference']*100:+.2f} percentage points)")
    lines.append(f"   95% CI:            [{dr['ci_95_lower']:+.4f}, {dr['ci_95_upper']:+.4f}]")
    lines.append(f"   Z-Statistic:       {dr['z_statistic']:.4f}")
    lines.append(f"   P-Value:          {dr['p_value']:.6f}")
    lines.append("")
    dr_verdict = "✅ STATISTICALLY SIGNIFICANT" if dr['significant'] else "❌ NOT SIGNIFICANT"
    lines.append(f"   Result: {dr_verdict} at α=0.05")
    if dr['significant']:
        direction_word = "reduces" if dr['difference'] < 0 else "increases"
        lines.append(f"   → New model {direction_word} default rate by {abs(dr['difference'])*100:.2f} percentage points")
    lines.append("")

    lines.append("⚙️  POWER ANALYSIS")
    lines.append("-" * 65)
    lines.append(f"   Approval Rate Test:")
    lines.append(f"     • Statistical Power: {ar['power']:.4f} (target: 0.80)")
    lines.append(f"     • Min Detectable Effect: {ar['mde']:.4f}")
    lines.append(f"   Default Rate Test:")
    lines.append(f"     • Statistical Power: {dr['power']:.4f} (target: 0.80)")
    lines.append(f"     • Min Detectable Effect: {dr['mde']:.4f}")
    lines.append("")

    lines.append("=" * 65)
    lines.append("📌 EXECUTIVE SUMMARY")
    lines.append("=" * 65)

    ar_sig = ar['significant']
    dr_sig = dr['significant']

    if ar_sig and dr_sig:
        lines.append("   ✅ RECOMMENDATION: DEPLOY THE NEW MODEL")
        lines.append("")
        lines.append("   Both tests show statistically significant improvements:")
        lines.append(f"     • Approval rate ↑ by {abs(ar['difference'])*100:.2f}pp (p={ar['p_value']:.4f})")
        lines.append(f"     • Default rate ↓ by {abs(dr['difference'])*100:.2f}pp (p={dr['p_value']:.4f})")
        lines.append("")
        lines.append("   The new model improves both metrics simultaneously.")
    elif ar_sig and not dr_sig:
        lines.append("   ⚠️  CONDITIONAL RECOMMENDATION")
        lines.append("")
        lines.append("   Approval rate improved significantly, but default rate change is not")
        lines.append("   statistically significant. Consider a larger sample or further testing.")
    elif not ar_sig and dr_sig:
        lines.append("   ⚠️  CAUTION: MIXED RESULTS")
        lines.append("")
        lines.append("   Default rate improved but approval rate did not change significantly.")
        lines.append("   Review business priorities before deploying.")
    else:
        lines.append("   ❌ RECOMMENDATION: DO NOT DEPLOY YET")
        lines.append("")
        lines.append("   Neither metric showed statistically significant improvement.")
        lines.append("   The observed differences could be due to random chance.")

    lines.append("")
    lines.append("=" * 65)

    report_text = "\n".join(lines)

    if output_path:
        with open(output_path, "w") as f:
            f.write(report_text)

    return report_text


def save_json_results(results, output_path):
    """Save results as JSON for programmatic consumption."""
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)


if __name__ == "__main__":
    from src.simulate import run_simulation
    results = run_simulation()
    report = generate_report(results)
    print(report)
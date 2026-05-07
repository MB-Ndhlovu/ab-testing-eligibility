"""
Generate readable summary reports for A/B test results.
"""

import json
from datetime import datetime


def generate_report(results, output_file=None):
    """
    Generate a formatted text report.

    Parameters:
        results: dict from run_experiment
        output_file: optional file path to save report

    Returns:
        str: formatted report
    """
    # Import format_results from simulate
    from src.simulate import format_results

    report_lines = []

    # Header
    report_lines.append("╔══════════════════════════════════════════════════════════════╗")
    report_lines.append("║        A/B TESTING FRAMEWORK FOR CREDIT ELIGIBILITY          ║")
    report_lines.append("║                    FINAL ANALYSIS REPORT                      ║")
    report_lines.append("╚══════════════════════════════════════════════════════════════╝")
    report_lines.append("")
    report_lines.append(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")

    # Executive Summary
    report_lines.append("┌──────────────────────────────────────────────────────────────┐")
    report_lines.append("│                     EXECUTIVE SUMMARY                        │")
    report_lines.append("└──────────────────────────────────────────────────────────────┘")

    approval_sig = results['tests']['approval_rate']['significant']
    default_sig = results['tests']['default_rate']['significant']
    approval_diff = results['tests']['approval_rate']['difference']
    default_diff = results['tests']['default_rate']['difference']

    report_lines.append("")
    report_lines.append(f"  • Approval Rate: {'SIGNIFICANT' if approval_sig else 'NOT SIGNIFICANT'}")
    report_lines.append(f"    Difference: {approval_diff:+.4f} (B vs A)")
    report_lines.append("")
    report_lines.append(f"  • Default Rate:  {'SIGNIFICANT' if default_sig else 'NOT SIGNIFICANT'}")
    report_lines.append(f"    Difference: {default_diff:+.4f} (B vs A)")
    report_lines.append("")

    # Sample overview
    report_lines.append("┌──────────────────────────────────────────────────────────────┐")
    report_lines.append("│                       SAMPLE OVERVIEW                        │")
    report_lines.append("└──────────────────────────────────────────────────────────────┘")
    report_lines.append("")
    report_lines.append(f"  Group A (Control):   {results['sample_size']['A']:,} applicants")
    report_lines.append(f"  Group B (Treatment): {results['sample_size']['B']:,} applicants")
    report_lines.append(f"  Total:              {results['sample_size']['A'] + results['sample_size']['B']:,} applicants")
    report_lines.append("")

    # Key Metrics Table
    report_lines.append("┌──────────────────────────────────────────────────────────────┐")
    report_lines.append("│                         KEY METRICS                         │")
    report_lines.append("└──────────────────────────────────────────────────────────────┘")
    report_lines.append("")
    report_lines.append(f"  {'Metric':<22} {'Group A':>10} {'Group B':>10} {'Diff':>10} {'Sig?':>6}")
    report_lines.append(f"  {'-'*58}")

    for metric in ['approval_rate', 'default_rate', 'avg_loan_amount', 'avg_processing_time']:
        val_A = results[metric]['A']
        val_B = results[metric]['B']
        diff = val_B - val_A

        test = results['tests'].get(metric, {})
        sig = "Yes" if test.get('significant', False) else "No"

        metric_name = metric.replace('_', ' ').title()
        if metric in ['approval_rate', 'default_rate']:
            report_lines.append(f"  {metric_name:<22} {val_A:>10.4f} {val_B:>10.4f} {diff:>+10.4f} {sig:>6}")
        elif metric == 'avg_loan_amount':
            report_lines.append(f"  {metric_name:<22} {val_A:>10.2f} {val_B:>10.2f} {diff:>+10.2f} {'N/A':>6}")
        else:
            report_lines.append(f"  {metric_name:<22} {val_A:>10.2f} {val_B:>10.2f} {diff:>+10.2f} {'N/A':>6}")

    report_lines.append("")

    # Statistical Test Details
    report_lines.append("┌──────────────────────────────────────────────────────────────┐")
    report_lines.append("│                  STATISTICAL TEST RESULTS                    │")
    report_lines.append("└──────────────────────────────────────────────────────────────┘")

    for metric, test_name in [('approval_rate', 'Approval Rate'), ('default_rate', 'Default Rate')]:
        test = results['tests'][metric]
        report_lines.append("")
        report_lines.append(f"  {test_name} Z-Test:")
        report_lines.append(f"    H₀: p_B - p_A = 0")
        report_lines.append(f"    p̂_A = {test['p_A']:.4f}, p̂_B = {test['p_B']:.4f}")
        report_lines.append(f"    Difference = {test['difference']:.4f}")
        report_lines.append(f"    Z-statistic = {test['z_statistic']:.4f}")
        report_lines.append(f"    P-value     = {test['p_value']:.6f}")
        report_lines.append(f"    95% CI: [{test['ci_95_lower']:.4f}, {test['ci_95_upper']:.4f}]")
        report_lines.append(f"    Result: {'REJECT H₀ - Significant difference' if test['significant'] else 'FAIL TO REJECT H₀ - No significant difference'}")

    report_lines.append("")

    # Power Analysis
    report_lines.append("┌──────────────────────────────────────────────────────────────┐")
    report_lines.append("│                      POWER ANALYSIS                         │")
    report_lines.append("└──────────────────────────────────────────────────────────────┘")
    report_lines.append("")

    for metric in ['approval_rate', 'default_rate']:
        pa = results['power_analysis'][metric]
        metric_name = metric.replace('_', ' ').title()
        report_lines.append(f"  {metric_name}:")
        report_lines.append(f"    Observed MDE: {pa['mde']:.4f}")
        report_lines.append(f"    Achieved Power: {pa['power']:.4f}")
        report_lines.append(f"    Sample for 80% power: {results['power_analysis']['sample_size_needed_80_power'][metric]:,}")
        report_lines.append("")

    # Final Recommendation
    report_lines.append("┌──────────────────────────────────────────────────────────────┐")
    report_lines.append("│                  FINAL RECOMMENDATION                        │")
    report_lines.append("└──────────────────────────────────────────────────────────────┘")
    report_lines.append("")

    if approval_sig and default_sig:
        if approval_diff > 0 and default_diff < 0:
            report_lines.append("  ★ RECOMMENDATION: ADOPT the new credit eligibility model")
            report_lines.append("")
            report_lines.append("    Justification:")
            report_lines.append("    - Approval rate significantly increased (+{:.1f}%)".format(approval_diff * 100))
            report_lines.append("    - Default rate significantly decreased (-{:.1f}%)".format(abs(default_diff) * 100))
            report_lines.append("    - Both key metrics moved in favorable directions")
        elif approval_diff > 0:
            report_lines.append("  ⚠ CAUTION: Mixed results detected")
            report_lines.append("")
            report_lines.append("    - Approval rate improved significantly")
            report_lines.append("    - Default rate worsened significantly")
            report_lines.append("    - Further analysis required before adoption")
        else:
            report_lines.append("  ⚠ Mixed results - manual review required")
    elif approval_sig:
        report_lines.append("  ★ RECOMMENDATION: ADOPT with monitoring")
        report_lines.append("")
        report_lines.append("    Justification:")
        report_lines.append("    - Approval rate significantly improved")
        report_lines.append("    - Default rate change not statistically significant")
        report_lines.append("    - Recommend monitoring default rate post-launch")
    elif default_sig:
        report_lines.append("  ★ RECOMMENDATION: ADOPT with monitoring")
        report_lines.append("")
        report_lines.append("    Justification:")
        report_lines.append("    - Default rate significantly improved")
        report_lines.append("    - Approval rate change not statistically significant")
        report_lines.append("    - Recommend monitoring approval rate post-launch")
    else:
        report_lines.append("  ⚠ NO SIGNIFICANT DIFFERENCE DETECTED")
        report_lines.append("")
        report_lines.append("    Neither metric showed statistically significant difference.")
        report_lines.append("    Consider: increasing sample size, refining model, or")
        report_lines.append("    accepting current performance as optimal.")

    report_lines.append("")
    report_lines.append("─" * 62)
    report_lines.append("End of Report")

    report = "\n".join(report_lines)

    if output_file:
        with open(output_file, 'w') as f:
            f.write(report)

    return report


def save_json_results(results, output_file):
    """Save results as JSON."""
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)


if __name__ == '__main__':
    from src.simulate import run_experiment
    results = run_experiment()
    report = generate_report(results)
    print(report)
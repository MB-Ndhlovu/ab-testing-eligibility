"""Generate readable summary reports from A/B test results."""

import json
from datetime import datetime


def generate_report(results, filepath=None):
    """
    Generate a formatted text report from results dict.

    Parameters
    ----------
    results : dict
        Output from run_simulation()
    filepath : str, optional
        If provided, save report to this file path

    Returns
    -------
    str
        Formatted report text
    """
    lines = []
    lines.append("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    lines.append("=" * 55)
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("")

    lines.append("EXPERIMENT SUMMARY")
    lines.append("-" * 55)
    lines.append(f"  Total applicants:     {results['experiment']['n_total']}")
    lines.append(f"  Per group:            {results['experiment']['n_per_group']}")
    lines.append(f"  Significance level:  α = {results['experiment']['alpha']}")
    lines.append("")

    lines.append("GROUP STATISTICS")
    lines.append("-" * 55)
    for group in ['A', 'B']:
        s = results['group_stats'][group]
        label = "Control (Current Model)" if group == 'A' else "Treatment (New Model)"
        lines.append(f"\n  Group {group} — {label}")
        lines.append(f"    Applications:       {s['n']}")
        lines.append(f"    Approved:          {s['approvals']} ({s['approval_rate']*100:.2f}%)")
        lines.append(f"    Defaults:          {s['defaults']} ({s['default_rate']*100:.2f}%)")
        lines.append(f"    Avg loan size:     ${s['avg_loan_size']:,.2f}")
        lines.append(f"    Avg processing:    {s['avg_processing_time']:.2f} hrs")

    lines.append("")
    lines.append("STATISTICAL ANALYSIS")
    lines.append("-" * 55)

    for metric_name, metric_key in [("Approval Rate", "approval_rate"), ("Default Rate", "default_rate")]:
        m = results['metrics'][metric_key]
        lines.append(f"\n  {metric_name}:")
        lines.append(f"    Control rate:        {m['group_a_rate']*100:.2f}%")
        lines.append(f"    Treatment rate:      {m['group_b_rate']*100:.2f}%")
        lines.append(f"    Absolute diff:       {m['absolute_diff']*100:+.2f}%")
        lines.append(f"    Relative diff:       {m['relative_diff']*100:+.2f}%")
        lines.append(f"    Z-statistic:         {m['z_statistic']:.4f}")
        lines.append(f"    P-value:             {m['p_value']:.6f}")
        lines.append(f"    95% CI:              [{m['ci_95_lower']*100:+.2f}%, {m['ci_95_upper']*100:+.2f}%]")
        lines.append(f"    Statistically sig?:  {'YES' if m['significant'] else 'NO'}")

    lines.append("")
    lines.append("POWER ANALYSIS")
    lines.append("-" * 55)
    ar = results['metrics']['approval_rate']
    dr = results['metrics']['default_rate']
    lines.append(f"  Approval rate power:         {ar['power']:.4f} ({ar['power']*100:.1f}%)")
    lines.append(f"  Default rate power:         {dr['power']:.4f} ({dr['power']*100:.1f}%)")
    lines.append(f"  Min detectable effect (AR): {ar['mde']*100:.2f}%")
    lines.append(f"  Min detectable effect (DR): {dr['mde']*100:.2f}%")

    lines.append("")
    lines.append("CONCLUSION")
    lines.append("=" * 55)
    ar_sig = ar['significant']
    dr_sig = dr['significant']

    if ar_sig and dr_sig and ar['absolute_diff'] > 0 and dr['absolute_diff'] < 0:
        lines.append("  RECOMMENDATION: Adopt new model (Group B)")
        lines.append("  - Significantly higher approval rate")
        lines.append("  - Significantly lower default rate")
    elif ar_sig and not dr_sig:
        lines.append("  RECOMMENDATION: Adopt new model (Group B)")
        lines.append("  - Significantly higher approval rate")
        lines.append("  - No statistically significant change in default rate")
    elif ar_sig and dr_sig and dr['absolute_diff'] > 0:
        lines.append("  CAUTION: New model increases defaults")
        lines.append("  - Higher approval rate but also higher default rate")
        lines.append("  - Requires further risk analysis before adoption")
    else:
        lines.append("  INCONCLUSIVE: Larger sample needed")
        lines.append("  - No statistically significant difference detected")
        lines.append("  - Consider increasing sample size or revising model")

    lines.append("=" * 55)

    report_text = "\n".join(lines)

    if filepath:
        with open(filepath, 'w') as f:
            f.write(report_text)

    return report_text


def save_json_results(results, filepath):
    """Save full results as JSON for programmatic consumption."""
    with open(filepath, 'w') as f:
        json.dump(results, f, indent=2, default=str)


if __name__ == '__main__':
    from src.simulate import run_simulation

    results = run_simulation()
    report = generate_report(results)
    print(report)
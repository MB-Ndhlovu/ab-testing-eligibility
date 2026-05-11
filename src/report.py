"""Generate readable summary reports for A/B test results."""

import json

def format_number(x, decimals=4):
    """Format number with given decimals."""
    return f"{x:.{decimals}f}"

def generate_report(results):
    """
    Generate a readable summary report from experiment results.

    Parameters
    ----------
    results : dict
        Output from run_experiment()

    Returns
    -------
    str
        Formatted text report
    """
    lines = []
    lines.append("=" * 70)
    lines.append("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY RESULTS")
    lines.append("=" * 70)

    lines.append("\n[SAMPLE INFORMATION]")
    lines.append(f"  Sample size per group: {results['n_per_group']:,}")

    lines.append("\n[DESCRIPTIVE METRICS]")
    for group in ['group_a', 'group_b']:
        label = "Control (A)" if group == 'group_a' else "Treatment (B)"
        m = results['metrics'][group]
        lines.append(f"\n  {label}:")
        lines.append(f"    Approval rate:     {m['approval_rate']:.4f} ({m['approval_rate']*100:.2f}%)")
        lines.append(f"    Default rate:      {m['default_rate']:.4f} ({m['default_rate']*100:.2f}%)")
        lines.append(f"    Avg loan size:     R{m['avg_loan_size']:,.0f}")
        lines.append(f"    Avg processing time: {m['processing_time']:.2f} days")

    lines.append("\n" + "=" * 70)
    lines.append("[APPROVAL RATE TEST — Two-Proportion Z-Test]")
    lines.append("=" * 70)
    at = results['approval_test']
    lines.append(f"  Control proportion (p1):   {at['p1']:.4f}")
    lines.append(f"  Treatment proportion (p2):  {at['p2']:.4f}")
    lines.append(f"  Observed effect (p2 - p1): {at['effect']:+.4f} ({at['effect']*100:+.2f} ppts)")
    lines.append(f"  Z-statistic:                {at['z_statistic']:.4f}")
    lines.append(f"  P-value:                   {at['p_value']:.6f}")
    lines.append(f"  95% CI for difference:     [{at['ci_lower']:.4f}, {at['ci_upper']:.4f}]")
    lines.append(f"  Conclusion:                {at['significance']} at α=0.05")
    lines.append(f"  Expected power (true params): {at['expected_power']:.4f}")
    lines.append(f"  MDE (80% power):           {at['mde']:.4f}")

    lines.append("\n" + "=" * 70)
    lines.append("[DEFAULT RATE TEST — Two-Proportion Z-Test]")
    lines.append("=" * 70)
    dt = results['default_test']
    lines.append(f"  Control proportion (p1):   {dt['p1']:.4f}")
    lines.append(f"  Treatment proportion (p2):  {dt['p2']:.4f}")
    lines.append(f"  Observed effect (p2 - p1):  {dt['effect']:+.4f} ({dt['effect']*100:+.2f} ppts)")
    lines.append(f"  Z-statistic:                {dt['z_statistic']:.4f}")
    lines.append(f"  P-value:                   {dt['p_value']:.6f}")
    lines.append(f"  95% CI for difference:     [{dt['ci_lower']:.4f}, {dt['ci_upper']:.4f}]")
    lines.append(f"  Conclusion:                {dt['significance']} at α=0.05")
    lines.append(f"  Expected power (true params): {dt['expected_power']:.4f}")
    lines.append(f"  MDE (80% power):           {dt['mde']:.4f}")

    lines.append("\n" + "=" * 70)
    lines.append("[EXECUTIVE SUMMARY]")
    lines.append("=" * 70)
    if at['significance'] == 'SIGNIFICANT':
        lines.append(f"  ✓ Approval rate is SIGNIFICANTLY HIGHER with new model")
        lines.append(f"    (+{at['effect']*100:.2f} percentage points, p={at['p_value']:.4f})")
    else:
        lines.append(f"  — Approval rate difference is NOT statistically significant")
        lines.append(f"    (effect: +{at['effect']*100:.2f} ppts, p={at['p_value']:.4f})")

    if dt['significance'] == 'SIGNIFICANT':
        lines.append(f"  ✓ Default rate is SIGNIFICANTLY LOWER with new model")
        lines.append(f"    ({dt['effect']*100:.2f} ppts, p={dt['p_value']:.4f})")
    else:
        lines.append(f"  — Default rate difference is NOT statistically significant")
        lines.append(f"    (effect: {dt['effect']*100:.2f} ppts, p={dt['p_value']:.4f})")

    lines.append("\n" + "=" * 70)
    return "\n".join(lines)

def results_to_json(results):
    """Convert results to JSON-serializable dict."""
    output = {
        'n_per_group': results['n_per_group'],
        'metrics': results['metrics'],
        'approval_test': {
            'p1': results['approval_test']['p1'],
            'p2': results['approval_test']['p2'],
            'effect': results['approval_test']['effect'],
            'z_statistic': results['approval_test']['z_statistic'],
            'p_value': results['approval_test']['p_value'],
            'ci_lower': results['approval_test']['ci_lower'],
            'ci_upper': results['approval_test']['ci_upper'],
            'significance': results['approval_test']['significance'],
            'mde': results['approval_test']['mde'],
            'expected_power': results['approval_test']['expected_power'],
        },
        'default_test': {
            'p1': results['default_test']['p1'],
            'p2': results['default_test']['p2'],
            'effect': results['default_test']['effect'],
            'z_statistic': results['default_test']['z_statistic'],
            'p_value': results['default_test']['p_value'],
            'ci_lower': results['default_test']['ci_lower'],
            'ci_upper': results['default_test']['ci_upper'],
            'significance': results['default_test']['significance'],
            'mde': results['default_test']['mde'],
            'expected_power': results['default_test']['expected_power'],
        }
    }
    return output

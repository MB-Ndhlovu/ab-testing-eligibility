"""
Generates a readable summary report from A/B test results.
"""

from src.simulate import run_simulation, format_test_result


def generate_report(results):
    """
    Generate a formatted text report from simulation results.

    Args:
        results: dict from simulate.run_simulation()

    Returns:
        str: Formatted report
    """
    stats = results['stats']
    tests = results['tests']
    meta = results['meta']

    lines = []
    lines.append("=" * 70)
    lines.append("       A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY MODEL")
    lines.append("=" * 70)

    lines.append("\n[EXPERIMENT SETUP]")
    lines.append(f"  Sample Size:        {meta['n_total']} total applicants")
    lines.append(f"  Control (Group A):  n = {stats['A']['n']}")
    lines.append(f"  Treatment (Group B): n = {stats['B']['n']}")
    lines.append(f"  Significance Level:  α = {meta['alpha']}")

    lines.append("\n[GROUP SUMMARY]")
    lines.append(f"  {'Metric':<20} {'Group A':>12} {'Group B':>12}")
    lines.append(f"  {'-'*20} {'-'*12} {'-'*12}")
    lines.append(f"  {'Approval Rate':<20} {stats['A']['approval_rate']:>12.4f} {stats['B']['approval_rate']:>12.4f}")
    lines.append(f"  {'Default Rate':<20} {stats['A']['default_rate']:>12.4f} {stats['B']['default_rate']:>12.4f}")
    lines.append(f"  {'Avg Loan Size (R)':<20} {stats['A']['avg_loan_size']:>12.2f} {stats['B']['avg_loan_size']:>12.2f}")
    lines.append(f"  {'Avg Processing (d)':<20} {stats['A']['avg_processing_time']:>12.2f} {stats['B']['avg_processing_time']:>12.2f}")

    lines.append("\n[STATISTICAL TESTS — TWO-PROPORTION Z-TEST]")

    for metric, label in [('approval_rate', 'Approval Rate'), ('default_rate', 'Default Rate')]:
        tr = tests[metric]
        ra = stats['A'][metric]
        rb = stats['B'][metric]
        fmt = format_test_result(metric, tr, ra, rb)
        diff = fmt['difference']
        sig_marker = "✓" if tr['significant'] else "✗"

        lines.append(f"\n  {sig_marker} {label.upper()}")
        lines.append(f"    Group A rate:  {ra:.4f}")
        lines.append(f"    Group B rate:  {rb:.4f}")
        lines.append(f"    Difference:     {diff:+.4f} ({diff*100:+.2f} pp)")
        lines.append(f"    Direction:      Group B is {fmt['direction']} than Group A")
        lines.append(f"    z-statistic:    {tr['z_statistic']:.4f}")
        lines.append(f"    p-value:        {tr['p_value']:.6f}")
        lines.append(f"    95% CI:         ({tr['ci_95'][0]:+.4f}, {tr['ci_95'][1]:+.4f})")
        lines.append(f"    Result:         {'SIGNIFICANT' if tr['significant'] else 'NOT SIGNIFICANT'} at α=0.05")
        if tr['significant']:
            lines.append(f"    Interpretation: We can reject the null hypothesis — the {label.lower()} difference is unlikely due to chance.")

    approval_sig = tests['approval_rate']['significant']
    default_sig = tests['default_rate']['significant']

    lines.append("\n[OVERALL CONCLUSION]")
    if approval_sig and default_sig:
        lines.append("  The new credit eligibility model (Group B) is unambiguously better.")
        lines.append("  It achieves a higher approval rate AND a lower default rate — both")
        lines.append("  statistically significant. Recommend deploying the new model.")
    elif approval_sig:
        lines.append("  Group B approves more applicants (significant), but the default rate")
        lines.append("  difference is not statistically significant. Further investigation")
        lines.append("  into risk profile recommended before deployment.")
    elif default_sig:
        lines.append("  Group B has a lower default rate (significant), but the approval rate")
        lines.append("  difference is not statistically significant. The new model may be")
        lines.append("  more selective without being more inclusive.")
    else:
        lines.append("  Neither metric shows a statistically significant difference at α=0.05.")
        lines.append("  Insufficient evidence to conclude that the new model differs from")
        lines.append("  the current model. Consider gathering more data or revising the model.")

    lines.append("\n" + "=" * 70)
    return "\n".join(lines)


def results_to_dict(results):
    """
    Convert full results object to a JSON-serializable dict.

    Args:
        results: dict from simulate.run_simulation()

    Returns:
        dict: Simplified results suitable for JSON serialization
    """
    stats = results['stats']
    tests = results['tests']

    output = {
        'experiment': {
            'n_total': results['meta']['n_total'],
            'n_per_group': results['meta']['n_per_group'],
            'alpha': results['meta']['alpha']
        },
        'group_A': stats['A'],
        'group_B': stats['B'],
        'tests': {}
    }

    for metric in ['approval_rate', 'default_rate']:
        tr = tests[metric]
        output['tests'][metric] = {
            'rate_A': stats['A'][metric],
            'rate_B': stats['B'][metric],
            'difference': stats['B'][metric] - stats['A'][metric],
            'z_statistic': tr['z_statistic'],
            'p_value': tr['p_value'],
            'ci_95_lower': tr['ci_95'][0],
            'ci_95_upper': tr['ci_95'][1],
            'significant': tr['significant']
        }

    return output


if __name__ == '__main__':
    results = run_simulation()
    report = generate_report(results)
    print(report)
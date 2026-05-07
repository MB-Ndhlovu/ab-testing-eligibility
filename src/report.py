"""
Generate readable summary report from simulation results.
"""
import json


def generate_report(results):
    """
    Generate a formatted text report from simulation results.

    Args:
        results: dict from run_simulation()

    Returns:
        str report
    """
    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY RESULTS")
    lines.append("=" * 60)

    lines.append("\n[SAMPLE METRICS]")
    d = results['data']
    for group in ['A', 'B']:
        g = d[f'group_{group}']
        label = "Control (A)" if group == 'A' else "Treatment (B)"
        lines.append(f"\n  {label}:")
        lines.append(f"    Sample size:         {g['n']:,}")
        lines.append(f"    Approval rate:       {g['approval_rate']:.2%}")
        lines.append(f"    Default rate:        {g['default_rate']:.2%}")
        lines.append(f"    Avg loan size:       R{g['avg_loan_size']:,.0f}")
        lines.append(f"    Avg processing time: {g['avg_processing_time']:.1f} hrs")

    for metric in ['approval_rate', 'default_rate']:
        lines.append(f"\n[{metric.upper().replace('_', ' ')}]")
        r = results[metric]
        sig_word = "SIGNIFICANT" if r['significant'] else "NOT SIGNIFICANT"
        lines.append(f"  Treatment effect:     {r['treatment_effect']:+.4f}")
        lines.append(f"  Z-statistic:          {r['z_statistic']:.4f}")
        lines.append(f"  P-value:              {r['p_value']:.6f}")
        lines.append(f"  95% CI:               [{r['ci_lower']:.4f}, {r['ci_upper']:.4f}]")
        lines.append(f"  Conclusion (α=0.05): {sig_word}")

    pwr = results['power_analysis']
    lines.append(f"\n[POWER ANALYSIS]")
    lines.append(f"  Sample size/group:    {pwr['sample_size_per_group']:,}")
    lines.append(f"  Min detectable effect: {pwr['minimum_detectable_effect']:.4f}")
    lines.append(f"  Power at MDE:          {pwr['power_at_mde']:.3f}")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)


def save_results_json(results, path):
    """Save results dict as JSON."""
    with open(path, 'w') as f:
        json.dump(results, f, indent=2)
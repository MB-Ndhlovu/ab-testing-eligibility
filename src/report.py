import json
import numpy as np

def make_serializable(obj):
    """Convert numpy types for JSON serialization."""
    if isinstance(obj, (np.floating, float)):
        return float(obj)
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    if isinstance(obj, tuple):
        return list(obj)
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_serializable(x) for x in obj]
    return obj

def generate_report(results):
    """Generate human-readable summary of A/B test results."""
    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY REPORT")
    lines.append("=" * 60)
    lines.append("")

    # Group summary
    lines.append("GROUP SUMMARY")
    lines.append("-" * 40)
    for group, data in results['groups'].items():
        lines.append(f"\n{group.upper()}")
        lines.append(f"  Sample size:        {data['n']}")
        lines.append(f"  Approval rate:      {data['approval_rate']:.4f}")
        lines.append(f"  Default rate:       {data['default_rate']:.4f}")
        lines.append(f"  Avg loan size:     ${data['avg_loan_size']:,.2f}")
        lines.append(f"  Avg processing:    {data['avg_processing_time']:.2f} days")

    # Approval rate test
    lines.append("\n" + "=" * 60)
    lines.append("APPROVAL RATE TEST")
    lines.append("-" * 40)
    ar = results['approval_rate_test']
    lines.append(f"  Z-statistic:        {ar['z_statistic']:.4f}")
    lines.append(f"  P-value:            {ar['p_value']:.6f}")
    lines.append(f"  95% CI for diff:   [{ar['ci_95'][0]:.6f}, {ar['ci_95'][1]:.6f}]")
    lines.append(f"  Significant:        {'YES' if ar['significant'] else 'NO'} (alpha=0.05)")

    # Default rate test
    lines.append("\n" + "=" * 60)
    lines.append("DEFAULT RATE TEST")
    lines.append("-" * 40)
    dr = results['default_rate_test']
    lines.append(f"  Z-statistic:        {dr['z_statistic']:.4f}")
    lines.append(f"  P-value:            {dr['p_value']:.6f}")
    lines.append(f"  95% CI for diff:   [{dr['ci_95'][0]:.6f}, {dr['ci_95'][1]:.6f}]")
    lines.append(f"  Significant:        {'YES' if dr['significant'] else 'NO'} (alpha=0.05)")

    # Power info
    lines.append("\n" + "=" * 60)
    lines.append("POWER ANALYSIS")
    lines.append("-" * 40)
    lines.append(f"  Power (approval test): {results['power']['approval_rate_test']:.4f}")
    lines.append(f"  Min detectable effect:  {results['power']['mde_approval_rate']:.6f}")

    # Conclusion
    lines.append("\n" + "=" * 60)
    lines.append("CONCLUSION")
    lines.append("-" * 40)
    ar_sig = results['approval_rate_test']['significant']
    dr_sig = results['default_rate_test']['significant']
    ar_diff = results['groups']['treatment']['approval_rate'] - results['groups']['control']['approval_rate']
    dr_diff = results['groups']['treatment']['default_rate'] - results['groups']['control']['default_rate']

    if ar_sig and dr_sig:
        lines.append("  Treatment is significantly better on BOTH metrics.")
        lines.append(f"  Approval rate improved by {ar_diff:.4f} ({ar_diff*100:.2f}%)")
        lines.append(f"  Default rate reduced by {abs(dr_diff):.4f} ({abs(dr_diff)*100:.2f}%)")
        lines.append("  RECOMMENDATION: Deploy the new model (Group B).")
    elif ar_sig:
        lines.append("  Treatment has higher approval rate.")
        lines.append("  But default rate difference is not significant.")
        lines.append("  RECOMMENDATION: Further analysis needed.")
    elif dr_sig:
        lines.append("  Treatment has lower default rate.")
        lines.append("  But approval rate difference is not significant.")
        lines.append("  RECOMMENDATION: Further analysis needed.")
    else:
        lines.append("  No statistically significant difference detected.")
        lines.append("  RECOMMENDATION: Keep current model or run larger test.")

    lines.append("=" * 60)
    return "\n".join(lines)

def save_results(results, filepath):
    """Save results dict as JSON."""
    with open(filepath, 'w') as f:
        json.dump(make_serializable(results), f, indent=2)
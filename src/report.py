from .simulate import run_simulation

def generate_report(results):
    """Generate a readable summary of the A/B test results."""
    r = results

    lines = []
    lines.append("=" * 60)
    lines.append("   A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  Sample Size  |  Group A (control): {r['sample_sizes']['group_a']:,}  |  Group B (treatment): {r['sample_sizes']['group_b']:,}")
    lines.append("")

    lines.append("-" * 60)
    lines.append("  METRIC 1: APPROVAL RATE")
    lines.append("-" * 60)
    lines.append(f"  Group A (control):   {r['approval_rate']['group_a']:.4f}  ({r['approval_rate']['group_a']*100:.2f}%)")
    lines.append(f"  Group B (treatment):  {r['approval_rate']['group_b']:.4f}  ({r['approval_rate']['group_b']*100:.2f}%)")
    lines.append(f"  Difference:           {r['approval_rate']['difference']:+.4f}  ({r['approval_rate']['difference']*100:+.2f} pp)")
    lines.append(f"  z-statistic:          {r['approval_rate']['z_statistic']:.4f}")
    lines.append(f"  p-value:             {r['approval_rate']['p_value']:.6f}")
    lines.append(f"  95% CI:               [{r['approval_rate']['ci_lower']:.4f}, {r['approval_rate']['ci_upper']:.4f}]")
    sig_word = "YES" if r['approval_rate']['significant'] else "NO"
    lines.append(f"  Statistically Significant (α=0.05): {sig_word}")
    lines.append("")

    lines.append("-" * 60)
    lines.append("  METRIC 2: DEFAULT RATE")
    lines.append("-" * 60)
    lines.append(f"  Group A (control):   {r['default_rate']['group_a']:.4f}  ({r['default_rate']['group_a']*100:.2f}%)")
    lines.append(f"  Group B (treatment): {r['default_rate']['group_b']:.4f}  ({r['default_rate']['group_b']*100:.2f}%)")
    lines.append(f"  Difference:          {r['default_rate']['difference']:+.4f}  ({r['default_rate']['difference']*100:+.2f} pp)")
    lines.append(f"  z-statistic:         {r['default_rate']['z_statistic']:.4f}")
    lines.append(f"  p-value:             {r['default_rate']['p_value']:.6f}")
    lines.append(f"  95% CI:              [{r['default_rate']['ci_lower']:.4f}, {r['default_rate']['ci_upper']:.4f}]")
    sig_word = "YES" if r['default_rate']['significant'] else "NO"
    lines.append(f"  Statistically Significant (α=0.05): {sig_word}")
    lines.append("")

    lines.append("-" * 60)
    lines.append("  SECONDARY METRICS")
    lines.append("-" * 60)
    lines.append(f"  Avg Loan Size (ZAR)     |  Group A: {r['avg_loan_size']['group_a']:,.2f}  |  Group B: {r['avg_loan_size']['group_b']:,.2f}")
    lines.append(f"  Avg Processing Time (s) |  Group A: {r['avg_processing_time']['group_a']:.2f}  |  Group B: {r['avg_processing_time']['group_b']:.2f}")
    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)
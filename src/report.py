"""
Generate readable summary report for A/B test results.
"""

def generate_report(results):
    lines = []
    lines.append("=" * 60)
    lines.append("  A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY REPORT")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"Sample Size: Control (A) = {results['sample_size']['group_a']}, Treatment (B) = {results['sample_size']['group_b']}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("  APPROVAL RATE")
    lines.append("-" * 60)
    lines.append(f"  Group A (Control):  {results['approval_rate']['group_a']:.2%}")
    lines.append(f"  Group B (Treatment): {results['approval_rate']['group_b']:.2%}")
    lines.append(f"  Difference:          {results['approval_rate']['diff']:+.2%}")
    lines.append(f"  Z-statistic:         {results['approval_rate']['z_statistic']:.4f}")
    lines.append(f"  P-value:             {results['approval_rate']['p_value']:.6f}")
    lines.append(f"  95% CI:              [{results['approval_rate']['ci_95'][0]:.4f}, {results['approval_rate']['ci_95'][1]:.4f}]")
    sig_approval = "SIGNIFICANT" if results['approval_rate']['significant'] else "NOT SIGNIFICANT"
    lines.append(f"  Conclusion (α=0.05):  {sig_approval}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("  DEFAULT RATE")
    lines.append("-" * 60)
    lines.append(f"  Group A (Control):  {results['default_rate']['group_a']:.2%}")
    lines.append(f"  Group B (Treatment): {results['default_rate']['group_b']:.2%}")
    lines.append(f"  Difference:          {results['default_rate']['diff']:+.2%}")
    lines.append(f"  Z-statistic:         {results['default_rate']['z_statistic']:.4f}")
    lines.append(f"  P-value:             {results['default_rate']['p_value']:.6f}")
    lines.append(f"  95% CI:              [{results['default_rate']['ci_95'][0]:.4f}, {results['default_rate']['ci_95'][1]:.4f}]")
    sig_default = "SIGNIFICANT" if results['default_rate']['significant'] else "NOT SIGNIFICANT"
    lines.append(f"  Conclusion (α=0.05):  {sig_default}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("  ADDITIONAL METRICS")
    lines.append("-" * 60)
    lines.append(f"  Avg Loan Size (A):      R{results['avg_loan_size']['group_a']:,.2f}")
    lines.append(f"  Avg Loan Size (B):      R{results['avg_loan_size']['group_b']:,.2f}")
    lines.append(f"  Avg Processing Time (A): {results['avg_processing_time']['group_a']:.2f} hours")
    lines.append(f"  Avg Processing Time (B): {results['avg_processing_time']['group_b']:.2f} hours")
    lines.append("")
    lines.append("=" * 60)
    lines.append("  OVERALL RECOMMENDATION")
    lines.append("=" * 60)
    
    if results['approval_rate']['significant'] and results['default_rate']['significant']:
        rec = "ADOPT new eligibility model — both approval rate increased and default rate decreased significantly."
    elif results['approval_rate']['significant']:
        rec = "CAUTION — approval rate improved but default rate not significantly changed. Review risk."
    elif results['default_rate']['significant']:
        rec = "CAUTION — default rate decreased but approval rate not significantly changed. Review impact on access."
    else:
        rec = "HOLD — no statistically significant improvement observed. Need larger sample or model refinement."
    
    lines.append(f"  {rec}")
    lines.append("=" * 60)
    
    return "\n".join(lines)
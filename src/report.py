def generate_report(results):
    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY RESULTS")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"{'METRIC':<25} {'GROUP A':<12} {'GROUP B':<12}")
    lines.append("-" * 50)
    lines.append(f"{'Approval Rate':<25} {results['approval_rate']['group_a']:<12.4f} {results['approval_rate']['group_b']:<12.4f}")
    lines.append(f"{'Default Rate':<25} {results['default_rate']['group_a']:<12.4f} {results['default_rate']['group_b']:<12.4f}")
    lines.append(f"{'Avg Loan Size':<25} ${results['a_avg_loan_size']:<11,.2f} ${results['b_avg_loan_size']:<11,.2f}")
    lines.append(f"{'Avg Processing Time':<25} {results['a_avg_processing_time']:<11.2f} {results['b_avg_processing_time']:<11.2f}")
    lines.append("")

    for metric in ['approval_rate', 'default_rate']:
        r = results[metric]
        sig_text = "SIGNIFICANT" if r['significant'] else "NOT SIGNIFICANT"
        lines.append(f"[{metric.upper().replace('_', ' ')}]")
        lines.append(f"  Z-statistic:     {r['z_statistic']}")
        lines.append(f"  P-value:         {r['p_value']}")
        lines.append(f"  95% CI:          [{r['ci_lower']:.4f}, {r['ci_upper']:.4f}]")
        lines.append(f"  Statistical Power: {r['statistical_power']:.4f}")
        lines.append(f"  Conclusion:      {sig_text} at α=0.05")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)
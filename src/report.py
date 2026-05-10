def generate_report(results):
    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    lines.append("=" * 60)
    lines.append("")

    lines.append("EXPERIMENT SETUP")
    lines.append("-" * 40)
    lines.append(f"  Total applicants : {results['n_total']}")
    lines.append(f"  Group A (Control): {results['n_group_a']}")
    lines.append(f"  Group B (Treatment): {results['n_group_b']}")
    lines.append(f"  Significance level (α): {results['alpha']}")
    lines.append("")

    lines.append("DESCRIPTIVE STATS")
    lines.append("-" * 40)
    lines.append(f"  {'Metric':<22} {'Group A':>12} {'Group B':>12}")
    lines.append(f"  {'Approval Rate':<22} {results['group_a']['approval_rate']:>12.2%} {results['group_b']['approval_rate']:>12.2%}")
    lines.append(f"  {'Default Rate':<22} {results['group_a']['default_rate']:>12.2%} {results['group_b']['default_rate']:>12.2%}")
    lines.append(f"  {'Avg Loan Size (R)':<22} {results['group_a']['avg_loan_size']:>12,.0f} {results['group_b']['avg_loan_size']:>12,.0f}")
    lines.append(f"  {'Avg Processing Time (h)':<22} {results['group_a']['avg_processing_time']:>12.2f} {results['group_b']['avg_processing_time']:>12.2f}")
    lines.append("")

    lines.append("HYPOTHESIS TESTS (Two-Proportion Z-Test)")
    lines.append("-" * 40)

    for metric_name, test in results["tests"].items():
        status = "SIGNIFICANT" if test["significant"] else "NOT SIGNIFICANT"
        lines.append(f"  {metric_name.upper().replace('_', ' ')}")
        lines.append(f"    Group A rate : {test['group_a_rate']:.2%}")
        lines.append(f"    Group B rate : {test['group_b_rate']:.2%}")
        diff_val = test["diff"]
        lines.append(f"    Difference   : {diff_val:+.2%}")
        ci_lower_val = test["ci_lower"]
        ci_upper_val = test["ci_upper"]
        lines.append(f"    95% CI        : [{ci_lower_val:+.2%}, {ci_upper_val:+.2%}]")
        z_stat_val = test["z_statistic"]
        p_val_fmt = test["p_value"]
        lines.append(f"    Z-statistic   : {z_stat_val:.4f}")
        lines.append(f"    P-value       : {p_val_fmt:.6f}")
        lines.append(f"    Conclusion    : {status} at α={results['alpha']}")
        lines.append("")

    lines.append("=" * 60)
    return "\n".join(lines)
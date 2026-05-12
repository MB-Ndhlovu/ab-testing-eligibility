def generate_report(results):
    lines = []
    lines.append("=" * 60)
    lines.append("   A/B TESTING REPORT — CREDIT ELIGIBILITY MODEL")
    lines.append("=" * 60)

    for metric, label in [("approval_rate", "Approval Rate"), ("default_rate", "Default Rate")]:
        r = results[metric]
        status = "SIGNIFICANT" if r["significant"] else "NOT SIGNIFICANT"
        lines.append(f"\n{label}")
        lines.append("-" * 40)
        lines.append(f"  Group A (Control):    {r['group_a']:.4f}")
        lines.append(f"  Group B (Treatment):  {r['group_b']:.4f}")
        lines.append(f"  Treatment Effect:      {r['treatment_effect']:+.4f}")
        lines.append(f"  Z-Statistic:          {r['z_statistic']:.4f}")
        lines.append(f"  P-Value:               {r['p_value']:.6f}")
        lines.append(f"  95% CI:                [{r['ci_95'][0]:+.4f}, {r['ci_95'][1]:+.4f}]")
        lines.append(f"  Statistical Power:    {r['power']:.4f}")
        lines.append(f"  Conclusion (α=0.05):  {status}")

    lines.append(f"\nAvg Loan Size")
    lines.append("-" * 40)
    lines.append(f"  Group A: R {results['avg_loan_size']['group_a']:,.2f}")
    lines.append(f"  Group B: R {results['avg_loan_size']['group_b']:,.2f}")
    lines.append(f"  Treatment Effect: R {results['avg_loan_size']['treatment_effect']:+,.2f}")

    lines.append(f"\nAvg Processing Time")
    lines.append("-" * 40)
    lines.append(f"  Group A: {results['avg_processing_time']['group_a']:.2f} hrs")
    lines.append(f"  Group B: {results['avg_processing_time']['group_b']:.2f} hrs")
    lines.append(f"  Treatment Effect: {results['avg_processing_time']['treatment_effect']:+.2f} hrs")

    lines.append("\n" + "=" * 60)
    return "\n".join(lines)
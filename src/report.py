"""Generate readable summary report."""
import json

def format_rate(val):
    return f"{val*100:.2f}%"

def generate_report(results, output_path=None):
    group_a = results["group_a"]
    group_b = results["group_b"]
    approval = results["approval_rate_test"]
    default = results["default_rate_test"]

    lines = []
    lines.append("=" * 60)
    lines.append("  A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY REPORT")
    lines.append("=" * 60)
    lines.append("")
    lines.append(f"  Sample size per group: {results['sample_size']:,}")
    lines.append("")
    lines.append("-" * 60)
    lines.append("  GROUP SUMMARY")
    lines.append("-" * 60)
    lines.append(f"  {'Metric':<20} {'Group A (Control)':<20} {'Group B (Treatment)':<20}")
    lines.append(f"  {'-'*18} {'-'*18} {'-'*18}")
    lines.append(f"  {'Approval Rate':<20} {format_rate(group_a['approval_rate']):<20} {format_rate(group_b['approval_rate']):<20}")
    lines.append(f"  {'Default Rate':<20} {format_rate(group_a['default_rate']):<20} {format_rate(group_b['default_rate']):<20}")
    lines.append(f"  {'Avg Loan Size':<20} {'R{:,.2f}'.format(group_a['avg_loan_size']):<20} {'R{:,.2f}'.format(group_b['avg_loan_size']):<20}")
    lines.append(f"  {'Processing Time':<20} {group_a['processing_time']:.2f} hrs{'':>6} {group_b['processing_time']:.2f} hrs")
    lines.append("")
    lines.append("-" * 60)
    lines.append("  STATISTICAL TESTS (Two-Proportion Z-Test, α=0.05)")
    lines.append("-" * 60)

    for test_name, test in [("Approval Rate", approval), ("Default Rate", default)]:
        lines.append(f"\n  >> {test_name}")
        lines.append(f"     Treatment effect: {'+' if test['treatment_effect'] >= 0 else ''}{test['treatment_effect']:.4f}")
        lines.append(f"     Z-statistic:     {test['z_statistic']:.4f}")
        lines.append(f"     P-value:         {test['p_value']:.6f}")
        lines.append(f"     95% CI:          [{test['ci_95_low']:.4f}, {test['ci_95_high']:.4f}]")
        sig_word = "SIGNIFICANT" if test['significant'] else "NOT SIGNIFICANT"
        direction = test['direction'].upper()
        lines.append(f"     Result:          {sig_word} — {direction}")

    lines.append("")
    lines.append("=" * 60)
    lines.append("  RECOMMENDATION")
    lines.append("=" * 60)
    if approval['significant'] and approval['direction'] == 'improvement':
        approval_rec = "APPROVE — new model significantly increases approval rate"
    elif approval['significant']:
        approval_rec = "REJECT — new model significantly decreases approval rate"
    else:
        approval_rec = "INCONCLUSIVE — no significant difference in approval rate"

    if default['significant'] and default['direction'] == 'improvement':
        default_rec = "APPROVE — new model significantly reduces default rate"
    elif default['significant']:
        default_rec = "REJECT — new model significantly increases default rate"
    else:
        default_rec = "INCONCLUSIVE — no significant difference in default rate"

    lines.append(f"  Approval Rate: {approval_rec}")
    lines.append(f"  Default Rate:  {default_rec}")
    lines.append("")
    lines.append("=" * 60)

    report_text = "\n".join(lines)
    print(report_text)

    if output_path:
        with open(output_path, "w") as f:
            f.write(report_text)
        print(f"\n[Report saved to {output_path}]")

    return report_text

if __name__ == "__main__":
    from simulate import run_simulation
    results = run_simulation()
    generate_report(results)
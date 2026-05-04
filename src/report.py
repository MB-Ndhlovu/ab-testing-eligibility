import json

def generate_report(results):
    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY RESULTS")
    lines.append("=" * 60)
    
    lines.append("\n--- GROUP SUMMARIES ---")
    a = results['group_a']
    b = results['group_b']
    
    lines.append(f"\nGroup A (Control) — n={a['n']}")
    lines.append(f"  Approval Rate:   {a['approval_rate']:.4f} ({int(a['approved'])}/{a['n']})")
    lines.append(f"  Default Rate:    {a['default_rate']:.4f}")
    lines.append(f"  Avg Loan Size:   ${a['avg_loan_size']:,.2f}")
    lines.append(f"  Avg Process Time: {a['avg_processing_time']:.2f} days")
    
    lines.append(f"\nGroup B (Treatment) — n={b['n']}")
    lines.append(f"  Approval Rate:   {b['approval_rate']:.4f} ({int(b['approved'])}/{b['n']})")
    lines.append(f"  Default Rate:    {b['default_rate']:.4f}")
    lines.append(f"  Avg Loan Size:   ${b['avg_loan_size']:,.2f}")
    lines.append(f"  Avg Process Time: {b['avg_processing_time']:.2f} days")
    
    lines.append("\n" + "=" * 60)
    lines.append("STATISTICAL TESTS (Two-Proportion Z-Test, α=0.05)")
    lines.append("=" * 60)
    
    at = results['approval_test']
    lines.append("\n[Approval Rate]")
    lines.append(f"  Z-Statistic:  {at['z_statistic']:.4f}")
    lines.append(f"  P-Value:      {at['p_value']:.6f}")
    lines.append(f"  95% CI:       [{at['ci_95'][0]:.4f}, {at['ci_95'][1]:.4f}]")
    lines.append(f"  MDE:          {at['mde']:.4f}")
    lines.append(f"  Power:        {at['power']:.4f}")
    lines.append(f"  Significant: {'YES' if at['significant'] else 'NO'}")
    
    dt = results['default_test']
    lines.append("\n[Default Rate]")
    lines.append(f"  Z-Statistic:  {dt['z_statistic']:.4f}")
    lines.append(f"  P-Value:      {dt['p_value']:.6f}")
    lines.append(f"  95% CI:       [{dt['ci_95'][0]:.4f}, {dt['ci_95'][1]:.4f}]")
    lines.append(f"  Significant:  {'YES' if dt['significant'] else 'NO'}")
    
    lines.append("\n" + "=" * 60)
    if at['significant'] and dt['significant']:
        lines.append("CONCLUSION: New model (B) is SIGNIFICANTLY BETTER on both metrics.")
    elif at['significant']:
        lines.append("CONCLUSION: New model (B) significantly improves approval rate only.")
    elif dt['significant']:
        lines.append("CONCLUSION: New model (B) significantly reduces default rate only.")
    else:
        lines.append("CONCLUSION: No statistically significant difference detected.")
    lines.append("=" * 60)
    
    return "\n".join(lines)
import json

def generate_report(results):
    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING FRAMEWORK - CREDIT ELIGIBILITY RESULTS")
    lines.append("=" * 60)
    
    for grp, stats in results['groups'].items():
        lines.append(f"\nGroup {grp} ({'Control' if grp == 'A' else 'Treatment'}):")
        lines.append(f"  Sample size:      {stats['n']}")
        lines.append(f"  Approval rate:    {stats['approval_rate']:.4f} ({stats['approval_rate']*100:.2f}%)")
        lines.append(f"  Default rate:     {stats['default_rate']:.4f} ({stats['default_rate']*100:.2f}%)")
        lines.append(f"  Avg loan size:    ${stats['avg_loan_size']:,.2f}")
        lines.append(f"  Avg processing:  {stats['avg_processing_time']:.1f} min")
    
    lines.append("\n" + "-" * 60)
    lines.append("STATISTICAL TEST RESULTS (Two-Proportion Z-Test)")
    lines.append("-" * 60)
    
    for metric, data in results['metrics'].items():
        metric_name = 'Approval Rate' if metric == 'approval_rate' else 'Default Rate'
        lines.append(f"\n{metric_name}:")
        lines.append(f"  Control (A):       {data['group_A']:.4f}")
        lines.append(f"  Treatment (B):     {data['group_B']:.4f}")
        lines.append(f"  Difference (B-A):  {data['difference']:+.4f}")
        lines.append(f"  Z-statistic:       {data['z_statistic']:.4f}")
        lines.append(f"  P-value:          {data['p_value']:.6f}")
        lines.append(f"  95% CI:            [{data['ci_lower']:.4f}, {data['ci_upper']:.4f}]")
        lines.append(f"  Statistical power: {data['power']:.4f}")
        lines.append(f"  Min detectable:    {data['mde']:.4f}")
        
        if data['significant_at_0.05']:
            lines.append(f"  Conclusion:        SIGNIFICANT (p < 0.05)")
        else:
            lines.append(f"  Conclusion:        NOT SIGNIFICANT (p >= 0.05)")
    
    lines.append("\n" + "=" * 60)
    lines.append("SUMMARY")
    lines.append("=" * 60)
    
    appr_sig = results['metrics']['approval_rate']['significant_at_0.05']
    def_sig = results['metrics']['default_rate']['significant_at_0.05']
    appr_diff = results['metrics']['approval_rate']['difference']
    def_diff = results['metrics']['default_rate']['difference']
    
    if appr_diff > 0 and not def_sig:
        verdict = "Treatment (B) shows higher approval rate with no significant increase in default rate. RECOMMEND adopting new model."
    elif appr_diff > 0 and def_diff > 0:
        verdict = "Treatment (B) shows higher approval rate BUT also higher default rate. CAUTION - review risk before adopting."
    elif def_diff < 0 and not appr_sig:
        verdict = "Treatment (B) shows lower default rate but no significant difference in approval. CONSIDER further testing."
    else:
        verdict = "No clear winner. Continue monitoring and consider larger sample size."
    
    lines.append(f"\n{verdict}")
    lines.append("=" * 60)
    
    return "\n".join(lines)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            results = json.load(f)
        print(generate_report(results))
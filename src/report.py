import json

def generate_report(results):
    """
    Generate a readable summary report from experiment results.
    """
    lines = []
    lines.append("=" * 60)
    lines.append("       A/B TESTING FRAMEWORK - CREDIT ELIGIBILITY")
    lines.append("=" * 60)
    
    lines.append("\n📊 EXPERIMENT SUMMARY")
    lines.append("-" * 40)
    s = results['summary']
    lines.append(f"  Total applications: {s['n_total']}")
    lines.append(f"  Group A (Control):  {s['group_a_n']} applicants")
    lines.append(f"  Group B (Treatment): {s['group_b_n']} applicants")
    
    lines.append("\n📈 APPROVAL RATE ANALYSIS")
    lines.append("-" * 40)
    ar = results['approval_rate']
    lines.append(f"  Group A (Control):  {ar['group_a']['rate']:.4f} ({ar['group_a']['successes']}/{ar['group_a']['n']})")
    lines.append(f"  Group B (Treatment): {ar['group_b']['rate']:.4f} ({ar['group_b']['successes']}/{ar['group_b']['n']})")
    lines.append(f"  Treatment Effect:    {ar['treatment_effect']:+.4f}")
    lines.append(f"  95% CI for Diff:     [{ar['ci_95'][0]:.4f}, {ar['ci_95'][1]:.4f}]")
    lines.append(f"  z-statistic:         {ar['z_statistic']:.4f}")
    lines.append(f"  p-value:             {ar['p_value']:.6f}")
    lines.append(f"  Statistical Power:   {ar['actual_power']:.4f}")
    lines.append(f"  MDE (80% power):     {ar['power_mde_80']:.4f}")
    lines.append(f"  MDE (90% power):     {ar['power_mde_90']:.4f}")
    sig_word = "✅ SIGNIFICANT" if ar['significant'] else "❌ NOT SIGNIFICANT"
    lines.append(f"  Conclusion (α=0.05): {sig_word}")
    
    lines.append("\n⚠️  DEFAULT RATE ANALYSIS")
    lines.append("-" * 40)
    dr = results['default_rate']
    lines.append(f"  Group A (Control):  {dr['group_a']['rate']:.4f} ({dr['group_a']['successes']}/{dr['group_a']['n']})")
    lines.append(f"  Group B (Treatment): {dr['group_b']['rate']:.4f} ({dr['group_b']['successes']}/{dr['group_b']['n']})")
    lines.append(f"  Treatment Effect:    {dr['treatment_effect']:+.4f}")
    lines.append(f"  95% CI for Diff:     [{dr['ci_95'][0]:.4f}, {dr['ci_95'][1]:.4f}]")
    lines.append(f"  z-statistic:         {dr['z_statistic']:.4f}")
    lines.append(f"  p-value:             {dr['p_value']:.6f}")
    lines.append(f"  Statistical Power:   {dr['actual_power']:.4f}")
    lines.append(f"  MDE (80% power):     {dr['power_mde_80']:.4f}")
    lines.append(f"  MDE (90% power):     {dr['power_mde_90']:.4f}")
    sig_word = "✅ SIGNIFICANT" if dr['significant'] else "❌ NOT SIGNIFICANT"
    lines.append(f"  Conclusion (α=0.05): {sig_word}")
    
    lines.append("\n💰 AVERAGE LOAN SIZE")
    lines.append("-" * 40)
    lines.append(f"  Group A: R{s['group_a_avg_loan']:,.2f}")
    lines.append(f"  Group B: R{s['group_b_avg_loan']:,.2f}")
    
    lines.append("\n⏱️  PROCESSING TIME (seconds)")
    lines.append("-" * 40)
    lines.append(f"  Group A: {s['group_a_avg_proc_time']:.1f}s")
    lines.append(f"  Group B: {s['group_b_avg_proc_time']:.1f}s")
    
    lines.append("\n" + "=" * 60)
    ar_sig = results['approval_rate']['significant']
    dr_sig = results['default_rate']['significant']
    
    if ar_sig and dr_sig:
        verdict = "🎯 RECOMMENDATION: Deploy Model B - significant improvement in BOTH approval rate AND default rate."
    elif ar_sig:
        verdict = "⚠️  RECOMMENDATION: Deploy Model B - significant approval improvement, but default rate not significantly improved."
    elif dr_sig:
        verdict = "⚠️  RECOMMENDATION: Deploy Model B - significant default improvement, but approval rate not significantly improved."
    else:
        verdict = "❌ RECOMMENDATION: Keep Model A - no statistically significant improvement detected in either metric."
    
    lines.append(f"\n{verdict}")
    lines.append("=" * 60)
    
    return "\n".join(lines)

if __name__ == '__main__':
    from simulate import run_experiment
    results = run_experiment()
    print(generate_report(results))
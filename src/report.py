"""Generate readable summary reports for A/B test results."""
import json

def format_pvalue(p):
    """Format p-value for display."""
    if p < 0.001:
        return "< 0.001"
    return f"{p:.4f}"

def format_ci(lower, upper):
    """Format confidence interval for display."""
    return f"({lower:.4f}, {upper:.4f})"

def generate_summary_report(results):
    """
    Generate a human-readable summary report.
    
    Parameters:
    -----------
    results : dict
        Results from simulate.run_simulation()
    
    Returns:
    --------
    str : Formatted report
    """
    stats = results['group_stats']
    approval = results['approval_rate_analysis']
    default = results['default_rate_analysis']
    
    lines = []
    lines.append("=" * 60)
    lines.append("       A/B TESTING FRAMEWORK FOR CREDIT ELIGIBILITY")
    lines.append("=" * 60)
    lines.append("")
    
    lines.append("EXECUTIVE SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Total Applicants: {stats['A']['n'] + stats['B']['n']}")
    lines.append(f"Group A (Control): {stats['A']['n']} applicants")
    lines.append(f"Group B (Treatment): {stats['B']['n']} applicants")
    lines.append("")
    
    lines.append("APPROVAL RATE ANALYSIS")
    lines.append("-" * 40)
    lines.append(f"  Group A (Control):  {approval['group_A_proportion']:.4f} ({approval['group_A_proportion']*100:.2f}%)")
    lines.append(f"  Group B (Treatment): {approval['group_B_proportion']:.4f} ({approval['group_B_proportion']*100:.2f}%)")
    lines.append(f"  Treatment Effect:   +{approval['treatment_effect']:.4f} ({approval['treatment_effect']*100:.2f} pp)")
    lines.append(f"  Z-Statistic:         {approval['z_statistic']:.4f}")
    lines.append(f"  P-Value:             {format_pvalue(approval['p_value'])}")
    lines.append(f"  95% CI:              {format_ci(approval['ci_lower'], approval['ci_upper'])}")
    lines.append(f"  Statistically Significant: {'YES' if approval['significant'] else 'NO'} (alpha=0.05)")
    lines.append("")
    
    lines.append("DEFAULT RATE ANALYSIS")
    lines.append("-" * 40)
    lines.append(f"  Group A (Control):  {default['group_A_proportion']:.4f} ({default['group_A_proportion']*100:.2f}%)")
    lines.append(f"  Group B (Treatment): {default['group_B_proportion']:.4f} ({default['group_B_proportion']*100:.2f}%)")
    lines.append(f"  Treatment Effect:   {default['treatment_effect']:.4f} ({default['treatment_effect']*100:.2f} pp)")
    lines.append(f"  Z-Statistic:         {default['z_statistic']:.4f}")
    lines.append(f"  P-Value:             {format_pvalue(default['p_value'])}")
    lines.append(f"  95% CI:              {format_ci(default['ci_lower'], default['ci_upper'])}")
    lines.append(f"  Statistically Significant: {'YES' if default['significant'] else 'NO'} (alpha=0.05)")
    lines.append("")
    
    lines.append("STATISTICAL POWER")
    lines.append("-" * 40)
    lines.append(f"  Approval Rate Power: {approval['power']:.4f} ({approval['power']*100:.2f}%)")
    lines.append(f"  Default Rate Power:  {default['power']:.4f} ({default['power']*100:.2f}%)")
    lines.append(f"  Min Detectable Effect (Approval): {approval['mde']:.4f} ({approval['mde']*100:.2f} pp)")
    lines.append(f"  Min Detectable Effect (Default): {default['mde']:.4f} ({default['mde']*100:.2f} pp)")
    lines.append("")
    
    lines.append("CONCLUSION")
    lines.append("-" * 40)
    if approval['significant'] and default['significant']:
        lines.append("  The new model (Group B) is SIGNIFICANTLY BETTER on both metrics.")
        lines.append("  - Higher approval rate (+{:.1f} pp)".format(approval['treatment_effect']*100))
        lines.append("  - Lower default rate ({:.1f} pp)".format(default['treatment_effect']*100))
        lines.append("  RECOMMENDATION: Deploy the new model.")
    elif approval['significant']:
        lines.append("  The new model shows SIGNIFICANT improvement in approval rate")
        lines.append("  but NO significant change in default rate.")
        lines.append("  RECOMMENDATION: Further analysis required.")
    elif default['significant']:
        lines.append("  The new model shows SIGNIFICANT improvement in default rate")
        lines.append("  but NO significant change in approval rate.")
        lines.append("  RECOMMENDATION: Further analysis required.")
    else:
        lines.append("  NO statistically significant differences detected.")
        lines.append("  RECOMMENDATION: Continue with current model.")
    
    lines.append("")
    lines.append("=" * 60)
    
    return "\n".join(lines)

def results_to_json(results):
    """Convert results to JSON-serializable format."""
    def make_serializable(obj):
        if isinstance(obj, dict):
            return {k: make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [make_serializable(i) for i in obj]
        elif isinstance(obj, (int, float)):
            return float(obj) if obj != int(obj) else int(obj)
        elif isinstance(obj, np_bool):
            return bool(obj)
        else:
            return obj
    
    import numpy as np
    np_bool = np.bool_
    
    return make_serializable(results)

if __name__ == '__main__':
    from simulate import run_simulation
    results = run_simulation()
    print(generate_summary_report(results))
import json

def generate_report(results):
    report = []
    report.append("=" * 60)
    report.append("A/B TESTING RESULTS: CREDIT ELIGIBILITY MODEL")
    report.append("=" * 60)
    report.append("")
    report.append(f"Sample Size per Group: {results['n_per_group']}")
    report.append("")
    report.append("-" * 60)
    report.append("APPROVAL RATE ANALYSIS")
    report.append("-" * 60)
    report.append(f"  Control (A):      {results['approval_rate_A']:.4f} ({results['approval_rate_A']*100:.2f}%)")
    report.append(f"  Treatment (B):   {results['approval_rate_B']:.4f} ({results['approval_rate_B']*100:.2f}%)")
    report.append(f"  Difference:       {results['approval_rate_B'] - results['approval_rate_A']:.4f}")
    report.append(f"  Z-statistic:      {results['approval_z']:.4f}")
    report.append(f"  P-value:          {results['approval_p_value']:.6f}")
    report.append(f"  95% CI:           [{results['approval_ci'][0]:.4f}, {results['approval_ci'][1]:.4f}]")
    report.append(f"  Significant:      {'YES' if results['approval_significant'] else 'NO'} (alpha=0.05)")
    report.append(f"  Power:            {results['power_approval']:.4f}")
    report.append("")
    report.append("-" * 60)
    report.append("DEFAULT RATE ANALYSIS")
    report.append("-" * 60)
    report.append(f"  Control (A):      {results['default_rate_A']:.4f} ({results['default_rate_A']*100:.2f}%)")
    report.append(f"  Treatment (B):   {results['default_rate_B']:.4f} ({results['default_rate_B']*100:.2f}%)")
    report.append(f"  Difference:       {results['default_rate_B'] - results['default_rate_A']:.4f}")
    report.append(f"  Z-statistic:      {results['default_z']:.4f}")
    report.append(f"  P-value:          {results['default_p_value']:.6f}")
    report.append(f"  95% CI:           [{results['default_ci'][0]:.4f}, {results['default_ci'][1]:.4f}]")
    report.append(f"  Significant:      {'YES' if results['default_significant'] else 'NO'} (alpha=0.05)")
    report.append(f"  Power:            {results['power_default']:.4f}")
    report.append("")
    report.append("-" * 60)
    report.append("POWER ANALYSIS")
    report.append("-" * 60)
    report.append(f"  Min Detectable Effect (80% power): {results['mde']:.4f}")
    report.append("")
    report.append("=" * 60)
    report.append("CONCLUSION")
    report.append("=" * 60)
    if results['approval_significant'] and results['default_significant']:
        report.append("  The new credit model (B) significantly outperforms the current")
        report.append("  model (A) on BOTH metrics. RECOMMEND: Deploy new model.")
    elif results['approval_significant']:
        report.append("  The new model shows significantly higher approval rates but")
        report.append("  no significant difference in default rates.")
    elif results['default_significant']:
        report.append("  The new model shows significantly lower default rates but")
        report.append("  no significant difference in approval rates.")
    else:
        report.append("  No statistically significant differences detected between")
        report.append("  the two models. MORE DATA may be needed.")
    report.append("")
    
    return "\n".join(report)

def save_results_json(results, filepath):
    import numpy as np
    save_data = {k: v for k, v in results.items() if k not in ['approval_ci', 'default_ci']}
    save_data['approval_ci'] = list(results['approval_ci'])
    save_data['default_ci'] = list(results['default_ci'])
    for key, value in save_data.items():
        if isinstance(value, (np.bool_, np.integer)):
            save_data[key] = bool(value) if isinstance(value, np.bool_) else int(value)
        elif isinstance(value, (np.floating,)):
            save_data[key] = float(value)
    with open(filepath, 'w') as f:
        json.dump(save_data, f, indent=2)
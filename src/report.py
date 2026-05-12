import json

def generate_report(results):
    """
    Generate a human-readable summary report from experiment results.
    
    Args:
        results: Dict from simulate.simulate_experiment()
    
    Returns:
        str: Formatted report
    """
    lines = []
    
    lines.append("=" * 70)
    lines.append("       A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY MODEL")
    lines.append("=" * 70)
    
    # Executive Summary
    lines.append("\n## EXECUTIVE SUMMARY")
    approval_sig = results['approval_analysis']['significant']
    default_sig = results['default_analysis']['significant']
    
    if approval_sig and default_sig:
        status = "RECOMMEND ADOPTING new model"
    elif approval_sig and not default_sig:
        status = "CAUTION — only approval rate improved"
    else:
        status = "INSUFFICIENT EVIDENCE to change models"
    
    lines.append(f"Recommendation: {status}")
    
    # Group Stats Table
    lines.append("\n## GROUP PERFORMANCE COMPARISON")
    lines.append("-" * 70)
    lines.append(f"{'Metric':<25} {'Group A (Control)':<20} {'Group B (Treatment)':<20}")
    lines.append("-" * 70)
    
    s_a = results['group_stats']['A']
    s_b = results['group_stats']['B']
    
    lines.append(f"{'Sample size':<25} {s_a['n']:<20} {s_b['n']:<20}")
    lines.append(f"{'Approval rate':<25} {s_a['approval_rate']:<20.4f} {s_b['approval_rate']:<20.4f}")
    lines.append(f"{'Default rate':<25} {s_a['default_rate']:<20.4f} {s_b['default_rate']:<20.4f}")
    lines.append(f"{'Avg loan size ($)':<25} {s_a['avg_loan_size']:<20,.2f} {s_b['avg_loan_size']:<20,.2f}")
    lines.append(f"{'Avg processing (min)':<25} {s_a['avg_processing_time']:<20.1f} {s_b['avg_processing_time']:<20.1f}")
    lines.append("-" * 70)
    
    # Statistical Test Results
    lines.append("\n## STATISTICAL TEST RESULTS (Two-Proportion Z-Test)")
    lines.append(f"Significance level: α = 0.05")
    
    lines.append("\n### Approval Rate")
    a = results['approval_analysis']
    te = results['treatment_effect_approval']
    lines.append(f"  Observed difference:  {te:+.4f} ({te*100:+.2f}%)")
    lines.append(f"  z-statistic:          {a['z_statistic']:.4f}")
    lines.append(f"  p-value:              {a['p_value']:.6f}")
    lines.append(f"  95% CI:               [{a['ci_lower']:.4f}, {a['ci_upper']:.4f}]")
    lines.append(f"  Conclusion:           {'Statistically significant' if a['significant'] else 'Not statistically significant'}")
    
    lines.append("\n### Default Rate")
    d = results['default_analysis']
    te = results['treatment_effect_default']
    lines.append(f"  Observed difference:  {te:+.4f} ({te*100:+.2f}%)")
    lines.append(f"  z-statistic:          {d['z_statistic']:.4f}")
    lines.append(f"  p-value:              {d['p_value']:.6f}")
    lines.append(f"  95% CI:               [{d['ci_lower']:.4f}, {d['ci_upper']:.4f}]")
    lines.append(f"  Conclusion:           {'Statistically significant' if d['significant'] else 'Not statistically significant'}")
    
    # Interpretation
    lines.append("\n## INTERPRETATION")
    if a['significant'] and d['significant']:
        lines.append("Both approval rate and default rate show statistically significant")
        lines.append("improvement under the new model (Group B). The new eligibility")
        lines.append("model approves more applicants AND selects lower-risk borrowers.")
        lines.append("Recommend adopting the new model.")
    elif a['significant']:
        lines.append("Only approval rate shows statistically significant improvement.")
        lines.append("While more applicants are approved, default rate difference is not")
        lines.append("statistically significant. Recommend further analysis before adopting.")
    elif d['significant']:
        lines.append("Only default rate shows statistically significant improvement.")
        lines.append("The new model selects lower-risk borrowers, but approval rate")
        lines.append("difference is not statistically significant. Further analysis needed.")
    else:
        lines.append("Neither metric shows a statistically significant difference at α=0.05.")
        lines.append("Insufficient evidence to conclude the new model differs from the")
        lines.append("current model. Consider increasing sample size or re-evaluating.")
    
    lines.append("\n" + "=" * 70)
    return "\n".join(lines)

def save_json_report(results, filepath):
    """Save results as JSON for programmatic consumption."""
    # Convert to JSON-serializable format
    output = {
        'group_stats': {},
        'approval_analysis': {},
        'default_analysis': {},
        'treatment_effects': {}
    }
    
    for group in ['A', 'B']:
        output['group_stats'][group] = {k: float(v) for k, v in results['group_stats'][group].items()}
    
    for key in ['z_statistic', 'p_value', 'ci_lower', 'ci_upper', 'significant', 'alpha']:
        output['approval_analysis'][key] = float(results['approval_analysis'][key])
        output['default_analysis'][key] = float(results['default_analysis'][key])
    
    output['treatment_effects']['approval'] = float(results['treatment_effect_approval'])
    output['treatment_effects']['default'] = float(results['treatment_effect_default'])
    
    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2)

if __name__ == '__main__':
    from src.simulate import simulate_experiment
    results = simulate_experiment(seed=42)
    report = generate_report(results)
    print(report)
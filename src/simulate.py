import numpy as np
from src.data_generator import generate_loan_data, compute_group_stats
from src.statistical import run_analysis

def simulate_experiment(seed=42):
    """
    Run a full A/B test experiment simulation.
    
    Args:
        seed: Random seed for reproducibility
    
    Returns:
        dict with experiment results
    """
    # Generate data
    df = generate_loan_data(n=5000, seed=seed)
    
    # Compute group stats
    stats = compute_group_stats(df)
    
    n_a = stats['A']['n']
    n_b = stats['B']['n']
    
    # Approval rate analysis
    approved_a = df[df['group'] == 'A']['approved'].sum()
    approved_b = df[df['group'] == 'B']['approved'].sum()
    
    approval_analysis = run_analysis(n_a, approved_a, n_b, approved_b)
    
    # Default rate analysis
    defaulted_a = df[df['group'] == 'A']['defaulted'].sum()
    defaulted_b = df[df['group'] == 'B']['defaulted'].sum()
    
    default_analysis = run_analysis(n_a, defaulted_a, n_b, defaulted_b)
    
    # Treatment effects
    treatment_effect_approval = stats['B']['approval_rate'] - stats['A']['approval_rate']
    treatment_effect_default = stats['B']['default_rate'] - stats['A']['default_rate']
    
    return {
        'group_stats': stats,
        'approval_analysis': approval_analysis,
        'default_analysis': default_analysis,
        'treatment_effect_approval': treatment_effect_approval,
        'treatment_effect_default': treatment_effect_default
    }

def format_results(results):
    """Format results into a summary string."""
    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING EXPERIMENT RESULTS")
    lines.append("=" * 60)
    
    lines.append("\n--- GROUP STATISTICS ---")
    for group in ['A', 'B']:
        s = results['group_stats'][group]
        lines.append(f"\nGroup {group}:")
        lines.append(f"  Sample size: {s['n']}")
        lines.append(f"  Approval rate: {s['approval_rate']:.4f}")
        lines.append(f"  Default rate: {s['default_rate']:.4f}")
        lines.append(f"  Avg loan size: ${s['avg_loan_size']:,.2f}")
        lines.append(f"  Avg processing time: {s['avg_processing_time']:.1f} min")
    
    lines.append("\n--- APPROVAL RATE ANALYSIS ---")
    a = results['approval_analysis']
    lines.append(f"  Treatment effect: {results['treatment_effect_approval']:+.4f}")
    lines.append(f"  z-statistic: {a['z_statistic']:.4f}")
    lines.append(f"  p-value: {a['p_value']:.6f}")
    lines.append(f"  95% CI: [{a['ci_lower']:.4f}, {a['ci_upper']:.4f}]")
    sig_word = "SIGNIFICANT" if a['significant'] else "NOT SIGNIFICANT"
    lines.append(f"  Conclusion (α={a['alpha']}): {sig_word}")
    
    lines.append("\n--- DEFAULT RATE ANALYSIS ---")
    d = results['default_analysis']
    lines.append(f"  Treatment effect: {results['treatment_effect_default']:+.4f}")
    lines.append(f"  z-statistic: {d['z_statistic']:.4f}")
    lines.append(f"  p-value: {d['p_value']:.6f}")
    lines.append(f"  95% CI: [{d['ci_lower']:.4f}, {d['ci_upper']:.4f}]")
    sig_word = "SIGNIFICANT" if d['significant'] else "NOT SIGNIFICANT"
    lines.append(f"  Conclusion (α={d['alpha']}): {sig_word}")
    
    lines.append("\n" + "=" * 60)
    return "\n".join(lines)

if __name__ == '__main__':
    results = simulate_experiment()
    print(format_results(results))
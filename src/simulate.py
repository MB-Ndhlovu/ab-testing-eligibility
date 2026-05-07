"""Run A/B test experiment simulation and compute treatment effects."""
import numpy as np
from .data_generator import generate_data, compute_group_stats
from .statistical import evaluate_metric

def run_simulation(alpha=0.05):
    """
    Run the full A/B test simulation.
    
    Parameters:
    -----------
    alpha : float
        Significance level for hypothesis testing
    
    Returns:
    --------
    dict with simulation results
    """
    # Generate data
    df = generate_data()
    
    # Compute group statistics
    stats = compute_group_stats(df)
    
    n_A = stats['A']['n']
    n_B = stats['B']['n']
    
    # Evaluate approval rate
    approval_result = evaluate_metric(
        name='Approval Rate',
        n_A=n_A,
        p_A=stats['A']['approval_rate'],
        n_B=n_B,
        p_B=stats['B']['approval_rate'],
        alpha=alpha
    )
    
    # Evaluate default rate
    default_result = evaluate_metric(
        name='Default Rate',
        n_A=n_A,
        p_A=stats['A']['default_rate'],
        n_B=n_B,
        p_B=stats['B']['default_rate'],
        alpha=alpha
    )
    
    return {
        'group_stats': stats,
        'approval_rate_analysis': approval_result,
        'default_rate_analysis': default_result,
        'alpha': alpha,
    }

def compute_treatment_effects(results):
    """Extract treatment effects from results."""
    approval_effect = results['approval_rate_analysis']['treatment_effect']
    default_effect = results['default_rate_analysis']['treatment_effect']
    return {
        'approval_rate_lift': approval_effect,
        'default_rate_change': default_effect,
        'approval_rate_lift_pct': (approval_effect / results['group_stats']['A']['approval_rate']) * 100,
        'default_rate_change_pct': (default_effect / results['group_stats']['A']['default_rate']) * 100,
    }

if __name__ == '__main__':
    results = run_simulation()
    print("Simulation complete")
    print(f"Approval Rate: {results['approval_rate_analysis']['group_A_proportion']:.4f} vs {results['approval_rate_analysis']['group_B_proportion']:.4f}")
    print(f"Default Rate: {results['default_rate_analysis']['group_A_proportion']:.4f} vs {results['default_rate_analysis']['group_B_proportion']:.4f}")
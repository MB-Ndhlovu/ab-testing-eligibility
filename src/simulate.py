"""
Run A/B test experiment simulation.
"""

import numpy as np
from .data_generator import generate_data, compute_summary_stats
from .statistical import two_proportion_ztest, confidence_interval_diff, power_analysis

def run_simulation(seed=42, alpha=0.05):
    """Run full A/B test simulation."""
    data = generate_data(n=5000, seed=seed)
    stats_summary = compute_summary_stats(data)
    
    n_a = stats_summary['group_a']['n']
    n_b = stats_summary['group_b']['n']
    p_approved_a = stats_summary['group_a']['approval_rate']
    p_approved_b = stats_summary['group_b']['approval_rate']
    p_default_a = stats_summary['group_a']['default_rate']
    p_default_b = stats_summary['group_b']['default_rate']
    
    # Test approval rate
    z_approval, p_approval = two_proportion_ztest(n_a, p_approved_a, n_b, p_approved_b)
    ci_approval = confidence_interval_diff(n_a, p_approved_a, n_b, p_approved_b, alpha)
    
    # Test default rate
    z_default, p_default = two_proportion_ztest(n_a, p_default_a, n_b, p_default_b)
    ci_default = confidence_interval_diff(n_a, p_default_a, n_b, p_default_b, alpha)
    
    # Power analysis
    mde_approval = abs(p_approved_b - p_approved_a)
    mde_default = abs(p_default_b - p_default_a)
    n_required_approval = power_analysis(p_approved_a, p_approved_b, alpha)
    n_required_default = power_analysis(p_default_a, p_default_b, alpha)
    
    results = {
        'sample_size': {'group_a': n_a, 'group_b': n_b},
        'approval_rate': {
            'group_a': round(p_approved_a, 4),
            'group_b': round(p_approved_b, 4),
            'diff': round(p_approved_b - p_approved_a, 4),
            'z_statistic': round(z_approval, 4),
            'p_value': round(p_approval, 6),
            'ci_95': (round(ci_approval[0], 4), round(ci_approval[1], 4)),
            'significant': p_approval < alpha,
            'mde_observed': round(mde_approval, 4),
            'n_required': n_required_approval,
        },
        'default_rate': {
            'group_a': round(p_default_a, 4),
            'group_b': round(p_default_b, 4),
            'diff': round(p_default_b - p_default_a, 4),
            'z_statistic': round(z_default, 4),
            'p_value': round(p_default, 6),
            'ci_95': (round(ci_default[0], 4), round(ci_default[1], 4)),
            'significant': p_default < alpha,
            'mde_observed': round(mde_default, 4),
            'n_required': n_required_default,
        },
        'avg_loan_size': {
            'group_a': round(stats_summary['group_a']['avg_loan_size'], 2),
            'group_b': round(stats_summary['group_b']['avg_loan_size'], 2),
        },
        'avg_processing_time': {
            'group_a': round(stats_summary['group_a']['avg_processing_time'], 2),
            'group_b': round(stats_summary['group_b']['avg_processing_time'], 2),
        }
    }
    
    return results
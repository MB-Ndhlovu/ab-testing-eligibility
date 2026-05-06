import numpy as np
from .data_generator import generate_loan_data, compute_group_stats
from .statistical import (
    two_proportion_ztest,
    confidence_interval_diff,
    statistical_power,
    minimum_detectable_effect
)

def run_simulation(seed=42, alpha=0.05):
    """Run A/B test simulation and return results.

    Args:
        seed: Random seed
        alpha: Significance level

    Returns:
        Dict with test results, group stats, and conclusions
    """
    np.random.seed(seed)
    df = generate_loan_data(n=5000, seed=seed)
    stats_dict = compute_group_stats(df)

    # Extract counts
    n_a = stats_dict['A']['n']
    n_b = stats_dict['B']['n']
    approved_a = int(stats_dict['A']['approval_rate'] * n_a)
    approved_b = int(stats_dict['B']['approval_rate'] * n_b)
    default_a = int(stats_dict['A']['default_rate'] * approved_a)
    default_b = int(stats_dict['B']['default_rate'] * approved_b)

    # Tests for approval rate
    z_approval, p_approval = two_proportion_ztest(n_a, approved_a, n_b, approved_b)
    ci_approval = confidence_interval_diff(n_a, approved_a, n_b, approved_b)

    # Tests for default rate
    z_default, p_default = two_proportion_ztest(n_a, default_a, n_b, default_b)
    ci_default = confidence_interval_diff(n_a, default_a, n_b, default_b)

    # Power calculations
    power_approval = statistical_power(
        stats_dict['A']['approval_rate'],
        stats_dict['B']['approval_rate'],
        n_a, n_b, alpha
    )
    mde_approval = minimum_detectable_effect(n_a, n_b, alpha)

    return {
        'groups': {
            'control': {'n': n_a, 'approval_rate': stats_dict['A']['approval_rate'],
                        'default_rate': stats_dict['A']['default_rate'],
                        'avg_loan_size': stats_dict['A']['avg_loan_size'],
                        'avg_processing_time': stats_dict['A']['avg_processing_time']},
            'treatment': {'n': n_b, 'approval_rate': stats_dict['B']['approval_rate'],
                          'default_rate': stats_dict['B']['default_rate'],
                          'avg_loan_size': stats_dict['B']['avg_loan_size'],
                          'avg_processing_time': stats_dict['B']['avg_processing_time']}
        },
        'approval_rate_test': {
            'z_statistic': round(z_approval, 4),
            'p_value': round(p_approval, 6),
            'ci_95': (round(ci_approval[0], 6), round(ci_approval[1], 6)),
            'significant': p_approval < alpha
        },
        'default_rate_test': {
            'z_statistic': round(z_default, 4),
            'p_value': round(p_default, 6),
            'ci_95': (round(ci_default[0], 6), round(ci_default[1], 6)),
            'significant': p_default < alpha
        },
        'power': {
            'approval_rate_test': round(power_approval, 4),
            'mde_approval_rate': round(mde_approval, 6)
        }
    }
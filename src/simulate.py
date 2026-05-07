"""
Experiment simulation: run A/B test and compute treatment effects.
"""
from src.data_generator import generate_loan_data, compute_group_metrics
from src.statistical import (
    two_proportion_ztest,
    confidence_interval_diff,
    statistical_power,
    minimum_detectable_effect
)


def run_simulation(seed=42):
    """
    Run full A/B test simulation.

    Args:
        seed: Random seed

    Returns:
        dict with all results
    """
    df = generate_loan_data(seed=seed)
    metrics = compute_group_metrics(df)

    mA = metrics['A']
    mB = metrics['B']

    results = {
        'data': {
            'group_A': {
                'n': int(mA['n']),
                'approval_rate': float(round(mA['approval_rate'], 4)),
                'default_rate': float(round(mA['default_rate'], 4)),
                'avg_loan_size': float(round(mA['avg_loan_size'], 2)),
                'avg_processing_time': float(round(mA['avg_processing_time'], 2))
            },
            'group_B': {
                'n': int(mB['n']),
                'approval_rate': float(round(mB['approval_rate'], 4)),
                'default_rate': float(round(mB['default_rate'], 4)),
                'avg_loan_size': float(round(mB['avg_loan_size'], 2)),
                'avg_processing_time': float(round(mB['avg_processing_time'], 2))
            }
        }
    }

    # Approval rate test
    nA, pA = mA['n'], mA['approval_rate']
    nB, pB = mB['n'], mB['approval_rate']

    approval_test = two_proportion_ztest(nA, pA, nB, pB)
    approval_ci = confidence_interval_diff(nA, pA, nB, pB)

    results['approval_rate'] = {
        'z_statistic': float(round(approval_test['z_statistic'], 4)),
        'p_value': float(round(approval_test['p_value'], 6)),
        'ci_lower': float(round(approval_ci[0], 4)),
        'ci_upper': float(round(approval_ci[1], 4)),
        'significant': bool(approval_test['p_value'] < 0.05),
        'treatment_effect': float(round(pB - pA, 4))
    }

    # Default rate test
    nA_d = mA['n']
    pA_d = mA['default_rate']
    nB_d = mB['n']
    pB_d = mB['default_rate']

    default_test = two_proportion_ztest(nA_d, pA_d, nB_d, pB_d)
    default_ci = confidence_interval_diff(nA_d, pA_d, nB_d, pB_d)

    results['default_rate'] = {
        'z_statistic': float(round(default_test['z_statistic'], 4)),
        'p_value': float(round(default_test['p_value'], 6)),
        'ci_lower': float(round(default_ci[0], 4)),
        'ci_upper': float(round(default_ci[1], 4)),
        'significant': bool(default_test['p_value'] < 0.05),
        'treatment_effect': float(round(pB_d - pA_d, 4))
    }

    # Power analysis
    n_half = nA
    mde = minimum_detectable_effect(n_half)

    results['power_analysis'] = {
        'sample_size_per_group': int(n_half),
        'minimum_detectable_effect': float(round(mde, 4)),
        'power_at_mde': float(round(statistical_power(n_half, pA, pA + mde), 3))
    }

    return results
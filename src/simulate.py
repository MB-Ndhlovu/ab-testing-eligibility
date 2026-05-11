"""Run A/B test experiment simulation."""

import numpy as np
from .data_generator import generate_data, compute_metrics
from .statistical import two_proportion_ztest, statistical_power, minimum_detectable_effect, test_significance

def run_experiment(n=5000, seed=42):
    """
    Run the full A/B test experiment.

    Parameters
    ----------
    n : int
        Sample size per group
    seed : int
        Random seed

    Returns
    -------
    dict
        Complete experiment results
    """
    # Generate data
    data = generate_data(n=n, seed=seed)

    # Compute metrics
    metrics = compute_metrics(data)

    n_a = metrics['group_a']['n']
    n_b = metrics['group_b']['n']

    # Get proportions for statistical tests
    p_approval_a = metrics['group_a']['approval_rate']
    p_approval_b = metrics['group_b']['approval_rate']

    # Default rate is among approved applications
    p_default_a = metrics['group_a']['default_rate']
    p_default_b = metrics['group_b']['default_rate']

    # Run z-tests
    approval_test = two_proportion_ztest(n_a, p_approval_a, n_b, p_approval_b)
    approval_test['significance'] = test_significance(approval_test['p_value'])

    default_test = two_proportion_ztest(n_a, p_default_a, n_b, p_default_b)
    default_test['significance'] = test_significance(default_test['p_value'])

    # Power analysis
    # Expected based on true parameters
    expected_power_approval = statistical_power(n, 0.62, 0.71)
    mde_approval = minimum_detectable_effect(n, power=0.8, p1=0.62)

    expected_power_default = statistical_power(n, 0.11, 0.09)
    mde_default = minimum_detectable_effect(n, power=0.8, p1=0.11)

    return {
        'n_per_group': n,
        'metrics': metrics,
        'approval_test': {
            **approval_test,
            'p1': p_approval_a,
            'p2': p_approval_b,
            'effect': p_approval_b - p_approval_a,
            'mde': mde_approval,
            'expected_power': expected_power_approval,
        },
        'default_test': {
            **default_test,
            'p1': p_default_a,
            'p2': p_default_b,
            'effect': p_default_b - p_default_a,
            'mde': mde_default,
            'expected_power': expected_power_default,
        },
        'observed_power_approval': statistical_power(n, p_approval_a, p_approval_b),
        'observed_power_default': statistical_power(n, p_default_a, p_default_b),
    }

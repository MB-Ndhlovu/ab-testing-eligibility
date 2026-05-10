import pandas as pd
from src.data_generator import generate_loan_data, compute_group_stats
from src.statistical import two_proportion_z_test, compute_power, minimum_detectable_effect
from dataclasses import dataclass, asdict
from typing import Dict, Any


@dataclass
class ExperimentResult:
    """Results from the A/B experiment simulation."""
    metric_name: str
    control_rate: float
    treatment_rate: float
    treatment_effect: float
    z_statistic: float
    p_value: float
    ci_lower: float
    ci_upper: float
    significant: bool
    power: float
    mde: float


def run_experiment(
    n: int = 5000,
    seed: int = 42
) -> Dict[str, Any]:
    """
    Run the full A/B experiment simulation.

    Args:
        n: Total sample size
        seed: Random seed

    Returns:
        Dictionary containing results and metadata
    """
    # Generate data
    df = generate_loan_data(n=n, seed=seed)
    stats = compute_group_stats(df)

    # Extract counts
    n_a = stats['A']['n']
    n_b = stats['B']['n']

    # Approval rate test
    approval_result = two_proportion_z_test(
        control_successes=int(stats['A']['approval_rate'] * n_a),
        control_total=n_a,
        treatment_successes=int(stats['B']['approval_rate'] * n_b),
        treatment_total=n_b
    )

    # Default rate test (on approved subset)
    default_result = two_proportion_z_test(
        control_successes=int(stats['A']['default_rate'] * stats['A']['approval_rate'] * n_a),
        control_total=int(stats['A']['approval_rate'] * n_a),
        treatment_successes=int(stats['B']['default_rate'] * stats['B']['approval_rate'] * n_b),
        treatment_total=int(stats['B']['approval_rate'] * n_b)
    )

    # Power and MDE for approval rate
    power_approval = compute_power(
        p1=stats['A']['approval_rate'],
        p2=stats['B']['approval_rate'],
        n1=n_a,
        n2=n_b
    )
    mde_approval = minimum_detectable_effect(n_a, n_b, stats['A']['approval_rate'])

    # Power and MDE for default rate
    n_approved_a = int(stats['A']['approval_rate'] * n_a)
    n_approved_b = int(stats['B']['approval_rate'] * n_b)

    power_default = compute_power(
        p1=stats['A']['default_rate'],
        p2=stats['B']['default_rate'],
        n1=n_approved_a,
        n2=n_approved_b
    )
    mde_default = minimum_detectable_effect(n_approved_a, n_approved_b, stats['A']['default_rate'])

    results = {
        'metadata': {
            'n_total': n,
            'n_control': n_a,
            'n_treatment': n_b,
            'seed': seed
        },
        'approval_rate': {
            'control': stats['A']['approval_rate'],
            'treatment': stats['B']['approval_rate'],
            'treatment_effect': stats['B']['approval_rate'] - stats['A']['approval_rate'],
            'z_statistic': approval_result.z_statistic,
            'p_value': approval_result.p_value,
            'ci_95': [approval_result.ci_lower, approval_result.ci_upper],
            'significant': approval_result.significant,
            'power': power_approval,
            'mde': mde_approval
        },
        'default_rate': {
            'control': stats['A']['default_rate'],
            'treatment': stats['B']['default_rate'],
            'treatment_effect': stats['B']['default_rate'] - stats['A']['default_rate'],
            'z_statistic': default_result.z_statistic,
            'p_value': default_result.p_value,
            'ci_95': [default_result.ci_lower, default_result.ci_upper],
            'significant': default_result.significant,
            'power': power_default,
            'mde': mde_default
        },
        'group_stats': {
            'A': stats['A'],
            'B': stats['B']
        }
    }

    return results


if __name__ == '__main__':
    import json
    results = run_experiment()
    print(json.dumps(results, indent=2, default=lambda x: float(x) if hasattr(x, '__float__') else x))
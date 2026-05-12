from src.data_generator import generate_credit_data, compute_group_stats
from src.statistical import two_proportion_ztest, minimum_detectable_effect, statistical_power

def run_simulation(n=5000, seed=42):
    """Run the full A/B test experiment simulation.

    Args:
        n: Total sample size
        seed: Random seed

    Returns:
        dict with experiment results
    """
    # Generate data
    df = generate_credit_data(n=n, seed=seed)
    stats = compute_group_stats(df)

    n_a = stats['A']['n']
    n_b = stats['B']['n']
    p_approval_A = stats['A']['approval_rate']
    p_approval_B = stats['B']['approval_rate']
    p_default_A = stats['A']['default_rate']
    p_default_B = stats['B']['default_rate']

    # Test approval rate (Group B - Group A)
    approval_test = two_proportion_ztest(n_a, p_approval_A, n_b, p_approval_B)

    # Test default rate (Group B - Group A)
    default_test = two_proportion_ztest(n_a, p_default_A, n_b, p_default_B)

    # Calculate MDE
    mde_approval = minimum_detectable_effect(n_a, p1=p_approval_A, p2=p_approval_B)
    mde_default = minimum_detectable_effect(n_a, p1=p_default_A, p2=p_default_B)

    # Calculate observed effects
    effect_approval = p_approval_B - p_approval_A
    effect_default = p_default_B - p_default_A

    results = {
        'n_A': n_a,
        'n_B': n_b,
        'approval': {
            'rate_A': p_approval_A,
            'rate_B': p_approval_B,
            'effect': effect_approval,
            'mde': mde_approval,
            'z_statistic': approval_test['z_statistic'],
            'p_value': approval_test['p_value'],
            'ci_95': approval_test['ci_95'],
            'significant': approval_test['significant']
        },
        'default': {
            'rate_A': p_default_A,
            'rate_B': p_default_B,
            'effect': effect_default,
            'mde': mde_default,
            'z_statistic': default_test['z_statistic'],
            'p_value': default_test['p_value'],
            'ci_95': default_test['ci_95'],
            'significant': default_test['significant']
        },
        'avg_loan_size': {
            'A': stats['A']['avg_loan_size'],
            'B': stats['B']['avg_loan_size']
        },
        'avg_processing_time': {
            'A': stats['A']['avg_processing_time'],
            'B': stats['B']['avg_processing_time']
        }
    }

    return results

if __name__ == '__main__':
    results = run_simulation()
    print(f"Approval effect: {results['approval']['effect']:.4f}, p={results['approval']['p_value']:.6f}")
    print(f"Default effect: {results['default']['effect']:.4f}, p={results['default']['p_value']:.6f}")
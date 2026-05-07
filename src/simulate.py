"""
Runs the A/B experiment simulation and computes treatment effects and significance.
"""

from src.data_generator import generate_data, compute_group_stats
from src.statistical import two_proportion_ztest


def run_simulation(seed=42):
    """
    Run the full A/B experiment simulation.

    Args:
        seed: Random seed for reproducibility

    Returns:
        dict with full results: data, stats, test results, summary
    """
    data = generate_data(n=5000, seed=seed)
    stats = compute_group_stats(data)

    n_a = stats['A']['n']
    n_b = stats['B']['n']

    # Test approval rate
    approval_test = two_proportion_ztest(
        n_control=n_a,
        p_control=stats['A']['approval_rate'],
        n_treatment=n_b,
        p_treatment=stats['B']['approval_rate']
    )

    # Test default rate
    default_test = two_proportion_ztest(
        n_control=n_a,
        p_control=stats['A']['default_rate'],
        n_treatment=n_b,
        p_treatment=stats['B']['default_rate']
    )

    results = {
        'data': data,
        'stats': stats,
        'tests': {
            'approval_rate': approval_test,
            'default_rate': default_test
        },
        'meta': {
            'n_total': 5000,
            'n_per_group': 2500,
            'alpha': 0.05
        }
    }

    return results


def format_test_result(metric_name, test_result, rate_a, rate_b):
    """Format a single test result for reporting."""
    diff = rate_b - rate_a
    direction = "higher" if diff > 0 else "lower"
    sig_word = "SIGNIFICANT" if test_result['significant'] else "not significant"

    return {
        'metric': metric_name,
        'rate_A': rate_a,
        'rate_B': rate_b,
        'difference': diff,
        'direction': direction,
        'z_statistic': test_result['z_statistic'],
        'p_value': test_result['p_value'],
        'ci_95_lower': test_result['ci_95'][0],
        'ci_95_upper': test_result['ci_95'][1],
        'significant': test_result['significant'],
        'conclusion': f"Group B is {direction} than Group A ({sig_word} at α=0.05)"
    }


if __name__ == '__main__':
    results = run_simulation()
    print("=== A/B Simulation Results ===")
    print(f"\nGroups:")
    print(f"  A (control): n={results['stats']['A']['n']}")
    print(f"  B (treatment): n={results['stats']['B']['n']}")

    for metric in ['approval_rate', 'default_rate']:
        tr = results['tests'][metric]
        ra = results['stats']['A'][metric]
        rb = results['stats']['B'][metric]
        fmt = format_test_result(metric, tr, ra, rb)
        print(f"\n--- {metric.upper().replace('_', ' ')} ---")
        print(f"  Group A: {ra:.4f}  |  Group B: {rb:.4f}")
        print(f"  Difference: {fmt['difference']:+.4f}")
        print(f"  z-statistic: {tr['z_statistic']:.4f}")
        print(f"  p-value: {tr['p_value']:.6f}")
        print(f"  95% CI: ({tr['ci_95'][0]:.4f}, {tr['ci_95'][1]:.4f})")
        print(f"  Conclusion: {fmt['conclusion']}")
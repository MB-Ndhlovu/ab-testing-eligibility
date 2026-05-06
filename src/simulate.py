"""Run A/B test simulation and compute treatment effects."""

import json
from src.data_generator import generate_loan_data, compute_group_metrics
from src.statistical import run_statistical_analysis


def run_experiment(n=5000, seed=42, alpha=0.05):
    """
    Run a complete A/B experiment.

    Args:
        n: Total sample size
        seed: Random seed
        alpha: Significance level

    Returns:
        dict with data, metrics, and statistical results
    """
    # Generate data
    df = generate_loan_data(n=n, seed=seed)

    # Compute group metrics
    metrics = compute_group_metrics(df)

    # Run statistical analysis
    stats_results = run_statistical_analysis(
        metrics['A'], metrics['B'], alpha=alpha
    )

    # Compute treatment effect summary
    treatment_effect = {
        'approval_rate_lift': metrics['B']['approval_rate'] - metrics['A']['approval_rate'],
        'default_rate_lift': metrics['B']['default_rate'] - metrics['A']['default_rate'],
        'avg_loan_size_A': metrics['A']['avg_loan_size'],
        'avg_loan_size_B': metrics['B']['avg_loan_size'],
        'avg_processing_time_A': metrics['A']['avg_processing_time'],
        'avg_processing_time_B': metrics['B']['avg_processing_time']
    }

    return {
        'n': n,
        'seed': seed,
        'alpha': alpha,
        'metrics': metrics,
        'stats': stats_results,
        'treatment_effect': treatment_effect
    }


def summarize_results(results):
    """Print a readable summary of experiment results."""
    print("=" * 70)
    print("A/B TESTING FRAMEWORK FOR CREDIT ELIGIBILITY")
    print("=" * 70)

    print("\n--- SAMPLE METRICS ---")
    print(f"Total sample size: {results['n']}")
    print(f"Control group (A): n={results['metrics']['A']['n']}")
    print(f"Treatment group (B): n={results['metrics']['B']['n']}")

    print("\n--- GROUP SUMMARY ---")
    print(f"{'Metric':<25} {'Group A (Control)':<22} {'Group B (Treatment)':<22}")
    print("-" * 70)

    a = results['metrics']['A']
    b = results['metrics']['B']

    print(f"{'Approvals':<25} {a['approved_count']}/{a['n']} ({a['approval_rate']:.4f})    {b['approved_count']}/{b['n']} ({b['approval_rate']:.4f})")
    print(f"{'Default Rate':<25} {a['default_rate']:.4f}              {b['default_rate']:.4f}")
    print(f"{'Avg Loan Size ($k)':<25} {a['avg_loan_size']:<22.2f} {b['avg_loan_size']:<22.2f}")
    print(f"{'Avg Processing (min)':<25} {a['avg_processing_time']:<22.2f} {b['avg_processing_time']:<22.2f}")

    print("\n--- APPROVAL RATE TEST ---")
    ap = results['stats']['approval']
    print(f"Control rate:     {ap['control_rate']:.4f}")
    print(f"Treatment rate:   {ap['treatment_rate']:.4f}")
    print(f"Difference:       {ap['diff']:.4f}")
    print(f"95% CI:          [{ap['ci_lower']:.4f}, {ap['ci_upper']:.4f}]")
    print(f"Z-statistic:      {ap['z_statistic']:.4f}")
    print(f"P-value:          {ap['p_value']:.6f}")
    print(f"Significant:      {'YES' if ap['significant'] else 'NO'} (α={results['alpha']})")
    print(f"Power:            {ap['power']:.4f}")
    print(f"MDE:              {ap['mde']:.4f}")

    print("\n--- DEFAULT RATE TEST ---")
    dp = results['stats']['default']
    print(f"Control rate:     {dp['control_rate']:.4f}")
    print(f"Treatment rate:   {dp['treatment_rate']:.4f}")
    print(f"Difference:       {dp['diff']:.4f}")
    print(f"95% CI:          [{dp['ci_lower']:.4f}, {dp['ci_upper']:.4f}]")
    print(f"Z-statistic:      {dp['z_statistic']:.4f}")
    print(f"P-value:          {dp['p_value']:.6f}")
    print(f"Significant:      {'YES' if dp['significant'] else 'NO'} (α={results['alpha']})")

    print("\n--- TREATMENT EFFECTS ---")
    te = results['treatment_effect']
    print(f"Approval rate lift:   {te['approval_rate_lift']:+.4f} ({te['approval_rate_lift']*100:+.2f}%)")
    print(f"Default rate lift:    {te['default_rate_lift']:+.4f} ({te['default_rate_lift']*100:+.2f}%)")

    print("\n--- CONCLUSION ---")
    approval_sig = results['stats']['approval']['significant']
    default_sig = results['stats']['default']['significant']

    if approval_sig and default_sig:
        print("The new model (B) significantly outperforms the current model (A)")
        print("on BOTH approval rate AND default rate. RECOMMEND DEPLOYMENT.")
    elif approval_sig:
        print("The new model (B) shows significantly higher approval rate,")
        print("but default rate difference is not statistically significant.")
    elif default_sig:
        print("The new model (B) shows significantly lower default rate,")
        print("but approval rate difference is not statistically significant.")
    else:
        print("No statistically significant difference detected between models.")
        print("More data may be needed.")

    print("=" * 70)

    return results


def save_results(results, filepath='experiment_results.json'):
    """Save results to JSON file."""
    # Convert any non-serializable types
    serializable = {
        'n': results['n'],
        'seed': results['seed'],
        'alpha': results['alpha'],
        'metrics': {
            group: {
                key: float(val) if isinstance(val, (float, np.floating)) else val
                for key, val in metrics.items()
            }
            for group, metrics in results['metrics'].items()
        },
        'stats': results['stats'],
        'treatment_effect': results['treatment_effect']
    }

    with open(filepath, 'w') as f:
        json.dump(serializable, f, indent=2, default=str)

    print(f"\nResults saved to {filepath}")


if __name__ == '__main__':
    import numpy as np

    results = run_experiment()
    summarize_results(results)
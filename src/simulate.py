"""Run A/B experiment simulation."""

from src.data_generator import generate_all_data
from src.statistical import analyze_metric


def run_experiment():
    """Execute full experiment: generate data, compute metrics, run statistics."""

    metrics_a, metrics_b = generate_all_data()

    print("=" * 60)
    print("A/B TEST EXPERIMENT — CREDIT ELIGIBILITY")
    print("=" * 60)

    print("\n[DATA GENERATION]")
    print(f"  Group A (Control): n={metrics_a['n']}")
    print(f"  Group B (Treatment): n={metrics_b['n']}")

    print("\n[RAW METRICS]")
    print(f"  {'Metric':<20} {'Group A':>12} {'Group B':>12} {'Effect':>12}")
    print(f"  {'-'*20} {'-'*12} {'-'*12} {'-'*12}")

    for key in ['approval_rate', 'default_rate', 'avg_loan_size', 'avg_processing_time']:
        v1 = metrics_a[key]
        v2 = metrics_b[key]
        eff = v2 - v1
        print(f"  {key:<20} {v1:>12.4f} {v2:>12.4f} {eff:>+12.4f}")

    print("\n[STATISTICAL ANALYSIS]")
    results = {}

    for metric in ['approval_rate', 'default_rate']:
        result = analyze_metric(metrics_a, metrics_b, metric)
        results[metric] = result

        print(f"\n  --- {metric.upper()} ---")
        print(f"  Group A: {result['group_a_value']:.4f}")
        print(f"  Group B: {result['group_b_value']:.4f}")
        print(f"  Treatment Effect: {result['treatment_effect']:+.4f}")
        print(f"  z-statistic: {result['z_statistic']:.4f}")
        print(f"  p-value: {result['p_value']:.6f}")
        print(f"  95% CI: [{result['ci_95'][0]:.4f}, {result['ci_95'][1]:.4f}]")
        sig_word = "SIGNIFICANT" if result['significant'] else "NOT SIGNIFICANT"
        print(f"  Conclusion (α=0.05): {sig_word}")

    summary = {
        'metrics_a': metrics_a,
        'metrics_b': metrics_b,
        'approval_rate_test': results['approval_rate'],
        'default_rate_test': results['default_rate']
    }

    return summary


if __name__ == '__main__':
    results = run_experiment()
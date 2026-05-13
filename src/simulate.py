"""Run A/B experiment simulation and compute treatment effects."""

from src.data_generator import generate_experiment_data, compute_group_stats
from src.statistical import analyze_metric


def run_simulation():
    """
    Run the complete A/B test simulation.

    Returns
    -------
    dict
        Contains group stats and statistical analysis results
    """
    data = generate_experiment_data()

    group_stats = compute_group_stats(data)

    approval_analysis = analyze_metric(
        data,
        metric_col='approval_rate',
        group_col='group'
    )

    default_analysis = analyze_metric(
        data,
        metric_col='defaulted',
        group_col='group'
    )

    group_a = data[data['group'] == 'A']
    group_b = data[data['group'] == 'B']

    approved_a = group_a[group_a['approved']]
    approved_b = group_b[group_b['approved']]

    results = {
        'experiment': {
            'n_total': len(data),
            'n_per_group': 2500,
            'alpha': 0.05
        },
        'group_stats': group_stats,
        'metrics': {
            'approval_rate': approval_analysis,
            'default_rate': default_analysis
        },
        'loan_size': {
            'group_a_avg': approved_a['loan_size'].mean() if len(approved_a) > 0 else 0,
            'group_b_avg': approved_b['loan_size'].mean() if len(approved_b) > 0 else 0
        },
        'processing_time': {
            'group_a_avg': group_a['processing_time'].mean(),
            'group_b_avg': group_b['processing_time'].mean()
        }
    }

    return results


def print_results(results):
    """Print a readable summary of results."""
    print("=" * 60)
    print("A/B TESTING FRAMEWORK — CREDIT ELIGIBILITY")
    print("=" * 60)

    print("\n[Experiment Design]")
    print(f"  Total applicants: {results['experiment']['n_total']}")
    print(f"  Per group: {results['experiment']['n_per_group']}")
    print(f"  Significance level (alpha): {results['experiment']['alpha']}")

    print("\n[Group Statistics]")
    for group in ['A', 'B']:
        s = results['group_stats'][group]
        print(f"\n  Group {group} ({'Control' if group == 'A' else 'Treatment'}):")
        print(f"    Applications: {s['n']}")
        print(f"    Approved: {s['approvals']} ({s['approval_rate']*100:.2f}%)")
        print(f"    Defaults: {s['defaults']} ({s['default_rate']*100:.2f}%)")
        print(f"    Avg loan size: ${s['avg_loan_size']:,.2f}")
        print(f"    Avg processing time: {s['avg_processing_time']:.2f} hrs")

    print("\n[Approval Rate Analysis]")
    ar = results['metrics']['approval_rate']
    print(f"  Group A (control): {ar['group_a_rate']*100:.2f}%")
    print(f"  Group B (treatment): {ar['group_b_rate']*100:.2f}%")
    print(f"  Absolute difference: {ar['absolute_diff']*100:.2f}%")
    print(f"  Relative difference: {ar['relative_diff']*100:.2f}%")
    print(f"  Z-statistic: {ar['z_statistic']:.4f}")
    print(f"  P-value: {ar['p_value']:.6f}")
    print(f"  95% CI: [{ar['ci_95_lower']*100:.2f}%, {ar['ci_95_upper']*100:.2f}%]")
    print(f"  Significant: {'YES' if ar['significant'] else 'NO'}")

    print("\n[Default Rate Analysis]")
    dr = results['metrics']['default_rate']
    print(f"  Group A (control): {dr['group_a_rate']*100:.2f}%")
    print(f"  Group B (treatment): {dr['group_b_rate']*100:.2f}%")
    print(f"  Absolute difference: {dr['absolute_diff']*100:.2f}%")
    print(f"  Relative difference: {dr['relative_diff']*100:.2f}%")
    print(f"  Z-statistic: {dr['z_statistic']:.4f}")
    print(f"  P-value: {dr['p_value']:.6f}")
    print(f"  95% CI: [{dr['ci_95_lower']*100:.2f}%, {dr['ci_95_upper']*100:.2f}%]")
    print(f"  Significant: {'YES' if dr['significant'] else 'NO'}")

    print("\n[Power Analysis]")
    print(f"  Approval rate power: {ar['power']:.4f}")
    print(f"  Default rate power: {dr['power']:.4f}")
    print(f"  Min detectable effect (approval): {ar['mde']*100:.2f}%")
    print(f"  Min detectable effect (default): {dr['mde']*100:.2f}%")

    print("\n[Loan Size & Processing Time]")
    print(f"  Avg loan size - Group A: ${results['loan_size']['group_a_avg']:,.2f}")
    print(f"  Avg loan size - Group B: ${results['loan_size']['group_b_avg']:,.2f}")
    print(f"  Avg processing time - Group A: {results['processing_time']['group_a_avg']:.2f} hrs")
    print(f"  Avg processing time - Group B: {results['processing_time']['group_b_avg']:.2f} hrs")

    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)

    ar_sig = ar['significant']
    dr_sig = dr['significant']

    if ar_sig and not dr_sig:
        print("  Group B (new model) significantly improves approval rate")
        print("  without increasing default rate. RECOMMEND ADOPTION.")
    elif ar_sig and dr_sig and ar['absolute_diff'] > 0 and dr['absolute_diff'] < 0:
        print("  Group B improves both metrics significantly. STRONG RECOMMENDATION.")
    elif ar_sig and dr_sig and dr['absolute_diff'] > 0:
        print("  Group B increases approval rate BUT also increases default rate.")
        print("  CAUTION — further analysis needed.")
    elif not ar_sig:
        print("  No statistically significant difference in approval rate detected.")
        print("  Consider larger sample size or different eligibility criteria.")

    print("=" * 60)


if __name__ == '__main__':
    results = run_simulation()
    print_results(results)
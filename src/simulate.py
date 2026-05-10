"""Run A/B test experiment simulation and compute treatment effects."""
from src.data_generator import generate_data, compute_group_stats
from src.statistical import two_proportion_ztest, statistical_power, minimum_detectable_effect


def run_experiment(n=5000, alpha=0.05):
    """Run a complete A/B experiment.

    Args:
        n: Sample size per group
        alpha: Significance level

    Returns:
        dict with experiment results
    """
    # Generate data
    df = generate_data(n)
    stats = compute_group_stats(df)

    group_a = stats['A']
    group_b = stats['B']

    # Compute approval rate test
    approval_test = two_proportion_ztest(
        group_a['n'], int(group_a['approval_rate'] * group_a['n']),
        group_b['n'], int(group_b['approval_rate'] * group_b['n'])
    )

    # Compute default rate test (among approved only)
    n_default_a = int(group_a['default_rate'] * group_a['approval_rate'] * group_a['n'])
    n_default_b = int(group_b['default_rate'] * group_b['approval_rate'] * group_b['n'])
    n_approved_a = int(group_a['approval_rate'] * group_a['n'])
    n_approved_b = int(group_b['approval_rate'] * group_b['n'])

    default_test = two_proportion_ztest(
        n_approved_a, n_default_a,
        n_approved_b, n_default_b
    )

    # Compute power and MDE for approval rate
    power = statistical_power(n, group_a['approval_rate'], group_b['approval_rate'], alpha)
    mde = minimum_detectable_effect(n, power=0.8, alpha=alpha, p1=group_a['approval_rate'])

    # Treatment effect
    treatment_effect_approval = group_b['approval_rate'] - group_a['approval_rate']
    treatment_effect_default = group_b['default_rate'] - group_a['default_rate']

    return {
        'sample_size': n,
        'alpha': alpha,
        'group_a': group_a,
        'group_b': group_b,
        'approval_rate_test': approval_test,
        'default_rate_test': default_test,
        'treatment_effect': {
            'approval_rate': round(treatment_effect_approval, 6),
            'default_rate': round(treatment_effect_default, 6)
        },
        'power': power,
        'mde': mde
    }


def summarize_results(results):
    """Create a human-readable summary of the experiment results."""
    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING FRAMEWORK FOR CREDIT ELIGIBILITY")
    lines.append("=" * 60)
    lines.append("")
    lines.append("EXPERIMENT CONFIGURATION")
    lines.append(f"  Sample size per group: {results['sample_size']:,}")
    lines.append(f"  Significance level (α): {results['alpha']}")
    lines.append(f"  Statistical power: {min(results['power'], 1.0):.2%}")
    lines.append(f"  Min detectable effect: {results['mde']:.4f}")
    lines.append("")

    lines.append("GROUP-LEVEL METRICS")
    lines.append(f"  {'Metric':<20} {'Group A (Control)':<22} {'Group B (Treatment)':<22}")
    lines.append("-" * 64)
    lines.append(f"  {'Approval Rate':<20} {results['group_a']['approval_rate']:.4f}{'':>14} {results['group_b']['approval_rate']:.4f}")
    lines.append(f"  {'Default Rate':<20} {results['group_a']['default_rate']:.4f}{'':>14} {results['group_b']['default_rate']:.4f}")
    lines.append(f"  {'Avg Loan Size':<20} R{results['group_a']['avg_loan_size']:,.2f}{'':>11} R{results['group_b']['avg_loan_size']:,.2f}")
    lines.append(f"  {'Avg Processing Time':<20} {results['group_a']['avg_processing_time']:.2f} min{'':>8} {results['group_b']['avg_processing_time']:.2f} min")
    lines.append("")

    lines.append("APPROVAL RATE ANALYSIS (Primary Metric)")
    lines.append(f"  Treatment effect: {results['treatment_effect']['approval_rate']:+.4f}")
    lines.append(f"  Z-statistic: {results['approval_rate_test']['z_statistic']:.4f}")
    lines.append(f"  P-value: {results['approval_rate_test']['p_value']:.6f}")
    lines.append(f"  95% CI: [{results['approval_rate_test']['ci_95_lower']:.4f}, {results['approval_rate_test']['ci_95_upper']:.4f}]")
    sig_label = "SIGNIFICANT" if results['approval_rate_test']['significant'] else "NOT SIGNIFICANT"
    lines.append(f"  Conclusion: {sig_label} at α={results['alpha']}")
    lines.append("")

    lines.append("DEFAULT RATE ANALYSIS (Safety Metric)")
    lines.append(f"  Treatment effect: {results['treatment_effect']['default_rate']:+.4f}")
    lines.append(f"  Z-statistic: {results['default_rate_test']['z_statistic']:.4f}")
    lines.append(f"  P-value: {results['default_rate_test']['p_value']:.6f}")
    lines.append(f"  95% CI: [{results['default_rate_test']['ci_95_lower']:.4f}, {results['default_rate_test']['ci_95_upper']:.4f}]")
    sig_label = "SIGNIFICANT" if results['default_rate_test']['significant'] else "NOT SIGNIFICANT"
    lines.append(f"  Conclusion: {sig_label} at α={results['alpha']}")
    lines.append("")
    lines.append("=" * 60)

    return "\n".join(lines)


if __name__ == '__main__':
    results = run_experiment()
    print(summarize_results(results))
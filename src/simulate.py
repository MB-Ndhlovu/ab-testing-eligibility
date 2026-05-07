"""
Run A/B test experiment simulation.
"""

import numpy as np
from scipy import stats
from src.data_generator import generate_data, compute_group_stats
from src.statistical import two_proportion_z_test, compute_statistical_power, minimum_detectable_effect


def run_experiment(n=5000, seed=42, alpha=0.05):
    """
    Run the full A/B experiment.

    Parameters:
        n: total number of applicants
        seed: random seed
        alpha: significance level

    Returns:
        dict with all experiment results
    """
    # Generate data
    df = generate_data(n=n, seed=seed)

    # Compute group statistics
    group_stats = compute_group_stats(df)

    # Prepare results
    results = {
        'sample_size': {'A': group_stats['A']['n_total'], 'B': group_stats['B']['n_total']},
        'approval_rate': {
            'A': group_stats['A']['approval_rate'],
            'B': group_stats['B']['approval_rate'],
        },
        'default_rate': {
            'A': group_stats['A']['default_rate'],
            'B': group_stats['B']['default_rate'],
        },
        'avg_loan_amount': {
            'A': group_stats['A']['avg_loan_amount'],
            'B': group_stats['B']['avg_loan_amount'],
        },
        'avg_processing_time': {
            'A': group_stats['A']['avg_processing_time'],
            'B': group_stats['B']['avg_processing_time'],
        },
        'tests': {},
        'power_analysis': {},
    }

    # Two-proportion z-test for approval rate
    approval_test = two_proportion_z_test(
        n_A=group_stats['A']['n_total'],
        x_A=group_stats['A']['n_approved'],
        n_B=group_stats['B']['n_total'],
        x_B=group_stats['B']['n_approved'],
    )
    results['tests']['approval_rate'] = approval_test

    # Two-proportion z-test for default rate
    default_test = two_proportion_z_test(
        n_A=group_stats['A']['n_approved'],
        x_A=int(df[df['group'] == 'A']['defaulted'].sum()),
        n_B=group_stats['B']['n_approved'],
        x_B=int(df[df['group'] == 'B']['defaulted'].sum()),
    )
    results['tests']['default_rate'] = default_test

    # Power analysis
    n_per_group = n // 2
    mde_approval = abs(group_stats['B']['approval_rate'] - group_stats['A']['approval_rate'])
    mde_default = abs(group_stats['B']['default_rate'] - group_stats['A']['default_rate'])

    results['power_analysis'] = {
        'approval_rate': {
            'mde': mde_approval,
            'power': compute_statistical_power(n_per_group, group_stats['A']['approval_rate'], mde_approval, alpha),
        },
        'default_rate': {
            'mde': mde_default,
            'power': compute_statistical_power(n_per_group, group_stats['A']['default_rate'], mde_default, alpha),
        },
        'sample_size_needed_80_power': {
            'approval_rate': compute_sample_size_needed(group_stats['A']['approval_rate'], mde_approval, 0.8, alpha),
            'default_rate': compute_sample_size_needed(group_stats['A']['default_rate'], mde_default, 0.8, alpha),
        },
    }

    return results


def compute_sample_size_needed(p_A, mde, power=0.8, alpha=0.05):
    """
    Compute sample size needed per group.
    """
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    p_B = p_A + mde
    p_pooled = (p_A + p_B) / 2

    se = np.sqrt(2 * p_pooled * (1 - p_pooled))
    n = ((z_crit + z_beta) / (mde / se)) ** 2

    return int(np.ceil(n))


def format_results(results):
    """Format results for display."""
    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING RESULTS - CREDIT ELIGIBILITY MODEL")
    lines.append("=" * 60)

    lines.append("\n--- Sample Summary ---")
    lines.append(f"Group A (Control):  n = {results['sample_size']['A']}")
    lines.append(f"Group B (Treatment): n = {results['sample_size']['B']}")

    lines.append("\n--- Group Statistics ---")
    lines.append(f"{'Metric':<25} {'Group A':>12} {'Group B':>12} {'Difference':>12}")
    lines.append("-" * 65)

    for metric in ['approval_rate', 'default_rate', 'avg_loan_amount', 'avg_processing_time']:
        val_A = results[metric]['A']
        val_B = results[metric]['B']
        diff = val_B - val_A
        metric_name = metric.replace('_', ' ').title()
        lines.append(f"{metric_name:<25} {val_A:>12.4f} {val_B:>12.4f} {diff:>+12.4f}")

    lines.append("\n--- Approval Rate Test (Two-Proportion Z-Test) ---")
    test = results['tests']['approval_rate']
    lines.append(f"  Group A rate: {test['p_A']:.4f}")
    lines.append(f"  Group B rate: {test['p_B']:.4f}")
    lines.append(f"  Difference:   {test['difference']:+.4f}")
    lines.append(f"  Z-statistic:   {test['z_statistic']:.4f}")
    lines.append(f"  P-value:       {test['p_value']:.6f}")
    lines.append(f"  95% CI:        [{test['ci_95_lower']:.4f}, {test['ci_95_upper']:.4f}]")
    sig_text = "SIGNIFICANT" if test['significant'] else "NOT SIGNIFICANT"
    lines.append(f"  Conclusion:    {sig_text} at α=0.05")

    lines.append("\n--- Default Rate Test (Two-Proportion Z-Test) ---")
    test = results['tests']['default_rate']
    lines.append(f"  Group A rate: {test['p_A']:.4f}")
    lines.append(f"  Group B rate: {test['p_B']:.4f}")
    lines.append(f"  Difference:   {test['difference']:+.4f}")
    lines.append(f"  Z-statistic:   {test['z_statistic']:.4f}")
    lines.append(f"  P-value:       {test['p_value']:.6f}")
    lines.append(f"  95% CI:        [{test['ci_95_lower']:.4f}, {test['ci_95_upper']:.4f}]")
    sig_text = "SIGNIFICANT" if test['significant'] else "NOT SIGNIFICANT"
    lines.append(f"  Conclusion:    {sig_text} at α=0.05")

    lines.append("\n--- Power Analysis ---")
    for metric in ['approval_rate', 'default_rate']:
        pa = results['power_analysis'][metric]
        lines.append(f"  {metric.title()}:")
        lines.append(f"    MDE: {pa['mde']:.4f}")
        lines.append(f"    Power: {pa['power']:.4f}")

    lines.append("\n" + "=" * 60)
    lines.append("FINAL RECOMMENDATION")
    lines.append("=" * 60)

    approval_sig = results['tests']['approval_rate']['significant']
    default_sig = results['tests']['default_rate']['significant']
    approval_diff = results['tests']['approval_rate']['difference']
    default_diff = results['tests']['default_rate']['difference']

    if approval_sig and default_sig:
        if approval_diff > 0 and default_diff < 0:
            lines.append("ADOPT the new model (Group B) - it significantly improves")
            lines.append("approval rate AND reduces default rate.")
        elif approval_diff > 0:
            lines.append("CAUTION: Approval rate improved but default rate worsened.")
            lines.append("Further analysis recommended before adoption.")
        else:
            lines.append("Mixed results - review required.")
    elif approval_sig:
        lines.append("Approval rate significantly improved. Default rate change is")
        lines.append("not statistically significant. Consider adoption with monitoring.")
    elif default_sig:
        lines.append("Default rate significantly improved. Approval rate change is")
        lines.append("not statistically significant. Consider adoption with monitoring.")
    else:
        lines.append("No statistically significant differences detected at α=0.05.")
        lines.append("Consider increasing sample size for more definitive results.")

    lines.append("=" * 60)

    return "\n".join(lines)


if __name__ == '__main__':
    results = run_experiment()
    print(format_results(results))
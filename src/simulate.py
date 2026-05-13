"""Run the A/B test experiment simulation."""

from src.data_generator import generate_experiment_data, compute_group_summary
from src.statistical import analyze_metric


def run_simulation(n_per_group=5000):
    """
    Run the full A/B test experiment.

    Parameters
    ----------
    n_per_group : int
        Number of applicants per group.

    Returns
    -------
    dict
        Complete simulation results with all metrics and statistics.
    """
    group_a, group_b = generate_experiment_data(n_per_group)

    summary_a = compute_group_summary(group_a)
    summary_b = compute_group_summary(group_b)

    approval_result = analyze_metric(group_a, group_b, metric="approved", is_approval=True)

    group_a_approved = group_a[group_a["approved"]]
    group_b_approved = group_b[group_b["approved"]]

    default_result = analyze_metric(group_a, group_b, metric="defaulted", is_approval=False)

    results = {
        "n_per_group": n_per_group,
        "group_a": summary_a,
        "group_b": summary_b,
        "approval_rate_test": approval_result,
        "default_rate_test": default_result,
        "alpha": 0.05,
    }

    return results


def print_simulation_results(results):
    """Print formatted simulation results."""
    print("=" * 60)
    print("A/B TESTING FRAMEWORK - CREDIT ELIGIBILITY")
    print("=" * 60)

    print("\n📊 GROUP SUMMARIES")
    print("-" * 40)
    print(f"{'Metric':<25} {'Group A (Control)':>15} {'Group B (Treatment)':>18}")
    print("-" * 40)

    ga = results["group_a"]
    gb = results["group_b"]

    print(f"{'Sample Size':<25} {ga['n']:>15} {gb['n']:>18}")
    print(f"{'Approved Count':<25} {ga['approved_count']:>15} {gb['approved_count']:>18}")
    print(f"{'Approval Rate':<25} {ga['approval_rate']:>15.4f} {gb['approval_rate']:>18.4f}")
    print(f"{'Defaulted Count':<25} {ga['defaulted_count']:>15} {gb['defaulted_count']:>18}")
    print(f"{'Default Rate':<25} {ga['default_rate']:>15.4f} {gb['default_rate']:>18.4f}")
    print(f"{'Avg Loan Size ($)':<25} {ga['avg_loan_size']:>15,.2f} {gb['avg_loan_size']:>18,.2f}")
    print(f"{'Avg Processing (hrs)':<25} {ga['avg_processing_time_hours']:>15.2f} {gb['avg_processing_time_hours']:>18.2f}")

    print("\n📈 APPROVAL RATE TEST (Two-Proportion Z-Test)")
    print("-" * 50)
    ar = results["approval_rate_test"]
    print(f"  Group A Rate:    {ar['p1']:.4f} ({ar['n_a']:,} trials, {ar['x_a']:,} successes)")
    print(f"  Group B Rate:    {ar['p2']:.4f} ({ar['n_b']:,} trials, {ar['x_b']:,} successes)")
    print(f"  Difference:      {ar['difference']:+.4f}")
    print(f"  95% CI:          [{ar['ci_95_lower']:+.4f}, {ar['ci_95_upper']:+.4f}]")
    print(f"  Z-Statistic:     {ar['z_statistic']:.4f}")
    print(f"  P-Value:         {ar['p_value']:.6f}")
    print(f"  Significant:     {'✅ YES' if ar['significant'] else '❌ NO'} (α=0.05)")
    print(f"  Direction:       {ar['direction']} (higher is better)")

    print("\n📉 DEFAULT RATE TEST (Two-Proportion Z-Test)")
    print("-" * 50)
    dr = results["default_rate_test"]
    print(f"  Group A Rate:    {dr['p1']:.4f}")
    print(f"  Group B Rate:    {dr['p2']:.4f}")
    print(f"  Difference:      {dr['difference']:+.4f}")
    print(f"  95% CI:          [{dr['ci_95_lower']:+.4f}, {dr['ci_95_upper']:+.4f}]")
    print(f"  Z-Statistic:     {dr['z_statistic']:.4f}")
    print(f"  P-Value:         {dr['p_value']:.6f}")
    print(f"  Significant:     {'✅ YES' if dr['significant'] else '❌ NO'} (α=0.05)")
    print(f"  Direction:       {dr['direction']} (lower is better)")

    print("\n⚙️  POWER ANALYSIS")
    print("-" * 50)
    print(f"  Approval Rate Test - Power: {ar['power']:.4f}, MDE: {ar['mde']:.4f}")
    print(f"  Default Rate Test  - Power: {dr['power']:.4f}, MDE: {dr['mde']:.4f}")

    print("\n" + "=" * 60)
    print("CONCLUSION")
    print("=" * 60)

    ar_sig = "✅ SIGNIFICANT" if ar['significant'] else "❌ NOT SIGNIFICANT"
    dr_sig = "✅ SIGNIFICANT" if dr['significant'] else "❌ NOT SIGNIFICANT"

    print(f"  Approval Rate: {ar_sig} - New model {'improves' if ar['difference'] > 0 else 'worsens'} approval rate by {abs(ar['difference'])*100:.2f}%")
    print(f"  Default Rate:  {dr_sig} - New model {'reduces' if dr['difference'] < 0 else 'increases'} default rate by {abs(dr['difference'])*100:.2f}%")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    results = run_simulation()
    print_simulation_results(results)
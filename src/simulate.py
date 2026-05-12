"""Run A/B test experiment simulation."""

from src.data_generator import generate_credit_data, compute_group_stats
from src.statistical import run_ab_test


def convert_to_native(obj):
    """Convert numpy types to Python native types for JSON serialization."""
    import numpy as np
    if isinstance(obj, dict):
        return {k: convert_to_native(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_to_native(i) for i in obj]
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, (np.bool_,)):
        return bool(obj)
    elif isinstance(obj, np.ndarray):
        return obj.tolist()
    return obj


def run_experiment(seed: int = 42, n_per_group: int = 2500) -> dict:
    """Run the full A/B experiment.

    Args:
        seed: Random seed.
        n_per_group: Applicants per group.

    Returns:
        Dict with data, stats, and test results.
    """
    df = generate_credit_data(n_per_group=n_per_group, seed=seed)
    stats = compute_group_stats(df)

    results = {
        "approval_rate": run_ab_test(stats["A"], stats["B"], "approval_rate"),
        "default_rate": run_ab_test(stats["A"], stats["B"], "default_rate"),
    }

    return {
        "data": df,
        "group_stats": convert_to_native(stats),
        "test_results": convert_to_native(results),
    }


def summarize_results(experiment_output: dict) -> str:
    """Build a readable summary string from experiment results."""
    stats = experiment_output["group_stats"]
    results = experiment_output["test_results"]

    lines = []
    lines.append("=" * 60)
    lines.append("A/B TESTING — CREDIT ELIGIBILITY RESULTS")
    lines.append("=" * 60)
    lines.append("")
    lines.append("GROUP STATISTICS")
    lines.append("-" * 40)
    for group in ["A", "B"]:
        s = stats[group]
        lines.append(f"Group {group} (n={s['n']}):")
        lines.append(f"  Approval Rate:     {s['approval_rate']:.4f}")
        lines.append(f"  Default Rate:      {s['default_rate']:.4f}")
        lines.append(f"  Avg Loan Size:     R{s['avg_loan_size']:,.2f}")
        lines.append(f"  Avg Process Time:  {s['avg_processing_time']:.1f} min")
        lines.append("")

    lines.append("STATISTICAL TEST RESULTS (Two-Proportion Z-Test)")
    lines.append("-" * 40)

    for metric, res in results.items():
        lines.append(f"\n{metric.upper().replace('_', ' ')}")
        lines.append(f"  Group A: {res['group_a_rate']:.4f}  |  Group B: {res['group_b_rate']:.4f}")
        lines.append(f"  Treatment Effect:  {res['treatment_effect']:+.4f}")
        lines.append(f"  Z-Statistic:      {res['z_statistic']:.4f}")
        lines.append(f"  P-Value:          {res['p_value']:.6f}")
        lines.append(f"  95% CI:           [{res['ci_95_lower']:.4f}, {res['ci_95_upper']:.4f}]")
        lines.append(f"  Power:            {res['statistical_power']:.4f}")
        lines.append(f"  MDE:              {res['mde']:.4f}")
        lines.append(f"  Conclusion (α=0.05): {res['conclusion']}")

    lines.append("")
    lines.append("=" * 60)
    return "\n".join(lines)
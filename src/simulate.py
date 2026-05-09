"""Run A/B test experiment simulation and compute results."""

from typing import Dict, Any
from src.data_generator import generate_credit_data, compute_group_stats
from src.statistical import two_proportion_z_test, statistical_power, minimum_detectable_effect


def run_experiment(n_samples: int = 5000, alpha: float = 0.05) -> Dict[str, Any]:
    """
    Run the complete A/B experiment simulation.

    Args:
        n_samples: Total number of samples
        alpha: Significance level

    Returns:
        Dictionary containing all experiment results
    """
    # Generate data
    group_a, group_b = generate_credit_data(n_samples)

    # Compute group statistics
    stats_a = compute_group_stats(group_a)
    stats_b = compute_group_stats(group_b)

    # Test approval rate
    approval_result = two_proportion_z_test(
        n1=stats_a["n"],
        p1=stats_a["approval_rate"],
        n2=stats_b["n"],
        p2=stats_b["approval_rate"],
    )

    # Test default rate
    default_result = two_proportion_z_test(
        n1=stats_a["n"],
        p1=stats_a["default_rate"],
        n2=stats_b["n"],
        p2=stats_b["default_rate"],
    )

    # Compute power and MDE
    approval_power = statistical_power(
        stats_a["n"], stats_b["n"], stats_a["approval_rate"], stats_b["approval_rate"], alpha
    )
    default_power = statistical_power(
        stats_a["n"], stats_b["n"], stats_a["default_rate"], stats_b["default_rate"], alpha
    )

    approval_mde = minimum_detectable_effect(
        stats_a["n"], stats_b["n"], alpha, 0.80, stats_a["approval_rate"]
    )
    default_mde = minimum_detectable_effect(
        stats_a["n"], stats_b["n"], alpha, 0.80, stats_a["default_rate"]
    )

    return {
        "group_a": stats_a,
        "group_b": stats_b,
        "approval_rate_test": approval_result,
        "default_rate_test": default_result,
        "approval_power": approval_power,
        "default_power": default_power,
        "approval_mde": approval_mde,
        "default_mde": default_mde,
        "alpha": alpha,
    }


def interpret_results(results: Dict[str, Any]) -> Dict[str, str]:
    """Generate human-readable interpretations of test results."""
    interpretations = {}

    # Approval rate interpretation
    ar = results["approval_rate_test"]
    if ar["p_value"] < results["alpha"]:
        ar_significant = "SIGNIFICANT"
        ar_direction = "higher" if ar["difference"] > 0 else "lower"
        ar_conclusion = f"Group B has a {ar_direction} approval rate (statistically significant)."
    else:
        ar_significant = "NOT SIGNIFICANT"
        ar_conclusion = "No significant difference in approval rates between groups."

    interpretations["approval"] = (
        f"[{ar_significant}] "
        f"z={ar['z_statistic']:.3f}, p={ar['p_value']:.4f}, "
        f"diff={ar['difference']:.4f} (95% CI: [{ar['ci_lower']:.4f}, {ar['ci_upper']:.4f}]). "
        f"{ar_conclusion}"
    )

    # Default rate interpretation
    dr = results["default_rate_test"]
    if dr["p_value"] < results["alpha"]:
        dr_significant = "SIGNIFICANT"
        dr_direction = "lower" if dr["difference"] < 0 else "higher"
        dr_conclusion = f"Group B has a {dr_direction} default rate (statistically significant)."
    else:
        dr_significant = "NOT SIGNIFICANT"
        dr_conclusion = "No significant difference in default rates between groups."

    interpretations["default"] = (
        f"[{dr_significant}] "
        f"z={dr['z_statistic']:.3f}, p={dr['p_value']:.4f}, "
        f"diff={dr['difference']:.4f} (95% CI: [{dr['ci_lower']:.4f}, {dr['ci_upper']:.4f}]). "
        f"{dr_conclusion}"
    )

    return interpretations


if __name__ == "__main__":
    results = run_experiment()
    for key, value in results.items():
        if key not in ("group_a", "group_b"):
            print(f"{key}: {value:.4f}" if isinstance(value, float) else f"{key}: {value}")
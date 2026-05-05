"""Run the A/B experiment simulation."""

from .data_generator import generate_data, compute_group_stats
from .statistical import two_proportion_ztest, power_min_detectable_effect


def run_simulation(n_total: int = 5000, seed: int = 42) -> dict:
    """Run full A/B experiment.

    Returns:
        dict with raw data, stats, and statistical results.
    """
    data = generate_data(n_total, seed)
    stats_group = compute_group_stats(data)

    a_approved = int(data["group_a"]["approved"].sum())
    b_approved = int(data["group_b"]["approved"].sum())
    a_defaulted = int(data["group_a"]["defaulted"].sum())
    b_defaulted = int(data["group_b"]["defaulted"].sum())
    n = data["n_per_group"]

    approval_result = two_proportion_ztest(n, a_approved, n, b_approved)
    default_result = two_proportion_ztest(n, a_defaulted, n, b_defaulted,
                                          alternative="smaller")

    approval_mde = power_min_detectable_effect(n, n, stats_group["A"]["approval_rate"])
    default_mde = power_min_detectable_effect(n, n, stats_group["A"]["default_rate"])

    return {
        "data": data,
        "stats": stats_group,
        "approval_test": approval_result,
        "default_test": default_result,
        "approval_mde": approval_mde,
        "default_mde": default_mde,
        "n_per_group": n,
    }
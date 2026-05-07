"""
Run the A/B experiment simulation: compute metrics and run statistical tests.
"""

import numpy as np
from src.data_generator import generate_data, compute_group_metrics
from src.statistical import (
    two_proportion_ztest,
    confidence_interval_diff,
    min_detectable_effect,
    statistical_power,
)


def run_experiment() -> dict:
    """
    Execute the full A/B test simulation.

    Returns
    -------
    results : dict — metrics for both groups and statistical test results
    """
    group_A, group_B = generate_data()

    metrics_A = compute_group_metrics(group_A)
    metrics_B = compute_group_metrics(group_B)

    # Approval rate test
    n_A = metrics_A["n"]
    n_B = metrics_B["n"]
    approved_A = int(metrics_A["approval_rate"] * n_A)
    approved_B = int(metrics_B["approval_rate"] * n_B)

    approval_test = two_proportion_ztest(n_A, approved_A, n_B, approved_B)
    approval_ci = confidence_interval_diff(n_A, approved_A, n_B, approved_B)
    approval_mde = min_detectable_effect(n_A)

    # Default rate test (conditional on approval)
    def_A = int(metrics_A["default_rate"] * approved_A)
    def_B = int(metrics_B["default_rate"] * approved_B)

    default_test = two_proportion_ztest(n_A, def_A, n_B, def_B)
    default_ci = confidence_interval_diff(n_A, def_A, n_B, def_B)
    default_mde = min_detectable_effect(n_A)

    # Power at observed MDE
    approval_obs_mde = abs(metrics_B["approval_rate"] - metrics_A["approval_rate"])
    default_obs_mde = abs(metrics_B["default_rate"] - metrics_A["default_rate"])

    approval_power = statistical_power(n_A, metrics_A["approval_rate"], approval_obs_mde)
    default_power = statistical_power(n_A, metrics_A["default_rate"], default_obs_mde)

    return {
        "n_per_group": n_A,
        "metrics_A": metrics_A,
        "metrics_B": metrics_B,
        "approval_rate_test": {
            "z_stat": approval_test["z_stat"],
            "p_value": approval_test["p_value"],
            "p_A": approval_test["p_A"],
            "p_B": approval_test["p_B"],
            "ci_lower": approval_ci[0],
            "ci_upper": approval_ci[1],
            "mde": approval_mde,
            "power_at_obs_mde": approval_power,
            "significant": approval_test["p_value"] < 0.05,
        },
        "default_rate_test": {
            "z_stat": default_test["z_stat"],
            "p_value": default_test["p_value"],
            "p_A": default_test["p_A"],
            "p_B": default_test["p_B"],
            "ci_lower": default_ci[0],
            "ci_upper": default_ci[1],
            "mde": default_mde,
            "power_at_obs_mde": default_power,
            "significant": default_test["p_value"] < 0.05,
        },
    }
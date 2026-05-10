"""
Run A/B experiment simulation.
Generates data, runs statistical tests, returns results.
"""

import json
from src.data_generator import generate_data, compute_group_stats
from src.statistical import two_proportion_ztest, compute_power, compute_mde


def run_experiment(n: int = 5000) -> dict:
    """
    Run the full A/B experiment.

    Args:
        n: Number of applicants per group

    Returns:
        Dictionary with all results
    """
    outcomes_A, outcomes_B = generate_data(n)

    stats_A = compute_group_stats(outcomes_A)
    stats_B = compute_group_stats(outcomes_B)

    # --- Approval rate test ---
    approval_test = two_proportion_ztest(
        n1=stats_A["n"],
        x1=int(stats_A["n_approved"]),
        n2=stats_B["n"],
        x2=int(stats_B["n_approved"]),
    )

    approval_power = compute_power(
        n1=stats_A["n"],
        n2=stats_B["n"],
        p1=stats_A["approval_rate"],
        p2=stats_B["approval_rate"],
    )

    approval_mde = compute_mde(
        n1=stats_A["n"],
        n2=stats_B["n"],
        p1=stats_A["approval_rate"],
    )

    # --- Default rate test ---
    default_test = two_proportion_ztest(
        n1=stats_A["n"],
        x1=int(outcomes_A["defaulted"].sum()),
        n2=stats_B["n"],
        x2=int(outcomes_B["defaulted"].sum()),
    )

    default_power = compute_power(
        n1=stats_A["n"],
        n2=stats_B["n"],
        p1=stats_A["default_rate"],
        p2=stats_B["default_rate"],
    )

    default_mde = compute_mde(
        n1=stats_A["n"],
        n2=stats_B["n"],
        p1=stats_A["default_rate"],
    )

    results = {
        "sample_size_per_group": n,
        "group_A": {
            "approval_rate": round(float(stats_A["approval_rate"]), 4),
            "default_rate": round(float(stats_A["default_rate"]), 4),
            "avg_loan_size": round(float(stats_A["avg_loan_size"]), 2),
            "avg_processing_time_hrs": round(float(stats_A["avg_processing_time"]), 2),
        },
        "group_B": {
            "approval_rate": round(float(stats_B["approval_rate"]), 4),
            "default_rate": round(float(stats_B["default_rate"]), 4),
            "avg_loan_size": round(float(stats_B["avg_loan_size"]), 2),
            "avg_processing_time_hrs": round(float(stats_B["avg_processing_time"]), 2),
        },
        "approval_rate_test": {
            "z_statistic": round(float(approval_test.z_statistic), 4),
            "p_value": round(float(approval_test.p_value), 6),
            "diff": round(float(approval_test.diff), 4),
            "ci_95_lower": round(float(approval_test.ci_lower), 4),
            "ci_95_upper": round(float(approval_test.ci_upper), 4),
            "significant": bool(approval_test.significant),
            "power": round(float(approval_power), 4),
            "mde": round(float(approval_mde), 4),
        },
        "default_rate_test": {
            "z_statistic": round(float(default_test.z_statistic), 4),
            "p_value": round(float(default_test.p_value), 6),
            "diff": round(float(default_test.diff), 4),
            "ci_95_lower": round(float(default_test.ci_lower), 4),
            "ci_95_upper": round(float(default_test.ci_upper), 4),
            "significant": bool(default_test.significant),
            "power": round(float(default_power), 4),
            "mde": round(float(default_mde), 4),
        },
    }

    return results
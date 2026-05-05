"""
Run the A/B experiment simulation and compute treatment effects.
"""

from src.data_generator import generate_data, summarize
from src.statistical import (
    two_proportion_ztest,
    confidence_interval_diff,
    statistical_power,
    min_detectable_effect,
)


def run_experiment(n=5000, alpha=0.05, seed=42):
    """
    Run the full A/B experiment.

    Parameters
    ----------
    n : int
        Total number of simulated applicants.
    alpha : float
        Significance level.
    seed : int
        Random seed.

    Returns
    -------
    dict with detailed experiment results.
    """
    data = generate_data(n=n, seed=seed)
    summary = summarize(data)

    ga = data["group_a"]
    gb = data["group_b"]

    n_a = len(ga["approved"])
    n_b = len(gb["approved"])

    # Approval rate test
    approved_a = int(ga["approved"].sum())
    approved_b = int(gb["approved"].sum())

    approval_test = two_proportion_ztest(n_a, approved_a, n_b, approved_b)
    approval_ci = confidence_interval_diff(n_a, approved_a, n_b, approved_b, alpha=alpha)

    # Default rate test (only among approved)
    approved_idx_a = ga["approved"]
    approved_idx_b = gb["approved"]

    defaulted_a_count = int(ga["defaulted"][approved_idx_a].sum())
    defaulted_b_count = int(gb["defaulted"][approved_idx_b].sum())

    approved_count_a = approved_a
    approved_count_b = approved_b

    default_test = two_proportion_ztest(
        approved_count_a, defaulted_a_count,
        approved_count_b, defaulted_b_count,
    )
    default_ci = confidence_interval_diff(
        approved_count_a, defaulted_a_count,
        approved_count_b, defaulted_b_count,
        alpha=alpha,
    )

    # Power analysis
    p_approval_a = approved_a / n_a
    p_approval_b = approved_b / n_b
    approval_power = statistical_power(p_approval_a, p_approval_b, n_a, alpha=alpha)

    p_default_a = defaulted_a_count / approved_count_a if approved_count_a else 0
    p_default_b = defaulted_b_count / approved_count_b if approved_count_b else 0
    default_power = statistical_power(p_default_a, p_default_b, approved_count_a, alpha=alpha)

    approval_mde = min_detectable_effect(p_approval_a, n_a, power=0.8, alpha=alpha)
    default_mde  = min_detectable_effect(p_default_a, approved_count_a, power=0.8, alpha=alpha)

    return {
        "sample_sizes": {"group_a": n_a, "group_b": n_b},
        "summary": summary,
        "approval_rate": {
            "test": approval_test,
            "ci": approval_ci,
            "power": approval_power,
            "mde": approval_mde,
            "significant": approval_test["p_value"] < alpha,
        },
        "default_rate": {
            "test": default_test,
            "ci": default_ci,
            "power": default_power,
            "mde": default_mde,
            "significant": default_test["p_value"] < alpha,
        },
        "alpha": alpha,
    }
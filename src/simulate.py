"""Run A/B experiment simulation and compute treatment effects."""
from .data_generator import generate_credit_data, compute_group_summary
from .statistical import two_proportion_ztest, statistical_power, minimum_detectable_effect


def run_experiment(n=5000):
    """
    Run the full A/B experiment: generate data and run statistical tests.

    Returns a dict with raw data summary, statistical results, and power info.
    """
    df = generate_credit_data(n=n)

    summaries = compute_group_summary(df)

    group_a = summaries["A"]
    group_b = summaries["B"]

    # --- Approval Rate Test ---
    approval_result = two_proportion_ztest(
        n_success_a=int(group_a["approval_rate"] * group_a["n"]),
        n_trials_a=group_a["n"],
        n_success_b=int(group_b["approval_rate"] * group_b["n"]),
        n_trials_b=group_b["n"],
    )

    # --- Default Rate Test ---
    # default rate is conditional on being approved
    n_approved_a = int(group_a["approval_rate"] * group_a["n"])
    n_defaulted_a = int(group_a["default_rate"] * n_approved_a)
    n_approved_b = int(group_b["approval_rate"] * group_b["n"])
    n_defaulted_b = int(group_b["default_rate"] * n_approved_b)

    default_result = two_proportion_ztest(
        n_success_a=n_defaulted_a,
        n_trials_a=n_approved_a,
        n_success_b=n_defaulted_b,
        n_trials_b=n_approved_b,
    )

    # --- Power Analysis ---
    power_approval = statistical_power(
        group_a["n"], group_b["n"],
        group_a["approval_rate"], group_b["approval_rate"]
    )
    mde_approval = minimum_detectable_effect(group_a["n"], group_b["n"])

    return {
        "n_total": n,
        "group_a": group_a,
        "group_b": group_b,
        "approval_rate_test": approval_result,
        "default_rate_test": default_result,
        "power_approval": power_approval,
        "mde_approval": mde_approval,
    }

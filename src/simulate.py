import pandas as pd
from src.data_generator import generate_credit_data, compute_group_metrics
from src.statistical import two_proportion_z_test, calculate_statistical_power, minimum_detectable_effect


def run_experiment(n_applicants: int = 5000) -> dict:
    """
    Run the complete A/B experiment simulation.

    Args:
        n_applicants: Total number of applicants to generate

    Returns:
        Dictionary containing all experiment results
    """
    # Generate data
    df = generate_credit_data(n=n_applicants)

    # Compute metrics for each group
    metrics_a = compute_group_metrics(df, "A")
    metrics_b = compute_group_metrics(df, "B")

    # Approval rate z-test
    approval_test = two_proportion_z_test(
        n1=metrics_a["total_applicants"],
        x1=metrics_a["approval_count"],
        n2=metrics_b["total_applicants"],
        x2=metrics_b["approval_count"]
    )

    # Default rate z-test (among approved)
    df_approved_a = df[(df["group"] == "A") & df["approved"]]
    df_approved_b = df[(df["group"] == "B") & df["approved"]]

    default_test = two_proportion_z_test(
        n1=len(df_approved_a),
        x1=int(df_approved_a["defaulted"].sum()),
        n2=len(df_approved_b),
        x2=int(df_approved_b["defaulted"].sum())
    )

    # Calculate power and MDE for approval rate
    n_a = metrics_a["total_applicants"]
    n_b = metrics_b["total_applicants"]
    effect_approval = abs(metrics_b["approval_rate"] - metrics_a["approval_rate"])

    power_approval = calculate_statistical_power(n_a, n_b, effect_approval)
    mde_approval = minimum_detectable_effect(n_a, n_b)

    # Calculate power and MDE for default rate
    n_default_a = len(df_approved_a)
    n_default_b = len(df_approved_b)
    effect_default = abs(metrics_b["default_rate"] - metrics_a["default_rate"])

    power_default = calculate_statistical_power(n_default_a, n_default_b, effect_default)
    mde_default = minimum_detectable_effect(n_default_a, n_default_b)

    return {
        "data": df,
        "metrics": {
            "group_a": metrics_a,
            "group_b": metrics_b
        },
        "approval_rate_test": approval_test,
        "default_rate_test": default_test,
        "power_analysis": {
            "approval_rate": {
                "observed_effect": effect_approval,
                "power": power_approval,
                "mde": mde_approval
            },
            "default_rate": {
                "observed_effect": effect_default,
                "power": power_default,
                "mde": mde_default
            }
        },
        "sample_sizes": {
            "group_a": n_a,
            "group_b": n_b,
            "approved_a": n_default_a,
            "approved_b": n_default_b
        }
    }
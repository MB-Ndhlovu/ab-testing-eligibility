"""Run A/B test experiment simulation."""

from src.data_generator import generate_credit_data, compute_group_metrics
from src.statistical import two_proportion_z_test, statistical_power, minimum_detectable_effect


def run_simulation(n: int = 5000, seed: int = 42) -> dict:
    """
    Run the full A/B test experiment.

    Args:
        n: Sample size per group
        seed: Random seed

    Returns:
        Dictionary with all experiment results
    """
    group_a = generate_credit_data(n=n, group="A", seed=seed)
    group_b = generate_credit_data(n=n, group="B", seed=seed)

    metrics_a = compute_group_metrics(group_a)
    metrics_b = compute_group_metrics(group_b)

    approval_test = two_proportion_z_test(
        x1=metrics_a["approvals"],
        n1=n,
        x2=metrics_b["approvals"],
        n2=n,
    )

    default_test = two_proportion_z_test(
        x1=metrics_a["defaults"],
        n1=metrics_a["approvals"],
        x2=metrics_b["defaults"],
        n2=metrics_b["approvals"],
    )

    power_approval = statistical_power(
        n1=n, n2=n, p1=metrics_a["approval_rate"], p2=metrics_b["approval_rate"]
    )
    power_default = statistical_power(
        n1=metrics_a["approvals"],
        n2=metrics_b["approvals"],
        p1=metrics_a["default_rate"],
        p2=metrics_b["default_rate"],
    )

    mde_approval = minimum_detectable_effect(
        n1=n, n2=n, power=0.8, alpha=0.05, p1=metrics_a["approval_rate"]
    )
    mde_default = minimum_detectable_effect(
        n1=metrics_a["approvals"],
        n2=metrics_b["approvals"],
        power=0.8,
        alpha=0.05,
        p1=metrics_a["default_rate"],
    )

    return {
        "group_a": metrics_a,
        "group_b": metrics_b,
        "approval_test": approval_test,
        "default_test": default_test,
        "power": {
            "approval": power_approval,
            "default": power_default,
        },
        "mde": {
            "approval": mde_approval,
            "default": mde_default,
        },
        "sample_size": n,
        "alpha": 0.05,
    }
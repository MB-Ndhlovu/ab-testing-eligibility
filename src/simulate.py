from src.data_generator import generate_credit_data, compute_group_summary
from src.statistical import two_proportion_ztest, statistical_power, minimum_detectable_effect


def run_experiment(df, alpha: float = 0.05) -> dict:
    """Run A/B experiment and compute all statistical results.

    Args:
        df: DataFrame from data_generator
        alpha: Significance level

    Returns:
        dict with group summaries, test results, and power analysis
    """
    summary_a = compute_group_summary(df, "A")
    summary_b = compute_group_summary(df, "B")

    n_a = summary_a["n"]
    n_b = summary_b["n"]

    approved_a = int(summary_a["approval_rate"] * n_a)
    approved_b = int(summary_b["approval_rate"] * n_b)

    defaulted_a = int(summary_a["default_rate"] * approved_a) if approved_a > 0 else 0
    defaulted_b = int(summary_b["default_rate"] * approved_b) if approved_b > 0 else 0

    approval_test = two_proportion_ztest(n_a, approved_a, n_b, approved_b)
    default_test = two_proportion_ztest(n_a, defaulted_a, n_b, defaulted_b)

    power_approval = statistical_power(n_a, n_b, summary_a["approval_rate"],
                                       summary_b["approval_rate"], alpha)
    power_default = statistical_power(n_a, n_b, summary_a["default_rate"],
                                        summary_b["default_rate"], alpha)

    mde_approval = minimum_detectable_effect(n_a, n_b, summary_a["approval_rate"], alpha)
    mde_default = minimum_detectable_effect(n_a, n_b, summary_a["default_rate"], alpha)

    return {
        "group_a": summary_a,
        "group_b": summary_b,
        "approval_test": approval_test,
        "default_test": default_test,
        "power_approval": power_approval,
        "power_default": power_default,
        "mde_approval": mde_approval,
        "mde_default": mde_default,
        "alpha": alpha,
    }
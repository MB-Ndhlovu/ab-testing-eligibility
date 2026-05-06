from src.data_generator import generate_experiment_data, compute_group_metrics
from src.statistical import (
    two_proportion_ztest,
    confidence_interval_diff,
    statistical_power,
    minimum_detectable_effect,
    test_significance
)


def run_simulation(seed=42, alpha=0.05):
    df = generate_experiment_data(seed=seed)

    metrics_a = compute_group_metrics(df, "A")
    metrics_b = compute_group_metrics(df, "B")

    n_a = metrics_a["n"]
    n_b = metrics_b["n"]
    ar_a = metrics_a["approval_rate"]
    ar_b = metrics_b["approval_rate"]
    dr_a = metrics_a["default_rate"]
    dr_b = metrics_b["default_rate"]

    ar_ztest = two_proportion_ztest(n_a, ar_a, n_b, ar_b)
    ar_ci = confidence_interval_diff(n_a, ar_a, n_b, ar_b)
    ar_significant = test_significance(ar_ztest["p_value"], alpha)

    dr_ztest = two_proportion_ztest(n_a, dr_a, n_b, dr_b)
    dr_ci = confidence_interval_diff(n_a, dr_a, n_b, dr_b)
    dr_significant = test_significance(dr_ztest["p_value"], alpha)

    ar_power = statistical_power(n_a, n_b, ar_a, ar_b, alpha)
    dr_power = statistical_power(n_a, n_b, dr_a, dr_b, alpha)

    ar_mde = minimum_detectable_effect(n_a, n_b, ar_a, alpha)
    dr_mde = minimum_detectable_effect(n_a, n_b, dr_a, alpha)

    return {
        "group_a": metrics_a,
        "group_b": metrics_b,
        "approval_rate": {
            "z_statistic": ar_ztest["z_statistic"],
            "p_value": ar_ztest["p_value"],
            "ci_lower": ar_ci["ci_lower"],
            "ci_upper": ar_ci["ci_upper"],
            "significant": ar_significant,
            "power": ar_power["power"],
            "mde": ar_mde["mde"],
            "treatment_effect": ar_b - ar_a
        },
        "default_rate": {
            "z_statistic": dr_ztest["z_statistic"],
            "p_value": dr_ztest["p_value"],
            "ci_lower": dr_ci["ci_lower"],
            "ci_upper": dr_ci["ci_upper"],
            "significant": dr_significant,
            "power": dr_power["power"],
            "mde": dr_mde["mde"],
            "treatment_effect": dr_b - dr_a
        }
    }


if __name__ == "__main__":
    results = run_simulation()
    print(results)
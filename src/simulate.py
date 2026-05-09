"""Run the A/B experiment simulation and compute significance."""
from src.data_generator import group_a_summary, group_b_summary
from src.statistical import two_proportion_ztest, confidence_interval, statistical_power

def run_simulation():
    results = {}

    # Approval Rate
    n_a = group_a_summary["n"]
    n_b = group_b_summary["n"]
    ar_a = group_a_summary["approval_rate"]
    ar_b = group_b_summary["approval_rate"]
    dr_a = group_a_summary["default_rate"]
    dr_b = group_b_summary["default_rate"]

    z_ar, p_ar = two_proportion_ztest(n_a, ar_a, n_b, ar_b)
    ci_ar = confidence_interval(n_a, ar_a, n_b, ar_b)
    power_ar = statistical_power((n_a + n_b) // 2, ar_a, ar_b)

    z_dr, p_dr = two_proportion_ztest(n_a, dr_a, n_b, dr_b)
    ci_dr = confidence_interval(n_a, dr_a, n_b, dr_b)
    power_dr = statistical_power((n_a + n_b) // 2, dr_a, dr_b)

    results["approval_rate"] = {
        "group_a": ar_a,
        "group_b": ar_b,
        "treatment_effect": ar_b - ar_a,
        "z_statistic": z_ar,
        "p_value": p_ar,
        "ci_lower": ci_ar[0],
        "ci_upper": ci_ar[1],
        "significant": p_ar < 0.05,
        "power": power_ar,
    }

    results["default_rate"] = {
        "group_a": dr_a,
        "group_b": dr_b,
        "treatment_effect": dr_b - dr_a,
        "z_statistic": z_dr,
        "p_value": p_dr,
        "ci_lower": ci_dr[0],
        "ci_upper": ci_dr[1],
        "significant": p_dr < 0.05,
        "power": power_dr,
    }

    results["avg_loan_size"] = {
        "group_a": group_a_summary["avg_loan_size"],
        "group_b": group_b_summary["avg_loan_size"],
        "treatment_effect": group_b_summary["avg_loan_size"] - group_a_summary["avg_loan_size"],
    }

    results["avg_processing_time"] = {
        "group_a": group_a_summary["avg_processing_time"],
        "group_b": group_b_summary["avg_processing_time"],
        "treatment_effect": group_b_summary["avg_processing_time"] - group_a_summary["avg_processing_time"],
    }

    return results
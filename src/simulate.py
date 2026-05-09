from src.data_generator import generate_data, compute_summary
from src.statistical import two_proportion_ztest, confidence_interval

def run_experiment(seed=42):
    records = generate_data(n=5000, seed=seed)
    summary = compute_summary(records)

    # Metrics for group A (control)
    n_a = summary["A"]["n"]
    approved_a = round(summary["A"]["approval_rate"] * n_a)
    defaulted_a = round(summary["A"]["default_rate"] * approved_a)

    # Metrics for group B (treatment)
    n_b = summary["B"]["n"]
    approved_b = round(summary["B"]["approval_rate"] * n_b)
    defaulted_b = round(summary["B"]["default_rate"] * approved_b)

    # Two-proportion z-test for approval_rate
    approval_test = two_proportion_ztest(n_a, approved_a, n_b, approved_b)
    approval_ci = confidence_interval(n_a, approved_a, n_b, approved_b)

    # Two-proportion z-test for default_rate (among approved)
    default_test = two_proportion_ztest(n_a, defaulted_a, n_b, defaulted_b)
    default_ci = confidence_interval(n_a, defaulted_a, n_b, defaulted_b)

    results = {
        "group_a": {
            "n": n_a,
            "approval_rate": round(summary["A"]["approval_rate"], 4),
            "default_rate": round(summary["A"]["default_rate"], 4),
            "avg_loan_size": round(summary["A"]["avg_loan_size"], 2),
            "avg_processing_time": round(summary["A"]["avg_processing_time"], 2),
        },
        "group_b": {
            "n": n_b,
            "approval_rate": round(summary["B"]["approval_rate"], 4),
            "default_rate": round(summary["B"]["default_rate"], 4),
            "avg_loan_size": round(summary["B"]["avg_loan_size"], 2),
            "avg_processing_time": round(summary["B"]["avg_processing_time"], 2),
        },
        "approval_rate_test": {
            "z_statistic": approval_test["z_statistic"],
            "p_value": approval_test["p_value"],
            "ci_lower": approval_ci["ci_lower"],
            "ci_upper": approval_ci["ci_upper"],
            "significant": approval_test["p_value"] < 0.05,
        },
        "default_rate_test": {
            "z_statistic": default_test["z_statistic"],
            "p_value": default_test["p_value"],
            "ci_lower": default_ci["ci_lower"],
            "ci_upper": default_ci["ci_upper"],
            "significant": default_test["p_value"] < 0.05,
        }
    }

    return results

if __name__ == "__main__":
    results = run_experiment()
    print("Approval rate z-test:", results["approval_rate_test"])
    print("Default rate z-test:", results["default_rate_test"])
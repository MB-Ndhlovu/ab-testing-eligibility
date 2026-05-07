"""
Run the A/B experiment simulation.
Computes summary stats and runs z-tests for each metric.
"""

from src.data_generator import data_a, data_b, summary_a, summary_b
from src.statistical import two_proportion_ztest, statistical_power, minimum_detectable_effect


def run_simulation():
    results = {}

    # --- Approval Rate ---
    n_a = summary_a["n"]
    n_b = summary_b["n"]
    x_a_approval = summary_a["n_approved"]
    x_b_approval = summary_b["n_approved"]

    approval_test = two_proportion_ztest(n_a, x_a_approval, n_b, x_b_approval)
    approval_power = statistical_power(n_a, n_b, approval_test["p_a"], approval_test["p_b"])
    approval_mde = minimum_detectable_effect(n_a, n_b, approval_test["p_a"])

    results["approval_rate"] = {
        "group_a_rate": approval_test["p_a"],
        "group_b_rate": approval_test["p_b"],
        "diff": approval_test["diff"],
        "z_stat": approval_test["z_stat"],
        "p_value": approval_test["p_value"],
        "ci_95": [approval_test["ci_lower"], approval_test["ci_upper"]],
        "significant": approval_test["significant"],
        "power": approval_power,
        "mde": approval_mde,
    }

    # --- Default Rate ---
    n_a_def = summary_a["n_approved"]
    n_b_def = summary_b["n_approved"]
    x_a_default = int(summary_a["default_rate"] * n_a_def)
    x_b_default = int(summary_b["default_rate"] * n_b_def)

    default_test = two_proportion_ztest(n_a_def, x_a_default, n_b_def, x_b_default)
    default_power = statistical_power(n_a_def, n_b_def, default_test["p_a"], default_test["p_b"])
    default_mde = minimum_detectable_effect(n_a_def, n_a_def, default_test["p_a"])

    results["default_rate"] = {
        "group_a_rate": default_test["p_a"],
        "group_b_rate": default_test["p_b"],
        "diff": default_test["diff"],
        "z_stat": default_test["z_stat"],
        "p_value": default_test["p_value"],
        "ci_95": [default_test["ci_lower"], default_test["ci_upper"]],
        "significant": default_test["significant"],
        "power": default_power,
        "mde": default_mde,
    }

    # --- Avg Loan Size (two-sample t-test) ---
    from scipy import stats as scipy_stats

    loan_a = data_a["loan_size"][data_a["approved"] == 1]
    loan_b = data_b["loan_size"][data_b["approved"] == 1]
    t_stat, p_val_loan = scipy_stats.ttest_ind(loan_a, loan_b)

    results["avg_loan_size"] = {
        "group_a_mean": float(loan_a.mean()),
        "group_b_mean": float(loan_b.mean()),
        "diff": float(loan_b.mean() - loan_a.mean()),
        "t_stat": float(t_stat),
        "p_value": float(p_val_loan),
    }

    # --- Avg Processing Time ---
    proc_a = data_a["processing_time"][data_a["approved"] == 1]
    proc_b = data_b["processing_time"][data_b["approved"] == 1]
    t_stat_proc, p_val_proc = scipy_stats.ttest_ind(proc_a, proc_b)

    results["avg_processing_time"] = {
        "group_a_mean": float(proc_a.mean()),
        "group_b_mean": float(proc_b.mean()),
        "diff": float(proc_b.mean() - proc_a.mean()),
        "t_stat": float(t_stat_proc),
        "p_value": float(p_val_proc),
    }

    return results


if __name__ == "__main__":
    r = run_simulation()
    for metric, data in r.items():
        print(f"\n=== {metric.upper()} ===")
        for k, v in data.items():
            print(f"  {k}: {v}")
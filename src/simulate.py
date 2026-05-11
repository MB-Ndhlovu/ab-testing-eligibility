"""Run the A/B experiment simulation."""
import numpy as np
from .data_generator import group_a, group_b
from .statistical import two_proportion_ztest, power_analysis

def run_experiment():
    n_a = len(group_a["approved"])
    n_b = len(group_b["approved"])

    # --- Approval Rate ---
    ar_a = group_a["approved"].sum()
    ar_b = group_b["approved"].sum()
    ar_test = two_proportion_ztest(
        n_success=(ar_a, ar_b),
        n_total=(n_a, n_b),
    )

    # --- Default Rate ---
    dr_a = group_a["defaulted"].sum()
    dr_b = group_b["defaulted"].sum()
    # Denominator: only approved applications
    ar_a_int = int(ar_a)
    ar_b_int = int(ar_b)
    dr_test = two_proportion_ztest(
        n_success=(dr_a, dr_b),
        n_total=(ar_a_int, ar_b_int),
    )

    # --- Avg Loan Size ( Welch's t-test approximation) ---
    loans_a = group_a["loan_size"][group_a["approved"] == 1]
    loans_b = group_b["loan_size"][group_b["approved"] == 1]

    t_stat, t_pval = None, None
    if len(loans_a) > 1 and len(loans_b) > 1:
        t_stat, t_pval = run_t_test(loans_a, loans_b)

    # --- Processing Time ---
    time_a = group_a["processing_time"]
    time_b = group_b["processing_time"]
    t_time_stat, t_time_pval = None, None
    if len(time_a) > 1 and len(time_b) > 1:
        t_time_stat, t_time_pval = run_t_test(time_a, time_b)

    return {
        "approval_rate": ar_test,
        "default_rate": dr_test,
        "avg_loan_size": {"t_stat": t_stat, "p_value": t_pval},
        "processing_time": {"t_stat": t_time_stat, "p_value": t_time_pval},
        "n_a": n_a,
        "n_b": n_b,
    }

def run_t_test(a, b):
    from scipy import stats as sp_stats
    t = sp_stats.ttest_ind(a, b, equal_var=False)
    return t.statistic, t.pvalue
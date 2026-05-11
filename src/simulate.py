"""
Runs the A/B experiment simulation:
  - Loads or generates data
  - Computes per-group summary stats
  - Runs two-proportion z-tests for approval_rate and default_rate
  - Returns a results dictionary
"""

import numpy as np
import pandas as pd
from src.statistical import two_proportion_ztest, compute_power, minimum_detectable_effect

def run_experiment(df: pd.DataFrame) -> dict:
    n_a = int((df["group"] == "A").sum())
    n_b = int((df["group"] == "B").sum())

    # Summary stats
    grp_a = df[df["group"] == "A"]
    grp_b = df[df["group"] == "B"]

    results = {
        "group_a": {
            "n": n_a,
            "approval_rate": grp_a["approved"].mean(),
            "default_rate":  grp_a["defaulted"].mean(),
            "avg_loan_size": grp_a["loan_size"].mean(),
            "avg_processing_time": grp_a["processing_time"].mean(),
        },
        "group_b": {
            "n": n_b,
            "approval_rate": grp_b["approved"].mean(),
            "default_rate":  grp_b["defaulted"].mean(),
            "avg_loan_size": grp_b["loan_size"].mean(),
            "avg_processing_time": grp_b["processing_time"].mean(),
        },
    }

    # Two-proportion z-tests
    for metric, x_a_fn, x_b_fn in [
        ("approval_rate",
         lambda: int(grp_a["approved"].sum()),
         lambda: int(grp_b["approved"].sum())),
        ("default_rate",
         lambda: int(grp_a["defaulted"].sum()),
         lambda: int(grp_b["defaulted"].sum())),
    ]:
        x_a = x_a_fn()
        x_b = x_b_fn()
        alt = "larger" if metric == "approval_rate" else "smaller"
        test = two_proportion_ztest(n_a, n_b, x_a, x_b, alternative=alt)
        results[metric] = {
            "x_a": x_a, "x_b": x_b,
            "rate_a": round(x_a / n_a, 4),
            "rate_b": round(x_b / n_b, 4),
            "z_statistic": test["z_statistic"],
            "p_value": test["p_value"],
            "ci_95": test["ci_95"],
            "diff": test["diff"],
            "significant": test["significant"],
        }

    # Power analysis (using observed proportions)
    p_approval_a = results["group_a"]["approval_rate"]
    p_approval_b = results["group_b"]["approval_rate"]
    results["power_approval"] = compute_power(n_a, n_b, p_approval_a, p_approval_b)
    p_default_a = results["group_a"]["default_rate"]
    p_default_b = results["group_b"]["default_rate"]
    results["power_default"] = compute_power(n_a, n_b, p_default_a, p_default_b)

    results["mde"] = minimum_detectable_effect(n_a, n_b)

    return results
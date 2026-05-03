import pandas as pd
from src.statistical import two_proportion_ztest, confidence_interval, statistical_power, min_detectable_effect

def run_simulation(df, alpha=0.05):
    df_A = df[df["group"] == "A"]
    df_B = df[df["group"] == "B"]

    n_A = len(df_A)
    n_B = len(df_B)

    approval_A = df_A["approved"].mean()
    approval_B = df_B["approved"].mean()
    default_A = df_A["defaulted"].mean()
    default_B = df_B["defaulted"].mean()

    # Two-proportion z-test for approval rate
    z_approval, p_approval = two_proportion_ztest(n_A, approval_A, n_B, approval_B)
    ci_approval = confidence_interval(approval_A, approval_B, n_A, n_B, alpha)
    power_approval = statistical_power(n_A, n_B, approval_A, approval_B, alpha)
    mde_approval = min_detectable_effect(n_A, n_B, approval_A, alpha)

    # Two-proportion z-test for default rate
    z_default, p_default = two_proportion_ztest(n_A, default_A, n_B, default_B)
    ci_default = confidence_interval(default_A, default_B, n_A, n_B, alpha)
    power_default = statistical_power(n_A, n_B, default_A, default_B, alpha)
    mde_default = min_detectable_effect(n_A, n_B, default_A, alpha)

    results = {
        "n_per_group": n_A,
        "alpha": alpha,
        "approval_rate": {
            "group_A": approval_A, "group_B": approval_B,
            "z_statistic": z_approval, "p_value": p_approval,
            "ci_95": ci_approval, "power": power_approval,
            "mde": mde_approval, "significant": p_approval < alpha,
            "effect": approval_B - approval_A,
        },
        "default_rate": {
            "group_A": default_A, "group_B": default_B,
            "z_statistic": z_default, "p_value": p_default,
            "ci_95": ci_default, "power": power_default,
            "mde": mde_default, "significant": p_default < alpha,
            "effect": default_B - default_A,
        },
    }
    return results
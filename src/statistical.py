"""
Statistical analysis module for A/B testing.
Implements two-proportion z-test, confidence intervals, power, and MDE.
"""
import numpy as np
from scipy import stats

def two_proportion_ztest(n1, p1, n2, p2):
    """
    Two-proportion z-test comparing two binomial proportions.

    Returns: z_stat, p_value (two-tailed)
    """
    p_pooled = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    if se == 0:
        return np.nan, np.nan
    z = (p1 - p2) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value

def confidence_interval(n1, p1, n2, p2, alpha=0.05):
    """
    Wald confidence interval for the difference p1 - p2.
    Returns (lower, upper).
    """
    diff = p1 - p2
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    margin = z_crit * se
    return diff - margin, diff + margin

def statistical_power(n1, p1, n2, p2, alpha=0.05, mde=None):
    """
    Compute statistical power for a two-proportion z-test.
    If mde is provided, power is computed for detecting that effect size.
    Otherwise uses the observed difference as the effect.
    """
    if mde is None:
        mde = abs(p1 - p2)
    if mde == 0:
        return 0.0
    p_pooled = (n1 * p1 + n2 * p2) / (n1 + n2)
    se_null = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    se_alt = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = (mde / se_alt) - z_crit
    return stats.norm.cdf(z_power)

def minimum_detectable_effect(n1, n2, alpha=0.05, power=0.80):
    """
    Minimum detectable effect (absolute difference) for given sample sizes.
    """
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)
    # Approximate pooled p = 0.5 for conservative MDE
    se = np.sqrt(0.5 * 0.5 * (1/n1 + 1/n2))
    return (z_crit + z_power) * se

def run_analysis(n_A, p_approval_A, n_B, p_approval_B,
                 n_A_def, p_default_A, n_B_def, p_default_B,
                 alpha=0.05):
    """
    Run full statistical analysis on two metrics.

    Returns dict with results for approval_rate and default_rate.
    """
    results = {}

    # --- Approval Rate ---
    z_app, p_app = two_proportion_ztest(n_A, p_approval_A, n_B, p_approval_B)
    ci_app = confidence_interval(n_A, p_approval_A, n_B, p_approval_B, alpha)
    power_app = statistical_power(n_A, p_approval_A, n_B, p_approval_B, alpha)
    mde_app = minimum_detectable_effect(n_A, n_B, alpha)

    results["approval_rate"] = {
        "group_A": round(p_approval_A, 4),
        "group_B": round(p_approval_B, 4),
        "difference": round(p_approval_B - p_approval_A, 4),
        "z_statistic": round(z_app, 4),
        "p_value": round(p_app, 4),
        "ci_lower": round(ci_app[0], 4),
        "ci_upper": round(ci_app[1], 4),
        "significant": p_app < alpha,
        "power": round(power_app, 4),
        "mde": round(mde_app, 4),
    }

    # --- Default Rate ---
    z_def, p_def = two_proportion_ztest(n_A_def, p_default_A, n_B_def, p_default_B)
    ci_def = confidence_interval(n_A_def, p_default_A, n_B_def, p_default_B, alpha)
    power_def = statistical_power(n_A_def, p_default_A, n_B_def, p_default_B, alpha)
    mde_def = minimum_detectable_effect(n_A_def, n_B_def, alpha)

    results["default_rate"] = {
        "group_A": round(p_default_A, 4),
        "group_B": round(p_default_B, 4),
        "difference": round(p_default_B - p_default_A, 4),
        "z_statistic": round(z_def, 4),
        "p_value": round(p_def, 4),
        "ci_lower": round(ci_def[0], 4),
        "ci_upper": round(ci_def[1], 4),
        "significant": p_def < alpha,
        "power": round(power_def, 4),
        "mde": round(mde_def, 4),
    }

    return results
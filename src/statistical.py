import numpy as np
from scipy import stats


def two_proportion_ztest(n1, p1, n2, p2):
    """Two-proportion z-test for difference in proportions."""
    p_pooled = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    z = (p1 - p2) / se if se > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return {"z_statistic": z, "p_value": p_value}


def confidence_interval_diff(n1, p1, n2, p2, confidence=0.95):
    """Wald confidence interval for difference in proportions."""
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    if se == 0:
        return (0, 0)
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    diff = p1 - p2
    return (diff - z * se, diff + z * se)


def statistical_power(n, p1, p2, alpha=0.05):
    """Compute statistical power for two-proportion test."""
    p_pooled = (p1 + p2) / 2
    se = np.sqrt(p_pooled * (1 - p_pooled) * (2 / n))
    if se == 0:
        return 0
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = (abs(p1 - p2) / se) - z_crit
    power = stats.norm.cdf(z_power)
    return power


def minimum_detectable_effect(n, alpha=0.05, power=0.80):
    """Minimum detectable effect at given n, alpha, and power."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p = 0.5  # baseline proportion estimate
    mde = (z_alpha + z_beta) * np.sqrt(2 * p * (1 - p) / n)
    return mde


def analyze_metric(name, n_a, rate_a, n_b, rate_b, alpha=0.05):
    result = two_proportion_ztest(n_a, rate_a, n_b, rate_b)
    ci = confidence_interval_diff(n_a, rate_a, n_b, rate_b)
    power = statistical_power(min(n_a, n_b), rate_a, rate_b, alpha)
    mde = minimum_detectable_effect(min(n_a, n_b), alpha)

    return {
        "metric": name,
        "group_a_rate": rate_a,
        "group_b_rate": rate_b,
        "treatment_effect": rate_b - rate_a,
        "z_statistic": result["z_statistic"],
        "p_value": result["p_value"],
        "ci_lower": ci[0],
        "ci_upper": ci[1],
        "significant": result["p_value"] < alpha,
        "power": power,
        "mde": mde,
    }
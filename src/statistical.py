"""Statistical analysis for two-proportion z-tests."""

import numpy as np
from scipy import stats


def two_proportion_ztest(n_A, p_A, n_B, p_B):
    """
    Two-proportion z-test comparing proportions from two groups.

    Args:
        n_A: Number of trials in group A (control)
        p_A: Proportion of successes in group A
        n_B: Number of trials in group B (treatment)
        p_B: Proportion of successes in group B

    Returns:
        dict with z_statistic, p_value, ci_lower, ci_upper
    """
    # Pooled proportion under null hypothesis
    p_pooled = (n_A * p_A + n_B * p_B) / (n_A + n_B)

    # Standard error
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_A + 1 / n_B))

    # Z-statistic
    z_stat = (p_B - p_A) / se

    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # 95% Confidence interval for the difference
    diff = p_B - p_A
    se_diff = np.sqrt((p_A * (1 - p_A)) / n_A + (p_B * (1 - p_B)) / n_B)
    ci_lower = diff - 1.96 * se_diff
    ci_upper = diff + 1.96 * se_diff

    # Statistical power and minimum detectable effect
    alpha = 0.05
    z_crit = stats.norm.ppf(1 - alpha / 2)

    # Power: probability of detecting true difference of (p_B - p_A)
    mde = abs(p_B - p_A)
    if mde > 0:
        z_power = (mde - z_crit * se_diff) / se_diff
        power = 1 - stats.norm.cdf(z_power) + stats.norm.cdf(-z_power - z_power)
    else:
        power = alpha

    return {
        "z_statistic": z_stat,
        "p_value": p_value,
        "ci_95": (ci_lower, ci_upper),
        "significant": p_value < alpha,
        "power": power,
        "mde": mde,
    }


def analyze_metric(data, metric_name, n_A=None, n_B=None):
    """
    Analyze a binary metric (approval_rate or default_rate) across groups.

    Args:
        data: dict from data_generator.generate_data()
        metric_name: 'approval_rate' or 'default_rate'
        n_A: optional override for group A size
        n_B: optional override for group B size

    Returns:
        dict with group stats and test results
    """
    gA = data["group_A"]
    gB = data["group_B"]

    p_A = gA[metric_name]
    p_B = gB[metric_name]

    if n_A is None:
        n_A = gA["n"]
    if n_B is None:
        n_B = gB["n"]

    test_results = two_proportion_ztest(n_A, p_A, n_B, p_B)

    return {
        "metric": metric_name,
        "group_A_rate": p_A,
        "group_B_rate": p_B,
        "treatment_effect": p_B - p_A,
        "n_A": n_A,
        "n_B": n_B,
        "test": test_results,
    }
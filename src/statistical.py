"""Statistical tests for A/B testing."""

import numpy as np
from scipy import stats


def two_proportion_ztest(n1: int, p1: float, n2: int, p2: float):
    """Two-proportion z-test.

    Args:
        n1: Sample size group 1.
        p1: Proportion group 1.
        n2: Sample size group 2.
        p2: Proportion group 2.

    Returns:
        z-statistic, p-value (two-tailed)
    """
    p_pool = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    if se == 0:
        return 0.0, 1.0
    z = (p1 - p2) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value


def confidence_interval_diff(p1: float, p2: float, n1: int, n2: int, alpha: float = 0.05):
    """95% confidence interval for the difference between two proportions.

    Args:
        p1: Proportion group 1.
        p2: Proportion group 2.
        n1: Sample size group 1.
        n2: Sample size group 2.
        alpha: Significance level (default 0.05 for 95% CI).

    Returns:
        (lower, upper) tuple
    """
    diff = p1 - p2
    se = np.sqrt((p1 * (1 - p1)) / n1 + (p2 * (1 - p2)) / n2)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    margin = z_crit * se
    return diff - margin, diff + margin


def statistical_power(p1: float, p2: float, n1: int, n2: int, alpha: float = 0.05) -> float:
    """Calculate statistical power for a two-proportion test.

    Args:
        p1: Proportion group 1.
        p2: Proportion group 2.
        n1: Sample size group 1.
        n2: Sample size group 2.
        alpha: Significance level.

    Returns:
        Power (probability of detecting true effect).
    """
    se_null = np.sqrt(p1 * (1 - p1) * (1/n1 + 1/n2))
    if se_null == 0:
        return 0.0
    z_crit = stats.norm.ppf(1 - alpha / 2)
    diff = abs(p2 - p1)
    z_power = (diff / se_null) - z_crit
    power = stats.norm.cdf(z_power)
    return power


def minimum_detectable_effect(p1: float, n1: int, n2: int, alpha: float = 0.05, power: float = 0.80) -> float:
    """Minimum detectable effect (MDE) for given sample sizes.

    Args:
        p1: Baseline proportion.
        n1: Sample size group 1.
        n2: Sample size group 2.
        alpha: Significance level.
        power: Desired statistical power.

    Returns:
        Minimum absolute difference that can be detected.
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    se = np.sqrt(p1 * (1 - p1) * (1/n1 + 1/n2))
    mde = (z_alpha + z_beta) * se
    return mde


def run_ab_test(group_a_stats: dict, group_b_stats: dict, metric: str) -> dict:
    """Run full A/B test analysis for a proportion metric.

    Args:
        group_a_stats: Stats dict for group A.
        group_b_stats: Stats dict for group B.
        metric: Metric name ('approval_rate' or 'default_rate').

    Returns:
        Dict with z-stat, p-value, CI, power, conclusion.
    """
    n_a = group_a_stats["n"]
    n_b = group_b_stats["n"]
    p_a = group_a_stats[metric]
    p_b = group_b_stats[metric]

    z_stat, p_value = two_proportion_ztest(n_a, p_a, n_b, p_b)
    ci_lower, ci_upper = confidence_interval_diff(p_a, p_b, n_a, n_b)
    power = statistical_power(p_a, p_b, n_a, n_b)
    mde = minimum_detectable_effect(p_a, n_a, n_b)

    significant = p_value < 0.05
    conclusion = "SIGNIFICANT" if significant else "NOT SIGNIFICANT"

    return {
        "metric": metric,
        "group_a_rate": round(p_a, 4),
        "group_b_rate": round(p_b, 4),
        "treatment_effect": round(p_b - p_a, 4),
        "z_statistic": round(z_stat, 4),
        "p_value": round(p_value, 6),
        "ci_95_lower": round(ci_lower, 4),
        "ci_95_upper": round(ci_upper, 4),
        "statistical_power": round(power, 4),
        "mde": round(mde, 4),
        "significant_at_0.05": significant,
        "conclusion": conclusion,
    }
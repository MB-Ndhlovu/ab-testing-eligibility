"""
Statistical analysis: two-proportion z-test, confidence intervals, power analysis.
"""
import numpy as np
from scipy import stats


def two_proportion_ztest(n1, p1, n2, p2):
    """
    Two-proportion z-test.

    Args:
        n1: Sample size group 1
        p1: Proportion success group 1
        n2: Sample size group 2
        p2: Proportion success group 2

    Returns:
        dict with z_statistic, p_value (two-tailed)
    """
    p_pool = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    if se == 0:
        return {'z_statistic': 0.0, 'p_value': 1.0, 'se': 0.0}
    z = (p2 - p1) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return {'z_statistic': z, 'p_value': p_value, 'se': se, 'p_pool': p_pool}


def confidence_interval_diff(n1, p1, n2, p2, confidence=0.95):
    """
    Confidence interval for difference in proportions (p2 - p1).

    Args:
        n1, p1: Group 1 size and proportion
        n2, p2: Group 2 size and proportion
        confidence: Confidence level (default 0.95)

    Returns:
        (lower, upper) tuple
    """
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    if se == 0:
        return (0.0, 0.0)
    z = stats.norm.ppf((1 + confidence) / 2)
    diff = p2 - p1
    return (diff - z * se, diff + z * se)


def statistical_power(n, p1, p2, alpha=0.05):
    """
    Compute statistical power for two-proportion z-test.

    Args:
        n: Sample size per group (assumes equal groups)
        p1: Baseline proportion
        p2: Treatment proportion
        alpha: Significance level

    Returns:
        Power (probability of detecting true difference)
    """
    p_pool = (p1 + p2) / 2
    se = np.sqrt(p_pool * (1 - p_pool) * (2 / n))
    if se == 0:
        return 0.0
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    diff = abs(p2 - p1)
    z_beta = (diff / se) - z_alpha
    power = stats.norm.cdf(z_beta)
    return power


def minimum_detectable_effect(n, alpha=0.05, power=0.80):
    """
    Minimum detectable effect (MDE) for given sample size.

    Args:
        n: Sample size per group
        alpha: Significance level
        power: Desired power

    Returns:
        Minimum detectable absolute difference in proportions
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p = 0.5  # conservative estimate
    mde = (z_alpha + z_beta) * np.sqrt(2 * p * (1 - p) / n)
    return mde
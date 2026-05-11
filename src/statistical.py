"""Statistical analysis for A/B testing."""

import numpy as np
from scipy import stats
from typing import Tuple


def two_proportion_z_test(
    x1: int, n1: int, x2: int, n2: int
) -> dict:
    """
    Two-proportion z-test for comparing success rates.

    Args:
        x1: Number of successes in group 1 (control)
        n1: Total sample size group 1
        x2: Number of successes in group 2 (treatment)
        n2: Total sample size group 2

    Returns:
        Dictionary with z_statistic, p_value, ci_lower, ci_upper
    """
    p1 = x1 / n1
    p2 = x2 / n2
    p_diff = p2 - p1

    p_pooled = (x1 + x2) / (n1 + n2)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))

    if se == 0:
        return {
            "z_statistic": 0.0,
            "p_value": 1.0,
            "diff": p_diff,
            "ci_lower": 0.0,
            "ci_upper": 0.0,
            "significant": False,
        }

    z_stat = p_diff / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    se_unpooled = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    ci_lower = p_diff - 1.96 * se_unpooled
    ci_upper = p_diff + 1.96 * se_unpooled

    return {
        "z_statistic": float(z_stat),
        "p_value": float(p_value),
        "diff": float(p_diff),
        "ci_lower": float(ci_lower),
        "ci_upper": float(ci_upper),
        "significant": p_value < 0.05,
        "p1": float(p1),
        "p2": float(p2),
    }


def statistical_power(
    n1: int, n2: int, p1: float, p2: float, alpha: float = 0.05
) -> float:
    """
    Calculate statistical power for two-proportion test.

    Args:
        n1: Sample size group 1
        n2: Sample size group 2
        p1: Proportion group 1
        p2: Proportion group 2
        alpha: Significance level

    Returns:
        Power (probability of detecting true effect)
    """
    p_pooled = (p1 + p2) / 2
    se_null = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    se_alt = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)

    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_diff = abs(p2 - p1) / se_alt

    power = stats.norm.cdf(z_diff - z_crit) + stats.norm.cdf(-z_diff - z_crit)
    return float(power)


def minimum_detectable_effect(
    n1: int, n2: int, power: float = 0.8, alpha: float = 0.05, p1: float = 0.5
) -> float:
    """
    Calculate minimum detectable effect (MDE) for two-proportion test.

    Args:
        n1: Sample size group 1
        n2: Sample size group 2
        power: Desired statistical power
        alpha: Significance level
        p1: Baseline proportion

    Returns:
        Minimum detectable absolute difference
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    se_null = np.sqrt(2 * p1 * (1 - p1) / ((n1 + n2) / 2))
    se_alt = np.sqrt(p1 * (1 - p1) / n1 + p1 * (1 - p1) / n2)

    mde = (z_alpha + z_beta) * np.sqrt(p1 * (1 - p1) / n1 + p1 * (1 - p1) / n2)
    return float(mde)
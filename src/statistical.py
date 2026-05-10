"""
Statistical tests for two-proportion A/B tests.
Implements two-proportion z-test, confidence intervals, power, and MDE.
"""

import numpy as np
from scipy import stats
from typing import NamedTuple


class ZTestResult(NamedTuple):
    """Results from a two-proportion z-test."""
    z_statistic: float
    p_value: float
    ci_lower: float
    ci_upper: float
    diff: float
    se: float
    significant: bool


def two_proportion_ztest(n1: int, x1: int, n2: int, x2: int) -> ZTestResult:
    """
    Two-proportion z-test comparing rates between control and treatment.

    Args:
        n1: Control group sample size
        x1: Control group successes (e.g., approvals)
        n2: Treatment group sample size
        x2: Treatment group successes (e.g., approvals)

    Returns:
        ZTestResult with z-statistic, p-value, 95% CI, and significance
    """
    p1 = x1 / n1 if n1 > 0 else 0
    p2 = x2 / n2 if n2 > 0 else 0

    diff = p2 - p1

    # Pooled proportion under null hypothesis
    p_pooled = (x1 + x2) / (n1 + n2) if (n1 + n2) > 0 else 0

    # Standard error under null (pooled)
    se_null = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2)) if (n1 > 0 and n2 > 0) else 0

    # Standard error for CI (unpooled, more appropriate for CI)
    se_ci = np.sqrt((p1 * (1 - p1) / n1) + (p2 * (1 - p2) / n2)) if (n1 > 0 and n2 > 0) else 0

    z_stat = diff / se_null if se_null > 0 else 0

    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # 95% CI for the difference (using unpooled SE)
    margin = 1.96 * se_ci
    ci_lower = diff - margin
    ci_upper = diff + margin

    significant = p_value < 0.05

    return ZTestResult(
        z_statistic=z_stat,
        p_value=p_value,
        ci_lower=ci_lower,
        ci_upper=ci_upper,
        diff=diff,
        se=se_ci,
        significant=significant,
    )


def compute_power(n1: int, n2: int, p1: float, p2: float, alpha: float = 0.05) -> float:
    """
    Compute statistical power for a two-proportion z-test.

    Args:
        n1: Control group sample size
        n2: Treatment group sample size
        p1: Control proportion
        p2: Treatment proportion
        alpha: Significance level

    Returns:
        Power (probability of detecting a true effect)
    """
    diff = abs(p2 - p1)
    if diff == 0:
        return alpha

    p_pooled = (p1 + p2) / 2
    se_null = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    se_alt = np.sqrt((p1 * (1 - p1) / n1) + (p2 * (1 - p2) / n2))

    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_effect = diff / se_alt

    power = stats.norm.cdf(z_effect - z_crit) + stats.norm.cdf(-z_effect - z_crit)
    return power


def compute_mde(n1: int, n2: int, p1: float, alpha: float = 0.05, power: float = 0.80) -> float:
    """
    Compute minimum detectable effect (MDE) for a two-proportion z-test.

    Args:
        n1: Control group sample size
        n2: Treatment group sample size
        p1: Control proportion
        alpha: Significance level
        power: Desired statistical power (default 0.80)

    Returns:
        Minimum detectable absolute difference in proportions
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    se_null = np.sqrt(2 * p1 * (1 - p1) / ((1/n1 + 1/n2)))

    mde = (z_alpha + z_beta) * se_null
    return mde
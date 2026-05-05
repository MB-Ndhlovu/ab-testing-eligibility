"""
Statistical utilities for A/B testing: two-proportion z-test, confidence intervals,
statistical power, and minimum detectable effect.
"""

import numpy as np
from scipy import stats


def two_proportion_ztest(n1, x1, n2, x2):
    """
    Two-proportion z-test.

    Parameters
    ----------
    n1 : int  — number of trials group 1
    x1 : int  — number of successes group 1
    n2 : int  — number of trials group 2
    x2 : int  — number of successes group 2

    Returns
    -------
    dict with keys: z_stat, p_value, diff, pooled_p, se
    """
    p1 = x1 / n1
    p2 = x2 / n2
    diff = p2 - p1
    pooled_p = (x1 + x2) / (n1 + n2)
    se = np.sqrt(pooled_p * (1 - pooled_p) * (1/n1 + 1/n2))

    if se == 0:
        z_stat = 0.0
    else:
        z_stat = diff / se

    p_value = 2 * stats.norm.sf(abs(z_stat))

    return {
        "z_stat": z_stat,
        "p_value": p_value,
        "diff": diff,
        "pooled_p": pooled_p,
        "se": se,
    }


def confidence_interval_diff(n1, x1, n2, x2, alpha=0.05):
    """
    Wald confidence interval for the difference p2 - p1.

    Returns
    -------
    tuple (lower, upper)
    """
    p1 = x1 / n1
    p2 = x2 / n2
    diff = p2 - p1

    # Unpooled SE for CI (different from pooled in test)
    se = np.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    z_crit = stats.norm.ppf(1 - alpha / 2)

    lower = diff - z_crit * se
    upper = diff + z_crit * se
    return lower, upper


def statistical_power(p1, p2, n, alpha=0.05):
    """
    Compute statistical power for a two-proportion z-test.

    Parameters
    ----------
    p1 : float — baseline proportion
    p2 : float — treatment proportion
    n  : int   — sample size per group
    alpha : float — significance level

    Returns
    -------
    float — power (0 to 1)
    """
    se_null = np.sqrt(2 * p1 * (1 - p1) / n)
    se_alt  = np.sqrt(p1*(1-p1)/n + p2*(1-p2)/n)

    z_crit = stats.norm.ppf(1 - alpha / 2)
    effect = abs(p2 - p1)

    # Power = P(reject H0 | p2 is true)
    z_power = (effect - z_crit * se_null) / se_alt
    power = stats.norm.sf(-z_power)  # one-sided upper tail

    return float(power)


def min_detectable_effect(p1, n, power=0.8, alpha=0.05):
    """
    Find the minimum detectable effect (MDE) given power and sample size.

    Returns
    -------
    float — minimum |p2 - p1| that achieves desired power
    """
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    pooled_var = 2 * p1 * (1 - p1)
    se_null = np.sqrt(pooled_var / n)

    mde = z_crit * se_null + z_beta * np.sqrt(p1*(1-p1)/n + (p1+0.01)*(1-p1-0.01)/n)
    return float(mde)
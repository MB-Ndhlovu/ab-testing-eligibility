"""
Two-proportion z-test, confidence intervals, p-value, statistical power,
and minimum detectable effect (MDE) calculations.
"""

import numpy as np
from scipy import stats

def two_proportion_ztest(n_a: int, n_b: int, x_a: int, x_b: int,
                         alternative: str = "two-sided") -> dict:
    """
    Performs a two-proportion z-test comparing proportions in group A vs B.

    Parameters
    ----------
    n_a, n_b : int — number of trials in each group
    x_a, x_b : int — number of successes in each group
    alternative : str — 'two-sided', 'larger', or 'smaller'

    Returns
    -------
    dict with z_statistic, p_value, ci_95 (lower, upper), significant
    """
    p_a = x_a / n_a
    p_b = x_b / n_b
    p_pool = (x_a + x_b) / (n_a + n_b)

    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    z_stat = (p_b - p_a) / se

    if alternative == "two-sided":
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        z_crit = stats.norm.ppf(0.975)
    elif alternative == "larger":
        p_value = 1 - stats.norm.cdf(z_stat)
        z_crit = stats.norm.ppf(0.95)
    else:
        p_value = stats.norm.cdf(z_stat)
        z_crit = stats.norm.ppf(0.95)

    diff = p_b - p_a
    ci_95 = (diff - z_crit * se, diff + z_crit * se)

    return {
        "z_statistic": round(z_stat, 4),
        "p_value": round(p_value, 6),
        "ci_95": (round(ci_95[0], 5), round(ci_95[1], 5)),
        "significant": p_value < 0.05,
        "p_a": round(p_a, 4),
        "p_b": round(p_b, 4),
        "diff": round(diff, 5),
    }


def compute_power(n_a: int, n_b: int, p_a: float, p_b: float,
                   alpha: float = 0.05) -> float:
    """
    Power of a two-proportion z-test under the given alternative proportion.
    """
    p_pool = (p_a * n_a + p_b * n_b) / (n_a + n_b)
    se_null = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    se_alt  = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
    z_crit  = stats.norm.ppf(1 - alpha / 2)
    z_rej   = z_crit - abs(p_b - p_a) / se_alt
    power   = stats.norm.cdf(z_rej)
    return round(power, 4)


def minimum_detectable_effect(n_a: int, n_b: int,
                               alpha: float = 0.05,
                               power: float = 0.80) -> float:
    """
    Returns the minimum absolute difference in proportions that can be
    detected with the given sample sizes, alpha, and power.
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta  = stats.norm.ppf(power)
    p_avg   = 0.5  # conservative estimate
    se      = np.sqrt(2 * p_avg * (1 - p_avg) * (1 / n_a + 1 / n_b))
    mde     = (z_alpha + z_beta) * se
    return round(mde, 5)
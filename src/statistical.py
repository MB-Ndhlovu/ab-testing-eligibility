"""
Statistical utilities for two-proportion z-tests, confidence intervals,
statistical power, and minimum detectable effect.
"""

import numpy as np
from scipy import stats


def two_proportion_ztest(n_A: int, x_A: int, n_B: int, x_B: int):
    """
    Two-proportion z-test comparing approval/default rates.

    Parameters
    ----------
    n_A : int — sample size group A
    x_A : int — successes (approved / defaulted) group A
    n_B : int — sample size group B
    x_B : int — successes group B

    Returns
    -------
    dict with z_stat, p_value (two-sided), pooled_proportion
    """
    p_A = x_A / n_A
    p_B = x_B / n_B
    p_pool = (x_A + x_B) / (n_A + n_B)

    se_pool = np.sqrt(p_pool * (1 - p_pool) * (1 / n_A + 1 / n_B))
    z_stat = (p_B - p_A) / se_pool
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    return {
        "z_stat": z_stat,
        "p_value": p_value,
        "p_pool": p_pool,
        "p_A": p_A,
        "p_B": p_B,
    }


def confidence_interval_diff(n_A: int, x_A: int, n_B: int, x_B: int, alpha: float = 0.05):
    """
    95% CI for the difference p_B - p_A using Wald-style CI.

    Parameters
    ----------
    n_A, x_A, n_B, x_B : counts
    alpha : significance level (default 0.05 → 95% CI)

    Returns
    -------
    (lower, upper) tuple
    """
    p_A = x_A / n_A
    p_B = x_B / n_B
    diff = p_B - p_A

    se = np.sqrt(p_A * (1 - p_A) / n_A + p_B * (1 - p_B) / n_B)
    z_crit = stats.norm.ppf(1 - alpha / 2)

    return diff - z_crit * se, diff + z_crit * se


def statistical_power(n: int, p_A: float, mde: float, alpha: float = 0.05) -> float:
    """
    Compute power for a two-proportion z-test.

    Parameters
    ----------
    n : int — sample size per group
    p_A : float — baseline proportion
    mde : float — minimum detectable effect (absolute difference p_B - p_A)
    alpha : float — significance level

    Returns
    -------
    power : float in [0, 1]
    """
    p_B = p_A + mde
    p_pool = (p_A + p_B) / 2
    se = np.sqrt(p_pool * (1 - p_pool) * (2 / n))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = (mde / se) - z_crit
    return stats.norm.cdf(z_power)


def min_detectable_effect(n: int, power: float = 0.80, alpha: float = 0.05) -> float:
    """
    Minimum detectable effect given sample size and desired power.

    Parameters
    ----------
    n : int — sample size per group
    power : float — desired statistical power (default 0.80)
    alpha : float — significance level (default 0.05)

    Returns
    -------
    mde : float — minimum absolute difference detectable
    """
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)
    factor = z_crit + z_power
    # Approximation: p_A ≈ 0.5 gives max variance, iterate once for refinement
    p_A = 0.5
    se_approx = np.sqrt(2 * p_A * (1 - p_A) / n)
    mde_approx = factor * se_approx
    # Refine using p_A ≈ 0.1 and p_B ≈ p_A + mde (conservative for small p)
    p_pool = p_A + mde_approx / 2
    se_refined = np.sqrt(2 * p_pool * (1 - p_pool) / n)
    return factor * se_refined
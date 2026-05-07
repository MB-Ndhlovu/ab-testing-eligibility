"""
Statistical functions for two-proportion z-tests.
"""

import numpy as np
from scipy import stats


def two_proportion_ztest(n_a, x_a, n_b, x_b, alpha=0.05):
    """
    Two-proportion z-test comparing two binomial proportions.

    Parameters
    ----------
    n_a : int  — number of trials in group A
    x_a : int  — number of successes in group A
    n_b : int  — number of trials in group B
    x_b : int  — number of successes in group B
    alpha : float — significance level

    Returns
    -------
    dict with z_stat, p_value, ci_lower, ci_upper, significant
    """
    p_a = x_a / n_a
    p_b = x_b / n_b
    diff = p_b - p_a

    # Pooled SE under H0
    p_pooled = (x_a + x_b) / (n_a + n_b)
    se_pooled = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_a + 1 / n_b))

    # Z-statistic
    z_stat = diff / se_pooled if se_pooled > 0 else 0.0

    # P-value (two-tailed)
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # 95% CI for the difference (using unpooled SE)
    se_diff = np.sqrt((p_a * (1 - p_a) / n_a) + (p_b * (1 - p_b) / n_b))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = diff - z_crit * se_diff
    ci_upper = diff + z_crit * se_diff

    significant = p_value < alpha

    return {
        "p_a": p_a,
        "p_b": p_b,
        "diff": diff,
        "z_stat": z_stat,
        "p_value": p_value,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "significant": significant,
        "alpha": alpha,
    }


def statistical_power(n_a, n_b, p_a, p_b, alpha=0.05):
    """
    Compute statistical power for a two-proportion z-test.
    Assumes equal-sized groups.
    """
    se_null = np.sqrt(2 * p_a * (1 - p_a) / n_a)
    se_alt = np.sqrt((p_a * (1 - p_a) / n_a) + (p_b * (1 - p_b) / n_b))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    diff = abs(p_b - p_a)
    z_power = diff / se_alt - z_crit * (se_null / se_alt)
    power = stats.norm.cdf(z_power)
    return power


def minimum_detectable_effect(n_a, n_b, p_a, alpha=0.05, power=0.80):
    """
    Compute the minimum detectable effect (MDE) for given n and power.
    Returns the difference p_b - p_a that would be detected.
    """
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)
    se = np.sqrt(2 * p_a * (1 - p_a) / n_a)
    mde = (z_crit + z_power) * se
    return mde


if __name__ == "__main__":
    # Quick sanity check
    result = two_proportion_ztest(2500, 1550, 2500, 1775)
    print("=== Two-Proportion Z-Test Demo ===")
    for k, v in result.items():
        print(f"  {k}: {v}")
    print(f"\n  power @ 2500/group, p_a=0.62, p_b=0.71: {statistical_power(2500, 2500, 0.62, 0.71):.4f}")
    print(f"  MDE @ 2500/group, p_a=0.62, 80% power: {minimum_detectable_effect(2500, 2500, 0.62):.4f}")
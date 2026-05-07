"""
Statistical analysis for two-proportion z-tests.
"""

import numpy as np
from scipy import stats


def two_proportion_z_test(n_A, x_A, n_B, x_B):
    """
    Perform a two-proportion z-test.

    Parameters:
        n_A: number of trials in group A (control)
        x_A: number of successes in group A
        n_B: number of trials in group B (treatment)
        x_B: number of successes in group B

    Returns:
        dict with z_statistic, p_value, confidence_interval
    """
    p_A = x_A / n_A
    p_B = x_B / n_B

    # Pooled proportion
    p_pooled = (x_A + x_B) / (n_A + n_B)

    # Standard error
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_A + 1/n_B))

    # Z-statistic
    z_stat = (p_B - p_A) / se if se > 0 else 0

    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # 95% Confidence Interval for the difference
    se_diff = np.sqrt((p_A * (1 - p_A) / n_A) + (p_B * (1 - p_B) / n_B))
    ci_95 = (p_B - p_A - 1.96 * se_diff, p_B - p_A + 1.96 * se_diff)

    return {
        'p_A': p_A,
        'p_B': p_B,
        'difference': p_B - p_A,
        'z_statistic': z_stat,
        'p_value': p_value,
        'ci_95_lower': ci_95[0],
        'ci_95_upper': ci_95[1],
        'significant': p_value < 0.05,
    }


def compute_statistical_power(n, p_A, mde, alpha=0.05):
    """
    Compute statistical power for a two-proportion test.

    Parameters:
        n: sample size per group
        p_A: baseline proportion
        mde: minimum detectable effect (absolute difference)
        alpha: significance level

    Returns:
        float: statistical power (0 to 1)
    """
    p_B = p_A + mde

    # Pooled proportion under null
    p_pooled = (2 * p_A + mde) / 2

    # Standard error under null
    se_null = np.sqrt(2 * p_pooled * (1 - p_pooled) / n)

    # Critical value for z
    z_crit = stats.norm.ppf(1 - alpha / 2)

    # Effect size
    effect = abs(p_B - p_A)

    # Power
    if effect > 0:
        se_alt = np.sqrt(p_A * (1 - p_A) / n + p_B * (1 - p_B) / n)
        z_power = (effect - z_crit * se_null) / se_alt
        power = 1 - stats.norm.cdf(z_power)
    else:
        power = alpha / 2

    return power


def minimum_detectable_effect(n, power=0.8, alpha=0.05):
    """
    Compute minimum detectable effect for given sample size and power.

    Parameters:
        n: sample size per group
        power: desired statistical power
        alpha: significance level

    Returns:
        float: minimum detectable effect (absolute)
    """
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    # Approximate MDE for two proportions
    # Using pooled variance estimate
    p = 0.5  # conservative estimate
    mde = (z_crit + z_beta) * np.sqrt(2 * p * (1 - p) / n)

    return mde


if __name__ == '__main__':
    # Test with sample data
    result = two_proportion_z_test(2500, 1550, 2500, 1775)
    print("Two-proportion z-test result:")
    for k, v in result.items():
        if isinstance(v, float):
            print(f"  {k}: {v:.6f}")
        else:
            print(f"  {k}: {v}")
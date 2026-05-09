"""Statistical analysis for A/B testing using two-proportion z-tests."""

import numpy as np
from scipy import stats
from typing import Tuple, Optional


def two_proportion_z_test(
    n1: int, p1: float, n2: int, p2: float, alternative: str = "two-sided"
) -> dict:
    """
    Perform a two-proportion z-test comparing two binomial proportions.

    Args:
        n1: Sample size of group 1 (control)
        p1: Proportion in group 1
        n2: Sample size of group 2 (treatment)
        p2: Proportion in group 2
        alternative: 'two-sided', 'larger', or 'smaller'

    Returns:
        Dictionary with z_statistic, p_value, and confidence_interval
    """
    p_pooled = (n1 * p1 + n2 * p2) / (n1 + n2)

    if p_pooled == 0 or p_pooled == 1:
        return {
            "z_statistic": 0.0,
            "p_value": 1.0,
            "ci_lower": 0.0,
            "ci_upper": 0.0,
            "difference": p2 - p1,
        }

    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    z_stat = (p2 - p1) / se

    if alternative == "two-sided":
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    elif alternative == "larger":
        p_value = 1 - stats.norm.cdf(z_stat)
    else:
        p_value = stats.norm.cdf(z_stat)

    # 95% CI for the difference using unpooled standard error
    se_unpooled = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z_crit = stats.norm.ppf(0.975)
    ci_lower = (p2 - p1) - z_crit * se_unpooled
    ci_upper = (p2 - p1) + z_crit * se_unpooled

    return {
        "z_statistic": z_stat,
        "p_value": p_value,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "difference": p2 - p1,
        "se": se_unpooled,
    }


def statistical_power(
    n1: int, n2: int, p1: float, p2: float, alpha: float = 0.05
) -> float:
    """
    Calculate the statistical power for a two-proportion z-test.

    Args:
        n1: Sample size of group 1
        n2: Sample size of group 2
        p1: Baseline proportion
        p2: Target proportion
        alpha: Significance level

    Returns:
        Power (probability of detecting true effect)
    """
    p_pooled = (n1 * p1 + n2 * p2) / (n1 + n2)
    se_null = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    se_alt = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)

    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_effect = (p2 - p1) / se_alt

    power = stats.norm.cdf(z_effect - z_crit * (se_null / se_alt)) + \
            stats.norm.cdf(-z_effect - z_crit * (se_null / se_alt))

    return min(1.0, max(0.0, power))


def minimum_detectable_effect(
    n1: int, n2: int, alpha: float = 0.05, power: float = 0.80, p1: float = 0.5
) -> float:
    """
    Calculate the minimum detectable effect (MDE) for a two-proportion test.

    Args:
        n1: Sample size of group 1
        n2: Sample size of group 2
        alpha: Significance level
        power: Desired statistical power
        p1: Baseline proportion

    Returns:
        Minimum detectable effect (absolute difference)
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    p_pooled = (n1 * p1 + n2 * 0.5) / (n1 + n2)  # assume p2 ~ 0.5 for MDE
    se_null = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))

    p2_guess = p1 + 0.05  # start with 5% absolute difference estimate
    se_alt = np.sqrt(p1 * (1 - p1) / n1 + p2_guess * (1 - p2_guess) / n2)

    # Iterative approach for MDE
    mde = 0.01
    for _ in range(100):
        se_alt_mde = np.sqrt(p1 * (1 - p1) / n1 + (p1 + mde) * (1 - p1 - mde) / n2)
        if se_alt_mde <= 0:
            mde += 0.01
            continue
        z_eff = mde / se_alt_mde
        current_power = stats.norm.cdf(z_eff - z_alpha) + stats.norm.cdf(-z_eff - z_alpha)
        if current_power >= power:
            return mde
        mde += 0.005

    return mde


if __name__ == "__main__":
    # Demo
    result = two_proportion_z_test(2500, 0.62, 2500, 0.71)
    print("Two-proportion z-test:")
    for k, v in result.items():
        print(f"  {k}: {v:.4f}")

    power = statistical_power(2500, 2500, 0.62, 0.71)
    print(f"\nStatistical power: {power:.4f}")

    mde = minimum_detectable_effect(2500, 2500, 0.05, 0.80, 0.62)
    print(f"Minimum detectable effect: {mde:.4f}")
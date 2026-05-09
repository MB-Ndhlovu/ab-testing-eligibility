import numpy as np
from scipy import stats


def two_proportion_ztest(n1: int, x1: int, n2: int, x2: int) -> dict:
    """Two-proportion z-test for difference in proportions.

    Args:
        n1: Number of trials in group 1
        x1: Number of successes in group 1
        n2: Number of trials in group 2
        x2: Number of successes in group 2

    Returns:
        dict with z_statistic, p_value, ci_lower, ci_upper, significant
    """
    p1 = x1 / n1
    p2 = x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)

    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z_stat = (p2 - p1) / se

    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    diff = p2 - p1
    se_diff = np.sqrt((p1 * (1 - p1) / n1) + (p2 * (1 - p2) / n2))
    ci_lower = diff - 1.96 * se_diff
    ci_upper = diff + 1.96 * se_diff

    return {
        "p1": p1,
        "p2": p2,
        "difference": diff,
        "z_statistic": z_stat,
        "p_value": p_value,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "significant": p_value < 0.05,
    }


def statistical_power(n1: int, n2: int, p1: float, p2: float, alpha: float = 0.05) -> float:
    """Calculate statistical power for two-proportion z-test.

    Args:
        n1: Sample size group 1
        n2: Sample size group 2
        p1: Baseline proportion
        p2: Treatment proportion
        alpha: Significance level

    Returns:
        Power as a probability (0 to 1)
    """
    z_crit = stats.norm.ppf(1 - alpha / 2)
    p_pool = (p1 + p2) / 2
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z_ncp = abs(p2 - p1) / se
    power = 1 - stats.norm.cdf(z_crit - z_ncp) + stats.norm.cdf(-z_crit - z_ncp)
    return power


def minimum_detectable_effect(n1: int, n2: int, p1: float, alpha: float = 0.05,
                               power: float = 0.80) -> float:
    """Find minimum detectable effect for given sample sizes.

    Args:
        n1: Sample size group 1
        n2: Sample size group 2
        p1: Baseline proportion
        alpha: Significance level
        power: Desired statistical power

    Returns:
        Minimum detectable absolute difference in proportions
    """
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p_pool = p1 * (1 - p1)
    se = np.sqrt(p_pool * (1 / n1 + 1 / n2))
    mde = (z_crit + z_beta) * se
    return mde


if __name__ == "__main__":
    result = two_proportion_ztest(n1=2500, x1=1550, n2=2500, x2=1775)
    print("Two-proportion z-test result:")
    for k, v in result.items():
        print(f"  {k}: {v}")
    print(f"\nPower: {statistical_power(2500, 2500, 0.62, 0.71):.4f}")
    print(f"MDE: {minimum_detectable_effect(2500, 2500, 0.62):.4f}")
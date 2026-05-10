"""Statistical analysis for two-proportion z-tests."""
import numpy as np
from scipy import stats


def two_proportion_ztest(n1, x1, n2, x2):
    """Two-proportion z-test for comparing two success proportions.

    Args:
        n1: Sample size group 1
        x1: Number of successes group 1
        n2: Sample size group 2
        x2: Number of successes group 2

    Returns:
        dict with z_stat, p_value, ci_lower, ci_upper, significance
    """
    p1 = x1 / n1
    p2 = x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)

    # Standard error under null hypothesis
    se_null = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))

    # Z-statistic
    z_stat = (p1 - p2) / se_null if se_null > 0 else 0

    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # 95% Confidence Interval for the difference (Wald method)
    se_diff = np.sqrt((p1 * (1 - p1) / n1) + (p2 * (1 - p2) / n2))
    margin = 1.96 * se_diff
    ci_lower = (p1 - p2) - margin
    ci_upper = (p1 - p2) + margin

    # Statistical significance at alpha = 0.05
    significant = p_value < 0.05

    return {
        'z_statistic': round(z_stat, 4),
        'p_value': round(p_value, 6),
        'ci_95_lower': round(ci_lower, 6),
        'ci_95_upper': round(ci_upper, 6),
        'significant': significant,
        'p1': round(p1, 6),
        'p2': round(p2, 6),
        'difference': round(p1 - p2, 6)
    }


def statistical_power(n, p1, p2, alpha=0.05):
    """Calculate statistical power for a two-proportion z-test.

    Args:
        n: Sample size per group
        p1: Proportion in group 1 (control)
        p2: Proportion in group 2 (treatment)
        alpha: Significance level (default 0.05)

    Returns:
        Power as a probability (0 to 1)
    """
    se_diff = np.sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / n)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_effect = abs(p1 - p2) / se_diff

    power = stats.norm.cdf(z_effect - z_crit) + stats.norm.cdf(-z_effect - z_crit)
    return round(min(power, 1.0), 4)


def minimum_detectable_effect(n, power=0.8, alpha=0.05, p1=0.5):
    """Calculate minimum detectable effect (MDE) for a given power.

    Args:
        n: Sample size per group
        power: Desired statistical power (default 0.8)
        alpha: Significance level (default 0.05)
        p1: Baseline proportion (default 0.5)

    Returns:
        Minimum detectable effect as absolute proportion difference
    """
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    se_base = np.sqrt(p1 * (1 - p1) * 2 / n)
    mde = (z_crit + z_beta) * se_base
    return round(mde, 6)


if __name__ == '__main__':
    # Quick test
    result = two_proportion_ztest(5000, 3100, 5000, 3550)
    print("Test result:", result)
    print("Power:", statistical_power(5000, 0.62, 0.71))
    print("MDE:", minimum_detectable_effect(5000))
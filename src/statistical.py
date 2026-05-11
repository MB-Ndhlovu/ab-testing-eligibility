"""Statistical tests for A/B testing."""

import numpy as np
from scipy import stats

def two_proportion_ztest(n1, p1, n2, p2):
    """
    Two-proportion z-test for comparing two proportions.

    Parameters
    ----------
    n1, n2 : int
        Sample sizes for group 1 and group 2
    p1, p2 : float
        Observed proportions for group 1 and group 2

    Returns
    -------
    dict
        Contains z_statistic, p_value, ci_lower, ci_upper (95% CI for difference)
    """
    # Pooled proportion under null hypothesis
    p_pooled = (n1 * p1 + n2 * p2) / (n1 + n2)

    # Standard error
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))

    # Z-statistic
    z_stat = (p2 - p1) / se if se > 0 else 0

    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # 95% CI for difference (using unpooled standard error)
    se_diff = np.sqrt(p1 * (1 - p1) / n1 + p2 * (2 - p2) / n2)
    ci_lower = (p2 - p1) - 1.96 * se_diff
    ci_upper = (p2 - p1) + 1.96 * se_diff

    return {
        'z_statistic': z_stat,
        'p_value': p_value,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
    }

def statistical_power(n, p1, p2, alpha=0.05):
    """
    Calculate statistical power for a two-proportion z-test.

    Parameters
    ----------
    n : int
        Sample size per group (assumes equal group sizes)
    p1, p2 : float
        Expected proportions
    alpha : float
        Significance level (default 0.05)

    Returns
    -------
    float
        Statistical power (probability of detecting true difference)
    """
    # Pooled proportion under null
    p_pooled = (p1 + p2) / 2

    # Standard error under null
    se_null = np.sqrt(2 * p_pooled * (1 - p_pooled) / n)

    # Critical value (z for alpha/2)
    z_crit = stats.norm.ppf(1 - alpha / 2)

    # Effect size
    delta = abs(p2 - p1)

    # Power = P(reject null | true effect = delta)
    # This is P(|Z| > z_crit - delta/se_null)
    se_alt = np.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
    z_power = (delta / se_alt) - z_crit * (se_null / se_alt)

    power = 1 - stats.norm.cdf(z_power) + stats.norm.cdf(-z_power - 2 * (delta / se_alt))
    return max(0, min(1, power))

def minimum_detectable_effect(n, power=0.8, alpha=0.05, p1=0.5):
    """
    Calculate minimum detectable effect (MDE) for a given power.

    Parameters
    ----------
    n : int
        Sample size per group
    power : float
        Desired statistical power (default 0.8)
    alpha : float
        Significance level (default 0.05)
    p1 : float
        Baseline proportion (default 0.5)

    Returns
    -------
    float
        Minimum detectable effect (absolute difference in proportions)
    """
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)

    # MDE formula for two-proportion test
    p2 = np.linspace(0.01, 0.99, 1000)
    delta = np.abs(p2 - p1)
    se_pooled = np.sqrt(2 * ((p1 + p2) / 2) * (1 - (p1 + p2) / 2) / n)

    # Power calculation
    z_effect = (delta / se_pooled) - z_crit
    power_vals = stats.norm.cdf(z_effect)

    idx = np.argmin(np.abs(power_vals - power))
    return delta[idx]

def test_significance(p_value, alpha=0.05):
    """Return significance conclusion."""
    if p_value < alpha:
        return "SIGNIFICANT"
    return "NOT SIGNIFICANT"

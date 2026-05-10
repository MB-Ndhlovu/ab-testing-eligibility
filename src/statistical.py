import numpy as np
from scipy import stats

def two_proportion_ztest(n1, p1, n2, p2):
    """Two-proportion z-test for comparing two proportions."""
    p_pooled = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    z = (p2 - p1) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value

def confidence_interval(n1, p1, n2, p2, confidence=0.95):
    """95% CI for the difference between two proportions."""
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    diff = p2 - p1
    se = np.sqrt((p1 * (1 - p1) / n1) + (p2 * (1 - p2) / n2))
    lower = diff - z * se
    upper = diff + z * se
    return lower, upper

def statistical_power(n, p1, p2, alpha=0.05):
    """Calculate statistical power for a two-proportion z-test."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    p_pooled = (p1 + p2) / 2
    se = np.sqrt(p_pooled * (1 - p_pooled) * (2 / n))
    z_effect = abs(p2 - p1) / se
    power = stats.norm.cdf(z_effect - z_alpha) + stats.norm.cdf(-z_effect - z_alpha)
    return power

def minimum_detectable_effect(n, alpha=0.05, power=0.80):
    """Find the minimum detectable effect size for given n, alpha, power."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p = 0.5
    mde = (z_alpha + z_beta) * np.sqrt(2 * p * (1 - p) / n)
    return mde
import numpy as np
from scipy import stats

def two_proportion_ztest(n1, p1, n2, p2):
    """Two-proportion z-test."""
    p_pool = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z = (p2 - p1) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value

def confidence_interval(p1, p2, n1, n2, alpha=0.05):
    """95% CI for difference in proportions."""
    se = np.sqrt((p1*(1-p1)/n1) + (p2*(1-p2)/n2))
    z_crit = stats.norm.ppf(1 - alpha/2)
    diff = p2 - p1
    return (diff - z_crit * se, diff + z_crit * se)

def statistical_power(n1, n2, p1, p2, alpha=0.05):
    """Approximate statistical power."""
    p_pool = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z_crit = stats.norm.ppf(1 - alpha/2)
    z_ncp = abs(p2 - p1) / se
    power = 1 - stats.norm.cdf(z_crit - z_ncp)
    return power

def min_detectable_effect(n1, n2, p1, alpha=0.05, power=0.80):
    """Minimum detectable effect given sample sizes."""
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    p_pool = p1  # use baseline
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    mde = (z_alpha + z_beta) * se
    return mde
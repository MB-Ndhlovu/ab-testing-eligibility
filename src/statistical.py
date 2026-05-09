"""Statistical analysis for two-proportion z-tests."""
from scipy import stats
import numpy as np

def two_proportion_ztest(n1, p1, n2, p2):
    """Two-proportion z-test comparing two success proportions."""
    p_pool = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z = (p1 - p2) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value

def confidence_interval(n1, p1, n2, p2, alpha=0.05):
    """95% CI for the difference between two proportions."""
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    diff = p1 - p2
    return (diff - z_crit * se, diff + z_crit * se)

def statistical_power(n, p1, p2, alpha=0.05):
    """Approximate power for a two-proportion z-test."""
    p_pool = (p1 + p2) / 2
    se = np.sqrt(p_pool * (1 - p_pool) * (2 / n))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_ncp = abs(p1 - p2) / se
    power = 1 - stats.norm.cdf(z_crit - z_ncp)
    return power

def minimum_detectable_effect(n, p, alpha=0.05, power=0.80):
    """Minimum detectable effect (absolute) for given n, baseline p, alpha, power."""
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p_pool = p
    se = np.sqrt(2 * p_pool * (1 - p_pool) / n)
    mde = (z_crit + z_beta) * se
    return mde
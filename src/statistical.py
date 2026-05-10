"""Statistical analysis for two-proportion z-tests."""

import numpy as np
from scipy import stats


def two_proportion_ztest(n_success, n_total, p_null=0.0):
    """Two-proportion z-test.
    
    Args:
        n_success: array-like of successes in each group
        n_total: array-like of totals in each group
        p_null: null hypothesis proportion (typically 0)
    
    Returns:
        z_statistic, p_value
    """
    n_success = np.asarray(n_success)
    n_total = np.asarray(n_total)
    
    p1, p2 = n_success[0] / n_total[0], n_success[1] / n_total[1]
    p_pool = n_success.sum() / n_total.sum()
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n_total[0] + 1/n_total[1]))
    
    if se == 0:
        return np.inf, 0.0
    
    z = (p1 - p2 - p_null) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    
    return z, p_value


def confidence_interval(n_success, n_total, alpha=0.05):
    """95% CI for difference in proportions."""
    n_success = np.asarray(n_success)
    n_total = np.asarray(n_total)
    
    p1, p2 = n_success[0] / n_total[0], n_success[1] / n_total[1]
    diff = p1 - p2
    se = np.sqrt(p1*(1-p1)/n_total[0] + p2*(1-p2)/n_total[1])
    z_crit = stats.norm.ppf(1 - alpha/2)
    
    return diff - z_crit*se, diff + z_crit*se


def statistical_power(n_total, p1, p2, alpha=0.05):
    """Calculate statistical power for two-proportion test."""
    p_pool = (p1 + p2) / 2
    se = np.sqrt(p_pool * (1 - p_pool) * (2 / n_total))
    diff = abs(p1 - p2)
    z_crit = stats.norm.ppf(1 - alpha/2)
    z_power = (diff - z_crit * se) / se
    return stats.norm.cdf(z_power)


def minimum_detectable_effect(n_total, alpha=0.05, power=0.80):
    """Minimum detectable effect (proportion difference) for given power."""
    z_crit = stats.norm.ppf(1 - alpha/2)
    z_power = stats.norm.ppf(power)
    return (z_crit + z_power) / np.sqrt(2 / n_total)
"""
Statistical tests for A/B testing: two-proportion z-test, confidence intervals, power analysis.
"""

import numpy as np
from scipy import stats

def two_proportion_ztest(n1, p1, n2, p2):
    """Two-proportion z-test for difference in proportions."""
    p_pooled = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    z = (p1 - p2) / se if se > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value

def confidence_interval_diff(n1, p1, n2, p2, alpha=0.05):
    """95% confidence interval for difference in proportions."""
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    diff = p1 - p2
    return (diff - z_crit * se, diff + z_crit * se)

def power_analysis(p1, p2, alpha=0.05, power=0.80):
    """Minimum detectable effect (MDE) at given power."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    
    def solve_n(p1, p2, z_alpha, z_beta):
        p_avg = (p1 + p2) / 2
        numerator = (z_alpha * np.sqrt(2 * p_avg * (1 - p_avg)) +
                     z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2)))**2
        denominator = (p1 - p2)**2
        return numerator / denominator if denominator > 0 else float('inf')
    
    n_required = solve_n(p1, p2, z_alpha, z_beta)
    return int(np.ceil(n_required))

def minimum_detectable_effect(n, alpha=0.05, power=0.80, p_base=0.5):
    """Find MDE for given sample size n."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    
    mde = (z_alpha + z_beta) * np.sqrt(2 * p_base * (1 - p_base) / n)
    return mde
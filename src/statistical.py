import numpy as np
from scipy import stats

def two_proportion_ztest(n1, x1, n2, x2, alternative='two-sided'):
    p1 = x1 / n1
    p2 = x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z_stat = (p2 - p1) / se
    
    if alternative == 'two-sided':
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    elif alternative == 'larger':
        p_value = 1 - stats.norm.cdf(z_stat)
    else:
        p_value = stats.norm.cdf(z_stat)
    
    return z_stat, p_value, p1, p2, se

def confidence_interval(n1, p1, n2, p2, alpha=0.05):
    z_crit = stats.norm.ppf(1 - alpha/2)
    diff = p2 - p1
    se_diff = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    ci_lower = diff - z_crit * se_diff
    ci_upper = diff + z_crit * se_diff
    return (ci_lower, ci_upper)

def statistical_power(n1, n2, p1, p2, alpha=0.05):
    se_null = np.sqrt(p1 * (1 - p1) * (1/n1 + 1/n2))
    z_crit = stats.norm.ppf(1 - alpha/2)
    z_effect = abs(p2 - p1) / se_null
    power = stats.norm.cdf(z_effect - z_crit) + stats.norm.cdf(-z_effect - z_crit)
    return power

def minimum_detectable_effect(n1, n2, alpha=0.05, power=0.80):
    z_crit = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    p_avg = 0.5
    se = np.sqrt(p_avg * (1 - p_avg) * (1/n1 + 1/n2))
    mde = (z_crit + z_beta) * se
    return mde
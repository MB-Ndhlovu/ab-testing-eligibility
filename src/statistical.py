import numpy as np
from scipy import stats

def two_proportion_z_test(n1, p1, n2, p2):
    p_pooled = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    z = (p2 - p1) / se if se > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value

def confidence_interval(p1, p2, n1, n2, alpha=0.05):
    diff = p2 - p1
    se = np.sqrt((p1 * (1 - p1) / n1) + (p2 * (1 - p2) / n2))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    margin = z_crit * se
    return (diff - margin, diff + margin)

def statistical_power(p1, p2, n, alpha=0.05):
    z_crit = stats.norm.ppf(1 - alpha / 2)
    p_pooled = (p1 + p2) / 2
    se = np.sqrt(2 * p_pooled * (1 - p_pooled) / n)
    z_power = (abs(p2 - p1) / se) - z_crit
    return stats.norm.cdf(z_power)

def minimum_detectable_effect(n, alpha=0.05, power=0.8):
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p = 0.5
    return (z_crit + z_beta) * np.sqrt(2 * p * (1 - p) / n)
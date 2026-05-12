import numpy as np
from scipy import stats

def two_proportion_ztest(n1, p1, n2, p2):
    p_pool = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se if se > 0 else 0.0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value

def confidence_interval(n1, p1, n2, p2, alpha=0.05):
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    diff = p2 - p1
    return (diff - z_crit * se, diff + z_crit * se)

def statistical_power(n, p1, p2, alpha=0.05):
    z_crit = stats.norm.ppf(1 - alpha / 2)
    p_pool = (p1 + p2) / 2
    se = np.sqrt(p_pool * (1 - p_pool) * (2 / n))
    z_ncp = (abs(p2 - p1)) / se
    power = 1 - stats.norm.cdf(z_crit - z_ncp)
    return power

def minimum_detectable_effect(n, p1, alpha=0.05, power=0.80):
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)
    p_pool = p1
    se = np.sqrt(p_pool * (1 - p_pool) * (2 / n))
    mde = (z_crit + z_power) * se
    return mde
import numpy as np
from scipy import stats

def two_proportion_ztest(n1, p1, n2, p2):
    p_pooled = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    z = (p2 - p1) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value

def confidence_interval(n1, p1, n2, p2, alpha=0.05):
    diff = p2 - p1
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = diff - z_crit * se
    ci_upper = diff + z_crit * se
    return (ci_lower, ci_upper)

def statistical_power(n, p1, p2, alpha=0.05):
    z_crit = stats.norm.ppf(1 - alpha / 2)
    p_pooled = (p1 + p2) / 2
    se = np.sqrt(p_pooled * (1 - p_pooled) * (2 / n))
    z_power = (abs(p2 - p1) - z_crit * np.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)) / np.sqrt(p_pooled * (1 - p_pooled) * (2 / n))
    power = stats.norm.cdf(z_power)
    return max(0, min(1, power))

def minimum_detectable_effect(n, alpha=0.05, power=0.80):
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)
    mde = (z_crit + z_power) * np.sqrt(0.5 * 0.5 * (2 / n))
    return mde
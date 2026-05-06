import numpy as np
from scipy import stats

def two_proportion_ztest(n1, p1, n2, p2, alternative='two-sided'):
    p_pool = (p1 * n1 + p2 * n2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    if se == 0:
        return 0.0, 1.0
    
    if alternative == 'larger':
        z = (p2 - p1) / se
        p_value = 1 - stats.norm.cdf(z)
    elif alternative == 'smaller':
        z = (p1 - p2) / se
        p_value = stats.norm.cdf(z)
    else:
        z = (p1 - p2) / se
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    
    return float(z), float(p_value)

def confidence_interval_diff(n1, p1, n2, p2, confidence=0.95):
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    if se == 0:
        return (p1 - p2, p1 - p2)
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    diff = p2 - p1
    return (float(diff - z * se), float(diff + z * se))

def statistical_power(n, p1, p2, alpha=0.05):
    p_pool = (p1 + p2) / 2
    se = np.sqrt(p_pool * (1 - p_pool) * (2 / n))
    if se == 0:
        return 0.0
    z_crit = stats.norm.ppf(1 - alpha)
    z_power = (abs(p2 - p1) / se) - z_crit
    power = stats.norm.cdf(z_power)
    return float(power)

def minimum_detectable_effect(n, alpha=0.05, power=0.8):
    z_alpha = stats.norm.ppf(1 - alpha)
    z_beta = stats.norm.ppf(power)
    p = 0.5
    se = np.sqrt(2 * p * (1 - p) / n)
    mde = (z_alpha + z_beta) * se
    return float(mde)

if __name__ == '__main__':
    n1, p1 = 2500, 0.62
    n2, p2 = 2500, 0.71
    z, p = two_proportion_ztest(n1, p1, n2, p2, alternative='larger')
    ci = confidence_interval_diff(n1, p1, n2, p2)
    print(f"z={z:.3f}, p={p:.4f}, 95% CI={ci}")
    print(f"Power: {statistical_power(2500, 0.62, 0.71):.3f}")
    print(f"MDE: {minimum_detectable_effect(2500):.4f}")
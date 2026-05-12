import numpy as np
from scipy import stats

def two_proportion_ztest(n1, p1, n2, p2):
    p_pool = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    if se == 0:
        return 0.0, 1.0
    z = (p1 - p2) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value

def confidence_interval(n1, p1, n2, p2, confidence=0.95):
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    if se == 0:
        return (p1 - p2, p1 - p2)
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    diff = p1 - p2
    return (diff - z * se, diff + z * se)

def statistical_power(n1, p1, n2, p2, alpha=0.05, n1_ratio=1.0):
    p_pool = (n1 * p1 + n2 * p2) / (n1 + n2)
    se_null = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    if se_null == 0:
        return 0.0
    z_crit = stats.norm.ppf(1 - alpha / 2)
    diff = abs(p1 - p2)
    se_alt = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    if se_alt == 0:
        return 0.0
    z_alt = (diff - z_crit * se_null) / se_alt
    power = 1 - stats.norm.cdf(z_alt)
    return power

def minimum_detectable_effect(n1, n2, alpha=0.05, power=0.8):
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p_pool = 0.5
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    if se == 0:
        return float("inf")
    mde = (z_crit + z_beta) * se
    return mde

def test_metric(label, n1, p1, n2, p2, alpha=0.05):
    z, p = two_proportion_ztest(n1, p1, n2, p2)
    ci_low, ci_high = confidence_interval(n1, p1, n2, p2)
    power = statistical_power(n1, p1, n2, p2, alpha)
    mde = minimum_detectable_effect(n1, n2, alpha)
    significant = bool(p < alpha)
    return {
        "metric": label,
        "z_statistic": round(z, 4),
        "p_value": round(p, 6),
        "ci_95_low": round(ci_low, 6),
        "ci_95_high": round(ci_high, 6),
        "significant": significant,
        "power": round(power, 4),
        "mde": round(mde, 6),
        "control_rate": p1,
        "treatment_rate": p2,
    }

if __name__ == "__main__":
    result = test_metric("approval_rate", 2500, 0.62, 2500, 0.71)
    print(result)
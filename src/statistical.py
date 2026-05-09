import numpy as np
from scipy import stats

def two_proportion_ztest(n1, x1, n2, x2):
    p1 = x1 / n1 if n1 > 0 else 0
    p2 = x2 / n2 if n2 > 0 else 0
    p_pool = (x1 + x2) / (n1 + n2) if (n1 + n2) > 0 else 0

    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2)) if (n1 > 0 and n2 > 0) else 0
    z = (p2 - p1) / se if se > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    return {"z_statistic": round(z, 4), "p_value": round(p_value, 6), "p_pool": round(p_pool, 4)}

def confidence_interval(n1, x1, n2, x2, confidence=0.95):
    p1 = x1 / n1 if n1 > 0 else 0
    p2 = x2 / n2 if n2 > 0 else 0
    diff = p2 - p1
    se = np.sqrt((p1*(1-p1)/n1) + (p2*(1-p2)/n2)) if (n1 > 0 and n2 > 0) else 0
    z_crit = stats.norm.ppf((1 + confidence) / 2)
    margin = z_crit * se
    return {"diff": round(diff, 4), "ci_lower": round(diff - margin, 4), "ci_upper": round(diff + margin, 4)}

def statistical_power(n1, n2, p1, p2, alpha=0.05):
    z_crit = stats.norm.ppf(1 - alpha / 2)
    p_pool = (p1 + p2) / 2
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z_power = (abs(p2 - p1) / se) if se > 0 else 0
    power = stats.norm.cdf(z_power - z_crit) + stats.norm.cdf(-z_power - z_crit)
    return {"power": round(power, 4), "z_crit": round(z_crit, 4)}

def minimum_detectable_effect(n1, n2, alpha=0.05, power=0.80):
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p_pool = 0.5
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    mde = (z_crit + z_beta) * se
    return {"mde": round(mde, 4), "mde_relative": f"{(mde * 100):.2f}% of baseline"}

if __name__ == "__main__":
    # Example: approval rate test
    result = two_proportion_ztest(2500, 1550, 2500, 1775)
    ci = confidence_interval(2500, 1550, 2500, 1775)
    pwr = statistical_power(2500, 2500, 0.62, 0.71)
    mde = minimum_detectable_effect(2500, 2500)
    print("Z-test:", result)
    print("CI:", ci)
    print("Power:", pwr)
    print("MDE:", mde)
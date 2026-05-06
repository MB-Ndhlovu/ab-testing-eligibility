import numpy as np
from scipy import stats


def two_proportion_ztest(n1, p1, n2, p2):
    p_pooled = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n1 + 1 / n2))
    z = (p2 - p1) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return {
        "z_statistic": z,
        "p_value": p_value,
        "p_pooled": p_pooled
    }


def confidence_interval_diff(n1, p1, n2, p2, confidence=0.95):
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z_crit = stats.norm.ppf((1 + confidence) / 2)
    diff = p2 - p1
    ci_lower = diff - z_crit * se
    ci_upper = diff + z_crit * se
    return {"diff": diff, "ci_lower": ci_lower, "ci_upper": ci_upper, "se": se}


def statistical_power(n1, n2, p1, p2, alpha=0.05):
    z_crit = stats.norm.ppf(1 - alpha / 2)
    p_pooled = (n1 * p1 + n2 * p2) / (n1 + n2)
    se_null = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n1 + 1 / n2))
    se_alt = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    z_alt = (p2 - p1) / se_alt
    power = 1 - stats.norm.cdf(z_crit - (p2 - p1) / se_alt) + \
            stats.norm.cdf(-z_crit - (p2 - p1) / se_alt)
    return {"power": power, "z_critical": z_crit, "z_alt": z_alt}


def minimum_detectable_effect(n1, n2, p1, alpha=0.05, power=0.80):
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    se = np.sqrt(p1 * (1 - p1) / n1 + p1 * (1 - p1) / n2)
    mde = (z_crit + z_beta) * se
    return {"mde": mde, "mde_relative": mde / p1}


def test_significance(p_value, alpha=0.05):
    return p_value < alpha


if __name__ == "__main__":
    result = two_proportion_ztest(2500, 0.62, 2500, 0.71)
    print("Z-test result:", result)
    ci = confidence_interval_diff(2500, 0.62, 2500, 0.71)
    print("95% CI:", ci)
    pwr = statistical_power(2500, 2500, 0.62, 0.71)
    print("Power:", pwr)
    mde = minimum_detectable_effect(2500, 2500, 0.62)
    print("MDE:", mde)
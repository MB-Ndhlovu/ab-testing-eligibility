"""Two-proportion z-test, confidence intervals, power analysis."""
import numpy as np
from scipy import stats

def two_proportion_ztest(n1, x1, n2, x2):
    """Two-proportion z-test.
    
    Returns z-statistic, p-value (two-tailed).
    """
    p1 = x1 / n1
    p2 = x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z = (p1 - p2) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value

def confidence_interval(n1, x1, n2, x2, confidence=0.95):
    """95% CI for the difference in proportions."""
    p1 = x1 / n1
    p2 = x2 / n2
    diff = p1 - p2
    z_crit = stats.norm.ppf(1 - (1 - confidence) / 2)
    se = np.sqrt((p1 * (1 - p1)) / n1 + (p2 * (1 - p2)) / n2)
    margin = z_crit * se
    return diff - margin, diff + margin

def statistical_power(n, p1, p2, alpha=0.05):
    """Compute statistical power given sample size and proportions."""
    z_crit = stats.norm.ppf(1 - alpha / 2)
    p_pool = (p1 + p2) / 2
    se = np.sqrt(p_pool * (1 - p_pool) * (2 / n))
    z_power = (abs(p1 - p2) / se) - z_crit
    power = stats.norm.cdf(z_power)
    return power

def minimum_detectable_effect(n, power=0.80, alpha=0.05):
    """Find minimum detectable effect size given n, power, alpha."""
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)
    mde = (z_crit + z_power) * np.sqrt(0.5 * 0.5 * (2 / n))
    return mde

def test_metric(n1, x1, n2, x2, metric_name, higher_is_better=True):
    z, p = two_proportion_ztest(n1, x1, n2, x2)
    ci_low, ci_high = confidence_interval(n1, x1, n2, x2)
    significant = p < 0.05

    p1 = x1 / n1
    p2 = x2 / n2
    effect = p2 - p1

    return {
        "metric": metric_name,
        "group_a_rate": p1,
        "group_b_rate": p2,
        "treatment_effect": effect,
        "z_statistic": round(z, 4),
        "p_value": round(p, 6),
        "ci_95_low": round(ci_low, 6),
        "ci_95_high": round(ci_high, 6),
        "significant": significant,
        "direction": "improvement" if (significant and effect > 0 and higher_is_better) or (significant and effect < 0 and not higher_is_better) else "degradation" if significant else "no significant difference",
    }

if __name__ == "__main__":
    # Demo
    n = 5000
    x1 = int(0.62 * n)
    x2 = int(0.71 * n)
    result = test_metric(n, x1, n, x2, "approval_rate", higher_is_better=True)
    print(result)
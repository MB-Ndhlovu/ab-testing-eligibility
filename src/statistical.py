import numpy as np
from scipy import stats

def two_proportion_ztest(n1, p1, n2, p2):
    """Two-proportion z-test for comparing two rates.

    Args:
        n1: Sample size group 1
        p1: Observed proportion group 1
        n2: Sample size group 2
        p2: Observed proportion group 2

    Returns:
        dict with z_statistic, p_value, confidence_interval
    """
    p_pooled = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    z = (p2 - p1) / se

    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    # 95% CI for the difference (p2 - p1)
    se_diff = np.sqrt(p1*(1-p1)/n1 + p2*(1-p2)/n2)
    ci_lower = (p2 - p1) - 1.96 * se_diff
    ci_upper = (p2 - p1) + 1.96 * se_diff

    return {
        'z_statistic': z,
        'p_value': p_value,
        'ci_95': (ci_lower, ci_upper),
        'significant': p_value < 0.05
    }

def minimum_detectable_effect(n, alpha=0.05, power=0.8, p1=None, p2=None):
    """Calculate minimum detectable effect for given sample size."""
    from scipy.stats import norm
    z_alpha = norm.ppf(1 - alpha/2)
    z_beta = norm.ppf(power)
    p_avg = (p1 + p2) / 2 if p1 and p2 else 0.5
    mde = (z_alpha + z_beta) * np.sqrt(2 * p_avg * (1 - p_avg) / n)
    return mde

def statistical_power(n, mde, p1, alpha=0.05):
    """Calculate statistical power for given effect size."""
    from scipy.stats import norm
    z_alpha = norm.ppf(1 - alpha/2)
    z_beta = (mde * np.sqrt(2 * n / (p1 * (1 - p1))) - z_alpha)
    power = norm.cdf(z_beta)
    return power

if __name__ == '__main__':
    result = two_proportion_ztest(2500, 0.62, 2500, 0.71)
    print(f"z={result['z_statistic']:.4f}, p={result['p_value']:.6f}, "
          f"CI={result['ci_95']}, sig={result['significant']}")
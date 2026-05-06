import numpy as np
from scipy import stats

def two_proportion_ztest(n1, x1, n2, x2):
    """Two-proportion z-test for difference in proportions.

    Args:
        n1, x1: Control group size and successes
        n2, x2: Treatment group size and successes

    Returns:
        z-statistic and two-tailed p-value
    """
    p1 = x1 / n1
    p2 = x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    z = (p2 - p1) / se if se > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value

def confidence_interval_diff(n1, x1, n2, x2, confidence=0.95):
    """Compute confidence interval for difference in proportions.

    Args:
        n1, x1: Control group size and successes
        n2, x2: Treatment group size and successes
        confidence: Confidence level (default 0.95)

    Returns:
        (lower, upper) tuple
    """
    p1 = x1 / n1
    p2 = x2 / n2
    diff = p2 - p1
    se = np.sqrt((p1*(1-p1)/n1) + (p2*(1-p2)/n2))
    z_crit = stats.norm.ppf((1 + confidence) / 2)
    return (diff - z_crit * se, diff + z_crit * se)

def statistical_power(p1, p2, n1, n2, alpha=0.05):
    """Calculate statistical power for a two-proportion test.

    Args:
        p1, p2: Proportions in control and treatment
        n1, n2: Sample sizes
        alpha: Significance level

    Returns:
        Power (probability of detecting true difference)
    """
    diff = abs(p2 - p1)
    se_null = np.sqrt(p1 * (1 - p1) * (1/n1 + 1/n2))
    se_alt = np.sqrt((p1*(1-p1)/n1) + (p2*(1-p2)/n2))
    z_crit = stats.norm.ppf(1 - alpha/2)
    z_power = (diff - z_crit * se_null) / se_alt
    return 1 - stats.norm.cdf(z_power)

def minimum_detectable_effect(n1, n2, alpha=0.05, power=0.8):
    """Compute minimum detectable effect (MDE) for given sample sizes.

    Args:
        n1, n2: Sample sizes
        alpha: Significance level
        power: Desired statistical power

    Returns:
        Minimum absolute difference in proportions
    """
    z_alpha = stats.norm.ppf(1 - alpha/2)
    z_beta = stats.norm.ppf(power)
    p_pool = 0.5  # conservative estimate
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    return (z_alpha + z_beta) * se
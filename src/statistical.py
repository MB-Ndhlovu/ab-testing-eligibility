"""Statistical utilities for two-proportion z-tests."""
import numpy as np
from scipy import stats

def two_proportion_ztest(n_success, n_total, alternative="two-sided"):
    """
    Two-proportion z-test using pooled SE (consistent with the test itself).
    CI uses the same pooled SE for consistency between p-value and interval.

    Parameters
    ----------
    n_success : tuple (x1, x2) — number of successes in each group
    n_total : tuple (n1, n2) — group sizes
    alternative : str — 'two-sided', 'larger', 'smaller'

    Returns
    -------
    dict with z_stat, p_value, ci_95 (tuple), significant (bool at alpha=0.05)
    """
    x1, x2 = n_success
    n1, n2 = n_total

    p1 = x1 / n1
    p2 = x2 / n2
    p_pool = (x1 + x2) / (n1 + n2)

    # Pooled SE — used for both test and CI (matched for consistency)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2))
    if se == 0:
        z_stat = 0.0
    else:
        z_stat = (p1 - p2) / se

    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))  # two-sided

    # 95% CI using pooled SE (consistent with test)
    ci_lower = (p1 - p2) - 1.96 * se
    ci_upper = (p1 - p2) + 1.96 * se

    return {
        "p1": p1,
        "p2": p2,
        "difference": p1 - p2,
        "z_stat": z_stat,
        "p_value": p_value,
        "ci_95": (ci_lower, ci_upper),
        "significant": p_value < 0.05,
    }

def power_analysis(p1, p2, n, alpha=0.05):
    """Compute statistical power for a given sample size and proportions."""
    p_pool = (p1 + p2) / 2
    se = np.sqrt(p_pool * (1 - p_pool) * (2 / n))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_ncp = abs(p1 - p2) / se
    power = stats.norm.cdf(z_ncp - z_crit) + stats.norm.cdf(-z_ncp - z_crit)
    return power

def min_detectable_effect(n, alpha=0.05, power=0.8):
    """Minimum detectable effect (absolute) given sample size and power."""
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)
    p_pool = 0.5  # conservative; solve for MDE iteratively in practice
    mde = (z_crit + z_power) * np.sqrt(2 * p_pool * (1 - p_pool) / n)
    return mde
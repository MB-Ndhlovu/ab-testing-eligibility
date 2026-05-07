"""Statistical utilities for two-proportion z-tests and power analysis."""
import numpy as np
from scipy import stats


def two_proportion_ztest(n_A, x_A, n_B, x_B):
    """Two-proportion z-test comparing rates in groups A and B.

    Parameters
    ----------
    n_A : int  — number of trials in group A
    x_A : int  — number of successes in group A
    n_B : int  — number of trials in group B
    x_B : int  — number of successes in group B

    Returns
    -------
    dict with keys: z_statistic, p_value, ci_lower, ci_upper
        95% CI for the difference (p_B - p_A)
    """
    p_A = x_A / n_A
    p_B = x_B / n_B
    p_pool = (x_A + x_B) / (n_A + n_B)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_A + 1 / n_B))
    z = (p_B - p_A) / se

    # two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    # 95% CI for difference using normal approximation
    diff = p_B - p_A
    z_crit = stats.norm.ppf(0.975)
    ci_lower = diff - z_crit * se
    ci_upper = diff + z_crit * se

    return {
        'z_statistic': round(z, 4),
        'p_value': round(p_value, 6),
        'ci_lower': round(ci_lower, 6),
        'ci_upper': round(ci_upper, 6),
        'diff': round(diff, 6),
        'p_A': round(p_A, 6),
        'p_B': round(p_B, 6),
    }


def power_min_detectable_effect(n_A, n_B, alpha=0.05, power=0.80):
    """Compute minimum detectable effect (MDE) at given power.

    Parameters
    ----------
    n_A, n_B : int  — group sizes
    alpha : float   — significance level
    power : float   — desired power (1 - β)

    Returns
    -------
    float — absolute difference in proportions that can be detected
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    # Assume p ≈ 0.5 for most conservative MDE
    p = 0.5
    se = np.sqrt(2 * p * (1 - p) / n_A)
    mde = (z_alpha + z_beta) * se
    return round(mde, 4)
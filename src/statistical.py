"""Statistical tests for A/B testing two proportions."""

import numpy as np
from scipy import stats


def two_proportion_ztest(n_A: int, x_A: int, n_B: int, x_B: int, alpha: float = 0.05):
    """Two-proportion z-test comparing conversion rates.

    Args:
        n_A: Sample size for group A (control).
        x_A: Number of successes in group A.
        n_B: Sample size for group B (treatment).
        x_B: Number of successes in group B.
        alpha: Significance level (default 0.05).

    Returns:
        dict with keys: z_statistic, p_value, ci_lower, ci_upper, significant, mde
    """
    p_A = x_A / n_A
    p_B = x_B / n_B
    diff = p_B - p_A

    # Pooled proportion under null hypothesis
    p_pooled = (x_A + x_B) / (n_A + n_B)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_A + 1 / n_B))

    if se == 0:
        z_stat = 0.0
    else:
        z_stat = diff / se

    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    # 95% CI for the difference using unpooled standard error
    se_unpooled = np.sqrt((p_A * (1 - p_A)) / n_A + (p_B * (1 - p_B)) / n_B)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    ci_lower = diff - z_crit * se_unpooled
    ci_upper = diff + z_crit * se_unpooled

    significant = p_value < alpha

    # Minimum detectable effect (80% power, two-tailed)
    power = 0.80
    z_beta = stats.norm.ppf(power)
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    mde = (z_alpha + z_beta) * np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_A + 1 / n_B))

    return {
        "p_A": p_A,
        "p_B": p_B,
        "diff": diff,
        "z_statistic": z_stat,
        "p_value": p_value,
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "significant": significant,
        "mde": mde,
        "n_A": n_A,
        "n_B": n_B,
    }
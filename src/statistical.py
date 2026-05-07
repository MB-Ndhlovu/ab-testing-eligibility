"""Statistical tests for A/B testing of proportions."""
import numpy as np
from scipy import stats


def two_proportion_ztest(n_success_a, n_trials_a, n_success_b, n_trials_b):
    """
    Two-proportion z-test comparing success rates.

    Returns z-statistic, p-value (two-tailed), and 95% CI for p_b - p_a.
    """
    p_a = n_success_a / n_trials_a
    p_b = n_success_b / n_trials_b
    p_pooled = (n_success_a + n_success_b) / (n_trials_a + n_trials_b)

    se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_trials_a + 1 / n_trials_b))
    z = (p_b - p_a) / se if se > 0 else 0.0

    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    # 95% CI for difference using unpooled standard error
    se_diff = np.sqrt((p_a * (1 - p_a)) / n_trials_a + (p_b * (1 - p_b)) / n_trials_b)
    ci_lower = (p_b - p_a) - 1.96 * se_diff
    ci_upper = (p_b - p_a) + 1.96 * se_diff

    return {
        "z_statistic": round(z, 4),
        "p_value": round(p_value, 6),
        "ci_95_lower": round(ci_lower, 4),
        "ci_95_upper": round(ci_upper, 4),
        "significant": p_value < 0.05,
    }


def statistical_power(n_a, n_b, p_a, p_a_b, alpha=0.05):
    """
    Compute statistical power given sample sizes and proportions.
    p_a_b is the treatment proportion (what we expect in B).
    """
    p_pooled = (p_a + p_a_b) / 2
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_a + 1 / n_b))
    effect = abs(p_a_b - p_a)
    if se == 0:
        return 0.0
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = (effect / se) - z_crit
    power = stats.norm.cdf(z_power)
    return round(power, 4)


def minimum_detectable_effect(n_a, n_b, alpha=0.05, power=0.80):
    """
    Return the minimum detectable effect (absolute) given sample sizes and power.
    """
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    # Assume p_a ≈ 0.5 for a conservative MDE
    p_pooled = 0.5
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_a + 1 / n_b))
    mde = (z_crit + z_beta) * se
    return round(mde, 4)

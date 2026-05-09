"""Statistical analysis for A/B testing: two-proportion z-test, confidence intervals, power."""

import numpy as np
from scipy import stats


def two_proportion_ztest(n_successes_a: int, n_trials_a: int, n_successes_b: int, n_trials_b: int) -> dict:
    """Two-proportion z-test comparing success rates between two groups.

    Returns z-statistic, p-value, 95% CI for the difference, and statistical conclusion.
    """
    p_a = n_successes_a / n_trials_a
    p_b = n_successes_b / n_trials_b
    p_pooled = (n_successes_a + n_successes_b) / (n_trials_a + n_trials_b)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_trials_a + 1 / n_trials_b))
    diff = p_b - p_a
    z = diff / se if se > 0 else 0.0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    # 95% CI for the difference (Wald)
    se_diff = np.sqrt(p_a * (1 - p_a) / n_trials_a + p_b * (1 - p_b) / n_trials_b)
    ci_lower = diff - 1.96 * se_diff
    ci_upper = diff + 1.96 * se_diff

    significant = p_value < 0.05
    alpha = 0.05

    return {
        "group_a_rate": round(p_a, 4),
        "group_b_rate": round(p_b, 4),
        "difference": round(diff, 4),
        "z_statistic": round(z, 4),
        "p_value": round(p_value, 6),
        "ci_95_lower": round(ci_lower, 4),
        "ci_95_upper": round(ci_upper, 4),
        "significant_at_0.05": significant,
        "alpha": alpha,
        "p_pooled": round(p_pooled, 4),
    }


def compute_power(n_a: int, n_b: int, p_a: float, p_b: float, alpha: float = 0.05) -> float:
    """Compute statistical power for a two-proportion z-test."""
    p_pooled = (p_a + p_b) / 2
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_a + 1 / n_b))
    diff = abs(p_b - p_a)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = (diff / se) - z_crit if se > 0 else 0.0
    power = stats.norm.cdf(z_power)
    return round(power, 4)


def minimum_detectable_effect(n_a: int, n_b: int, alpha: float = 0.05, power: float = 0.80) -> float:
    """Minimum detectable effect (absolute) for given sample sizes and power."""
    p_a_guess = 0.5  # conservative midpoint
    p_pooled = p_a_guess
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_a + 1 / n_b))
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    mde = (z_crit + z_beta) * se
    return round(mde, 4)
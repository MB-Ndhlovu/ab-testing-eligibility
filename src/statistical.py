"""Statistical tests for two-proportion comparisons."""

import numpy as np
from scipy import stats


def two_proportion_z_test(n_a, p_a, n_b, p_b):
    """Two-proportion z-test comparing rates between groups."""
    p_pooled = (n_a * p_a + n_b * p_b) / (n_a + n_b)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1 / n_a + 1 / n_b))
    z = (p_b - p_a) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return {"z": z, "p_value": p_value, "p_pooled": p_pooled, "se": se}


def confidence_interval(p_a, p_b, n_a, n_b, confidence=0.95):
    """95% CI for the difference in proportions."""
    se = np.sqrt((p_a * (1 - p_a) / n_a) + (p_b * (1 - p_b) / n_b))
    z = stats.norm.ppf(1 - (1 - confidence) / 2)
    diff = p_b - p_a
    return (diff - z * se, diff + z * se)


def minimum_detectable_effect(n_a, n_b, alpha=0.05, power=0.8):
    """Minimum detectable effect for given sample sizes."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p_pooled = 0.5
    se = np.sqrt(2 * p_pooled * (1 - p_pooled) / n_a)
    return (z_alpha + z_beta) * se
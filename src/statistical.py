"""Statistical analysis: two-proportion z-test, confidence intervals, power."""

import numpy as np
from scipy import stats


def two_proportion_ztest(n_a, x_a, n_b, x_b):
    """Two-proportion z-test comparing treatment vs control.

    Returns z-statistic, two-tailed p-value, and 95% CI for (p_b - p_a).
    """
    p_a = x_a / n_a
    p_b = x_b / n_b
    diff = p_b - p_a

    p_pool = (x_a + x_b) / (n_a + n_b)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n_a + 1/n_b))
    z = diff / se if se > 0 else 0
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    se_diff = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
    ci_lower = diff - 1.96 * se_diff
    ci_upper = diff + 1.96 * se_diff

    return {
        "z": float(z),
        "p_value": float(p_value),
        "ci_95": (float(ci_lower), float(ci_upper)),
        "diff": float(diff),
    }


def power_and_mde(n_a, n_b, alpha=0.05, power=0.80):
    """Compute minimum detectable effect (MDE) at given power and alpha."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    pooled_p = 0.5
    se = np.sqrt(pooled_p * (1 - pooled_p) * (1/n_a + 1/n_b))
    mde = (z_alpha + z_beta) * se
    return float(mde)


def analyze_metric(label, n_a, rate_a, n_b, rate_b, alpha=0.05):
    """Run full statistical analysis for one rate metric."""
    result = two_proportion_ztest(n_a, rate_a * n_a, n_b, rate_b * n_b)
    mde = power_and_mde(n_a, n_b, alpha=alpha)
    significant = result["p_value"] < alpha
    return {
        "metric": label,
        "control_rate": rate_a,
        "treatment_rate": rate_b,
        "z": result["z"],
        "p_value": result["p_value"],
        "ci_95": result["ci_95"],
        "diff": result["diff"],
        "mde": mde,
        "significant": significant,
    }
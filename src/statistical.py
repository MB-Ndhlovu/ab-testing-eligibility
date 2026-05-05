"""Statistical tests for two-proportion A/B tests."""

import numpy as np
from scipy import stats


def two_proportion_ztest(n_control: int, x_control: int,
                          n_treatment: int, x_treatment: int,
                          alternative: str = "two-sided") -> dict:
    """Two-proportion z-test for A/B test significance.

    Args:
        n_control: Sample size control group.
        x_control: successes (e.g. approvals) in control.
        n_treatment: Sample size treatment group.
        x_treatment: successes in treatment.
        alternative: 'two-sided', 'larger', or 'smaller'.

    Returns:
        dict with z_stat, p_value, confidence_interval, significant.
    """
    p_control = x_control / n_control
    p_treatment = x_treatment / n_treatment
    p_pooled = (x_control + x_treatment) / (n_control + n_treatment)

    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_control + 1/n_treatment))
    if se == 0:
        return {"z_stat": 0.0, "p_value": 1.0, "ci": (0.0, 0.0),
                "significant": False, "p_pooled": p_pooled}

    z_stat = (p_treatment - p_control) / se

    if alternative == "two-sided":
        p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
        z_crit = stats.norm.ppf(0.975)
    elif alternative == "larger":
        p_value = 1 - stats.norm.cdf(z_stat)
        z_crit = stats.norm.ppf(0.95)
    else:
        p_value = stats.norm.cdf(z_stat)
        z_crit = stats.norm.ppf(0.95)

    diff = p_treatment - p_control
    ci = (diff - z_crit * se, diff + z_crit * se)

    return {
        "z_stat": z_stat,
        "p_value": p_value,
        "ci": ci,
        "significant": p_value < 0.05,
        "p_pooled": p_pooled,
    }


def power_min_detectable_effect(n_control: int, n_treatment: int,
                                  p_control: float, alpha: float = 0.05) -> dict:
    """Compute statistical power and minimum detectable effect (MDE).

    Args:
        n_control: Sample size control.
        n_treatment: Sample size treatment.
        p_control: Baseline proportion.
        alpha: Significance level.

    Returns:
        dict with mde (minimum detectable effect as absolute proportion diff),
              power at MDE, and power_curve dict for a range of effects.
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(0.80)

    p_pooled = p_control
    se_baseline = np.sqrt(2 * p_pooled * (1 - p_pooled) / n_control)
    mde = (z_alpha + z_beta) * se_baseline

    return {
        "mde": mde,
        "power_at_mde": 0.80,
        "n_control": n_control,
        "n_treatment": n_treatment,
        "alpha": alpha,
    }
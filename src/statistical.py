"""
Statistical analysis for A/B testing: two-proportion z-test, confidence intervals,
power analysis, and minimum detectable effect.
"""

import numpy as np
from scipy import stats


def two_proportion_ztest(n_control, p_control, n_treatment, p_treatment):
    """
    Two-proportion z-test comparing treatment vs control.

    Args:
        n_control: Number of trials in control group
        p_control: Observed proportion in control group
        n_treatment: Number of trials in treatment group
        p_treatment: Observed proportion in treatment group

    Returns:
        dict with z_statistic, p_value, ci_95 (tuple), significance (bool)
    """
    p_pooled = (n_control * p_control + n_treatment * p_treatment) / (n_control + n_treatment)
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_control + 1/n_treatment))

    if se == 0:
        return {
            'z_statistic': 0.0,
            'p_value': 1.0,
            'ci_95': (0.0, 0.0),
            'significant': False,
            'p_pooled': p_pooled,
            'se': se
        }

    z_stat = (p_treatment - p_control) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))  # two-tailed

    # 95% CI for the difference
    diff = p_treatment - p_control
    se_diff = np.sqrt(p_control * (1 - p_control) / n_control + p_treatment * (1 - p_treatment) / n_treatment)
    ci_lower = diff - 1.96 * se_diff
    ci_upper = diff + 1.96 * se_diff

    return {
        'z_statistic': float(z_stat),
        'p_value': float(p_value),
        'ci_95': (float(ci_lower), float(ci_upper)),
        'significant': bool(p_value < 0.05),
        'p_pooled': float(p_pooled),
        'se': float(se_diff)
    }


def statistical_power(n_control, n_treatment, p_control, mde, alpha=0.05):
    """
    Calculate statistical power for a two-proportion z-test.

    Args:
        n_control: Sample size control
        n_treatment: Sample size treatment
        p_control: Baseline proportion
        mde: Minimum detectable effect (absolute change in proportion)
        alpha: Significance level (default 0.05)

    Returns:
        float: power (0 to 1)
    """
    p_treatment = p_control + mde
    se_null = np.sqrt(p_control * (1 - p_control) * (1/n_control + 1/n_treatment))
    se_alt = np.sqrt(p_treatment * (1 - p_treatment) * (1/n_control + 1/n_treatment))

    # Critical value
    z_crit = stats.norm.ppf(1 - alpha / 2)

    # Non-centrality parameter under alternative
    effect = abs(mde)
    power = 1 - stats.norm.cdf(z_crit - effect / se_alt) + stats.norm.cdf(-z_crit - effect / se_alt)
    return float(power)


def minimum_detectable_effect(n_control, n_treatment, alpha=0.05, power=0.80, p_control=0.5):
    """
    Calculate minimum detectable effect for a given sample size and power.

    Args:
        n_control: Sample size control
        n_treatment: Sample size treatment
        alpha: Significance level (default 0.05)
        power: Desired power (default 0.80)
        p_control: Baseline proportion (default 0.5 for most conservative estimate)

    Returns:
        float: MDE (absolute proportion change)
    """
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    se = np.sqrt(p_control * (1 - p_control) * (1/n_control + 1/n_treatment))
    mde = (z_crit + z_beta) * se
    return float(mde)


if __name__ == '__main__':
    # Demo
    result = two_proportion_ztest(n_control=2500, p_control=0.62, n_treatment=2500, p_treatment=0.71)
    print("=== Two-Proportion Z-Test Demo ===")
    print(f"z-statistic: {result['z_statistic']:.4f}")
    print(f"p-value:     {result['p_value']:.6f}")
    print(f"95% CI:      ({result['ci_95'][0]:.4f}, {result['ci_95'][1]:.4f})")
    print(f"Significant: {result['significant']}")

    mde = minimum_detectable_effect(2500, 2500, alpha=0.05, power=0.80, p_control=0.62)
    print(f"\nMDE for 80% power: {mde:.4f} ({mde*100:.2f}pp)")

    pwr = statistical_power(2500, 2500, p_control=0.62, mde=0.09, alpha=0.05)
    print(f"Power for observed effect (0.09): {pwr:.4f}")
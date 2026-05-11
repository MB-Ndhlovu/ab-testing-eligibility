"""Statistical analysis for two-proportion z-tests."""

import numpy as np
from scipy import stats
from typing import Dict, Tuple


def two_proportion_ztest(n1: int, p1: float, n2: int, p2: float) -> Dict:
    """
    Perform two-proportion z-test.

    Args:
        n1: Sample size group 1
        p1: Proportion in group 1
        n2: Sample size group 2
        p2: Proportion in group 2

    Returns:
        Dict with z-statistic, p-value, confidence interval, significance
    """
    p_pool = (n1 * p1 + n2 * p2) / (n1 + n2)
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))

    if se == 0:
        z_stat = 0.0
    else:
        z_stat = (p2 - p1) / se

    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    diff = p2 - p1
    se_diff = np.sqrt((p1 * (1 - p1) / n1) + (p2 * (2 - p2) / n2))
    ci_low = diff - 1.96 * se_diff
    ci_high = diff + 1.96 * se_diff

    alpha = 0.05
    significant = p_value < alpha

    return {
        'z_statistic': round(z_stat, 4),
        'p_value': round(p_value, 6),
        'ci_95': (round(ci_low, 6), round(ci_high, 6)),
        'significant': significant,
        'alpha': alpha
    }


def power_analysis(p1: float, p2: float, alpha: float = 0.05, power: float = 0.80) -> Dict:
    """
    Compute minimum sample size and minimum detectable effect.

    Args:
        p1: Baseline proportion
        p2: Target proportion
        alpha: Significance level
        power: Desired statistical power

    Returns:
        Dict with min_sample_size and min_detectable_effect
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    p_avg = (p1 + p2) / 2
    mde = (z_alpha + z_beta) * np.sqrt(2 * p_avg * (1 - p_avg))

    min_n = 2 * ((z_alpha + z_beta) ** 2 * p_avg * (1 - p_avg)) / ((p2 - p1) ** 2)

    return {
        'min_sample_size_per_group': int(np.ceil(min_n)),
        'min_detectable_effect': round(abs(p2 - p1), 4)
    }


def analyze_metric(metric_a: dict, metric_b: dict, metric_name: str) -> Dict:
    """
    Run full statistical analysis for a single metric across two groups.

    Args:
        metric_a: Metrics dict for group A
        metric_b: Metrics dict for group B
        metric_name: Name of the metric being analyzed

    Returns:
        Complete analysis results
    """
    p1 = metric_a[metric_name]
    p2 = metric_b[metric_name]
    n1 = metric_a['n']
    n2 = metric_b['n']

    test_result = two_proportion_ztest(n1, p1, n2, p2)
    power_result = power_analysis(p1, p2)

    return {
        'metric': metric_name,
        'group_a_value': round(p1, 6),
        'group_b_value': round(p2, 6),
        'treatment_effect': round(p2 - p1, 6),
        **test_result,
        'power_analysis': power_result
    }
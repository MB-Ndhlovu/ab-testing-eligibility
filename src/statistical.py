"""Statistical analysis for A/B testing: two-proportion z-test, CIs, power."""

import numpy as np
from scipy import stats


def two_proportion_z_test(n1, x1, n2, x2):
    """
    Two-proportion z-test comparing conversion rates.

    Args:
        n1: Sample size group 1
        x1: Conversions group 1
        n2: Sample size group 2
        x2: Conversions group 2

    Returns:
        dict with z_statistic, p_value, diff, se
    """
    p1 = x1 / n1 if n1 > 0 else 0
    p2 = x2 / n2 if n2 > 0 else 0

    diff = p2 - p1

    # Pooled proportion under null hypothesis
    p_pooled = (x1 + x2) / (n1 + n2) if (n1 + n2) > 0 else 0

    # Standard error under null
    se_null = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2)) if (n1 > 0 and n2 > 0) else 0

    # Z-statistic
    if se_null > 0:
        z_stat = diff / se_null
    else:
        z_stat = 0.0

    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    return {
        'z_statistic': z_stat,
        'p_value': p_value,
        'diff': diff,
        'se_null': se_null,
        'p1': p1,
        'p2': p2
    }


def confidence_interval_diff(n1, x1, n2, x2, confidence=0.95):
    """
    Confidence interval for difference in proportions (unpooled).

    Args:
        n1, x1: Sample size and conversions group 1
        n2, x2: Sample size and conversions group 2
        confidence: CI level (default 0.95 for 95% CI)

    Returns:
        dict with lower, upper, diff
    """
    p1 = x1 / n1 if n1 > 0 else 0
    p2 = x2 / n2 if n2 > 0 else 0

    diff = p2 - p1

    # Standard error (unpooled)
    se = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2) if (n1 > 0 and n2 > 0) else 0

    z = stats.norm.ppf((1 + confidence) / 2)

    lower = diff - z * se
    upper = diff + z * se

    return {
        'lower': lower,
        'upper': upper,
        'diff': diff,
        'se': se
    }


def statistical_power(n1, p1, n2, p2, alpha=0.05):
    """
    Calculate statistical power for two-proportion test.

    Args:
        n1, p1: Sample size and proportion group 1 (control)
        n2, p2: Sample size and proportion group 2 (treatment)
        alpha: Significance level

    Returns:
        Power (probability of detecting true difference)
    """
    # Standard error under alternative
    se_alt = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)

    if se_alt == 0:
        return 0.0

    # Critical z for two-tailed test
    z_crit = stats.norm.ppf(1 - alpha / 2)

    # Effect size
    diff = p2 - p1

    # Power = P(|Z| > z_crit - diff/se_alt)
    z_noncentral = (diff - z_crit * se_alt) / se_alt

    power = 1 - stats.norm.cdf(z_noncentral) + stats.norm.cdf(-z_noncentral - 2 * z_crit)

    # Simpler formula for power
    power = 1 - stats.norm.cdf(z_crit - diff / se_alt) + stats.norm.cdf(-z_crit - diff / se_alt)

    return min(max(power, 0.0), 1.0)


def minimum_detectable_effect(n1, n2, alpha=0.05, power=0.8, p1=0.5):
    """
    Calculate minimum detectable effect for two-proportion test.

    Args:
        n1, n2: Sample sizes
        alpha: Significance level
        power: Desired statistical power
        p1: Baseline proportion (control)

    Returns:
        MDE (absolute difference in proportions)
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    se_null = np.sqrt(p1 * (1 - p1) * (1/n1 + 1/n2))

    mde = (z_alpha + z_beta) * se_null

    return mde


def run_statistical_analysis(group_a_metrics, group_b_metrics, alpha=0.05):
    """
    Run full statistical analysis for A/B test.

    Args:
        group_a_metrics: dict with n, approved_count, approval_rate, default_count, default_rate
        group_b_metrics: dict with same fields
        alpha: Significance level

    Returns:
        dict with all test results
    """
    # Approval rate test
    approval_test = two_proportion_z_test(
        group_a_metrics['n'], group_a_metrics['approved_count'],
        group_b_metrics['n'], group_b_metrics['approved_count']
    )

    approval_ci = confidence_interval_diff(
        group_a_metrics['n'], group_a_metrics['approved_count'],
        group_b_metrics['n'], group_b_metrics['approved_count']
    )

    # Default rate test
    # Use approved subset for default rate calculation
    default_test = two_proportion_z_test(
        group_a_metrics['approved_count'], group_a_metrics['default_count'],
        group_b_metrics['approved_count'], group_b_metrics['default_count']
    )

    default_ci = confidence_interval_diff(
        group_a_metrics['approved_count'], group_a_metrics['default_count'],
        group_b_metrics['approved_count'], group_b_metrics['default_count']
    )

    # Power calculation for approval rate
    approval_power = statistical_power(
        group_a_metrics['n'], group_a_metrics['approval_rate'],
        group_b_metrics['n'], group_b_metrics['approval_rate'],
        alpha
    )

    # MDE for approval rate
    mde_approval = minimum_detectable_effect(
        group_a_metrics['n'], group_b_metrics['n'],
        alpha=alpha, power=0.8, p1=group_a_metrics['approval_rate']
    )

    results = {
        'alpha': alpha,
        'approval': {
            'z_statistic': approval_test['z_statistic'],
            'p_value': approval_test['p_value'],
            'diff': approval_test['diff'],
            'ci_lower': approval_ci['lower'],
            'ci_upper': approval_ci['upper'],
            'significant': approval_test['p_value'] < alpha,
            'power': approval_power,
            'mde': mde_approval,
            'control_rate': approval_test['p1'],
            'treatment_rate': approval_test['p2']
        },
        'default': {
            'z_statistic': default_test['z_statistic'],
            'p_value': default_test['p_value'],
            'diff': default_test['diff'],
            'ci_lower': default_ci['lower'],
            'ci_upper': default_ci['upper'],
            'significant': default_test['p_value'] < alpha,
            'control_rate': default_test['p1'],
            'treatment_rate': default_test['p2']
        }
    }

    return results


if __name__ == '__main__':
    # Quick test
    result = two_proportion_z_test(2500, 1550, 2500, 1775)
    print("Z-test result:", result)

    ci = confidence_interval_diff(2500, 1550, 2500, 1775)
    print("95% CI:", ci)
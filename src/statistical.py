"""Statistical tests for A/B testing: two-proportion z-tests and power analysis."""

import numpy as np
from scipy import stats


def two_proportion_z_test(p1, p2, n1, n2, alternative='two-sided'):
    """
    Perform a two-proportion z-test.

    Parameters
    ----------
    p1 : float
        Proportion in group 1 (control)
    p2 : float
        Proportion in group 2 (treatment)
    n1 : int
        Sample size for group 1
    n2 : int
        Sample size for group 2
    alternative : str
        'two-sided', 'larger', or 'smaller'

    Returns
    -------
    dict
        Contains z_statistic, p_value, confidence_interval
    """
    p_pooled = (p1 * n1 + p2 * n2) / (n1 + n2)

    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))

    if se == 0:
        return {
            'z_statistic': 0.0,
            'p_value': 1.0,
            'ci_lower': 0.0,
            'ci_upper': 0.0,
            'significant': False
        }

    z = (p2 - p1) / se

    if alternative == 'two-sided':
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    elif alternative == 'larger':
        p_value = 1 - stats.norm.cdf(z)
    elif alternative == 'smaller':
        p_value = stats.norm.cdf(z)
    else:
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))

    se_diff = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)
    ci_lower = (p2 - p1) - 1.96 * se_diff
    ci_upper = (p2 - p1) + 1.96 * se_diff

    alpha = 0.05
    significant = p_value < alpha

    return {
        'z_statistic': z,
        'p_value': p_value,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'significant': significant,
        'control_rate': p1,
        'treatment_rate': p2,
        'absolute_diff': p2 - p1
    }


def compute_statistical_power(p1, p2, n1, n2, alpha=0.05):
    """
    Compute statistical power for a two-proportion z-test.

    Parameters
    ----------
    p1 : float
        Proportion in control group
    p2 : float
        Proportion in treatment group
    n1, n2 : int
        Sample sizes for each group
    alpha : float
        Significance level (default 0.05)

    Returns
    -------
    float
        Statistical power (0 to 1)
    """
    p_pooled = (p1 + p2) / 2
    se_null = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    se_alt = np.sqrt(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2)

    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_effect = abs(p2 - p1) / se_alt

    power = stats.norm.cdf(z_effect - z_crit) + stats.norm.cdf(-z_effect - z_crit)
    return power


def minimum_detectable_effect(p1, n, alpha=0.05, power=0.8):
    """
    Compute minimum detectable effect (MDE) for a given power.

    Parameters
    ----------
    p1 : float
        Baseline proportion
    n : int
        Sample size per group (assumes equal allocation)
    alpha : float
        Significance level
    power : float
        Desired statistical power (0 to 1)

    Returns
    -------
    float
        Minimum detectable effect (absolute difference)
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    p_pooled = p1

    se_pooled = np.sqrt(2 * p_pooled * (1 - p_pooled) / n)

    mde = (z_alpha + z_beta) * se_pooled
    return mde


def analyze_metric(data, metric_col, approval_col='approved', group_col='group'):
    """
    Analyze a binary metric across groups.

    Parameters
    ----------
    data : pd.DataFrame
        The experiment data
    metric_col : str
        Column name for the binary metric
    approval_col : str
        Column name indicating whether loan was approved
    group_col : str
        Column name for group assignment

    Returns
    -------
    dict
        Analysis results
    """
    group_a = data[data[group_col] == 'A']
    group_b = data[data[group_col] == 'B']

    if metric_col == 'approval_rate':
        mask_a = np.ones(len(group_a), dtype=bool)
        mask_b = np.ones(len(group_b), dtype=bool)
        p1 = group_a['approved'].mean()
        p2 = group_b['approved'].mean()
    else:
        mask_a = group_a['approved']
        mask_b = group_b['approved']
        p1 = group_a.loc[mask_a, metric_col].mean()
        p2 = group_b.loc[mask_b, metric_col].mean()

    n1 = len(group_a)
    n2 = len(group_b)

    z_result = two_proportion_z_test(p1, p2, n1, n2)

    power = compute_statistical_power(p1, p2, n1, n2)
    mde = minimum_detectable_effect(p1, min(n1, n2))

    return {
        'metric': metric_col,
        'group_a_rate': p1,
        'group_b_rate': p2,
        'absolute_diff': p2 - p1,
        'relative_diff': (p2 - p1) / p1 if p1 != 0 else 0,
        'z_statistic': z_result['z_statistic'],
        'p_value': z_result['p_value'],
        'ci_95_lower': z_result['ci_lower'],
        'ci_95_upper': z_result['ci_upper'],
        'significant': z_result['significant'],
        'power': power,
        'mde': mde
    }
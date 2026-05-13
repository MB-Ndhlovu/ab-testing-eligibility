"""Statistical analysis for A/B testing using two-proportion z-test."""

import numpy as np
from scipy import stats


def two_proportion_ztest(n1, x1, n2, x2):
    """
    Perform a two-proportion z-test.

    Parameters
    ----------
    n1 : int
        Number of trials in group 1 (control).
    x1 : int
        Number of successes in group 1.
    n2 : int
        Number of trials in group 2 (treatment).
    x2 : int
        Number of successes in group 2.

    Returns
    -------
    dict
        Results containing z-statistic, p-value, and confidence interval.
    """
    p1 = x1 / n1
    p2 = x2 / n2
    p_pooled = (x1 + x2) / (n1 + n2)

    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n1 + 1/n2))
    z_stat = (p2 - p1) / se if se > 0 else 0

    p_value_two_sided = 2 * (1 - stats.norm.cdf(abs(z_stat)))

    se_diff = np.sqrt((p1 * (1 - p1) / n1) + (p2 * (2 - p2) / n2))
    ci_margin = 1.96 * se_diff
    ci_lower = (p2 - p1) - ci_margin
    ci_upper = (p2 - p1) + ci_margin

    return {
        "z_statistic": round(z_stat, 4),
        "p_value": round(p_value_two_sided, 6),
        "p1": round(p1, 4),
        "p2": round(p2, 4),
        "difference": round(p2 - p1, 4),
        "ci_95_lower": round(ci_lower, 4),
        "ci_95_upper": round(ci_upper, 4),
        "significant": p_value_two_sided < 0.05,
    }


def compute_statistical_power(n, p1, p2, alpha=0.05):
    """
    Compute statistical power for a two-proportion test.

    Parameters
    ----------
    n : int
        Sample size per group.
    p1 : float
        Baseline proportion.
    p2 : float
        Treatment proportion.
    alpha : float
        Significance level.

    Returns
    -------
    float
        Statistical power (probability of detecting true effect).
    """
    se_null = np.sqrt(2 * p1 * (1 - p1) / n)
    se_alt = np.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    power = 1 - stats.norm.cdf(z_crit - (p2 - p1) / se_alt)
    return round(power, 4)


def minimum_detectable_effect(n, alpha=0.05, power=0.8):
    """
    Compute minimum detectable effect (MDE) for a two-proportion test.

    Parameters
    ----------
    n : int
        Sample size per group.
    alpha : float
        Significance level.
    power : float
        Desired statistical power.

    Returns
    -------
    float
        Minimum detectable effect (absolute difference).
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p_avg = 0.5
    se = np.sqrt(2 * p_avg * (1 - p_avg) / n)
    mde = (z_alpha + z_beta) * se
    return round(mde, 4)


def analyze_metric(group_a_data, group_b_data, metric, n_trials=2500, is_approval=True):
    """
    Analyze a binary metric between two groups.

    Parameters
    ----------
    group_a_data : pd.DataFrame
        Control group data.
    group_b_data : pd.DataFrame
        Treatment group data.
    metric : str
        Column name of the binary metric.
    n_trials : int
        Number of trials (e.g., total applications).
    is_approval : bool
        True if higher is better, False if lower is better.

    Returns
    -------
    dict
        Full statistical analysis results.
    """
    n_a = len(group_a_data)
    n_b = len(group_b_data)
    x_a = int(group_a_data[metric].sum())
    x_b = int(group_b_data[metric].sum())

    result = two_proportion_ztest(n_a, x_a, n_b, x_b)

    result["n_a"] = n_a
    result["n_b"] = n_b
    result["x_a"] = x_a
    result["x_b"] = x_b

    mde = minimum_detectable_effect(n_a, alpha=0.05, power=0.8)
    power = compute_statistical_power(n_a, result["p1"], result["p2"])

    result["power"] = power
    result["mde"] = mde
    result["direction"] = "↑" if is_approval else "↓"
    result["desired_direction"] = "higher_is_better" if is_approval else "lower_is_better"
    result["metric"] = metric

    return result


if __name__ == "__main__":
    from scipy.stats import norm
    print("Two-proportion z-test module ready.")
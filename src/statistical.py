import numpy as np
from scipy import stats

def two_proportion_ztest(n_success_a, n_trials_a, n_success_b, n_trials_b):
    p_a = n_success_a / n_trials_a
    p_b = n_success_b / n_trials_b
    p_pool = (n_success_a + n_success_b) / (n_trials_a + n_trials_b)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_trials_a + 1 / n_trials_b))
    z = (p_b - p_a) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    return z, p_value, p_a, p_b

def confidence_interval(n_success_a, n_trials_a, n_success_b, n_trials_b, alpha=0.05):
    p_a = n_success_a / n_trials_a
    p_b = n_success_b / n_trials_b
    diff = p_b - p_a
    se = np.sqrt(p_a * (1 - p_a) / n_trials_a + p_b * (1 - p_b) / n_trials_b)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    return diff, (diff - z_crit * se, diff + z_crit * se)

def statistical_power(n_a, n_b, p_a, p_b, alpha=0.05, mde=None):
    if mde is None:
        mde = abs(p_b - p_a) * 0.5
    p_pool = (p_a * n_a + p_b * n_b) / (n_a + n_b)
    se = np.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = (mde * np.sqrt(n_a * n_b / (n_a + n_b)) - z_alpha * se) / se
    return 1 - stats.norm.cdf(z_beta)

def minimum_detectable_effect(n_a, n_b, p_a, alpha=0.05, power=0.80):
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    p_pool = p_a * (1 - p_a)
    se = np.sqrt(p_pool * (2 / n_a))
    return (z_alpha + z_beta) * se

def test_metric(group_a, group_b, metric_name, n_trials_a, n_trials_b, alpha=0.05):
    n_success_a = int(group_a[metric_name] * n_trials_a)
    n_success_b = int(group_b[metric_name] * n_trials_b)

    z, p_val, p_a, p_b = two_proportion_ztest(n_success_a, n_trials_a, n_success_b, n_trials_b)
    diff, ci = confidence_interval(n_success_a, n_trials_a, n_success_b, n_trials_b, alpha)
    significant = p_val < alpha

    return {
        "metric": metric_name,
        "group_a_rate": round(p_a, 4),
        "group_b_rate": round(p_b, 4),
        "diff": round(diff, 4),
        "ci_lower": round(ci[0], 4),
        "ci_upper": round(ci[1], 4),
        "z_statistic": round(z, 4),
        "p_value": round(p_val, 6),
        "significant": significant,
    }
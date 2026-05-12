import numpy as np
from scipy import stats

def two_proportion_ztest(n_success_a, n_trials_a, n_success_b, n_trials_b):
    """Two-proportion z-test for comparing two binomial proportions."""
    p_a = n_success_a / n_trials_a
    p_b = n_success_b / n_trials_b
    p_pooled = (n_success_a + n_success_b) / (n_trials_a + n_trials_b)

    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_trials_a + 1/n_trials_b))
    z = (p_b - p_a) / se
    p_value = 2 * (1 - stats.norm.cdf(abs(z)))  # two-tailed

    return {
        'z_statistic': z,
        'p_value': p_value,
        'p_a': p_a,
        'p_b': p_b,
        'difference': p_b - p_a,
        'p_pooled': p_pooled,
    }

def confidence_interval(n_success_a, n_trials_a, n_success_b, n_trials_b, alpha=0.05):
    """95% CI for the difference between two proportions."""
    p_a = n_success_a / n_trials_a
    p_b = n_success_b / n_trials_b
    diff = p_b - p_a

    se = np.sqrt((p_a * (1 - p_a) / n_trials_a) + (p_b * (1 - p_b) / n_trials_b))
    z_crit = stats.norm.ppf(1 - alpha / 2)

    ci_lower = diff - z_crit * se
    ci_upper = diff + z_crit * se

    return {
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'se': se,
    }

def statistical_power(n_a, n_b, p_a, mde, alpha=0.05):
    """
    Compute statistical power given sample sizes and minimum detectable effect.
    mde = absolute difference in proportions we want to detect.
    """
    p_b = p_a + mde
    p_pooled = (p_a + p_b) / 2
    se_null = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_a + 1/n_b))
    se_alt = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)

    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_crit = z_alpha * se_null / se_alt
    power = 1 - stats.norm.cdf(z_crit) + stats.norm.cdf(-z_crit - (mde / se_alt))

    return {
        'power': power,
        'mde': mde,
    }

def minimum_detectable_effect(n_a, n_b, p_a, power=0.80, alpha=0.05):
    """Find the minimum detectable effect for a given power."""
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)

    # Iterative approach to solve for MDE
    for mde in np.linspace(0.001, 0.5, 1000):
        p_b = p_a + mde
        p_pooled = (p_a + p_b) / 2
        se_null = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_a + 1/n_b))
        se_alt = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)

        critical_value = z_alpha * se_null
        if mde / se_alt >= critical_value / se_alt + z_beta:
            return {'mde': mde, 'power': power}
    return {'mde': None, 'power': power}
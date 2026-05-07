"""Statistical tests for A/B testing: two-proportion z-test, confidence intervals, power analysis."""
import numpy as np
from scipy import stats

def two_proportion_ztest(n_A, p_A, n_B, p_B):
    """
    Two-proportion z-test comparing proportions from two groups.
    
    Parameters:
    -----------
    n_A : int
        Number of trials in group A (control)
    p_A : float
        Observed proportion in group A
    n_B : int
        Number of trials in group B (treatment)
    p_B : float
        Observed proportion in group B
    
    Returns:
    --------
    dict with z_statistic, p_value, pooled_proportion, se
    """
    pooled_p = (n_A * p_A + n_B * p_B) / (n_A + n_B)
    se = np.sqrt(pooled_p * (1 - pooled_p) * (1/n_A + 1/n_B))
    
    z_stat = (p_B - p_A) / se
    
    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    return {
        'z_statistic': z_stat,
        'p_value': p_value,
        'pooled_proportion': pooled_p,
        'se': se,
    }

def confidence_interval_difference(p_A, p_B, n_A, n_B, confidence=0.95):
    """
    Calculate confidence interval for the difference p_B - p_A.
    
    Parameters:
    -----------
    p_A : float
        Proportion in group A
    p_B : float
        Proportion in group B
    n_A : int
        Sample size group A
    n_B : int
        Sample size group B
    confidence : float
        Confidence level (default 0.95 for 95% CI)
    
    Returns:
    --------
    tuple (lower, upper) bounds
    """
    diff = p_B - p_A
    se = np.sqrt((p_A * (1 - p_A) / n_A) + (p_B * (1 - p_B) / n_B))
    z_crit = stats.norm.ppf((1 + confidence) / 2)
    margin = z_crit * se
    return (diff - margin, diff + margin)

def statistical_power(n_A, n_B, p_A, p_B, alpha=0.05):
    """
    Calculate statistical power for comparing two proportions.
    
    Parameters:
    -----------
    n_A : int
        Sample size group A
    n_B : int
        Sample size group B
    p_A : float
        Proportion in group A (control)
    p_B : float
        Proportion in group B (treatment)
    alpha : float
        Significance level
    
    Returns:
    --------
    float : power (probability of detecting true difference)
    """
    pooled_p = (p_A + p_B) / 2
    se = np.sqrt(pooled_p * (1 - pooled_p) * (1/n_A + 1/n_B))
    diff = abs(p_B - p_A)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_effect = diff / se
    power = 1 - stats.norm.cdf(z_crit - z_effect) + stats.norm.cdf(-z_crit - z_effect)
    return power

def minimum_detectable_effect(n_A, n_B, alpha=0.05, power=0.80):
    """
    Calculate minimum detectable effect size (MDE) for two proportions.
    
    Parameters:
    -----------
    n_A : int
        Sample size group A
    n_B : int
        Sample size group B
    alpha : float
        Significance level
    power : float
        Desired statistical power
    
    Returns:
    --------
    float : minimum detectable effect size
    """
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    
    # Assume p = 0.5 for most conservative estimate
    p = 0.5
    se = np.sqrt(2 * p * (1 - p) / ((1/n_A + 1/n_B)))
    mde = (z_alpha + z_beta) * se
    return mde

def evaluate_metric(name, n_A, p_A, n_B, p_B, alpha=0.05):
    """
    Run full statistical evaluation for a single proportion metric.
    
    Parameters:
    -----------
    name : str
        Metric name
    n_A : int
        Sample size group A
    p_A : float
        Proportion in group A
    n_B : int
        Sample size group B
    p_B : float
        Proportion in group B
    alpha : float
        Significance level
    
    Returns:
    --------
    dict with all statistical results
    """
    z_result = two_proportion_ztest(n_A, p_A, n_B, p_B)
    ci = confidence_interval_difference(p_A, p_B, n_A, n_B, confidence=0.95)
    power = statistical_power(n_A, n_B, p_A, p_B, alpha)
    mde = minimum_detectable_effect(n_A, n_B, alpha, power=0.80)
    
    significant = z_result['p_value'] < alpha
    effect_direction = "higher" if p_B > p_A else "lower"
    
    return {
        'metric': name,
        'group_A_proportion': p_A,
        'group_B_proportion': p_B,
        'n_A': n_A,
        'n_B': n_B,
        'z_statistic': z_result['z_statistic'],
        'p_value': z_result['p_value'],
        'ci_lower': ci[0],
        'ci_upper': ci[1],
        'significant': significant,
        'power': power,
        'mde': mde,
        'effect_direction': effect_direction,
        'treatment_effect': p_B - p_A,
    }

if __name__ == '__main__':
    # Quick test
    result = evaluate_metric('Approval Rate', 5000, 0.62, 5000, 0.71)
    print(result)
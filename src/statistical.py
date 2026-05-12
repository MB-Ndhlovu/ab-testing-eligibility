import numpy as np
from scipy import stats

def two_proportion_ztest(n1, x1, n2, x2):
    """
    Two-proportion z-test for comparing two proportions.
    
    Args:
        n1: Number of trials in group 1
        x1: Number of successes in group 1
        n2: Number of trials in group 2
        x2: Number of successes in group 2
    
    Returns:
        z_stat: z-statistic
        p_value: two-tailed p-value
    """
    p1 = x1 / n1
    p2 = x2 / n2
    
    # Pooled proportion
    p_pool = (x1 + x2) / (n1 + n2)
    
    # Standard error
    se = np.sqrt(p_pool * (1 - p_pool) * (1/n1 + 1/n2))
    
    if se == 0:
        return 0.0, 1.0
    
    # z-statistic
    z_stat = (p1 - p2) / se
    
    # Two-tailed p-value
    p_value = 2 * (1 - stats.norm.cdf(abs(z_stat)))
    
    return z_stat, p_value

def proportion_confidence_interval(n1, x1, n2, x2, confidence=0.95):
    """
    Compute confidence interval for the difference in proportions.
    
    Args:
        n1, x1: Group 1 trials and successes
        n2, x2: Group 2 trials and successes
        confidence: Confidence level (default 0.95 for 95% CI)
    
    Returns:
        (lower, upper): Tuple of (CI lower bound, CI upper bound)
    """
    p1 = x1 / n1
    p2 = x2 / n2
    
    diff = p1 - p2
    
    # Standard error for difference
    se = np.sqrt((p1 * (1 - p1) / n1) + (p2 * (1 - p2) / n2))
    
    # Critical value
    alpha = 1 - confidence
    z_crit = stats.norm.ppf(1 - alpha / 2)
    
    lower = diff - z_crit * se
    upper = diff + z_crit * se
    
    return lower, upper

def statistical_power(n, p1, p2, alpha=0.05):
    """
    Compute statistical power for two-proportion test.
    
    Args:
        n: Sample size per group (assumes equal allocation)
        p1: Control proportion
        p2: Treatment proportion
        alpha: Significance level (default 0.05)
    
    Returns:
        power: Probability of detecting true effect
    """
    # Pooled proportion under alternative
    p_pool = (p1 + p2) / 2
    
    # Standard error under null
    se_null = np.sqrt(2 * p_pool * (1 - p_pool) / n)
    
    # Standard error under alternative
    se_alt = np.sqrt(p1 * (1 - p1) / n + p2 * (1 - p2) / n)
    
    # Critical value (z for alpha/2)
    z_crit = stats.norm.ppf(1 - alpha / 2)
    
    # Critical value in terms of difference
    diff = abs(p2 - p1)
    critical_diff = z_crit * se_null
    
    # Power = P(|Z| > z_crit - diff/se_alt)
    z_power = (diff - critical_diff) / se_alt
    power = 1 - stats.norm.cdf(z_power) + stats.norm.cdf(-z_power - diff / se_alt)
    power = 1 - stats.norm.cdf(z_crit - diff / se_alt)
    
    return power

def minimum_detectable_effect(n, alpha=0.05, power=0.8, p_control=None):
    """
    Compute minimum detectable effect (MDE) for given sample size.
    
    Args:
        n: Sample size per group
        alpha: Significance level
        power: Desired statistical power
        p_control: Baseline proportion (if None, uses 0.5 for worst case)
    
    Returns:
        mde: Minimum detectable difference
    """
    if p_control is None:
        p_control = 0.5
    
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_beta = stats.norm.ppf(power)
    
    p_treatment = p_control  # placeholder, solve for difference
    
    # MDE formula for two proportions
    p_pool = p_control
    mde = (z_alpha + z_beta) * np.sqrt(2 * p_pool * (1 - p_pool) / n)
    
    return mde

def run_analysis(n_control, x_control, n_treatment, x_treatment, alpha=0.05):
    """
    Run full statistical analysis on two proportions.
    
    Args:
        n_control: Control group sample size
        x_control: Control group successes
        n_treatment: Treatment group sample size
        x_treatment: Treatment group successes
        alpha: Significance level (default 0.05)
    
    Returns:
        dict with z_stat, p_value, ci_lower, ci_upper, significant
    """
    z_stat, p_value = two_proportion_ztest(n_control, x_control, n_treatment, x_treatment)
    ci_lower, ci_upper = proportion_confidence_interval(n_control, x_control, n_treatment, x_treatment)
    
    significant = p_value < alpha
    
    return {
        'z_statistic': z_stat,
        'p_value': p_value,
        'ci_lower': ci_lower,
        'ci_upper': ci_upper,
        'significant': significant,
        'alpha': alpha
    }

if __name__ == '__main__':
    # Test with dummy data
    result = run_analysis(2500, 1550, 2500, 1775)
    print("Test Analysis:")
    for k, v in result.items():
        print(f"  {k}: {v}")
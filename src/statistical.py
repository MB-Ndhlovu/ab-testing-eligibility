import numpy as np
from scipy import stats

def two_proportion_ztest(n_success_a, n_total_a, n_success_b, n_total_b, alternative='two-sided'):
    """
    Two-proportion z-test comparing success rates between two groups.
    
    Returns: z_statistic, p_value
    """
    p_a = n_success_a / n_total_a if n_total_a > 0 else 0
    p_b = n_success_b / n_total_b if n_total_b > 0 else 0
    
    # Pooled proportion under null hypothesis
    p_pooled = (n_success_a + n_success_b) / (n_total_a + n_total_b)
    
    # Standard error
    se = np.sqrt(p_pooled * (1 - p_pooled) * (1/n_total_a + 1/n_total_b))
    
    if se == 0:
        return 0.0, 1.0
    
    z = (p_b - p_a) / se
    
    if alternative == 'two-sided':
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    elif alternative == 'greater':
        p_value = 1 - stats.norm.cdf(z)
    elif alternative == 'less':
        p_value = stats.norm.cdf(z)
    else:
        p_value = 2 * (1 - stats.norm.cdf(abs(z)))
    
    return z, p_value

def confidence_interval_diff(p_a, p_b, n_a, n_b, confidence=0.95):
    """
    Confidence interval for the difference in proportions (p_b - p_a).
    """
    se = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
    if se == 0:
        return (0.0, 0.0)
    
    z_crit = stats.norm.ppf((1 + confidence) / 2)
    diff = p_b - p_a
    margin = z_crit * se
    
    return (diff - margin, diff + margin)

def statistical_power(n_a, n_b, p_a, mde, alpha=0.05, alternative='two-sided'):
    """
    Compute statistical power for a two-proportion z-test.
    
    mde: minimum detectable effect (absolute difference)
    """
    p_b = p_a + mde
    se_null = np.sqrt(p_a * (1 - p_a) * (1/n_a + 1/n_b))
    se_alt = np.sqrt(p_b * (1 - p_b) * (1/n_a + 1/n_b))
    
    if se_null == 0 or se_alt == 0:
        return 0.0
    
    # Critical value under null
    z_crit = stats.norm.ppf(1 - alpha / 2) if alternative == 'two-sided' else stats.norm.ppf(1 - alpha)
    
    # Non-centrality parameter under alternative
    ncp = mde / se_alt
    
    # Power: P(reject H0 | H1 true)
    if alternative == 'two-sided':
        power = (1 - stats.norm.cdf(z_crit - ncp)) + stats.norm.cdf(-z_crit - ncp)
    else:
        power = 1 - stats.norm.cdf(z_crit - ncp)
    
    return power

def minimum_detectable_effect(n_a, n_b, p_a, power=0.8, alpha=0.05, alternative='two-sided'):
    """
    Find the minimum detectable effect for given power and sample sizes.
    """
    # Binary search for MDE
    low, high = 0.001, 1.0 - p_a
    tolerance = 0.0001
    
    for _ in range(100):
        mde = (low + high) / 2
        pwr = statistical_power(n_a, n_b, p_a, mde, alpha, alternative)
        
        if abs(pwr - power) < 0.01:
            return mde
        
        if pwr < power:
            low = mde
        else:
            high = mde
    
    return (low + high) / 2

if __name__ == '__main__':
    # Test with example numbers
    z, p = two_proportion_ztest(310, 500, 355, 500, alternative='two-sided')
    ci = confidence_interval_diff(310/500, 355/500, 500, 500)
    print(f"z={z:.4f}, p={p:.4f}, CI={ci}")
    
    pwr = statistical_power(2500, 2500, 0.62, 0.09)
    mde = minimum_detectable_effect(2500, 2500, 0.62, power=0.8)
    print(f"Power: {pwr:.4f}, MDE: {mde:.4f}")
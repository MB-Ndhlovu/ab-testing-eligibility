import pandas as pd
from src.data_generator import generate_credit_data, compute_group_stats
from src.statistical import two_proportion_ztest, confidence_interval, statistical_power

def run_simulation(seed=42):
    df = generate_credit_data(n=5000, seed=seed)
    
    stats_a = compute_group_stats(df, 'A')
    stats_b = compute_group_stats(df, 'B')
    
    results = {}
    
    for metric in ['approval_rate', 'default_rate']:
        n_a = stats_a['n']
        n_b = stats_b['n']
        p_a = stats_a[metric]
        p_b = stats_b[metric]
        
        z, p_value = two_proportion_ztest(n_a, p_a, n_b, p_b)
        ci_lower, ci_upper = confidence_interval(n_a, p_a, n_b, p_b)
        power = statistical_power(n_a, p_a, p_b)
        significant = p_value < 0.05
        
        results[metric] = {
            'group_a': p_a,
            'group_b': p_b,
            'treatment_effect': p_b - p_a,
            'z_statistic': round(z, 4),
            'p_value': round(p_value, 6),
            'ci_95_lower': round(ci_lower, 4),
            'ci_95_upper': round(ci_upper, 4),
            'statistical_power': round(power, 4),
            'significant_at_0.05': bool(significant)
        }
    
    results['group_stats'] = {
        'A': {k: round(v, 4) if isinstance(v, float) else v for k, v in stats_a.items()},
        'B': {k: round(v, 4) if isinstance(v, float) else v for k, v in stats_b.items()}
    }
    
    return results
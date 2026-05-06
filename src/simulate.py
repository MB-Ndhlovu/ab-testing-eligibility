import json
import numpy as np
from src.data_generator import generate_credit_data, get_group_stats
from src.statistical import two_proportion_ztest, confidence_interval_diff, statistical_power, minimum_detectable_effect

def make_serializable(obj):
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, (np.floating, float)):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_serializable(v) for v in obj]
    return obj

def run_simulation(df):
    stats = get_group_stats(df)
    results = {'metrics': {}, 'groups': stats}
    
    for metric in ['approval_rate', 'default_rate']:
        n_a = stats['A']['n']
        n_b = stats['B']['n']
        p_a = stats['A'][metric]
        p_b = stats['B'][metric]
        
        if metric == 'approval_rate':
            alt = 'larger'
        else:
            alt = 'smaller'
        
        z, p_val = two_proportion_ztest(n_a, p_a, n_b, p_b, alternative=alt)
        ci = confidence_interval_diff(n_a, p_a, n_b, p_b)
        
        effect = p_b - p_a
        power = statistical_power(n_a, p_a, p_b)
        mde = minimum_detectable_effect(n_a)
        
        significant = bool(p_val < 0.05)
        
        results['metrics'][metric] = {
            'group_A': round(float(p_a), 4),
            'group_B': round(float(p_b), 4),
            'difference': round(float(effect), 4),
            'z_statistic': round(float(z), 4),
            'p_value': round(float(p_val), 6),
            'ci_lower': round(float(ci[0]), 4),
            'ci_upper': round(float(ci[1]), 4),
            'significant_at_0.05': significant,
            'power': round(float(power), 4),
            'mde': round(float(mde), 4)
        }
    
    return results

if __name__ == '__main__':
    df = generate_credit_data()
    results = run_simulation(df)
    print(json.dumps(results, indent=2))
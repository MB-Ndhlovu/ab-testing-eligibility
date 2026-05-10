from src.data_generator import generate_credit_data, compute_group_stats
from src.statistical import two_proportion_ztest, confidence_interval_diff, statistical_power, minimum_detectable_effect

def run_experiment(seed=42):
    """
    Run the full A/B experiment simulation.
    """
    df = generate_credit_data(n=5000, seed=seed)
    stats = compute_group_stats(df)
    
    results = {}
    
    for metric in ['approval_rate', 'default_rate']:
        if metric == 'approval_rate':
            n_success_a = stats['A']['approval_count']
            n_total_a = stats['A']['n']
            n_success_b = stats['B']['approval_count']
            n_total_b = stats['B']['n']
            p_a = stats['A']['approval_rate']
            p_b = stats['B']['approval_rate']
            alternative = 'greater'  # B should be better
        else:
            # For default rate, approved only
            n_success_a = stats['A']['default_count']
            n_total_a = stats['A']['approval_count']
            n_success_b = stats['B']['default_count']
            n_total_b = stats['B']['approval_count']
            p_a = stats['A']['default_rate']
            p_b = stats['B']['default_rate']
            alternative = 'less'  # B should have lower default
        
        z, p = two_proportion_ztest(n_success_a, n_total_a, n_success_b, n_total_b, alternative='two-sided')
        ci = confidence_interval_diff(p_a, p_b, n_total_a, n_total_b, confidence=0.95)
        
        mde_80 = minimum_detectable_effect(n_total_a, n_total_b, p_a, power=0.8, alpha=0.05)
        mde_90 = minimum_detectable_effect(n_total_a, n_total_b, p_a, power=0.9, alpha=0.05)
        power_actual = statistical_power(n_total_a, n_total_b, p_a, abs(p_b - p_a), alpha=0.05)
        
        alpha = 0.05
        significant = p < alpha
        effect_direction = "positive (B > A)" if p_b > p_a else "negative (B < A)"
        
        results[metric] = {
            'group_a': {'rate': p_a, 'n': n_total_a, 'successes': int(n_success_a)},
            'group_b': {'rate': p_b, 'n': n_total_b, 'successes': int(n_success_b)},
            'treatment_effect': p_b - p_a,
            'z_statistic': z,
            'p_value': p,
            'ci_95': ci,
            'significant': significant,
            'alpha': alpha,
            'power_mde_80': mde_80,
            'power_mde_90': mde_90,
            'actual_power': power_actual,
            'effect_direction': effect_direction,
        }
    
    # Summary stats
    results['summary'] = {
        'n_total': len(df),
        'group_a_n': stats['A']['n'],
        'group_b_n': stats['B']['n'],
        'group_a_avg_loan': stats['A']['avg_loan_size'],
        'group_b_avg_loan': stats['B']['avg_loan_size'],
        'group_a_avg_proc_time': stats['A']['avg_processing_time'],
        'group_b_avg_proc_time': stats['B']['avg_processing_time'],
    }
    
    return results

if __name__ == '__main__':
    results = run_experiment()
    import json
    import numpy as np
    print(json.dumps(results, indent=2, default=lambda x: float(x) if isinstance(x, (float, np.floating)) else x))
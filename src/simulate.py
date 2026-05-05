import pandas as pd
import numpy as np
from src.data_generator import generate_credit_data, summarize_by_group
from src.statistical import two_proportion_ztest, confidence_interval, statistical_power

def run_simulation(seed=42):
    df = generate_credit_data(n=5000, seed=seed)
    summary = summarize_by_group(df)
    
    group_a = df[df['group'] == 'A']
    group_b = df[df['group'] == 'B']
    
    n_a = len(group_a)
    n_b = len(group_b)
    
    approved_a = group_a['approved'].mean()
    approved_b = group_b['approved'].mean()
    default_a = group_a[group_a['approved'] == 1]['defaulted'].mean()
    default_b = group_b[group_b['approved'] == 1]['defaulted'].mean()
    
    z_approval, p_approval = two_proportion_ztest(n_a, approved_a, n_b, approved_b)
    ci_approval = confidence_interval(n_a, approved_a, n_b, approved_b)
    
    z_default, p_default = two_proportion_ztest(n_a, default_a, n_b, default_b)
    ci_default = confidence_interval(n_a, default_a, n_b, default_b)
    
    power_approval = statistical_power(n_a, approved_a, approved_b)
    power_default = statistical_power(n_a, default_a, default_b)
    
    mde = minimum_detectable_effect(n_a)
    
    results = {
        'n_per_group': n_a,
        'approval_rate_A': approved_a,
        'approval_rate_B': approved_b,
        'default_rate_A': default_a,
        'default_rate_B': default_b,
        'approval_z': z_approval,
        'approval_p_value': p_approval,
        'approval_ci': ci_approval,
        'approval_significant': p_approval < 0.05,
        'default_z': z_default,
        'default_p_value': p_default,
        'default_ci': ci_default,
        'default_significant': p_default < 0.05,
        'power_approval': power_approval,
        'power_default': power_default,
        'mde': mde
    }
    
    return results, df, summary

def minimum_detectable_effect(n, alpha=0.05, power=0.80):
    from scipy import stats
    z_crit = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)
    mde = (z_crit + z_power) * np.sqrt(0.5 * 0.5 * (2 / n))
    return mde
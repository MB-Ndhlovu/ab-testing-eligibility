import pandas as pd
from src.data_generator import generate_credit_data
from src.statistical import (
    two_proportion_ztest,
    confidence_interval,
    statistical_power,
    minimum_detectable_effect
)

def summarize_group(df, group):
    g = df[df['group'] == group]
    approved = g['approved'].sum()
    defaulted = g['defaulted'].sum()
    n = len(g)
    n_approved = approved
    
    return {
        'n': n,
        'approved': approved,
        'defaulted': defaulted,
        'approval_rate': approved / n,
        'default_rate': defaulted / n_approved if n_approved > 0 else 0,
        'avg_loan_size': g.loc[g['approved'], 'loan_size'].mean() if n_approved > 0 else 0,
        'avg_processing_time': g.loc[g['approved'], 'processing_time'].mean() if n_approved > 0 else 0
    }

def run_simulation(n=5000, alpha=0.05):
    df = generate_credit_data(n=n)
    
    a = summarize_group(df, 'A')
    b = summarize_group(df, 'B')
    
    z_approval, p_approval, _, _, se_approval = two_proportion_ztest(
        a['n'], a['approved'], b['n'], b['approved']
    )
    ci_approval = confidence_interval(a['n'], a['approval_rate'], b['n'], b['approval_rate'])
    
    n_a_approved = a['approved']
    n_b_approved = b['approved']
    
    z_default, p_default, _, _, se_default = two_proportion_ztest(
        n_a_approved, a['defaulted'], n_b_approved, b['defaulted']
    )
    ci_default = confidence_interval(a['n'], a['default_rate'], b['n'], b['default_rate'])
    
    power_approval = statistical_power(a['n'], b['n'], a['approval_rate'], b['approval_rate'])
    mde_approval = minimum_detectable_effect(a['n'], b['n'])
    
    return {
        'group_a': a,
        'group_b': b,
        'approval_test': {
            'z_statistic': z_approval,
            'p_value': p_approval,
            'ci_95': ci_approval,
            'significant': p_approval < alpha,
            'mde': mde_approval,
            'power': power_approval
        },
        'default_test': {
            'z_statistic': z_default,
            'p_value': p_default,
            'ci_95': ci_default,
            'significant': p_default < alpha
        }
    }
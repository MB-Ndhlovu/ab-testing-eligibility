import numpy as np
import pandas as pd

def generate_credit_data(n=5000, seed=42):
    np.random.seed(seed)
    
    half = n // 2
    groups = ['A'] * half + ['B'] * half
    
    approval_rate_a = 0.62
    approval_rate_b = 0.71
    default_rate_a = 0.11
    default_rate_b = 0.09
    
    approved_a = np.random.random(half) < approval_rate_a
    approved_b = np.random.random(half) < approval_rate_b
    
    default_approved_a = approved_a & (np.random.random(half) < default_rate_a)
    default_approved_b = approved_b & (np.random.random(half) < default_rate_b)
    
    loan_size_a = np.where(approved_a, np.random.lognormal(9.5, 0.6, half), 0)
    loan_size_b = np.where(approved_b, np.random.lognormal(9.7, 0.6, half), 0)
    
    processing_time_a = np.where(
        approved_a,
        np.random.normal(48, 15, half),
        np.random.normal(72, 20, half)
    )
    processing_time_b = np.where(
        approved_b,
        np.random.normal(44, 14, half),
        np.random.normal(68, 18, half)
    )
    
    df = pd.DataFrame({
        'group': groups,
        'approved': list(approved_a) + list(approved_b),
        'defaulted': list(default_approved_a) + list(default_approved_b),
        'loan_size': list(loan_size_a) + list(loan_size_b),
        'processing_time': list(processing_time_a) + list(processing_time_b)
    })
    
    return df

def summarize_by_group(df):
    summary = df.groupby('group').agg(
        total=('approved', 'count'),
        approved=('approved', 'sum'),
        defaulted=('defaulted', 'sum'),
        approval_rate=('approved', 'mean'),
        default_rate=('defaulted', lambda x: x[df.loc[x.index, 'approved'] == 1].mean()),
        avg_loan_size=('loan_size', lambda x: x[x > 0].mean()),
        avg_processing_time=('processing_time', 'mean')
    ).reset_index()
    
    summary['default_rate'] = df[df['approved'] == 1].groupby('group')['defaulted'].mean().values
    
    return summary
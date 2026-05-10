import numpy as np
import pandas as pd

def generate_credit_data(n=5000, seed=42):
    np.random.seed(seed)
    
    half = n // 2
    
    # Group A (control): approval_rate ~0.62, default_rate ~0.11
    group_a_approved = np.random.random(half) < 0.62
    group_a_defaulted = np.random.random(half) < 0.11
    
    # Group B (treatment): approval_rate ~0.71, default_rate ~0.09
    group_b_approved = np.random.random(half) < 0.71
    group_b_defaulted = np.random.random(half) < 0.09
    
    df_a = pd.DataFrame({
        'loan_id': range(half),
        'group': 'A',
        'approved': group_a_approved,
        'defaulted': group_a_defaulted,
        'loan_size': np.random.lognormal(9.5, 0.6, half),
        'processing_time': np.random.exponential(48, half) + 10
    })
    
    df_b = pd.DataFrame({
        'loan_id': range(half, n),
        'group': 'B',
        'approved': group_b_approved,
        'defaulted': group_b_defaulted,
        'loan_size': np.random.lognormal(9.7, 0.6, half),
        'processing_time': np.random.exponential(45, half) + 8
    })
    
    df = pd.concat([df_a, df_b], ignore_index=True)
    df['loan_size'] = df['loan_size'].clip(1000, 500000).round(2)
    df['processing_time'] = df['processing_time'].round(1)
    
    return df


def compute_group_stats(df, group):
    g = df[df['group'] == group]
    n = len(g)
    return {
        'n': n,
        'approval_rate': g['approved'].mean(),
        'default_rate': g['defaulted'].mean(),
        'avg_loan_size': g['loan_size'].mean(),
        'avg_processing_time': g['processing_time'].mean()
    }
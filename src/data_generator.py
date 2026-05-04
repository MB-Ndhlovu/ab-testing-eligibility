import numpy as np
import pandas as pd

def generate_credit_data(n=5000, seed=42):
    np.random.seed(seed)
    
    half = n // 2
    groups = ['A'] * half + ['B'] * half
    
    approval_probs = {'A': 0.62, 'B': 0.71}
    default_probs = {'A': 0.11, 'B': 0.09}
    
    approval_rate = np.array([np.random.random() < approval_probs[g] for g in groups])
    default_rate = np.where(
        approval_rate,
        np.array([np.random.random() < default_probs[g] for g in groups]),
        False
    )
    
    base_loan_size = np.random.lognormal(mean=9.5, sigma=0.7, size=n)
    noise = np.random.normal(0, 0.1, size=n)
    avg_loan_size = np.where(approval_rate, base_loan_size * (1 + noise), 0.0)
    
    base_time = np.random.normal(loc=3.5, scale=1.2, size=n)
    time_noise = np.random.exponential(scale=0.5, size=n)
    processing_time = np.where(approval_rate, np.maximum(base_time + time_noise, 0.5), 0.0)
    
    df = pd.DataFrame({
        'group': groups,
        'approved': approval_rate,
        'defaulted': default_rate,
        'loan_size': avg_loan_size,
        'processing_time': processing_time
    })
    
    return df
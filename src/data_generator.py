"""
Generate synthetic credit eligibility data for A/B testing.
"""

import numpy as np

def generate_data(n=5000, seed=42):
    np.random.seed(seed)
    
    # Split into control (A) and treatment (B)
    n_a = n // 2
    n_b = n - n_a
    
    # Group A: control - current eligibility model
    # Approval ~62%, Default ~11%
    approved_a = np.random.random(n_a) < 0.62
    defaulted_a = approved_a & (np.random.random(n_a) < 0.11 / 0.62)
    
    # Group B: treatment - new eligibility model
    # Approval ~71%, Default ~9%
    approved_b = np.random.random(n_b) < 0.71
    defaulted_b = approved_b & (np.random.random(n_b) < 0.09 / 0.71)
    
    # Generate other features
    def generate_loan_features(n, approved_mask, base_size=15000, size_std=8000):
        loan_sizes = np.random.exponential(base_size, n) + np.random.normal(5000, 2000, n)
        loan_sizes = np.clip(loan_sizes, 1000, 100000)
        loan_sizes[~approved_mask] = 0
        
        processing_times = np.random.gamma(2, 5, n) + np.random.normal(10, 3, n)
        processing_times = np.clip(processing_times, 1, 72)
        processing_times[~approved_mask] = 0
        
        return loan_sizes, processing_times
    
    loan_sizes_a, proc_times_a = generate_loan_features(n_a, approved_a)
    loan_sizes_b, proc_times_b = generate_loan_features(n_b, approved_b)
    
    # Build DataFrame-like dict
    data = {
        'group': ['A'] * n_a + ['B'] * n_b,
        'approved': np.concatenate([approved_a, approved_b]),
        'defaulted': np.concatenate([defaulted_a, defaulted_b]),
        'loan_size': np.concatenate([loan_sizes_a, loan_sizes_b]),
        'processing_time': np.concatenate([proc_times_a, proc_times_b]),
    }
    
    return data

def compute_summary_stats(data):
    group_a_mask = np.array(data['group']) == 'A'
    group_b_mask = np.array(data['group']) == 'B'
    
    approved_a = np.array(data['approved'])[group_a_mask]
    approved_b = np.array(data['approved'])[group_b_mask]
    defaulted_a = np.array(data['defaulted'])[group_a_mask]
    defaulted_b = np.array(data['defaulted'])[group_b_mask]
    loan_size_a = np.array(data['loan_size'])[group_a_mask & np.array(data['approved'])]
    loan_size_b = np.array(data['loan_size'])[group_b_mask & np.array(data['approved'])]
    proc_a = np.array(data['processing_time'])[group_a_mask & np.array(data['approved'])]
    proc_b = np.array(data['processing_time'])[group_b_mask & np.array(data['approved'])]
    
    return {
        'group_a': {
            'n': group_a_mask.sum(),
            'approval_rate': approved_a.mean(),
            'default_rate': defaulted_a.mean(),
            'avg_loan_size': loan_size_a.mean() if len(loan_size_a) > 0 else 0,
            'avg_processing_time': proc_a.mean() if len(proc_a) > 0 else 0,
        },
        'group_b': {
            'n': group_b_mask.sum(),
            'approval_rate': approved_b.mean(),
            'default_rate': defaulted_b.mean(),
            'avg_loan_size': loan_size_b.mean() if len(loan_size_b) > 0 else 0,
            'avg_processing_time': proc_b.mean() if len(proc_b) > 0 else 0,
        }
    }
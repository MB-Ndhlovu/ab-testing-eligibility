import numpy as np
import pandas as pd

def generate_credit_data(n=5000, seed=42):
    np.random.seed(seed)
    
    # Split into control (A) and treatment (B)
    n_a = n // 2
    n_b = n - n_a
    
    # Group A: control - approval ~0.62, default ~0.11
    # Group B: treatment - approval ~0.71, default ~0.09
    
    # Simulate approval decision with slight noise
    approved_a = np.random.random(n_a) < 0.62 + np.random.normal(0, 0.02, n_a)
    approved_b = np.random.random(n_b) < 0.71 + np.random.normal(0, 0.02, n_b)
    
    # Simulate default given approval - add noise so results aren't perfectly clean
    defaulted_a = np.where(approved_a, 
                          np.random.random(n_a) < 0.11 + np.random.normal(0, 0.015, n_a),
                          False)
    defaulted_b = np.where(approved_b,
                           np.random.random(n_b) < 0.09 + np.random.normal(0, 0.015, n_b),
                           False)
    
    # Loan size: skewed distribution, approved loans only
    loan_size_a = np.where(approved_a, 
                           np.random.lognormal(mean=10.5, sigma=0.6, size=n_a), 0)
    loan_size_b = np.where(approved_b,
                           np.random.lognormal(mean=10.7, sigma=0.6, size=n_b), 0)
    
    # Processing time: seconds, slightly faster for B
    proc_time_a = np.random.normal(45, 8, n_a)
    proc_time_b = np.random.normal(42, 8, n_b)
    
    df_a = pd.DataFrame({
        'group': 'A',
        'approved': approved_a,
        'defaulted': defaulted_a,
        'loan_size': loan_size_a,
        'processing_time': proc_time_a
    })
    
    df_b = pd.DataFrame({
        'group': 'B',
        'approved': approved_b,
        'defaulted': defaulted_b,
        'loan_size': loan_size_b,
        'processing_time': proc_time_b
    })
    
    df = pd.concat([df_a, df_b], ignore_index=True)
    
    return df

def compute_group_stats(df):
    stats = {}
    for group in ['A', 'B']:
        g = df[df['group'] == group]
        approved = g['approved'].sum()
        total = len(g)
        defaulted = g['defaulted'].sum()
        approved_count = g['approved'].sum()
        
        stats[group] = {
            'n': total,
            'approval_count': approved_count,
            'approval_rate': approved_count / total,
            'default_count': defaulted,
            'default_rate': defaulted / approved_count if approved_count > 0 else 0,
            'avg_loan_size': g.loc[g['approved'], 'loan_size'].mean() if approved_count > 0 else 0,
            'avg_processing_time': g['processing_time'].mean()
        }
    return stats

if __name__ == '__main__':
    df = generate_credit_data()
    print(df.head(10))
    stats = compute_group_stats(df)
    for g, s in stats.items():
        print(f"\nGroup {g}:")
        for k, v in s.items():
            print(f"  {k}: {v:.4f}" if isinstance(v, float) else f"  {k}: {v}")
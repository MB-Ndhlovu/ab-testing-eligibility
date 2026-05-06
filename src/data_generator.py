import numpy as np
import pandas as pd

def generate_credit_data(n=5000, seed=42):
    np.random.seed(seed)
    
    half = n // 2
    group = np.array(['A'] * half + ['B'] * half)
    np.random.shuffle(group)
    
    approved = np.zeros(n, dtype=bool)
    defaulted = np.zeros(n, dtype=bool)
    loan_size = np.zeros(n)
    processing_time = np.zeros(n)
    
    for i in range(n):
        if group[i] == 'A':
            p_approve = 0.62 + np.random.normal(0, 0.05)
            p_default = 0.11 + np.random.normal(0, 0.02)
        else:
            p_approve = 0.71 + np.random.normal(0, 0.05)
            p_default = 0.09 + np.random.normal(0, 0.02)
        
        approved[i] = np.random.random() < max(0.3, min(0.9, p_approve))
        
        if approved[i]:
            defaulted[i] = np.random.random() < max(0.01, min(0.25, p_default))
            base_size = np.random.lognormal(9.5, 0.6)
            loan_size[i] = min(base_size, 50000)
            processing_time[i] = np.random.gamma(2, 15) + np.random.normal(25, 5)
        else:
            loan_size[i] = 0
            processing_time[i] = np.random.gamma(2, 10) + np.random.normal(15, 4)
    
    df = pd.DataFrame({
        'application_id': range(1, n + 1),
        'group': group,
        'approved': approved,
        'defaulted': defaulted,
        'loan_size': np.round(loan_size, 2),
        'processing_time': np.round(processing_time, 1)
    })
    
    return df

def get_group_stats(df):
    stats = {}
    for grp in ['A', 'B']:
        grp_df = df[df['group'] == grp]
        n_approved = grp_df['approved'].sum()
        n_total = len(grp_df)
        n_defaulted = grp_df['defaulted'].sum()
        approved_loan_df = grp_df[grp_df['approved']]
        
        stats[grp] = {
            'n': n_total,
            'approval_rate': n_approved / n_total,
            'default_rate': n_defaulted / n_approved if n_approved > 0 else 0,
            'avg_loan_size': approved_loan_df['loan_size'].mean() if len(approved_loan_df) > 0 else 0,
            'avg_processing_time': grp_df['processing_time'].mean()
        }
    return stats

if __name__ == '__main__':
    df = generate_credit_data()
    df.to_csv('/home/workspace/Projects/ab-testing-eligibility/credit_data.csv', index=False)
    print(f"Generated {len(df)} rows")
    print(df.head())
    stats = get_group_stats(df)
    for grp, s in stats.items():
        print(f"Group {grp}: approval={s['approval_rate']:.3f}, default={s['default_rate']:.3f}")
import numpy as np
import pandas as pd

def generate_credit_data(n=5000, seed=42):
    np.random.seed(seed)
    data = []

    for group in ['A', 'B']:
        for i in range(n):
            if group == 'A':
                approved = np.random.random() < 0.62
                defaulted = np.random.random() < 0.11 if approved else False
                loan_size = np.random.lognormal(9.5, 0.8) if approved else 0
                processing_time = np.random.normal(5.2, 1.5)
            else:
                approved = np.random.random() < 0.71
                defaulted = np.random.random() < 0.09 if approved else False
                loan_size = np.random.lognormal(9.7, 0.75) if approved else 0
                processing_time = np.random.normal(4.8, 1.4)

            data.append({
                'group': group,
                'approved': int(approved),
                'defaulted': int(defaulted),
                'loan_size': round(loan_size, 2),
                'processing_time': round(max(0.5, processing_time), 2)
            })

    return pd.DataFrame(data)

def compute_group_metrics(df):
    metrics = {}
    for group in ['A', 'B']:
        g = df[df['group'] == group]
        n = len(g)
        approved = g['approved'].sum()
        defaulted = g['defaulted'].sum()
        approved_with_loan = g[g['approved'] == 1]
        
        metrics[group] = {
            'n': n,
            'approval_rate': approved / n,
            'default_rate': defaulted / n,
            'avg_loan_size': approved_with_loan['loan_size'].mean() if len(approved_with_loan) > 0 else 0,
            'avg_processing_time': g['processing_time'].mean()
        }
    return metrics
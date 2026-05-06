import numpy as np
import pandas as pd

def generate_loan_data(n=5000, seed=42):
    """Generate synthetic loan application data for A/B test.

    Args:
        n: Total number of applicants
        seed: Random seed for reproducibility

    Returns:
        DataFrame with columns: applicant_id, group, approved, defaulted,
                                 loan_size, processing_time_days
    """
    np.random.seed(seed)
    groups = np.random.choice(['A', 'B'], size=n, p=[0.5, 0.5])

    approved = np.zeros(n, dtype=int)
    defaulted = np.zeros(n, dtype=int)
    loan_size = np.zeros(n)
    processing_time = np.zeros(n)

    for i in range(n):
        if groups[i] == 'A':
            # Control: approval ~62%, default ~11% of approved
            if np.random.random() < 0.62:
                approved[i] = 1
                loan_size[i] = np.random.lognormal(10.2, 0.5)
                processing_time[i] = np.random.gamma(5, 1.2) + 2
                if np.random.random() < 0.11:
                    defaulted[i] = 1
            else:
                loan_size[i] = 0
                processing_time[i] = np.random.gamma(3, 0.8) + 1
        else:
            # Treatment: approval ~71%, default ~9% of approved
            if np.random.random() < 0.71:
                approved[i] = 1
                loan_size[i] = np.random.lognormal(10.4, 0.5)
                processing_time[i] = np.random.gamma(4, 1.0) + 1.5
                if np.random.random() < 0.09:
                    defaulted[i] = 1
            else:
                loan_size[i] = 0
                processing_time[i] = np.random.gamma(3, 0.8) + 1

    # Add realistic noise: some random fluctuation in the underlying probabilities
    noise = np.random.normal(0, 0.02, size=n)
    approved_noise = ((groups == 'A') * (0.62 + noise) +
                       (groups == 'B') * (0.71 + noise * 0.8))
    approved = (np.random.random(n) < np.clip(approved_noise, 0, 1)).astype(int)
    # Recalculate defaults for newly approved
    defaulted = np.zeros(n, dtype=int)
    for i in range(n):
        if approved[i]:
            base_default = 0.11 if groups[i] == 'A' else 0.09
            defaulted[i] = 1 if np.random.random() < base_default + np.random.normal(0, 0.015) else 0

    return pd.DataFrame({
        'applicant_id': range(1, n + 1),
        'group': groups,
        'approved': approved,
        'defaulted': defaulted,
        'loan_size': np.round(loan_size, 2),
        'processing_time_days': np.round(processing_time, 2)
    })

def compute_group_stats(df):
    """Compute summary statistics per group."""
    stats = {}
    for group in ['A', 'B']:
        subset = df[df['group'] == group]
        n = len(subset)
        n_approved = subset['approved'].sum()
        n_defaulted = subset['defaulted'].sum()
        stats[group] = {
            'n': n,
            'approval_rate': n_approved / n,
            'default_rate': n_defaulted / n_approved if n_approved > 0 else 0,
            'avg_loan_size': subset[subset['approved'] == 1]['loan_size'].mean(),
            'avg_processing_time': subset['processing_time_days'].mean()
        }
    return stats
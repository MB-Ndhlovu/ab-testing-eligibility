"""
Data generator for synthetic loan application data.
Generates 5000 rows split into control (A) and treatment (B) groups.
"""
import numpy as np
import pandas as pd


def generate_loan_data(n=5000, seed=42):
    """
    Generate synthetic loan application data.

    Args:
        n: Total number of loan applications
        seed: Random seed for reproducibility

    Returns:
        DataFrame with columns: group, approved, defaulted, loan_size, processing_time
    """
    np.random.seed(seed)

    half = n // 2
    groups = np.array(['A'] * half + ['B'] * half)

    # Loan sizes: realistic distribution from R50,000 to R500,000
    loan_sizes = np.random.lognormal(mean=11.5, sigma=0.7, size=n)
    loan_sizes = np.clip(loan_sizes, 50000, 500000)

    # Processing times: hours, skewed distribution
    processing_times = np.random.gamma(shape=2.5, scale=4, size=n) + 1
    processing_times = np.clip(processing_times, 1, 72)

    # Approval outcomes with noise
    noise_approval = np.random.normal(0, 0.03, n)
    approval_probs = np.where(groups == 'A', 0.62 + noise_approval, 0.71 + noise_approval)
    approval_probs = np.clip(approval_probs, 0.1, 0.9)
    approved = (np.random.random(n) < approval_probs).astype(int)

    # Default outcomes conditional on approval, with noise
    # Base default probabilities
    base_default = np.where(groups == 'A', 0.11, 0.09)
    noise_default = np.random.normal(0, 0.02, n)
    default_probs = np.clip(base_default + noise_default, 0.02, 0.25)

    # Apply default only to approved loans
    defaulted = ((np.random.random(n) < default_probs) & (approved == 1)).astype(int)

    df = pd.DataFrame({
        'group': groups,
        'approved': approved,
        'defaulted': defaulted,
        'loan_size': loan_sizes.astype(int),
        'processing_time': np.round(processing_times, 1)
    })

    return df


def compute_group_metrics(df):
    """Compute aggregate metrics per group."""
    metrics = {}
    for group in ['A', 'B']:
        subset = df[df['group'] == group]
        n = len(subset)
        n_approved = subset['approved'].sum()
        n_defaulted = subset['defaulted'].sum()

        metrics[group] = {
            'n': n,
            'approval_rate': n_approved / n,
            'default_rate': n_defaulted / n_approved if n_approved > 0 else 0,
            'avg_loan_size': subset[subset['approved'] == 1]['loan_size'].mean() if n_approved > 0 else 0,
            'avg_processing_time': subset['processing_time'].mean()
        }
    return metrics
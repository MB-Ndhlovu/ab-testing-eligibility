"""Generate synthetic loan application data for A/B testing."""

import numpy as np
import pandas as pd


def generate_loan_data(n=5000, seed=42):
    """
    Generate synthetic loan application data.

    Args:
        n: Total number of records (split evenly between A and B)
        seed: Random seed for reproducibility

    Returns:
        DataFrame with columns: group, approved, defaulted, loan_size, processing_time
    """
    np.random.seed(seed)

    half = n // 2

    # Group A (control): approval ~62%, default ~11%
    group_a_approved_probs = 0.62
    group_a_default_probs = 0.11

    group_a_approved = np.random.random(half) < group_a_approved_probs
    # Default rate is conditional on being approved
    group_a_defaulted = group_a_approved & (np.random.random(half) < group_a_default_probs)

    # Group B (treatment): approval ~71%, default ~9%
    group_b_approved_probs = 0.71
    group_b_default_probs = 0.09

    group_b_approved = np.random.random(half) < group_b_approved_probs
    group_b_defaulted = group_b_approved & (np.random.random(half) < group_b_default_probs)

    # Loan sizes (in thousands) - add noise
    group_a_loan_sizes = np.random.lognormal(mean=4.2, sigma=0.6, size=half)
    group_b_loan_sizes = np.random.lognormal(mean=4.3, sigma=0.6, size=half)

    # Processing times (in minutes) - add noise
    group_a_times = np.random.lognormal(mean=2.8, sigma=0.5, size=half) + np.random.normal(0, 5, half)
    group_b_times = np.random.lognormal(mean=2.5, sigma=0.5, size=half) + np.random.normal(0, 5, half)

    # Clip negative processing times
    group_a_times = np.clip(group_a_times, 1, None)
    group_b_times = np.clip(group_b_times, 1, None)

    # Build DataFrame
    df_a = pd.DataFrame({
        'group': 'A',
        'approved': group_a_approved,
        'defaulted': group_a_defaulted,
        'loan_size': np.round(group_a_loan_sizes, 2),
        'processing_time': np.round(group_a_times, 2)
    })

    df_b = pd.DataFrame({
        'group': 'B',
        'approved': group_b_approved,
        'defaulted': group_b_defaulted,
        'loan_size': np.round(group_b_loan_sizes, 2),
        'processing_time': np.round(group_b_times, 2)
    })

    df = pd.concat([df_a, df_b], ignore_index=True)

    # Shuffle
    df = df.sample(frac=1, random_state=seed).reset_index(drop=True)

    return df


def compute_group_metrics(df):
    """Compute approval rate, default rate, avg loan size, avg processing time per group."""
    results = {}

    for group in ['A', 'B']:
        subset = df[df['group'] == group]
        n = len(subset)

        approved_rate = subset['approved'].mean()
        # Default rate is proportion of defaulted among approved loans
        approved_subset = subset[subset['approved']]
        default_rate = approved_subset['defaulted'].mean() if len(approved_subset) > 0 else 0

        avg_loan_size = subset[subset['approved']]['loan_size'].mean() if approved_subset.shape[0] > 0 else 0
        avg_processing_time = subset[subset['approved']]['processing_time'].mean() if approved_subset.shape[0] > 0 else 0

        results[group] = {
            'n': n,
            'approved_count': int(subset['approved'].sum()),
            'approval_rate': approved_rate,
            'default_count': int(subset['defaulted'].sum()),
            'default_rate': default_rate,
            'avg_loan_size': avg_loan_size if not pd.isna(avg_loan_size) else 0,
            'avg_processing_time': avg_processing_time if not pd.isna(avg_processing_time) else 0
        }

    return results


if __name__ == '__main__':
    df = generate_loan_data()
    print(df.head(10))
    print("\nMetrics:")
    print(compute_group_metrics(df))
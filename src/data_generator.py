"""
Generate synthetic loan application data for A/B test.
"""

import numpy as np
import pandas as pd


def generate_data(n=5000, seed=42):
    """
    Generate synthetic loan application data.

    Parameters:
        n: total number of applicants
        seed: random seed for reproducibility

    Returns:
        DataFrame with columns: applicant_id, group, approved, defaulted,
                                 loan_amount, processing_time
    """
    np.random.seed(seed)

    n_per_group = n // 2

    # Group A (control): current eligibility rules
    # ~62% approval rate, ~11% default rate
    group_a_approval_rate = 0.62
    group_a_default_rate = 0.11

    # Group B (treatment): new eligibility rules
    # ~71% approval rate, ~9% default rate
    group_b_approval_rate = 0.71
    group_b_default_rate = 0.09

    # Generate group A data
    group_a_approved = np.random.random(n_per_group) < group_a_approval_rate
    # Add noise to approval rate
    noise_approval_a = np.random.normal(0, 0.03, n_per_group)
    group_a_approved = np.random.random(n_per_group) < (group_a_approval_rate + noise_approval_a)

    group_a_defaulted = np.zeros(n_per_group, dtype=bool)
    group_a_defaulted[group_a_approved] = np.random.random(group_a_approved.sum()) < (group_a_default_rate + np.random.normal(0, 0.02, group_a_approved.sum()))

    # Generate group B data
    noise_approval_b = np.random.normal(0, 0.03, n_per_group)
    group_b_approved = np.random.random(n_per_group) < (group_b_approval_rate + noise_approval_b)

    group_b_defaulted = np.zeros(n_per_group, dtype=bool)
    group_b_defaulted[group_b_approved] = np.random.random(group_b_approved.sum()) < (group_b_default_rate + np.random.normal(0, 0.02, group_b_approved.sum()))

    # Loan amounts (in thousands)
    base_loan_amounts = np.random.lognormal(4.2, 0.6, n)  # median ~67k

    # Processing times (in hours)
    base_processing_times = np.random.gamma(2.5, 2.0, n) + np.random.uniform(0.5, 2.0, n)

    # Build DataFrame
    data = {
        'applicant_id': range(n),
        'group': ['A'] * n_per_group + ['B'] * n_per_group,
        'approved': np.concatenate([group_a_approved, group_b_approved]),
        'defaulted': np.concatenate([group_a_defaulted, group_b_defaulted]),
        'loan_amount': base_loan_amounts,
        'processing_time': base_processing_times,
    }

    df = pd.DataFrame(data)

    # Add some noise to continuous metrics
    df['loan_amount'] = df['loan_amount'] * np.random.uniform(0.85, 1.15, n)
    df['processing_time'] = df['processing_time'] * np.random.uniform(0.9, 1.1, n)

    # For non-approved loans, loan amount should be 0
    df.loc[~df['approved'], 'loan_amount'] = 0

    return df


def compute_group_stats(df):
    """
    Compute summary statistics for each group.

    Returns:
        dict with stats for each group
    """
    stats = {}
    for group in ['A', 'B']:
        grp = df[df['group'] == group]
        n_approved = grp['approved'].sum()
        n_defaulted = grp['defaulted'].sum()
        n_total = len(grp)

        stats[group] = {
            'n_total': n_total,
            'n_approved': n_approved,
            'approval_rate': n_approved / n_total,
            'default_rate': n_defaulted / n_approved if n_approved > 0 else 0,
            'avg_loan_amount': grp.loc[grp['approved'], 'loan_amount'].mean() if n_approved > 0 else 0,
            'avg_processing_time': grp['processing_time'].mean(),
        }

    return stats


if __name__ == '__main__':
    df = generate_data()
    print(f"Generated {len(df)} rows")
    print(df.head(10))
    stats = compute_group_stats(df)
    for group, s in stats.items():
        print(f"\nGroup {group}:")
        for k, v in s.items():
            if isinstance(v, float):
                print(f"  {k}: {v:.4f}")
            else:
                print(f"  {k}: {v}")
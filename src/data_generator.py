"""Generate synthetic loan application data for A/B testing."""

import numpy as np
import pandas as pd

np.random.seed(42)


def generate_loan_data(n=2500, approval_rate=0.62, default_rate=0.11):
    """
    Generate synthetic loan data for a single group.

    Parameters
    ----------
    n : int
        Number of loan applications
    approval_rate : float
        Target approval rate for the group
    default_rate : float
        Target default rate for approved loans

    Returns
    -------
    pd.DataFrame
        DataFrame with loan application records
    """
    approved = np.random.random(n) < approval_rate

    n_approved = approved.sum()
    defaulted = np.zeros(n, dtype=bool)
    defaulted[approved] = np.random.random(n_approved) < default_rate

    base_loan_size = np.random.lognormal(mean=10.5, sigma=0.6, size=n)

    base_loan_size = np.clip(base_loan_size, 1000, 500000)

    loan_size = base_loan_size * (1 + np.random.uniform(-0.1, 0.1, size=n))

    loan_size[~approved] = 0

    processing_time = np.where(
        approved,
        np.random.gamma(shape=3, scale=4, size=n) + np.random.uniform(0, 8, size=n),
        np.random.gamma(shape=2, scale=3, size=n) + np.random.uniform(0, 5, size=n)
    )

    return pd.DataFrame({
        'approved': approved,
        'defaulted': defaulted,
        'loan_size': loan_size,
        'processing_time': processing_time
    })


def generate_experiment_data():
    """
    Generate data for both control (Group A) and treatment (Group B).

    Returns
    -------
    dict
        Dictionary with 'group_a' and 'group_b' DataFrames
    """
    group_a = generate_loan_data(
        n=2500,
        approval_rate=0.62,
        default_rate=0.11
    )
    group_a['group'] = 'A'

    group_b = generate_loan_data(
        n=2500,
        approval_rate=0.71,
        default_rate=0.09
    )
    group_b['group'] = 'B'

    combined = pd.concat([group_a, group_b], ignore_index=True)
    combined['application_id'] = range(1, len(combined) + 1)

    return combined


def compute_group_stats(df, group_col='group'):
    """Compute summary statistics for each group."""
    stats = {}
    for group in df[group_col].unique():
        subset = df[df[group_col] == group]
        approved_count = subset['approved'].sum()
        total = len(subset)
        approved_mask = subset['approved']

        stats[group] = {
            'n': total,
            'approvals': approved_count,
            'approval_rate': approved_count / total,
            'defaults': subset['defaulted'].sum(),
            'default_rate': subset['defaulted'].sum() / approved_mask.sum() if approved_mask.sum() > 0 else 0,
            'avg_loan_size': subset.loc[approved_mask, 'loan_size'].mean() if approved_mask.sum() > 0 else 0,
            'avg_processing_time': subset['processing_time'].mean()
        }
    return stats


if __name__ == '__main__':
    data = generate_experiment_data()
    stats = compute_group_stats(data)
    print("Group Statistics:")
    for group, s in stats.items():
        print(f"\nGroup {group}:")
        print(f"  n = {s['n']}")
        print(f"  Approval rate: {s['approval_rate']:.4f}")
        print(f"  Default rate: {s['default_rate']:.4f}")
        print(f"  Avg loan size: ${s['avg_loan_size']:,.2f}")
        print(f"  Avg processing time: {s['avg_processing_time']:.2f} hours")
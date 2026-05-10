import numpy as np
import pandas as pd
from typing import Tuple


def generate_loan_data(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic loan application data for A/B test.

    Args:
        n: Total number of applicants
        seed: Random seed for reproducibility

    Returns:
        DataFrame with columns: applicant_id, group, approved, defaulted,
                                loan_size, processing_time
    """
    np.random.seed(seed)
    half = n // 2

    # Control group A: current model
    # Treatment group B: new model

    # Group A: approval_rate ~0.62, default_rate ~0.11 (conditional on approved)
    group_a_approved = np.random.random(half) < 0.62

    # Default rate conditional on approval
    group_a_defaulted = np.where(
        group_a_approved,
        np.random.random(half) < 0.11,
        False
    )

    # Group B: approval_rate ~0.71, default_rate ~0.09
    group_b_approved = np.random.random(half) < 0.71

    group_b_defaulted = np.where(
        group_b_approved,
        np.random.random(half) < 0.09,
        False
    )

    # Loan sizes: log-normal distribution (realistic for loans)
    group_a_loan_size = np.random.lognormal(mean=10.5, sigma=0.8, size=half)
    group_a_loan_size = np.clip(group_a_loan_size, 1000, 500000)

    group_b_loan_size = np.random.lognormal(mean=10.7, sigma=0.75, size=half)
    group_b_loan_size = np.clip(group_b_loan_size, 1000, 500000)

    # Processing time in minutes: skewed distribution
    group_a_proc_time = np.random.gamma(shape=3, scale=15, size=half) + 5
    group_b_proc_time = np.random.gamma(shape=3.5, scale=12, size=half) + 4

    # Combine
    df_a = pd.DataFrame({
        'applicant_id': range(half),
        'group': 'A',
        'approved': group_a_approved,
        'defaulted': group_a_defaulted,
        'loan_size': group_a_loan_size,
        'processing_time': group_a_proc_time
    })

    df_b = pd.DataFrame({
        'applicant_id': range(half, n),
        'group': 'B',
        'approved': group_b_approved,
        'defaulted': group_b_defaulted,
        'loan_size': group_b_loan_size,
        'processing_time': group_b_proc_time
    })

    return pd.concat([df_a, df_b], ignore_index=True)


def compute_group_stats(df: pd.DataFrame) -> dict:
    """Compute summary statistics for each group."""
    stats = {}
    for group in ['A', 'B']:
        grp = df[df['group'] == group]
        approved_count = grp['approved'].sum()
        total = len(grp)
        approved_approved = grp[grp['approved']]
        defaulted_count = approved_approved['defaulted'].sum()

        stats[group] = {
            'n': total,
            'approval_rate': approved_count / total,
            'default_rate': defaulted_count / approved_count if approved_count > 0 else 0,
            'avg_loan_size': grp['loan_size'].mean(),
            'processing_time_mean': grp['processing_time'].mean(),
        }
    return stats


if __name__ == '__main__':
    df = generate_loan_data()
    print(df.head())
    print("\nGroup stats:")
    for group, s in compute_group_stats(df).items():
        print(f"Group {group}: {s}")
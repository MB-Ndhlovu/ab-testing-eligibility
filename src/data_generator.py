"""Generate synthetic credit eligibility data for A/B testing."""
import numpy as np
import pandas as pd

np.random.seed(42)


def generate_data(n=5000):
    """Generate synthetic loan applicant data for two groups.

    Args:
        n: Number of applicants per group (default 5000)

    Returns:
        DataFrame with columns: group, approved, defaulted, loan_size, processing_time
    """
    # Group A: Control (current model)
    # Approval rate ~0.62, default rate ~0.11
    group_a_size = n
    group_a_approved = np.random.binomial(1, 0.62, group_a_size)
    # Default rate is conditional on approval
    group_a_defaulted = np.where(
        group_a_approved == 1,
        np.random.binomial(1, 0.11, group_a_size),
        0
    )
    group_a_loan_size = np.where(
        group_a_approved == 1,
        np.random.lognormal(np.log(15000), 0.4, group_a_size),
        0
    )
    group_a_processing_time = np.where(
        group_a_approved == 1,
        np.random.gamma(4, 11, group_a_size) + np.random.uniform(5, 15, group_a_size),
        np.random.gamma(3, 8, group_a_size) + np.random.uniform(2, 8, group_a_size)
    )

    # Group B: Treatment (new model)
    # Approval rate ~0.71, default rate ~0.09
    group_b_size = n
    group_b_approved = np.random.binomial(1, 0.71, group_b_size)
    group_b_defaulted = np.where(
        group_b_approved == 1,
        np.random.binomial(1, 0.09, group_b_size),
        0
    )
    group_b_loan_size = np.where(
        group_b_approved == 1,
        np.random.lognormal(np.log(16500), 0.4, group_b_size),
        0
    )
    group_b_processing_time = np.where(
        group_b_approved == 1,
        np.random.gamma(3.5, 10, group_b_size) + np.random.uniform(3, 12, group_b_size),
        np.random.gamma(3, 8, group_b_size) + np.random.uniform(2, 8, group_b_size)
    )

    # Combine into DataFrame
    df_a = pd.DataFrame({
        'applicant_id': range(1, n + 1),
        'group': 'A',
        'approved': group_a_approved,
        'defaulted': group_a_defaulted,
        'loan_size': np.round(group_a_loan_size, 2),
        'processing_time': np.round(group_a_processing_time, 2)
    })

    df_b = pd.DataFrame({
        'applicant_id': range(n + 1, 2 * n + 1),
        'group': 'B',
        'approved': group_b_approved,
        'defaulted': group_b_defaulted,
        'loan_size': np.round(group_b_loan_size, 2),
        'processing_time': np.round(group_b_processing_time, 2)
    })

    df = pd.concat([df_a, df_b], ignore_index=True)
    return df


def compute_group_stats(df):
    """Compute summary statistics for each group."""
    stats = {}
    for group in ['A', 'B']:
        subset = df[df['group'] == group]
        n = len(subset)
        n_approved = subset['approved'].sum()
        n_defaulted = subset['defaulted'].sum()
        approved_loans = subset[subset['approved'] == 1]

        stats[group] = {
            'n': n,
            'approval_rate': n_approved / n,
            'default_rate': n_defaulted / n_approved if n_approved > 0 else 0,
            'avg_loan_size': approved_loans['loan_size'].mean() if len(approved_loans) > 0 else 0,
            'avg_processing_time': subset['processing_time'].mean()
        }
    return stats


if __name__ == '__main__':
    df = generate_data()
    print(f"Generated {len(df)} rows")
    print(df.head())
    print("\nGroup statistics:")
    for group, s in compute_group_stats(df).items():
        print(f"Group {group}: {s}")
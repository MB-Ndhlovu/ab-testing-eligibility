import numpy as np
import pandas as pd

def generate_credit_data(n=5000, seed=42):
    """Generate synthetic credit eligibility data for A/B test.

    Args:
        n: Total number of applicants
        seed: Random seed for reproducibility

    Returns:
        DataFrame with columns: group, approved, defaulted, loan_size, processing_time
    """
    np.random.seed(seed)
    n_half = n // 2

    # Group A (control): current model
    # approval_rate ~0.62, default_rate ~0.11
    approved_A = np.random.binomial(1, 0.62, n_half)
    defaulted_A = np.random.binomial(approved_A, 0.11)
    loan_size_A = np.random.lognormal(mean=9.5, sigma=0.8, size=n_half) * approved_A
    processing_time_A = np.random.gamma(shape=3, scale=5, size=n_half) + 2

    # Group B (treatment): new model
    # approval_rate ~0.71, default_rate ~0.09
    approved_B = np.random.binomial(1, 0.71, n_half)
    defaulted_B = np.random.binomial(approved_B, 0.09)
    loan_size_B = np.random.lognormal(mean=9.7, sigma=0.75, size=n_half) * approved_B
    processing_time_B = np.random.gamma(shape=3.2, scale=4.5, size=n_half) + 1.8

    df_A = pd.DataFrame({
        'group': 'A',
        'approved': approved_A,
        'defaulted': defaulted_A,
        'loan_size': loan_size_A,
        'processing_time': processing_time_A
    })

    df_B = pd.DataFrame({
        'group': 'B',
        'approved': approved_B,
        'defaulted': defaulted_B,
        'loan_size': loan_size_B,
        'processing_time': processing_time_B
    })

    df = pd.concat([df_A, df_B], ignore_index=True)
    return df

def compute_group_stats(df):
    """Compute summary statistics for each group."""
    stats = {}
    for group in ['A', 'B']:
        g = df[df['group'] == group]
        approved_count = g['approved'].sum()
        total = len(g)
        defaulted_count = g['defaulted'].sum()
        approved_with_loan = g['approved'].sum()

        stats[group] = {
            'n': total,
            'approval_rate': approved_count / total,
            'default_rate': defaulted_count / approved_with_loan if approved_with_loan > 0 else 0,
            'avg_loan_size': g[g['approved'] == 1]['loan_size'].mean() if approved_with_loan > 0 else 0,
            'avg_processing_time': g['processing_time'].mean()
        }
    return stats

if __name__ == '__main__':
    df = generate_credit_data()
    stats = compute_group_stats(df)
    for group, s in stats.items():
        print(f"Group {group}: approval_rate={s['approval_rate']:.4f}, "
              f"default_rate={s['default_rate']:.4f}, "
              f"avg_loan_size={s['avg_loan_size']:.2f}, "
              f"avg_processing_time={s['avg_processing_time']:.2f}")
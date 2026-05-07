"""Generate synthetic credit eligibility data for A/B testing."""
import numpy as np
import pandas as pd

np.random.seed(42)

N = 5000

# Group A (control): current eligibility model
# Group B (treatment): new eligibility model

def generate_data():
    """Generate synthetic data for both groups."""
    # Group A: control
    # Approval ~62%, default among approved ~11%
    group_a_approved = np.random.random(N) < 0.62
    group_a_defaulted = np.random.random(N) < 0.11
    # Default only possible if approved
    group_a_defaulted = group_a_defaulted & group_a_approved

    # Group B: treatment (new model)
    # Approval ~71%, default among approved ~9%
    group_b_approved = np.random.random(N) < 0.71
    group_b_defaulted = np.random.random(N) < 0.09
    group_b_defaulted = group_b_defaulted & group_b_approved

    # Generate loan sizes (in Rands, ZAR) - realistic range
    base_loan_sizes = np.random.lognormal(mean=10.5, sigma=0.8, size=N)
    group_a_loan_size = base_loan_sizes * np.where(group_a_approved, 1, 0)
    group_b_loan_size = base_loan_sizes * np.where(group_b_approved, 1, 0)

    # Processing time in hours (realistic range)
    group_a_processing_time = np.random.exponential(scale=2.5, size=N)
    group_b_processing_time = np.random.exponential(scale=2.2, size=N)

    df = pd.DataFrame({
        'applicant_id': range(1, 2 * N + 1),
        'group': ['A'] * N + ['B'] * N,
        'approved': np.concatenate([group_a_approved, group_b_approved]),
        'defaulted': np.concatenate([group_a_defaulted, group_b_defaulted]),
        'loan_size': np.concatenate([group_a_loan_size, group_b_loan_size]),
        'processing_time': np.concatenate([group_a_processing_time, group_b_processing_time]),
    })

    return df

def compute_group_stats(df):
    """Compute summary statistics per group."""
    stats = {}
    for group in ['A', 'B']:
        group_df = df[df['group'] == group]
        n = len(group_df)
        n_approved = group_df['approved'].sum()
        n_defaulted = group_df['defaulted'].sum()
        approved_mask = group_df['approved']
        
        stats[group] = {
            'n': n,
            'approval_rate': n_approved / n,
            'default_rate': n_defaulted / n_approved if n_approved > 0 else 0,
            'avg_loan_size': group_df.loc[approved_mask, 'loan_size'].mean() if n_approved > 0 else 0,
            'avg_processing_time': group_df['processing_time'].mean(),
        }
    return stats

if __name__ == '__main__':
    df = generate_data()
    print(df.head(10))
    print("\nGroup Stats:")
    print(compute_group_stats(df))
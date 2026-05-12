import numpy as np
import pandas as pd

def generate_loan_data(n=5000, seed=42):
    """
    Generate synthetic loan applicant data for A/B testing.
    
    Args:
        n: Total number of applicants
        seed: Random seed for reproducibility
    
    Returns:
        DataFrame with columns: applicant_id, group, approved, defaulted,
                                loan_size, processing_time_minutes
    """
    np.random.seed(seed)
    
    # Split into control (A) and treatment (B) groups
    n_a = n // 2
    n_b = n - n_a
    
    # Group A (control): approval ~0.62, default ~0.11
    # Group B (treatment): approval ~0.71, default ~0.09
    approval_rate_a = 0.62
    default_rate_a = 0.11
    approval_rate_b = 0.71
    default_rate_b = 0.09
    
    # Generate base features for Group A
    income_a = np.random.normal(55000, 18000, n_a)
    credit_score_a = np.random.normal(680, 80, n_a)
    
    # Generate base features for Group B
    income_b = np.random.normal(55000, 18000, n_b)
    credit_score_b = np.random.normal(680, 80, n_b)
    
    # Approval decision with noise
    approval_prob_a = approval_rate_a + np.random.normal(0, 0.05, n_a)
    approval_prob_a = np.clip(approval_prob_a, 0, 1)
    approved_a = (np.random.random(n_a) < approval_prob_a).astype(int)
    
    approval_prob_b = approval_rate_b + np.random.normal(0, 0.05, n_b)
    approval_prob_b = np.clip(approval_prob_b, 0, 1)
    approved_b = (np.random.random(n_b) < approval_prob_b).astype(int)
    
    # Default decision (only among approved)
    default_prob_a = default_rate_a + np.random.normal(0, 0.02, n_a)
    default_prob_a = np.clip(default_prob_a, 0, 1)
    defaulted_a = (approved_a == 1) & (np.random.random(n_a) < default_prob_a)
    defaulted_a = defaulted_a.astype(int)
    
    default_prob_b = default_rate_b + np.random.normal(0, 0.02, n_b)
    default_prob_b = np.clip(default_prob_b, 0, 1)
    defaulted_b = (approved_b == 1) & (np.random.random(n_b) < default_prob_b)
    defaulted_b = defaulted_b.astype(int)
    
    # Loan sizes (among approved)
    loan_size_a = np.where(approved_a == 1,
                           np.random.lognormal(10.5, 0.5, n_a),
                           0)
    loan_size_b = np.where(approved_b == 1,
                           np.random.lognormal(10.5, 0.5, n_b),
                           0)
    
    # Processing time (in minutes)
    processing_time_a = np.where(approved_a == 1,
                                  np.random.gamma(4, 15, n_a) + 20,
                                  np.random.gamma(3, 10, n_a) + 10)
    processing_time_b = np.where(approved_b == 1,
                                  np.random.gamma(4, 12, n_b) + 18,
                                  np.random.gamma(3, 10, n_b) + 10)
    
    # Combine into DataFrame
    df_a = pd.DataFrame({
        'applicant_id': range(1, n_a + 1),
        'group': 'A',
        'approved': approved_a,
        'defaulted': defaulted_a,
        'loan_size': loan_size_a,
        'processing_time_minutes': processing_time_a
    })
    
    df_b = pd.DataFrame({
        'applicant_id': range(n_a + 1, n + 1),
        'group': 'B',
        'approved': approved_b,
        'defaulted': defaulted_b,
        'loan_size': loan_size_b,
        'processing_time_minutes': processing_time_b
    })
    
    df = pd.concat([df_a, df_b], ignore_index=True)
    return df

def compute_group_stats(df):
    """Compute summary statistics for each group."""
    stats = {}
    for group in ['A', 'B']:
        grp = df[df['group'] == group]
        n = len(grp)
        n_approved = grp['approved'].sum()
        n_defaulted = grp['defaulted'].sum()
        approved_loans = grp[grp['approved'] == 1]
        
        stats[group] = {
            'n': n,
            'approval_rate': n_approved / n,
            'default_rate': n_defaulted / n_approved if n_approved > 0 else 0,
            'avg_loan_size': approved_loans['loan_size'].mean() if len(approved_loans) > 0 else 0,
            'avg_processing_time': grp['processing_time_minutes'].mean()
        }
    return stats

if __name__ == '__main__':
    df = generate_loan_data()
    print(df.head(10))
    stats = compute_group_stats(df)
    for g, s in stats.items():
        print(f"\nGroup {g}:")
        for k, v in s.items():
            print(f"  {k}: {v:.4f}")
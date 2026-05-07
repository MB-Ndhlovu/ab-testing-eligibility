"""
Generates synthetic loan applicant data for A/B testing.
"""

import numpy as np

def generate_data(n=5000, seed=42):
    """
    Generate synthetic loan applicant data.

    Args:
        n: Total number of applicants (default 5000, split evenly between groups)
        seed: Random seed for reproducibility

    Returns:
        dict with keys: group, approved, defaulted, loan_size, processing_time
    """
    np.random.seed(seed)

    half = n // 2
    groups = np.array(['A'] * half + ['B'] * half)
    indices = np.random.permutation(n)
    groups = groups[indices]

    # Group A (control): current model
    # Group B (treatment): new model
    approval_probs = np.where(groups == 'A', 0.62, 0.71)
    default_probs = np.where(groups == 'A', 0.11, 0.09)

    approved = (np.random.random(n) < approval_probs).astype(int)
    defaulted = ((np.random.random(n) < default_probs) & (approved == 1)).astype(int)

    # Loan sizes: log-normal distribution (realistic for loans)
    base_loan = np.random.lognormal(mean=10.5, sigma=0.6, size=n)  # ~R36k median
    loan_size = np.round(base_loan, 2)

    # Processing time: normal distribution in days
    base_time = np.random.normal(loc=3.5, scale=1.2, size=n)
    base_time = np.clip(base_time, 0.5, 10)
    processing_time = np.round(base_time, 1)

    return {
        'group': groups,
        'approved': approved,
        'defaulted': defaulted,
        'loan_size': loan_size,
        'processing_time': processing_time
    }


def compute_group_stats(data):
    """
    Compute summary statistics for each group.

    Returns:
        dict with approval_rate, default_rate, avg_loan_size, avg_processing_time per group
    """
    group_a = data['group'] == 'A'
    group_b = data['group'] == 'B'

    a_approved = data['approved'][group_a]
    b_approved = data['approved'][group_b]
    a_defaulted = data['defaulted'][group_a]
    b_defaulted = data['defaulted'][group_b]

    return {
        'A': {
            'n': int(group_a.sum()),
            'approval_rate': float(a_approved.mean()),
            'default_rate': float(a_defaulted.sum() / a_approved.sum()) if a_approved.sum() > 0 else 0.0,
            'avg_loan_size': float(data['loan_size'][group_a].mean()),
            'avg_processing_time': float(data['processing_time'][group_a].mean()),
        },
        'B': {
            'n': int(group_b.sum()),
            'approval_rate': float(b_approved.mean()),
            'default_rate': float(b_defaulted.sum() / b_approved.sum()) if b_approved.sum() > 0 else 0.0,
            'avg_loan_size': float(data['loan_size'][group_b].mean()),
            'avg_processing_time': float(data['processing_time'][group_b].mean()),
        }
    }


if __name__ == '__main__':
    data = generate_data()
    stats = compute_group_stats(data)
    print("=== Group Statistics ===")
    for g, s in stats.items():
        print(f"\nGroup {g} (n={s['n']}):")
        print(f"  Approval Rate:    {s['approval_rate']:.4f}")
        print(f"  Default Rate:      {s['default_rate']:.4f}")
        print(f"  Avg Loan Size:     R{s['avg_loan_size']:.2f}")
        print(f"  Avg Process Time:  {s['avg_processing_time']:.1f} days")
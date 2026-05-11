"""Generate synthetic loan applicant data for A/B testing."""

import numpy as np

def generate_data(n=5000, seed=42):
    """
    Generate synthetic loan data for control (A) and treatment (B) groups.

    Parameters
    ----------
    n : int
        Number of applicants per group (default 5000)
    seed : int
        Random seed for reproducibility

    Returns
    -------
    dict
        Dictionary with 'group_a' and 'group_b' DataFrames containing:
        - approved: bool
        - defaulted: bool
        - loan_size: float (in thousands ZAR)
        - processing_time: float (in days)
    """
    np.random.seed(seed)

    # Group A (Control): approval_rate ~0.62, default_rate ~0.11
    approved_a = np.random.random(n) < 0.62
    # Among approved, default rate ~0.11
    defaulted_a = approved_a & (np.random.random(n) < 0.11)
    loan_size_a = np.random.lognormal(mean=4.2, sigma=0.7, size=n) * 1000  # avg ~50k ZAR
    processing_time_a = np.random.exponential(scale=3.5, size=n) + 1  # avg ~4.5 days

    # Group B (Treatment): approval_rate ~0.71, default_rate ~0.09
    approved_b = np.random.random(n) < 0.71
    defaulted_b = approved_b & (np.random.random(n) < 0.09)
    loan_size_b = np.random.lognormal(mean=4.35, sigma=0.68, size=n) * 1000  # avg ~55k ZAR
    processing_time_b = np.random.exponential(scale=3.0, size=n) + 1  # avg ~4 days

    return {
        'group_a': {
            'approved': approved_a,
            'defaulted': defaulted_a,
            'loan_size': loan_size_a,
            'processing_time': processing_time_a,
        },
        'group_b': {
            'approved': approved_b,
            'defaulted': defaulted_b,
            'loan_size': loan_size_b,
            'processing_time': processing_time_b,
        }
    }

def compute_metrics(data):
    """Compute summary metrics for each group."""
    metrics = {}
    for group_name, group_data in data.items():
        approved = group_data['approved']
        defaulted = group_data['defaulted']
        n = len(approved)

        metrics[group_name] = {
            'n': n,
            'approval_rate': approved.mean(),
            'default_rate': defaulted.sum() / approved.sum() if approved.sum() > 0 else 0,
            'avg_loan_size': group_data['loan_size'][approved].mean(),
            'processing_time': group_data['processing_time'][approved].mean(),
        }
    return metrics

"""
Generate synthetic credit eligibility data for A/B testing.
"""

import numpy as np

def generate_data(n=5000, seed=42):
    """
    Generate synthetic loan application data for control (A) and treatment (B).

    Parameters
    ----------
    n : int
        Total number of rows (split evenly between A and B).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    dict
        Dictionary with keys: group_a (dict), group_b (dict).
        Each group dict contains: approved (bool array), defaulted (bool array),
        loan_size (float array), processing_time (float array).
    """
    np.random.seed(seed)

    n_a = n // 2
    n_b = n - n_a  # handles odd n

    # --- Group A: Control ---
    approved_a = np.random.random(n_a) < 0.62
    defaulted_a = np.random.random(n_a) < 0.11

    loan_size_a = np.random.exponential(scale=15_000, size=n_a) + 2_000
    loan_size_a = np.clip(loan_size_a, 1_000, 100_000)
    loan_size_a[~approved_a] = 0

    processing_time_a = np.random.exponential(scale=3.5, size=n_a) + 0.5
    processing_time_a[~approved_a] = 0

    # --- Group B: Treatment ---
    approved_b = np.random.random(n_b) < 0.71
    defaulted_b = np.random.random(n_b) < 0.09

    loan_size_b = np.random.exponential(scale=15_000, size=n_b) + 2_000
    loan_size_b = np.clip(loan_size_b, 1_000, 100_000)
    loan_size_b[~approved_b] = 0

    processing_time_b = np.random.exponential(scale=2.8, size=n_b) + 0.5
    processing_time_b[~approved_b] = 0

    return {
        "group_a": {
            "approved": approved_a,
            "defaulted": defaulted_a,
            "loan_size": loan_size_a,
            "processing_time": processing_time_a,
        },
        "group_b": {
            "approved": approved_b,
            "defaulted": defaulted_b,
            "loan_size": loan_size_b,
            "processing_time": processing_time_b,
        },
    }


def summarize(data):
    """Compute summary statistics for both groups."""
    results = {}
    for group, label in [("group_a", "Group A (Control)"), ("group_b", "Group B (Treatment)")]:
        approved = data[group]["approved"]
        defaulted = data[group]["defaulted"]
        loan_size = data[group]["loan_size"]
        processing_time = data[group]["processing_time"]

        approved_loans = approved.sum()
        total = len(approved)
        results[label] = {
            "n": total,
            "approval_rate": approved_loans / total,
            "default_rate":  np.sum(defaulted) / approved_loans if approved_loans > 0 else 0,
            "avg_loan_size": np.mean(loan_size[approved]),
            "avg_processing_time": np.mean(processing_time[approved]),
        }
    return results
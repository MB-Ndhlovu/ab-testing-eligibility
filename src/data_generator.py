"""Generate synthetic credit eligibility data."""

import numpy as np

np.random.seed(42)

N = 2500  # applicants per group


def generate_data() -> dict:
    """Generate synthetic data for both groups."""
    group_a_approved = np.random.random(N) < 0.62
    group_a_defaulted = np.random.random(N) < 0.11

    group_b_approved = np.random.random(N) < 0.71
    group_b_defaulted = np.random.random(N) < 0.09

    def metrics(approved, defaulted):
        return {
            "approval_rate": approved.mean(),
            "default_rate": defaulted.mean(),
            "avg_loan_size": max(1000, np.random.normal(25000, 8000)),
            "processing_time": max(0.5, np.random.normal(3.5, 1.2)),
        }

    return {
        "group_a": {
            "n": N,
            "approved": group_a_approved,
            "defaulted": group_a_defaulted,
            "metrics": metrics(group_a_approved, group_a_defaulted),
        },
        "group_b": {
            "n": N,
            "approved": group_b_approved,
            "defaulted": group_b_defaulted,
            "metrics": metrics(group_b_approved, group_b_defaulted),
        },
    }
"""Generate synthetic credit eligibility data for A/B testing."""

import numpy as np
from typing import Tuple

np.random.seed(42)


def generate_credit_data(n_samples: int = 5000) -> Tuple[dict, dict]:
    """
    Generate synthetic credit eligibility data for control and treatment groups.

    Args:
        n_samples: Total number of samples (split evenly between groups).

    Returns:
        Tuple of (group_a_data, group_b_data) dictionaries containing:
            - approvals: array of 0/1 (approved/not approved)
            - defaults: array of 0/1 (defaulted/not defaulted)
            - loan_sizes: array of loan amounts
            - processing_times: array of processing times in hours
    """
    half = n_samples // 2

    # Group A (Control): current model
    # Approval rate ~62%, default rate ~11%
    approval_probs_a = np.random.beta(62, 38, half)  # realistic binomial approximation
    defaults_probs_a = np.random.beta(11, 89, half)

    group_a = {
        "approvals": (np.random.random(half) < approval_probs_a).astype(int),
        "defaults": (np.random.random(half) < defaults_probs_a).astype(int),
        "loan_sizes": np.random.lognormal(mean=10.5, sigma=0.6, size=half),  # skewed loan amounts
        "processing_times": np.random.gamma(shape=2, scale=2, size=half) + np.random.uniform(1, 5, half),
    }

    # Group B (Treatment): new model
    # Approval rate ~71%, default rate ~9%
    approval_probs_b = np.random.beta(71, 29, half)
    defaults_probs_b = np.random.beta(9, 91, half)

    group_b = {
        "approvals": (np.random.random(half) < approval_probs_b).astype(int),
        "defaults": (np.random.random(half) < defaults_probs_b).astype(int),
        "loan_sizes": np.random.lognormal(mean=10.7, sigma=0.55, size=half),  # slightly higher avg loan
        "processing_times": np.random.gamma(shape=2.2, scale=1.8, size=half) + np.random.uniform(0.8, 4.5, half),
    }

    return group_a, group_b


def compute_group_stats(group_data: dict) -> dict:
    """Compute summary statistics for a group."""
    n = len(group_data["approvals"])
    return {
        "n": n,
        "approval_rate": group_data["approvals"].mean(),
        "default_rate": group_data["defaults"].mean(),
        "avg_loan_size": group_data["loan_sizes"].mean(),
        "avg_processing_time": group_data["processing_times"].mean(),
    }


if __name__ == "__main__":
    group_a, group_b = generate_credit_data(5000)
    stats_a = compute_group_stats(group_a)
    stats_b = compute_group_stats(group_b)

    print("Group A (Control):")
    for k, v in stats_a.items():
        print(f"  {k}: {v:.4f}")

    print("\nGroup B (Treatment):")
    for k, v in stats_b.items():
        print(f"  {k}: {v:.4f}")
"""Generate synthetic credit eligibility data for A/B testing."""

import numpy as np
from typing import Tuple


def generate_credit_data(n: int = 5000, group: str = "A", seed: int = 42) -> dict:
    """
    Generate synthetic credit eligibility data.

    Args:
        n: Number of applicants
        group: 'A' (control) or 'B' (treatment)
        seed: Random seed for reproducibility

    Returns:
        Dictionary with keys: approved, defaulted, avg_loan_size, processing_time
    """
    np.random.seed(seed + (0 if group == "A" else 1))

    if group == "A":
        approval_prob = 0.62
        default_given_approved_prob = 0.11
        base_loan_size = 15000
        base_processing_time = 4.5
    else:
        approval_prob = 0.71
        default_given_approved_prob = 0.09
        base_loan_size = 15500
        base_processing_time = 3.8

    approved_mask = np.random.random(n) < approval_prob

    num_approved = approved_mask.sum()

    defaulted = np.zeros(n, dtype=bool)
    if num_approved > 0:
        default_draw = np.random.random(num_approved)
        defaulted[approved_mask] = default_draw < default_given_approved_prob

    loan_sizes = np.where(
        approved_mask,
        np.random.lognormal(np.log(base_loan_size), 0.3, n),
        0
    )

    processing_times = np.where(
        approved_mask,
        np.random.lognormal(np.log(base_processing_time), 0.25, n),
        0
    )

    return {
        "n": n,
        "approved": int(num_approved),
        "defaulted": int(defaulted.sum()),
        "avg_loan_size": float(loan_sizes[approved_mask].mean()) if num_approved > 0 else 0.0,
        "processing_time": float(processing_times[approved_mask].mean()) if num_approved > 0 else 0.0,
        "approval_rate": num_approved / n,
        "default_rate": defaulted.sum() / num_approved if num_approved > 0 else 0.0,
    }


def compute_group_metrics(data: dict) -> dict:
    """Compute summary metrics from generated data."""
    return {
        "n": data["n"],
        "approvals": data["approved"],
        "approval_rate": data["approval_rate"],
        "defaults": data["defaulted"],
        "default_rate": data["default_rate"],
        "avg_loan_size": data["avg_loan_size"],
        "avg_processing_time": data["processing_time"],
    }
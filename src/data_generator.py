"""
Data generator for A/B credit eligibility experiment.
Generates 5,000 synthetic loan applicant records per group.
"""

import numpy as np
from typing import Tuple

np.random.seed(42)

N = 5000


def generate_data() -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic credit applicant data for control (A) and treatment (B).

    Returns
    -------
    group_A : ndarray, shape (5000,)
        Structured array with fields: approved, defaulted, loan_size, processing_time
    group_B : ndarray, shape (5000,)
        Same fields for treatment group.
    """
    # Group A (control) — current model
    approved_A = np.random.rand(N) < 0.62
    defaulted_A = approved_A & (np.random.rand(N) < 0.11)
    loan_size_A = np.clip(
        np.random.normal(50_000, 20_000, N),
        5_000, 500_000
    )
    processing_time_A = np.clip(
        np.random.normal(4.2, 1.5, N),
        0.5, 15.0
    )

    # Group B (treatment) — new model
    approved_B = np.random.rand(N) < 0.71
    defaulted_B = approved_B & (np.random.rand(N) < 0.09)
    loan_size_B = np.clip(
        np.random.normal(52_000, 22_000, N),
        5_000, 500_000
    )
    processing_time_B = np.clip(
        np.random.normal(3.8, 1.2, N),
        0.5, 15.0
    )

    dtype = [
        ("approved", bool),
        ("defaulted", bool),
        ("loan_size", float),
        ("processing_time", float),
    ]

    group_A = np.zeros(N, dtype=dtype)
    group_A["approved"] = approved_A
    group_A["defaulted"] = defaulted_A
    group_A["loan_size"] = loan_size_A
    group_A["processing_time"] = processing_time_A

    group_B = np.zeros(N, dtype=dtype)
    group_B["approved"] = approved_B
    group_B["defaulted"] = defaulted_B
    group_B["loan_size"] = loan_size_B
    group_B["processing_time"] = processing_time_B

    return group_A, group_B


def compute_group_metrics(group: np.ndarray) -> dict:
    """Compute summary metrics for a group."""
    n = len(group)
    approved = group["approved"]
    defaulted = group["defaulted"]

    return {
        "n": n,
        "approval_rate": approved.sum() / n,
        "default_rate": defaulted.sum() / approved.sum() if approved.sum() > 0 else 0.0,
        "avg_loan_size": group["loan_size"].mean(),
        "avg_processing_time": group["processing_time"].mean(),
    }
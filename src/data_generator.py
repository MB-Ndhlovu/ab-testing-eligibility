"""
Data generator for A/B test simulation.
Generates synthetic credit application data for control and treatment groups.
"""

import numpy as np
from typing import Tuple

np.random.seed(42)


def generate_data(n: int = 5000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate synthetic credit application outcomes for two groups.

    Group A (control): current eligibility model
    Group B (treatment): new eligibility model

    Args:
        n: Number of applicants per group

    Returns:
        Tuple of (group_A_outcomes, group_B_outcomes) where each is a dict with:
            - approved: array of 0/1
            - defaulted: array of 0/1
            - loan_size: array of loan amounts
            - processing_time: array of processing times in hours
    """
    # Group A (control): approval ~62%, default ~11%
    approved_A = np.random.binomial(1, 0.62, n)
    defaulted_given_approved_A = np.random.binomial(1, 0.11, n)
    defaulted_A = approved_A * defaulted_given_approved_A

    # Loan size: log-normal distribution centered around R50,000
    loan_size_A = np.exp(np.random.normal(loc=10.8, scale=0.9, size=n))
    loan_size_A = np.clip(loan_size_A, 1000, 500000)

    # Processing time: right-skewed, ~24-72 hours typical
    processing_time_A = np.random.gamma(shape=2.5, scale=12, size=n) + 8

    # Group B (treatment): approval ~71%, default ~9%
    approved_B = np.random.binomial(1, 0.71, n)
    defaulted_given_approved_B = np.random.binomial(1, 0.09, n)
    defaulted_B = approved_B * defaulted_given_approved_B

    loan_size_B = np.exp(np.random.normal(loc=10.9, scale=0.9, size=n))
    loan_size_B = np.clip(loan_size_B, 1000, 500000)

    processing_time_B = np.random.gamma(shape=2.5, scale=11, size=n) + 7

    outcomes_A = {
        "approved": approved_A,
        "defaulted": defaulted_A,
        "loan_size": loan_size_A,
        "processing_time": processing_time_A,
    }
    outcomes_B = {
        "approved": approved_B,
        "defaulted": defaulted_B,
        "loan_size": loan_size_B,
        "processing_time": processing_time_B,
    }

    return outcomes_A, outcomes_B


def compute_group_stats(outcomes: dict) -> dict:
    """
    Compute aggregate statistics for a group.
    """
    approved = outcomes["approved"]
    defaulted = outcomes["defaulted"]
    loan_size = outcomes["loan_size"]
    processing_time = outcomes["processing_time"]

    n = len(approved)
    n_approved = approved.sum()

    return {
        "n": n,
        "n_approved": n_approved,
        "approval_rate": approved.mean(),
        "default_rate": defaulted.sum() / n_approved if n_approved > 0 else 0,
        "avg_loan_size": loan_size[approved == 1].mean() if n_approved > 0 else 0,
        "avg_processing_time": processing_time.mean(),
    }
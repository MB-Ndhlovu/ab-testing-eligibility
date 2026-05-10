"""Generate synthetic credit eligibility data for A/B testing."""

import numpy as np

np.random.seed(42)

N = 5000
N_A = N // 2
N_B = N // 2

APPROVAL_RATE_A = 0.62
APPROVAL_RATE_B = 0.71

DEFAULT_RATE_A = 0.11
DEFAULT_RATE_B = 0.09


def generate_data():
    """Generate synthetic loan applicant data for both groups."""
    # Group A (control) outcomes
    approved_A = np.random.random(N_A) < APPROVAL_RATE_A
    defaulted_A = np.random.random(N_A) < DEFAULT_RATE_A

    # Group B (treatment) outcomes
    approved_B = np.random.random(N_B) < APPROVAL_RATE_B
    defaulted_B = np.random.random(N_B) < DEFAULT_RATE_B

    # Loan amounts (in thousands, lognormal for realism)
    loan_size_A = np.random.lognormal(mean=4.2, sigma=0.9, size=N_A)
    loan_size_B = np.random.lognormal(mean=4.3, sigma=0.9, size=N_B)

    # Processing time in hours (gamma distribution)
    processing_time_A = np.random.gamma(shape=2.0, scale=2.5, size=N_A)
    processing_time_B = np.random.gamma(shape=2.2, scale=2.2, size=N_B)

    return {
        "group_A": {
            "approved": approved_A,
            "defaulted": defaulted_A,
            "loan_size": loan_size_A,
            "processing_time": processing_time_A,
            "n": N_A,
            "approval_rate": approved_A.mean(),
            "default_rate": defaulted_A.mean(),
            "avg_loan_size": loan_size_A.mean(),
            "avg_processing_time": processing_time_A.mean(),
        },
        "group_B": {
            "approved": approved_B,
            "defaulted": defaulted_B,
            "loan_size": loan_size_B,
            "processing_time": processing_time_B,
            "n": N_B,
            "approval_rate": approved_B.mean(),
            "default_rate": defaulted_B.mean(),
            "avg_loan_size": loan_size_B.mean(),
            "avg_processing_time": processing_time_B.mean(),
        },
    }
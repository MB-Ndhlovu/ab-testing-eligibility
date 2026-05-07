"""Generate synthetic loan application data for A/B testing."""
import numpy as np

rng = np.random.default_rng(42)

N = 2500  # applicants per group


def generate_data():
    """Generate 5000 rows: group A (control) and group B (treatment).

    Each row represents one loan application with:
        - group: 'A' or 'B'
        - approved: 1 if approved, 0 if denied
        - defaulted: 1 if defaulted, 0 if not (only meaningful if approved)
        - loan_size: loan amount in ZAR
        - processing_time_hours: hours to process application
    """
    # Group A: control — current eligibility model
    group_A_approved = rng.binomial(1, 0.62, N)
    group_A_defaulted = rng.binomial(1, 0.11, N) * group_A_approved
    group_A_loan_size = rng.lognormal(10.8, 0.55, N)  # median ~49k ZAR
    group_A_proc_time = rng.lognormal(2.8, 0.6, N)     # median ~16 hrs

    # Group B: treatment — new eligibility model
    group_B_approved = rng.binomial(1, 0.71, N)
    group_B_defaulted = rng.binomial(1, 0.09, N) * group_B_approved
    group_B_loan_size = rng.lognormal(10.9, 0.50, N)    # slightly larger loans
    group_B_proc_time = rng.lognormal(2.5, 0.55, N)     # slightly faster

    rows_A = np.column_stack([
        np.full(N, 'A'),
        group_A_approved,
        group_A_defaulted,
        group_A_loan_size,
        group_A_proc_time,
    ])
    rows_B = np.column_stack([
        np.full(N, 'B'),
        group_B_approved,
        group_B_defaulted,
        group_B_loan_size,
        group_B_proc_time,
    ])

    data = np.vstack([rows_A, rows_B])

    import pandas as pd
    df = pd.DataFrame(
        data,
        columns=[
            'group',
            'approved',
            'defaulted',
            'loan_size',
            'processing_time_hours',
        ],
    )
    df['approved'] = df['approved'].astype(int)
    df['defaulted'] = df['defaulted'].astype(int)
    df['loan_size'] = df['loan_size'].astype(float)
    df['processing_time_hours'] = df['processing_time_hours'].astype(float)

    return df
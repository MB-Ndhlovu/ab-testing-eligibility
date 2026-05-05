import numpy as np
import pandas as pd
from typing import Tuple

np.random.seed(42)


def generate_credit_data(n: int = 5000, group_ratio: float = 0.5) -> pd.DataFrame:
    """
    Generate synthetic credit application data for A/B testing.

    Args:
        n: Total number of applicants
        group_ratio: Proportion of applicants in Group A (control)

    Returns:
        DataFrame with columns: applicant_id, group, approved, defaulted,
                                 loan_size, processing_time_hours
    """
    n_a = int(n * group_ratio)
    n_b = n - n_a

    # Group A (control): current eligibility model
    # approval_rate ~0.62, default_rate ~0.11
    approval_rate_a = 0.62
    default_rate_a = 0.11

    # Group B (treatment): new eligibility model
    # approval_rate ~0.71, default_rate ~0.09
    approval_rate_b = 0.71
    default_rate_b = 0.09

    # Generate applicant IDs
    ids_a = [f"APP-A-{i:05d}" for i in range(n_a)]
    ids_b = [f"APP-B-{i:05d}" for i in range(n_b)]

    # Generate approval decisions with noise
    approved_a = np.random.random(n_a) < approval_rate_a
    approved_b = np.random.random(n_b) < approval_rate_b

    # Generate default outcomes (only for approved loans)
    defaulted_a = approved_a & (np.random.random(n_a) < default_rate_a + np.random.normal(0, 0.02, n_a))
    defaulted_b = approved_b & (np.random.random(n_b) < default_rate_b + np.random.normal(0, 0.02, n_b))

    # Clip default rates to valid range
    defaulted_a = defaulted_a & (np.random.random(n_a) < 0.95)
    defaulted_b = defaulted_b & (np.random.random(n_b) < 0.95)

    # Generate loan sizes (approved applications only)
    base_loan_a = np.random.lognormal(mean=9.5, sigma=0.8, size=n_a)
    base_loan_b = np.random.lognormal(mean=9.7, sigma=0.9, size=n_b)

    # Mask loan sizes for non-approved applications
    loan_size_a = np.where(approved_a, base_loan_a, 0)
    loan_size_b = np.where(approved_b, base_loan_b, 0)

    # Generate processing time (hours) - slightly faster for new model
    processing_time_a = np.random.exponential(scale=2.5, size=n_a) + np.random.normal(1.0, 0.3, n_a)
    processing_time_b = np.random.exponential(scale=2.2, size=n_b) + np.random.normal(0.9, 0.3, n_b)

    # Create DataFrames
    df_a = pd.DataFrame({
        "applicant_id": ids_a,
        "group": "A",
        "approved": approved_a,
        "defaulted": defaulted_a,
        "loan_size": loan_size_a,
        "processing_time_hours": processing_time_a
    })

    df_b = pd.DataFrame({
        "applicant_id": ids_b,
        "group": "B",
        "approved": approved_b,
        "defaulted": defaulted_b,
        "loan_size": loan_size_b,
        "processing_time_hours": processing_time_b
    })

    df = pd.concat([df_a, df_b], ignore_index=True)
    np.random.shuffle(df.values)

    return df


def compute_group_metrics(df: pd.DataFrame, group: str) -> dict:
    """Compute key metrics for a group."""
    g = df[df["group"] == group]
    approved = g["approved"]
    defaulted = g["defaulted"]
    approved_count = approved.sum()
    total_count = len(g)

    return {
        "approval_rate": approved.mean() if total_count > 0 else 0,
        "approval_count": int(approved_count),
        "total_applicants": total_count,
        "default_rate": defaulted.mean() if approved_count > 0 else 0,
        "default_count": int(defaulted.sum()),
        "avg_loan_size": g.loc[approved, "loan_size"].mean() if approved_count > 0 else 0,
        "avg_processing_time": g.loc[approved, "processing_time_hours"].mean() if approved_count > 0 else 0
    }
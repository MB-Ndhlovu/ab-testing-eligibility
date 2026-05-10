"""Generate synthetic loan application data for A/B testing."""

import numpy as np
import pandas as pd


def generate_data(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic loan application data.

    Args:
        n: Total number of records.
        seed: Random seed for reproducibility.

    Returns:
        DataFrame with columns: application_id, group, approved, defaulted, loan_size, processing_days
    """
    np.random.seed(seed)
    half = n // 2

    # Group A: control — approval ~62%, default ~11%
    group_a_approved = np.random.rand(half) < 0.62
    group_a_defaulted = np.zeros(half, dtype=bool)
    group_a_defaulted[group_a_approved] = np.random.rand(group_a_approved.sum()) < 0.11

    # Group B: treatment — approval ~71%, default ~9%
    group_b_approved = np.random.rand(half) < 0.71
    group_b_defaulted = np.zeros(half, dtype=bool)
    group_b_defaulted[group_b_approved] = np.random.rand(group_b_approved.sum()) < 0.09

    # Loan sizes with realistic variance
    loan_sizes_a = np.random.lognormal(mean=9.5, sigma=0.45, size=half).clip(1000, 150000)
    loan_sizes_b = np.random.lognormal(mean=9.7, sigma=0.45, size=half).clip(1000, 150000)

    # Processing days (approved applications only)
    proc_a = np.random.normal(5.0, 1.2, size=half)
    proc_a[~group_a_approved] = np.random.normal(8.0, 2.0, size=(~group_a_approved).sum())
    proc_b = np.random.normal(3.5, 1.0, size=half)
    proc_b[~group_b_approved] = np.random.normal(7.5, 1.8, size=(~group_b_approved).sum())

    df_a = pd.DataFrame({
        "application_id": [f"A-{i:05d}" for i in range(half)],
        "group": "A",
        "approved": group_a_approved,
        "defaulted": group_a_defaulted,
        "loan_size": loan_sizes_a.round(2),
        "processing_days": proc_a.round(1),
    })

    df_b = pd.DataFrame({
        "application_id": [f"B-{i:05d}" for i in range(half)],
        "group": "B",
        "approved": group_b_approved,
        "defaulted": group_b_defaulted,
        "loan_size": loan_sizes_b.round(2),
        "processing_days": proc_b.round(1),
    })

    return pd.concat([df_a, df_b], ignore_index=True)


def compute_group_metrics(df: pd.DataFrame) -> dict:
    """Compute summary metrics per group."""
    results = {}
    for group, grp in df.groupby("group"):
        approved = grp["approved"]
        defaulted = grp["defaulted"]
        results[group] = {
            "n": len(grp),
            "approval_rate": approved.mean(),
            "default_rate": defaulted.mean(),
            "avg_loan_size": grp["loan_size"].mean(),
            "avg_processing_days": grp["processing_days"].mean(),
        }
    return results
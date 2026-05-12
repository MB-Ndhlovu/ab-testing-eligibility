"""Generate synthetic credit eligibility data for A/B testing."""

import numpy as np
import pandas as pd


def generate_credit_data(n_per_group: int = 2500, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic credit eligibility data.

    Args:
        n_per_group: Number of applicants per group (default 2500).
        seed: Random seed for reproducibility.

    Returns:
        DataFrame with columns: group, approved, defaulted, loan_size, processing_time
    """
    np.random.seed(seed)

    records = []

    for group in ["A", "B"]:
        for i in range(n_per_group):
            if group == "A":
                approved = np.random.random() < 0.62
                default_rate = 0.11
                base_loan = np.random.uniform(10_000, 150_000)
                base_time = np.random.uniform(30, 120)
            else:
                approved = np.random.random() < 0.71
                default_rate = 0.09
                base_loan = np.random.uniform(10_000, 150_000)
                base_time = np.random.uniform(25, 100)

            defaulted = 0
            if approved:
                defaulted = 1 if np.random.random() < default_rate else 0

            loan_size = base_loan + np.random.normal(0, 5_000) if approved else 0
            loan_size = max(loan_size, 0)

            processing_time = base_time + np.random.normal(0, 10)

            records.append({
                "group": group,
                "applicant_id": f"{group}_{i+1}",
                "approved": 1 if approved else 0,
                "defaulted": defaulted,
                "loan_size": round(loan_size, 2),
                "processing_time": round(max(processing_time, 1), 1),
            })

    df = pd.DataFrame(records)
    return df


def compute_group_stats(df: pd.DataFrame) -> dict:
    """Compute summary statistics per group.

    Args:
        df: DataFrame from generate_credit_data.

    Returns:
        Dict with stats for each group.
    """
    stats = {}
    for group in ["A", "B"]:
        g = df[df["group"] == group]
        n = len(g)
        n_approved = g["approved"].sum()
        n_defaulted = g["defaulted"].sum()

        stats[group] = {
            "n": n,
            "approval_rate": g["approved"].mean(),
            "default_rate": g["defaulted"].mean() if n_approved > 0 else 0,
            "avg_loan_size": g[g["approved"] == 1]["loan_size"].mean() if n_approved > 0 else 0,
            "avg_processing_time": g[g["approved"] == 1]["processing_time"].mean() if n_approved > 0 else 0,
        }
    return stats
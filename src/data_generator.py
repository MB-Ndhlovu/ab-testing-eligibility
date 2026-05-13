"""Data generator for credit eligibility A/B test simulation."""

import numpy as np
import pandas as pd

np.random.seed(42)


def generate_loan_data(n=5000, approval_rate=0.62, default_rate=0.11, noise_scale=0.03):
    """
    Generate synthetic loan application data.

    Parameters
    ----------
    n : int
        Number of loan applications.
    approval_rate : float
        Base approval rate for the group.
    default_rate : float
        Base default rate (conditional on approval).
    noise_scale : float
        Scale for adding noise to simulate real-world variance.

    Returns
    -------
    pd.DataFrame
        DataFrame with loan outcomes.
    """
    approved = np.random.random(n) < approval_rate

    default_given_approved = default_rate + np.random.normal(0, noise_scale, n)
    default_given_approved = np.clip(default_given_approved, 0.01, 0.5)
    defaulted = approved & (np.random.random(n) < default_given_approved)

    loan_size = np.random.lognormal(mean=10.5, sigma=0.7, size=n)
    loan_size = np.clip(loan_size, 1000, 500000)

    processing_time = np.random.exponential(scale=2.5, size=n) + np.random.normal(1.5, 0.5, n)
    processing_time = np.clip(processing_time, 0.5, 24)

    return pd.DataFrame({
        "approved": approved,
        "defaulted": defaulted,
        "loan_size": loan_size,
        "processing_time_hours": processing_time,
    })


def generate_experiment_data(n_per_group=5000):
    """
    Generate data for both control (A) and treatment (B) groups.

    Parameters
    ----------
    n_per_group : int
        Number of samples per group.

    Returns
    -------
    tuple[pd.DataFrame, pd.DataFrame]
        (group_a, group_b) dataframes.
    """
    group_a = generate_loan_data(n=n_per_group, approval_rate=0.62, default_rate=0.11, noise_scale=0.03)
    group_a["group"] = "A"

    group_b = generate_loan_data(n=n_per_group, approval_rate=0.71, default_rate=0.09, noise_scale=0.03)
    group_b["group"] = "B"

    return group_a, group_b


def compute_group_summary(df):
    """Compute summary statistics for a group."""
    n = len(df)
    approved_count = df["approved"].sum()
    defaulted_count = df["defaulted"].sum()
    approved_rate = approved_count / n
    default_rate = defaulted_count / approved_count if approved_count > 0 else 0
    avg_loan_size = df.loc[df["approved"], "loan_size"].mean() if approved_count > 0 else 0
    avg_processing_time = df["processing_time_hours"].mean()

    return {
        "n": n,
        "approved_count": int(approved_count),
        "defaulted_count": int(defaulted_count),
        "approval_rate": round(approved_rate, 4),
        "default_rate": round(default_rate, 4),
        "avg_loan_size": round(avg_loan_size, 2),
        "avg_processing_time_hours": round(avg_processing_time, 2),
    }


if __name__ == "__main__":
    a, b = generate_experiment_data()
    print("Group A summary:", compute_group_summary(a))
    print("Group B summary:", compute_group_summary(b))
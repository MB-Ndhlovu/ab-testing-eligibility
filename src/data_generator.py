"""
Data generator for the A/B test experiment.
Generates synthetic loan application data for control (A) and treatment (B) groups.
"""
import numpy as np
import pandas as pd

np.random.seed(42)

N = 2500  # applicants per group

def generate_data():
    """Generate 5000 synthetic loan records: 2500 control (A), 2500 treatment (B)."""

    # --- Group A (Control) ---
    approved_A = np.random.random(N) < 0.62
    defaulted_A = approved_A & (np.random.random(N) < 0.11)

    loan_size_A = np.where(
        approved_A,
        np.random.lognormal(mean=10.5, sigma=0.5, size=N),
        0.0
    )
    # processing time: approved loans take 3-10 days, rejected take 1-2 days
    processing_time_A = np.where(
        approved_A,
        np.random.uniform(3, 10, size=N),
        np.random.uniform(1, 2, size=N)
    )

    df_A = pd.DataFrame({
        "group": "A",
        "approved": approved_A.astype(int),
        "defaulted": defaulted_A.astype(int),
        "loan_size": np.round(loan_size_A, 2),
        "processing_days": np.round(processing_time_A, 2),
    })

    # --- Group B (Treatment) ---
    approved_B = np.random.random(N) < 0.71
    defaulted_B = approved_B & (np.random.random(N) < 0.09)

    loan_size_B = np.where(
        approved_B,
        np.random.lognormal(mean=10.6, sigma=0.48, size=N),
        0.0
    )
    processing_time_B = np.where(
        approved_B,
        np.random.uniform(2.5, 8, size=N),
        np.random.uniform(0.5, 1.5, size=N)
    )

    df_B = pd.DataFrame({
        "group": "B",
        "approved": approved_B.astype(int),
        "defaulted": defaulted_B.astype(int),
        "loan_size": np.round(loan_size_B, 2),
        "processing_days": np.round(processing_time_B, 2),
    })

    df = pd.concat([df_A, df_B], ignore_index=True)
    return df

def summarize(df):
    """Return per-group summary statistics."""
    grp = df.groupby("group")
    return grp.agg(
        applicants=("approved", "count"),
        approval_rate=("approved", "mean"),
        default_rate=("defaulted", "mean"),
        avg_loan_size=("loan_size", lambda x: x[x > 0].mean()),
        avg_processing_days=("processing_days", "mean"),
    ).round(4)
"""Generate synthetic credit eligibility data for A/B testing."""
import numpy as np
import pandas as pd

np.random.seed(42)


def generate_credit_data(n=5000, p_approval_a=0.62, p_default_a=0.11,
                          p_approval_b=0.71, p_default_b=0.09):
    """
    Generate synthetic loan application data for two groups.

    Parameters
    ----------
    n : int
        Total number of records (split evenly between A and B)
    p_approval_a, p_approval_b : float
        True approval probabilities for group A and B
    p_default_a, p_default_b : float
        True default probabilities for group A and B

    Returns
    -------
    pd.DataFrame
    """
    half = n // 2

    # Group A (control)
    approved_a = np.random.random(half) < p_approval_a
    defaulted_a = approved_a & (np.random.random(half) < p_default_a)
    approved_and_not_default_a = approved_a & ~defaulted_a

    # Group B (treatment)
    approved_b = np.random.random(half) < p_approval_b
    defaulted_b = approved_b & (np.random.random(half) < p_default_b)
    approved_and_not_default_b = approved_b & ~defaulted_b

    # Loan sizes (in Rands, realistic South African lending scale)
    base_loan_a = np.random.lognormal(mean=11.0, sigma=0.9, size=half)
    base_loan_b = np.random.lognormal(mean=11.2, sigma=0.9, size=half)

    # Processing time in hours (A slightly slower)
    processing_time_a = np.random.exponential(scale=2.5, size=half) + 0.5
    processing_time_b = np.random.exponential(scale=2.2, size=half) + 0.5

    df_a = pd.DataFrame({
        "group": "A",
        "approved": approved_a,
        "defaulted": defaulted_a,
        "approved_not_defaulted": approved_and_not_default_a,
        "loan_size": np.round(base_loan_a, 2),
        "processing_time_hrs": np.round(processing_time_a, 2),
    })

    df_b = pd.DataFrame({
        "group": "B",
        "approved": approved_b,
        "defaulted": defaulted_b,
        "approved_not_defaulted": approved_and_not_default_b,
        "loan_size": np.round(base_loan_b, 2),
        "processing_time_hrs": np.round(processing_time_b, 2),
    })

    return pd.concat([df_a, df_b], ignore_index=True)


def compute_group_summary(df):
    """Compute summary statistics per group."""
    summaries = {}
    for group, gdf in df.groupby("group"):
        approved = gdf["approved"].sum()
        defaulted = gdf["defaulted"].sum()
        n = len(gdf)
        n_approved = approved
        n_defaulted = defaulted
        summaries[group] = {
            "n": n,
            "approval_rate": approved / n,
            "default_rate": defaulted / n_approved if n_approved > 0 else 0.0,
            "avg_loan_size": gdf.loc[gdf["approved"], "loan_size"].mean(),
            "avg_processing_time": gdf["processing_time_hrs"].mean(),
        }
    return summaries

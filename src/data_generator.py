import numpy as np
import pandas as pd


def generate_credit_data(n: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Generate synthetic credit eligibility data for A/B testing.

    Args:
        n: Total number of applicants
        seed: Random seed for reproducibility

    Returns:
        DataFrame with columns: applicant_id, group, approved, defaulted,
        loan_size, processing_time_seconds
    """
    np.random.seed(seed)

    half = n // 2

    group_a_approval_rate = 0.62
    group_a_default_rate = 0.11
    group_b_approval_rate = 0.71
    group_b_default_rate = 0.09

    approved_a = np.random.random(half) < group_a_approval_rate
    defaulted_a = np.random.random(half) < group_a_default_rate
    approved_b = np.random.random(half) < group_b_approval_rate
    defaulted_b = np.random.random(half) < group_b_default_rate

    loan_sizes_a = np.random.lognormal(mean=10.5, sigma=0.6, size=half)
    loan_sizes_a = np.clip(loan_sizes_a, 1000, 150000)
    loan_sizes_b = np.random.lognormal(mean=10.6, sigma=0.6, size=half)
    loan_sizes_b = np.clip(loan_sizes_b, 1000, 150000)

    processing_a = np.random.normal(loc=4.2, scale=1.8, size=half)
    processing_b = np.random.normal(loc=3.8, scale=1.6, size=half)
    processing_a = np.clip(processing_a, 0.5, 15)
    processing_b = np.clip(processing_b, 0.5, 15)

    df_a = pd.DataFrame({
        "applicant_id": range(1, half + 1),
        "group": "A",
        "approved": approved_a.astype(int),
        "defaulted": defaulted_a.astype(int),
        "loan_size": np.round(loan_sizes_a, 2),
        "processing_time_seconds": np.round(processing_a, 2),
    })

    df_b = pd.DataFrame({
        "applicant_id": range(half + 1, n + 1),
        "group": "B",
        "approved": approved_b.astype(int),
        "defaulted": defaulted_b.astype(int),
        "loan_size": np.round(loan_sizes_b, 2),
        "processing_time_seconds": np.round(processing_b, 2),
    })

    df = pd.concat([df_a, df_b], ignore_index=True)
    df["defaulted"] = df["defaulted"] * df["approved"]

    return df


def compute_group_summary(df: pd.DataFrame, group: str) -> dict:
    """Compute summary statistics for a group."""
    g = df[df["group"] == group]
    n = len(g)
    approved_sum = g["approved"].sum()
    defaulted_sum = g["defaulted"].sum()

    return {
        "group": group,
        "n": n,
        "approval_rate": approved_sum / n,
        "default_rate": defaulted_sum / approved_sum if approved_sum > 0 else 0,
        "avg_loan_size": g.loc[g["approved"] == 1, "loan_size"].mean(),
        "avg_processing_time": g["processing_time_seconds"].mean(),
    }


if __name__ == "__main__":
    df = generate_credit_data()
    print(df.head(10))
    for g in ["A", "B"]:
        s = compute_group_summary(df, g)
        print(f"\nGroup {g}:")
        for k, v in s.items():
            print(f"  {k}: {v}")
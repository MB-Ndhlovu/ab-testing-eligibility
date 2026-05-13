import numpy as np
import pandas as pd


def generate_credit_data(n=5000, seed=42):
    np.random.seed(seed)
    half = n // 2

    # Credit score distribution (300-850)
    scores_a = np.random.normal(680, 80, half).clip(300, 850)
    scores_b = np.random.normal(700, 80, half).clip(300, 850)

    # Income distribution (20k-200k)
    income_a = np.random.lognormal(10.8, 0.45, half)
    income_b = np.random.lognormal(11.0, 0.45, half)

    # Debt-to-income ratio
    dti_a = np.random.beta(2.5, 8, half) * 0.5
    dti_b = np.random.beta(2.5, 8, half) * 0.5

    # Loan amount requested
    loan_amount_a = np.random.lognormal(9.5, 0.7, half).clip(1000, 500000)
    loan_amount_b = np.random.lognormal(9.6, 0.7, half).clip(1000, 500000)

    df_a = pd.DataFrame({
        "group": "A",
        "credit_score": scores_a,
        "income": income_a,
        "dti": dti_a,
        "loan_amount": loan_amount_a,
    })

    df_b = pd.DataFrame({
        "group": "B",
        "credit_score": scores_b,
        "income": income_b,
        "dti": dti_b,
        "loan_amount": loan_amount_b,
    })

    df = pd.concat([df_a, df_b], ignore_index=True)

    # Eligibility rules for Group A (control): stricter
    approved_a = (
        (df.loc[df["group"] == "A", "credit_score"] >= 620) &
        (df.loc[df["group"] == "A", "dti"] <= 0.35) &
        (df.loc[df["group"] == "A", "income"] >= 25000)
    ).values

    # Eligibility rules for Group B (treatment): more inclusive
    approved_b = (
        (df.loc[df["group"] == "B", "credit_score"] >= 580) &
        (df.loc[df["group"] == "B", "dti"] <= 0.40) &
        (df.loc[df["group"] == "B", "income"] >= 22000)
    ).values

    approved = np.concatenate([approved_a, approved_b])
    df["approved"] = approved

    # Default probability given approval (add noise)
    base_default_prob = np.where(df["group"] == "A", 0.11, 0.09)
    noise = np.random.normal(0, 0.025, n)
    default_prob = np.clip(base_default_prob + noise, 0.01, 0.30)
    df["defaulted"] = np.random.binomial(1, default_prob)
    df.loc[df["approved"] == 0, "defaulted"] = 0

    # Processing time (seconds)
    base_time = np.where(df["group"] == "A", 180, 160)
    df["processing_time"] = np.maximum(30, base_time + np.random.normal(0, 40, n)).astype(int)

    return df


def compute_group_stats(df):
    stats = {}
    for group in ["A", "B"]:
        subset = df[df["group"] == group]
        approved = subset["approved"]
        defaulted = subset["defaulted"]

        n = len(subset)
        stats[group] = {
            "n": n,
            "approval_rate": approved.mean(),
            "default_rate": defaulted.sum() / approved.sum() if approved.sum() > 0 else 0,
            "avg_loan_size": subset.loc[approved == 1, "loan_amount"].mean(),
            "processing_time_mean": subset["processing_time"].mean(),
        }
    return stats
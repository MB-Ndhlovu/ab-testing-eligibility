"""Generate synthetic credit applicant data for A/B test."""

import numpy as np
import pandas as pd

RNG = np.random.default_rng(seed=42)

def generate_applicants(n: int = 5000) -> pd.DataFrame:
    """
    Generate n synthetic credit applicants with credit tiers and base profiles.
    """
    half = n // 2

    tiers_prime    = RNG.choice(["prime", "near_prime", "subprime"], size=half, p=[0.30, 0.45, 0.25])
    tiers_subprime = RNG.choice(["prime", "near_prime", "subprime"], size=n - half, p=[0.30, 0.45, 0.25])
    tiers = np.concatenate([tiers_prime, tiers_subprime])

    scores_prime    = np.clip(RNG.normal(720, 40,  half).astype(int), 300, 850)
    scores_subprime = np.clip(RNG.normal(630, 50,  n - half).astype(int), 300, 850)
    credit_scores = np.concatenate([scores_prime, scores_subprime])

    inc_prime    = RNG.normal(960_000,  200_000, half)
    inc_subprime = RNG.normal(480_000,  120_000, n - half)
    incomes = np.concatenate([inc_prime, inc_subprime])

    loan_multipliers = RNG.uniform(0.3, 1.2, n)
    loan_requests = np.clip(incomes * loan_multipliers, 10_000, 5_000_000)

    existing_debt = np.clip(incomes * RNG.uniform(0.05, 0.4, n), 0, 2_000_000)
    dti = (existing_debt / (incomes + 1)).round(4)

    df = pd.DataFrame({
        "applicant_id":  range(1, n + 1),
        "credit_tier":  tiers,
        "credit_score": credit_scores,
        "annual_income": incomes.round(0),
        "loan_request": loan_requests.round(0),
        "existing_debt": existing_debt.round(0),
        "dti": dti,
        "group": ["A"] * half + ["B"] * (n - half),
    })
    return df


def assign_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Apply eligibility rules and simulate loan outcomes.

    Group A (control): current model — tighter approval, moderate default risk.
    Group B (treatment): new model — looser approval, slightly better default
    performance. Noise added so results are not perfectly clean.
    """
    a_mask = df["group"] == "A"
    b_mask = df["group"] == "B"

    base_approval = {"prime": 0.92, "near_prime": 0.65, "subprime": 0.25}
    base_default  = {"prime": 0.04, "near_prime": 0.10, "subprime": 0.22}

    # --- Approval ---
    p_approve_a = df.loc[a_mask, "credit_tier"].map(base_approval).values
    p_approve_a = np.clip(p_approve_a + RNG.normal(0, 0.06, size=a_mask.sum()), 0.01, 0.99)

    p_approve_b = df.loc[b_mask, "credit_tier"].map(base_approval).values
    p_approve_b = np.clip(p_approve_b + 0.09 + RNG.normal(0, 0.06, size=b_mask.sum()), 0.01, 0.99)

    approved = np.zeros(len(df), dtype=bool)
    approved[a_mask] = RNG.random(size=a_mask.sum()) < p_approve_a
    approved[b_mask] = RNG.random(size=b_mask.sum()) < p_approve_b
    df["approved"] = approved

    # --- Default (only approved) ---
    defaulted = np.zeros(len(df), dtype=bool)
    approved_indices = df.index[df["approved"]].tolist()

    for idx in approved_indices:
        tier = df.loc[idx, "credit_tier"]
        p_def = base_default[tier]
        if df.loc[idx, "group"] == "B":
            p_def = max(0.01, p_def - 0.02)
        p_def = np.clip(p_def + RNG.normal(0, 0.025), 0.005, 0.5)
        defaulted[idx] = RNG.random() < p_def

    df["defaulted"] = defaulted

    # --- Loan size (approved only) ---
    loan_size = np.zeros(len(df))
    approved_mask = df["approved"].values
    loan_size[approved_mask] = (
        df.loc[approved_mask, "loan_request"].values * RNG.uniform(0.7, 1.1, size=approved_mask.sum())
    )
    df["loan_size"] = loan_size.round(0)

    # --- Processing time ---
    base_time = {"prime": 8, "near_prime": 18, "subprime": 35}

    proc_time = np.zeros(len(df))
    proc_time[approved_mask] = df.loc[approved_mask, "credit_tier"].map(base_time).values
    proc_time[approved_mask] = np.clip(proc_time[approved_mask] + RNG.normal(0, 3, size=approved_mask.sum()), 2, 120)

    not_approved = ~approved_mask
    proc_time[not_approved] = df.loc[not_approved, "credit_tier"].map(base_time).values * 0.4
    proc_time[not_approved] = np.clip(proc_time[not_approved] + RNG.normal(0, 2, size=not_approved.sum()), 1, 60)

    df["processing_time"] = proc_time.round(1)
    return df


def compute_summary(df: pd.DataFrame) -> dict:
    """Compute per-group summary statistics."""
    results = {}
    for group, gdf in df.groupby("group"):
        n = len(gdf)
        n_approved = int(gdf["approved"].sum())
        n_defaulted = int(gdf["defaulted"].sum())

        results[group] = {
            "n": n,
            "approval_rate": n_approved / n,
            "default_rate": n_defaulted / n_approved if n_approved > 0 else 0.0,
            "avg_loan_size": gdf.loc[gdf["approved"], "loan_size"].mean() if n_approved > 0 else 0.0,
            "avg_processing_time": round(gdf["processing_time"].mean(), 2),
        }
    return results


if __name__ == "__main__":
    df = generate_applicants(5000)
    df = assign_outcomes(df)
    summary = compute_summary(df)
    import json
    print(json.dumps(summary, indent=2))
    df.to_csv("/home/workspace/Projects/ab-testing-eligibility/data.csv", index=False)
    print("Data saved to data.csv")
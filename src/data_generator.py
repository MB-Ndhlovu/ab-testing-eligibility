"""Generate synthetic loan application data for A/B testing."""

import numpy as np
import pandas as pd

np.random.seed(42)

N_PER_GROUP = 2500


def generate_data() -> pd.DataFrame:
    group_a_approval_rate = 0.62
    group_a_default_rate = 0.11
    group_b_approval_rate = 0.71
    group_b_default_rate = 0.09

    records = []

    # Group A
    rng_a = np.random.default_rng(42)
    approved_a = rng_a.random(N_PER_GROUP) < group_a_approval_rate
    n_approved_a = approved_a.sum()
    defaulted_a = (rng_a.random(n_approved_a) < group_a_default_rate).astype(bool)
    loan_sizes_a = rng_a.lognormal(mean=10.5, sigma=0.8, size=n_approved_a)
    processing_a = rng_a.normal(loc=48, scale=12, size=n_approved_a)

    defaulted_idx_a = 0
    loan_idx_a = 0
    proc_idx_a = 0
    for i in range(N_PER_GROUP):
        approved = approved_a[i]
        if approved:
            defaulted = defaulted_a[defaulted_idx_a]
            defaulted_idx_a += 1
            loan_size = loan_sizes_a[loan_idx_a]
            loan_idx_a += 1
            proc_hours = processing_a[proc_idx_a]
            proc_idx_a += 1
        else:
            defaulted = False
            loan_size = 0.0
            proc_hours = 0.0
        records.append({
            "application_id": i + 1,
            "group": "A",
            "approved": approved,
            "loan_size": round(loan_size, 2),
            "processing_hours": round(proc_hours, 2),
            "defaulted": defaulted,
        })

    # Group B
    rng_b = np.random.default_rng(43)
    approved_b = rng_b.random(N_PER_GROUP) < group_b_approval_rate
    n_approved_b = approved_b.sum()
    defaulted_b = (rng_b.random(n_approved_b) < group_b_default_rate).astype(bool)
    loan_sizes_b = rng_b.lognormal(mean=10.5, sigma=0.8, size=n_approved_b)
    processing_b = rng_b.normal(loc=45, scale=11, size=n_approved_b)

    defaulted_idx_b = 0
    loan_idx_b = 0
    proc_idx_b = 0
    for i in range(N_PER_GROUP):
        approved = approved_b[i]
        if approved:
            defaulted = defaulted_b[defaulted_idx_b]
            defaulted_idx_b += 1
            loan_size = loan_sizes_b[loan_idx_b]
            loan_idx_b += 1
            proc_hours = processing_b[proc_idx_b]
            proc_idx_b += 1
        else:
            defaulted = False
            loan_size = 0.0
            proc_hours = 0.0
        records.append({
            "application_id": N_PER_GROUP + i + 1,
            "group": "B",
            "approved": approved,
            "loan_size": round(loan_size, 2),
            "processing_hours": round(proc_hours, 2),
            "defaulted": defaulted,
        })

    return pd.DataFrame(records)


def summarize(df: pd.DataFrame) -> dict:
    summary = {}
    for group in ["A", "B"]:
        g = df[df["group"] == group]
        approved = g[g["approved"]]
        n_total = len(g)
        n_approved = len(approved)
        summary[group] = {
            "n_total": n_total,
            "n_approved": n_approved,
            "approval_rate": round(n_approved / n_total, 4),
            "default_rate": round(approved["defaulted"].mean(), 4) if n_approved > 0 else 0.0,
            "avg_loan_size": round(approved["loan_size"].mean(), 2) if n_approved > 0 else 0.0,
            "avg_processing_hours": round(approved["processing_hours"].mean(), 2) if n_approved > 0 else 0.0,
        }
    return summary


if __name__ == "__main__":
    df = generate_data()
    print(df.head(10))
    print(summarize(df))
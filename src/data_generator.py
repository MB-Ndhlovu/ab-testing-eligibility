import numpy as np
import pandas as pd

np.random.seed(42)

N = 5000
n_per_group = N // 2

def generate_data():
    group_a_approval = 0.62
    group_a_default = 0.11
    group_b_approval = 0.71
    group_b_default = 0.09

    approved_a = np.random.binomial(1, group_a_approval, n_per_group)
    default_a = np.random.binomial(1, group_a_default, n_per_group)
    approved_a_mask = approved_a == 1
    approved_b = np.random.binomial(1, group_b_approval, n_per_group)
    default_b = np.random.binomial(1, group_b_default, n_per_group)
    approved_b_mask = approved_b == 1

    data = {
        "applicant_id": list(range(1, N + 1)),
        "group": ["A"] * n_per_group + ["B"] * n_per_group,
        "approved": list(approved_a) + list(approved_b),
        "defaulted": list(default_a) + list(default_b),
    }
    df = pd.DataFrame(data)

    base_loan_a = np.random.lognormal(10.5, 0.6, n_per_group)
    base_loan_b = np.random.lognormal(10.6, 0.6, n_per_group)

    loan_size_a = np.where(approved_a_mask, base_loan_a, 0)
    loan_size_b = np.where(approved_b_mask, base_loan_b, 0)

    proc_time_a = np.random.exponential(3.5, n_per_group)
    proc_time_b = np.random.exponential(3.2, n_per_group)

    df.loc[:n_per_group - 1, "loan_size"] = loan_size_a
    df.loc[n_per_group:, "loan_size"] = loan_size_b
    df["loan_size"] = df["loan_size"].astype(float)

    df.loc[:n_per_group - 1, "processing_time"] = proc_time_a
    df.loc[n_per_group:, "processing_time"] = proc_time_b

    noise_mask = np.random.rand(N) < 0.03
    df.loc[noise_mask & (df["group"] == "A"), "approved"] ^= 1
    df.loc[noise_mask & (df["group"] == "B"), "approved"] ^= 1
    df["approved"] = df["approved"].clip(0, 1).astype(int)
    df["defaulted"] = df["defaulted"].clip(0, 1).astype(int)

    return df

def compute_group_stats(df, group):
    g = df[df["group"] == group]
    approved = g["approved"]
    defaulted = g["defaulted"]
    n = len(g)
    approval_rate = approved.mean()
    default_rate = defaulted.mean()
    avg_loan_size = g.loc[approved == 1, "loan_size"].mean() if approved.sum() > 0 else 0.0
    avg_processing_time = g["processing_time"].mean()
    return {
        "n": n,
        "approval_rate": approval_rate,
        "default_rate": default_rate,
        "avg_loan_size": avg_loan_size,
        "avg_processing_time": avg_processing_time,
    }
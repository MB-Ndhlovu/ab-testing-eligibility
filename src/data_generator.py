"""Generate synthetic credit eligibility data for A/B testing."""

import numpy as np
import pandas as pd

np.random.seed(42)

N = 5000
n_a = 2500
n_b = 2500

approved_a = np.random.rand(n_a) < 0.62
approved_b = np.random.rand(n_b) < 0.71

default_a = np.zeros(n_a, dtype=bool)
default_a[approved_a] = np.random.rand(approved_a.sum()) < 0.11

default_b = np.zeros(n_b, dtype=bool)
default_b[approved_b] = np.random.rand(approved_b.sum()) < 0.09

loan_size_a = np.random.exponential(scale=15000, size=n_a)
loan_size_b = np.random.exponential(scale=15500, size=n_b)

processing_a = np.random.exponential(scale=4.5, size=n_a)
processing_b = np.random.exponential(scale=4.2, size=n_b)

approved_a = approved_a.astype(int)
approved_b = approved_b.astype(int)
default_a = default_a.astype(int)
default_b = default_b.astype(int)

df_a = pd.DataFrame({
    "group": "A",
    "approved": approved_a,
    "defaulted": default_a,
    "loan_size": loan_size_a,
    "processing_time": processing_a,
})
df_a["defaulted"] = df_a["defaulted"] * df_a["approved"]

df_b = pd.DataFrame({
    "group": "B",
    "approved": approved_b,
    "defaulted": default_b,
    "loan_size": loan_size_b,
    "processing_time": processing_b,
})
df_b["defaulted"] = df_b["defaulted"] * df_b["approved"]

df = pd.concat([df_a, df_b], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

df.to_csv("data.csv", index=False)

metrics_a = {
    "approval_rate": df_a["approved"].mean(),
    "default_rate": df_a["defaulted"].mean(),
    "avg_loan_size": df_a["loan_size"].mean(),
    "processing_time": df_a["processing_time"].mean(),
}
metrics_b = {
    "approval_rate": df_b["approved"].mean(),
    "default_rate": df_b["defaulted"].mean(),
    "avg_loan_size": df_b["loan_size"].mean(),
    "processing_time": df_b["processing_time"].mean(),
}

print("Data generation complete")
print(f"Group A: {n_a} applicants, approval_rate={metrics_a['approval_rate']:.4f}, default_rate={metrics_a['default_rate']:.4f}")
print(f"Group B: {n_b} applicants, approval_rate={metrics_b['approval_rate']:.4f}, default_rate={metrics_b['default_rate']:.4f}")
import numpy as np
import pandas as pd

np.random.seed(42)

N = 5000
n_per_group = N // 2

# Group A (control): approval ~0.62, default ~0.11
# Group B (treatment): approval ~0.71, default ~0.09

approved_A = np.random.binomial(1, 0.62, n_per_group)
defaulted_A = np.random.binomial(1, np.where(approved_A == 1, 0.11 * 1.15, 0), n_per_group)
defaulted_A = np.clip(defaulted_A, 0, 1)

approved_B = np.random.binomial(1, 0.71, n_per_group)
defaulted_B = np.random.binomial(1, np.where(approved_B == 1, 0.09 * 1.10, 0), n_per_group)
defaulted_B = np.clip(defaulted_B, 0, 1)

loan_size_A = np.random.lognormal(mean=9.5, sigma=0.8, size=n_per_group)
loan_size_B = np.random.lognormal(mean=9.7, sigma=0.8, size=n_per_group)

processing_A = np.random.normal(4.2, 1.5, n_per_group)
processing_B = np.random.normal(3.8, 1.4, n_per_group)

df_A = pd.DataFrame({
    "group": "A",
    "approved": approved_A,
    "defaulted": defaulted_A,
    "loan_size": np.round(loan_size_A, 2),
    "processing_time": np.round(processing_A, 3),
})

df_B = pd.DataFrame({
    "group": "B",
    "approved": approved_B,
    "defaulted": defaulted_B,
    "loan_size": np.round(loan_size_B, 2),
    "processing_time": np.round(processing_B, 3),
})

df = pd.concat([df_A, df_B], ignore_index=True)
df.to_csv("/home/workspace/Projects/ab-testing-eligibility/data.csv", index=False)

print(f"Generated {len(df)} rows — Group A: {len(df_A)}, Group B: {len(df_B)}")
print(f"Group A approval rate: {df_A['approved'].mean():.4f}")
print(f"Group B approval rate: {df_B['approved'].mean():.4f}")
print(f"Group A default rate:  {df_A['defaulted'].mean():.4f}")
print(f"Group B default rate:  {df_B['defaulted'].mean():.4f}")
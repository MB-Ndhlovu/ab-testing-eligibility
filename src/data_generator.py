import numpy as np
import pandas as pd

def generate_data(n=5000, seed=42):
    np.random.seed(seed)
    half = n // 2

    # Control group A
    group_a_approved = np.random.random(half) < 0.62
    group_a_defaulted = np.random.random(half) < 0.11

    # Treatment group B
    group_b_approved = np.random.random(half) < 0.71
    group_b_defaulted = np.random.random(half) < 0.09

    # Simulate loan sizes (R) and processing times (hours)
    group_a_loan_size = np.random.lognormal(mean=12, sigma=0.8, size=half)
    group_a_proc_time = np.random.exponential(scale=2.5, size=half) + 0.5

    group_b_loan_size = np.random.lognormal(mean=12.2, sigma=0.8, size=half)
    group_b_proc_time = np.random.exponential(scale=2.2, size=half) + 0.5

    df_a = pd.DataFrame({
        "group": "A",
        "approved": group_a_approved,
        "defaulted": group_a_defaulted,
        "loan_size": group_a_loan_size,
        "processing_time": group_a_proc_time,
    })

    df_b = pd.DataFrame({
        "group": "B",
        "approved": group_b_approved,
        "defaulted": group_b_defaulted,
        "loan_size": group_b_loan_size,
        "processing_time": group_b_proc_time,
    })

    return pd.concat([df_a, df_b], ignore_index=True)

def compute_group_stats(df):
    stats = {}
    for group in ["A", "B"]:
        subset = df[df["group"] == group]
        n = len(subset)
        stats[group] = {
            "n": int(n),
            "approval_rate": float(subset["approved"].mean()),
            "default_rate": float(subset["defaulted"].mean()),
            "avg_loan_size": float(subset["loan_size"].mean()),
            "avg_processing_time": float(subset["processing_time"].mean()),
        }
    return stats

if __name__ == "__main__":
    df = generate_data()
    print(df.head())
    stats = compute_group_stats(df)
    for g, s in stats.items():
        print(f"Group {g}: {s}")
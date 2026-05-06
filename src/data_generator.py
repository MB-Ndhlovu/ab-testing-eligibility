import numpy as np
import pandas as pd


def generate_experiment_data(n=5000, seed=42):
    np.random.seed(seed)

    group_a_size = n // 2
    group_b_size = n - group_a_size

    group_a_approval = 0.62
    group_b_approval = 0.71
    group_a_default = 0.11
    group_b_default = 0.09

    group_a_approved = np.random.random(group_a_size) < group_a_approval
    group_b_approved = np.random.random(group_b_size) < group_b_approval

    group_a_default_given_approved = np.array([
        np.random.random() < group_a_default if approved else False
        for approved in group_a_approved
    ])
    group_b_default_given_approved = np.array([
        np.random.random() < group_b_default if approved else False
        for approved in group_b_approved
    ])

    group_a_loan_size = np.where(
        group_a_approved,
        np.random.normal(15000, 5000, group_a_size),
        0
    )
    group_b_loan_size = np.where(
        group_b_approved,
        np.random.normal(15500, 5200, group_b_size),
        0
    )

    group_a_loan_size = np.clip(group_a_loan_size, 1000, 50000)
    group_b_loan_size = np.clip(group_b_loan_size, 1000, 50000)

    group_a_processing = np.where(
        group_a_approved,
        np.random.normal(4.5, 1.2, group_a_size),
        np.random.normal(1.5, 0.5, group_a_size)
    )
    group_b_processing = np.where(
        group_b_approved,
        np.random.normal(3.8, 1.0, group_b_size),
        np.random.normal(1.2, 0.4, group_b_size)
    )

    df_a = pd.DataFrame({
        "applicant_id": range(group_a_size),
        "group": "A",
        "approved": group_a_approved,
        "defaulted": group_a_default_given_approved,
        "loan_size": group_a_loan_size,
        "processing_time": group_a_processing
    })

    df_b = pd.DataFrame({
        "applicant_id": range(group_a_size, n),
        "group": "B",
        "approved": group_b_approved,
        "defaulted": group_b_default_given_approved,
        "loan_size": group_b_loan_size,
        "processing_time": group_b_processing
    })

    df = pd.concat([df_a, df_b], ignore_index=True)

    return df


def compute_group_metrics(df, group):
    g = df[df["group"] == group]
    approved = g[g["approved"]]

    return {
        "group": group,
        "n": len(g),
        "n_approved": g["approved"].sum(),
        "approval_rate": g["approved"].mean(),
        "default_rate": approved["defaulted"].mean() if len(approved) > 0 else 0,
        "avg_loan_size": approved["loan_size"].mean() if len(approved) > 0 else 0,
        "avg_processing_time": g["processing_time"].mean()
    }


if __name__ == "__main__":
    data = generate_experiment_data()
    print(data.head(10))
    print("\nGroup A metrics:", compute_group_metrics(data, "A"))
    print("Group B metrics:", compute_group_metrics(data, "B"))
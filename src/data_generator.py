import numpy as np

np.random.seed(42)

N = 5000
n_per_group = N // 2

APPROVAL_A = 0.62
APPROVAL_B = 0.71
DEFAULT_A = 0.11
DEFAULT_B = 0.09

def generate_data():
    approved_a = np.random.random(n_per_group) < APPROVAL_A
    approved_b = np.random.random(n_per_group) < APPROVAL_B

    defaulted_a = (np.random.random(n_per_group) < DEFAULT_A) & approved_a
    defaulted_b = (np.random.random(n_per_group) < DEFAULT_B) & approved_b

    loan_size_a = np.where(
        approved_a,
        np.clip(np.random.lognormal(10.5, 0.6, n_per_group), 1000, 500000),
        0
    )
    loan_size_b = np.where(
        approved_b,
        np.clip(np.random.lognormal(10.7, 0.55, n_per_group), 1000, 500000),
        0
    )

    processing_time_a = np.clip(
        np.random.normal(4.2, 1.8, n_per_group) + np.random.normal(0, 0.4, n_per_group),
        0.5, 24
    )
    processing_time_b = np.clip(
        np.random.normal(3.8, 1.6, n_per_group) + np.random.normal(0, 0.4, n_per_group),
        0.5, 24
    )

    return {
        "group_a": {
            "approved": approved_a,
            "defaulted": defaulted_a,
            "loan_size": loan_size_a,
            "processing_time": processing_time_a,
            "approval_rate": approved_a.mean(),
            "default_rate": defaulted_a.sum() / n_per_group,
            "avg_loan_size": loan_size_a[loan_size_a > 0].mean() if loan_size_a[loan_size_a > 0].size > 0 else 0,
            "avg_processing_time": processing_time_a[approved_a].mean() if approved_a.sum() > 0 else 0,
        },
        "group_b": {
            "approved": approved_b,
            "defaulted": defaulted_b,
            "loan_size": loan_size_b,
            "processing_time": processing_time_b,
            "approval_rate": approved_b.mean(),
            "default_rate": defaulted_b.sum() / n_per_group,
            "avg_loan_size": loan_size_b[loan_size_b > 0].mean() if loan_size_b[loan_size_b > 0].size > 0 else 0,
            "avg_processing_time": processing_time_b[approved_b].mean() if approved_b.sum() > 0 else 0,
        },
    }

if __name__ == "__main__":
    data = generate_data()
    print("Group A — Approval Rate:", round(data["group_a"]["approval_rate"], 4))
    print("Group A — Default Rate:", round(data["group_a"]["default_rate"], 4))
    print("Group A — Avg Loan Size:", round(data["group_a"]["avg_loan_size"], 2))
    print("Group A — Avg Processing Time:", round(data["group_a"]["avg_processing_time"], 2))
    print()
    print("Group B — Approval Rate:", round(data["group_b"]["approval_rate"], 4))
    print("Group B — Default Rate:", round(data["group_b"]["default_rate"], 4))
    print("Group B — Avg Loan Size:", round(data["group_b"]["avg_loan_size"], 2))
    print("Group B — Avg Processing Time:", round(data["group_b"]["avg_processing_time"], 2))
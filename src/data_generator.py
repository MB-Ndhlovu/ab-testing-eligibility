"""Generate synthetic credit eligibility data for A/B testing."""

import numpy as np

np.random.seed(42)

N = 5000
n_a = 2500
n_b = 2500

approval_rate_a = 0.62
approval_rate_b = 0.71

default_rate_a = 0.11
default_rate_b = 0.09

def generate_data():
    approved_a = np.random.binomial(n_a, approval_rate_a)
    approved_b = np.random.binomial(n_b, approval_rate_b)

    defaulted_a = np.random.binomial(approved_a, default_rate_a)
    defaulted_b = np.random.binomial(approved_b, default_rate_b)

    loan_size_a = np.random.lognormal(mean=np.log(18500), sigma=0.45, size=approved_a)
    loan_size_b = np.random.lognormal(mean=np.log(19200), sigma=0.45, size=approved_b)

    proc_time_a = np.random.gamma(shape=4, scale=1.05, size=n_a) + np.random.uniform(0, 1, size=n_a)
    proc_time_b = np.random.gamma(shape=4, scale=0.95, size=n_b) + np.random.uniform(0, 1, size=n_b)

    return {
        "group_a": {
            "n": n_a,
            "approved": approved_a,
            "approval_rate": approved_a / n_a,
            "defaults": defaulted_a,
            "default_rate": defaulted_a / approved_a if approved_a > 0 else 0,
            "avg_loan_size": float(np.mean(loan_size_a)),
            "avg_processing_time": float(np.mean(proc_time_a)),
        },
        "group_b": {
            "n": n_b,
            "approved": approved_b,
            "approval_rate": approved_b / n_b,
            "defaults": defaulted_b,
            "default_rate": defaulted_b / approved_b if approved_b > 0 else 0,
            "avg_loan_size": float(np.mean(loan_size_b)),
            "avg_processing_time": float(np.mean(proc_time_b)),
        },
    }

def get_summary(data):
    a = data["group_a"]
    b = data["group_b"]
    return {
        "approval_rate": {
            "control": a["approval_rate"],
            "treatment": b["approval_rate"],
        },
        "default_rate": {
            "control": a["default_rate"],
            "treatment": b["default_rate"],
        },
        "avg_loan_size": {
            "control": a["avg_loan_size"],
            "treatment": b["avg_loan_size"],
        },
        "processing_time": {
            "control": a["avg_processing_time"],
            "treatment": b["avg_processing_time"],
        },
    }

if __name__ == "__main__":
    data = generate_data()
    print("Data generated:")
    for group, stats in data.items():
        print(f"  {group}: {stats}")
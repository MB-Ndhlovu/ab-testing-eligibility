"""
Generate synthetic loan applicant data for A/B testing.
"""

import numpy as np

np.random.seed(42)

N = 5000
n_a = N // 2  # 2500
n_b = N // 2  # 2500

# ── Loan amounts ───────────────────────────────────────────────
base_loan_a = np.random.normal(85_000, 40_000, n_a)
base_loan_b = np.random.normal(90_000, 42_000, n_b)

# ── Approval outcomes (Bernoulli with target rates) ─────────────
approved_a = np.random.binomial(1, 0.62, n_a)
approved_b = np.random.binomial(1, 0.71, n_b)

# ── Default outcomes (only among approved, Bernoulli) ──────────
defaulted_a = np.where(
    approved_a == 1,
    np.random.binomial(1, 0.11, n_a),
    0,
)
defaulted_b = np.where(
    approved_b == 1,
    np.random.binomial(1, 0.09, n_b),
    0,
)

# ── Processing time (hours, log-normal) ────────────────────────
processing_a = np.random.lognormal(mean=np.log(3.5), sigma=0.55, size=n_a)
processing_b = np.random.lognormal(mean=np.log(3.2), sigma=0.50, size=n_b)

# ── Loan amounts (approved only) ──────────────────────────────
loan_size_a = np.where(approved_a == 1, np.clip(base_loan_a, 5_000, 500_000), 0.0)
loan_size_b = np.where(approved_b == 1, np.clip(base_loan_b, 5_000, 500_000), 0.0)

# ── Pack into dicts ─────────────────────────────────────────────
data_a = {
    "group": "A",
    "approved": approved_a,
    "defaulted": defaulted_a,
    "loan_size": loan_size_a,
    "processing_time": processing_a,
}

data_b = {
    "group": "B",
    "approved": approved_b,
    "defaulted": defaulted_b,
    "loan_size": loan_size_b,
    "processing_time": processing_b,
}


def compute_summary(data):
    approved = data["approved"]
    defaulted = data["defaulted"]
    loan_size = data["loan_size"]
    processing_time = data["processing_time"]

    n = len(approved)
    n_approved = int(approved.sum())
    n_defaulted = int(defaulted.sum())

    return {
        "group": data["group"],
        "n": n,
        "n_approved": n_approved,
        "approval_rate": n_approved / n,
        "default_rate": n_defaulted / n_approved if n_approved > 0 else 0.0,
        "avg_loan_size": float(loan_size[approved == 1].mean()) if n_approved > 0 else 0.0,
        "avg_processing_time": float(processing_time[approved == 1].mean()) if n_approved > 0 else 0.0,
    }


summary_a = compute_summary(data_a)
summary_b = compute_summary(data_b)


if __name__ == "__main__":
    print("=== Group A (Control) Summary ===")
    for k, v in summary_a.items():
        print(f"  {k}: {v}")

    print("\n=== Group B (Treatment) Summary ===")
    for k, v in summary_b.items():
        print(f"  {k}: {v}")
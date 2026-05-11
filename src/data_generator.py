"""Generate synthetic loan application data for A/B test."""
import numpy as np

np.random.seed(42)

N = 2500  # per group

# Group A: control — current eligibility model
# Group B: treatment — new eligibility model

# Outcomes are independent Bernoulli trials with slight noise added
group_a_approved = np.random.binomial(1, 0.62, N)
group_a_defaulted = np.random.binomial(1, 0.11, N)
# Make default conditional on approval (can't default if not approved)
group_a_defaulted = group_a_defaulted * group_a_approved

group_b_approved = np.random.binomial(1, 0.71, N)
group_b_defaulted = np.random.binomial(1, 0.09, N)
group_b_defaulted = group_b_defaulted * group_b_approved

# Loan sizes: log-normal, approved get larger loans
base_size = 50_000
group_a_loans = group_a_approved * np.random.lognormal(
    mean=np.log(base_size), sigma=0.5, size=N
)
group_b_loans = group_b_approved * np.random.lognormal(
    mean=np.log(base_size * 1.05), sigma=0.5, size=N
)

# Processing time in minutes (normal, skewed right)
group_a_time = np.random.gamma(shape=3, scale=4, size=N) + 5
group_b_time = np.random.gamma(shape=3, scale=3.5, size=N) + 4

group_a = {
    "approved": group_a_approved,
    "defaulted": group_a_defaulted,
    "loan_size": group_a_loans,
    "processing_time": group_a_time,
}

group_b = {
    "approved": group_b_approved,
    "defaulted": group_b_defaulted,
    "loan_size": group_b_loans,
    "processing_time": group_b_time,
}

def summary_stats(grp):
    approved = grp["approved"]
    defaulted = grp["defaulted"]
    n = len(approved)
    n_approved = approved.sum()
    n_defaulted = defaulted.sum()
    return {
        "n": n,
        "approval_rate": n_approved / n,
        "default_rate": n_defaulted / n_approved if n_approved > 0 else 0,
        "avg_loan_size": grp["loan_size"][approved == 1].mean() if n_approved > 0 else 0,
        "avg_processing_time": grp["processing_time"].mean(),
    }

print("=== Group A (Control) ===")
for k, v in summary_stats(group_a).items():
    print(f"  {k}: {v:.4f}")

print("\n=== Group B (Treatment) ===")
for k, v in summary_stats(group_b).items():
    print(f"  {k}: {v:.4f}")
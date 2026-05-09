"""Generate synthetic loan applicant data for A/B test."""
import numpy as np

np.random.seed(42)

N = 5000

# Group A (control): approval ~0.62, default ~0.11
group_a_approved = np.random.random(N) < 0.62
group_a_defaulted = np.random.random(N) < 0.11

# Group B (treatment): approval ~0.71, default ~0.09
group_b_approved = np.random.random(N) < 0.71
group_b_defaulted = np.random.random(N) < 0.09

# Continuous metrics with noise
group_a_loan_size = np.abs(np.random.normal(18500, 7500, N))
group_a_processing_time = np.abs(np.random.normal(6.4, 2.1, N))

group_b_loan_size = np.abs(np.random.normal(19200, 7800, N))
group_b_processing_time = np.abs(np.random.normal(5.9, 2.0, N))

# Apply defaults: only approved applications can default
group_a_defaulted = group_a_defaulted & group_a_approved
group_b_defaulted = group_b_defaulted & group_b_approved

def get_summary(group_approved, group_defaulted, group_loan_size, group_processing_time):
    n = len(group_approved)
    approval_rate = group_approved.mean()
    default_rate = group_defaulted.sum() / group_approved.sum()
    avg_loan_size = group_loan_size[group_approved].mean()
    avg_processing_time = group_processing_time[group_approved].mean()
    return {
        "n": n,
        "approval_rate": approval_rate,
        "default_rate": default_rate,
        "avg_loan_size": avg_loan_size,
        "avg_processing_time": avg_processing_time,
    }

group_a_summary = get_summary(group_a_approved, group_a_defaulted, group_a_loan_size, group_a_processing_time)
group_b_summary = get_summary(group_b_approved, group_b_defaulted, group_b_loan_size, group_b_processing_time)

if __name__ == "__main__":
    print("=== Group A (Control) ===")
    for k, v in group_a_summary.items():
        print(f"  {k}: {v:.4f}")

    print("\n=== Group B (Treatment) ===")
    for k, v in group_b_summary.items():
        print(f"  {k}: {v:.4f}")
"""Synthetic data generator for credit eligibility A/B test."""
import numpy as np

np.random.seed(42)

N = 5000

# Group A: control — current eligibility model
# Group B: treatment — new eligibility model

def generate_data():
    group_a_approved = np.random.binomial(N, 0.62)
    group_a_defaults = np.random.binomial(group_a_approved, 0.11)

    group_b_approved = np.random.binomial(N, 0.71)
    group_b_defaults = np.random.binomial(group_b_approved, 0.09)

    approval_rate_a = group_a_approved / N
    approval_rate_b = group_b_approved / N
    default_rate_a = group_a_defaults / group_a_approved if group_a_approved > 0 else 0
    default_rate_b = group_b_defaults / group_b_approved if group_b_approved > 0 else 0

    avg_loan_size_a = np.random.normal(18500, 4200, group_a_approved).mean()
    avg_loan_size_b = np.random.normal(19200, 4400, group_b_approved).mean()

    processing_time_a = np.random.normal(4.2, 1.1, N).mean()
    processing_time_b = np.random.normal(3.9, 1.0, N).mean()

    return {
        "group_a": {
            "approved": group_a_approved,
            "rejected": N - group_a_approved,
            "defaults": group_a_defaults,
            "approval_rate": approval_rate_a,
            "default_rate": default_rate_a,
            "avg_loan_size": avg_loan_size_a,
            "processing_time": processing_time_a,
        },
        "group_b": {
            "approved": group_b_approved,
            "rejected": N - group_b_approved,
            "defaults": group_b_defaults,
            "approval_rate": approval_rate_b,
            "default_rate": default_rate_b,
            "avg_loan_size": avg_loan_size_b,
            "processing_time": processing_time_b,
        },
    }

if __name__ == "__main__":
    data = generate_data()
    print("Group A (control):")
    print(f"  Approved: {data['group_a']['approved']}/{N} ({data['group_a']['approval_rate']:.4f})")
    print(f"  Default rate: {data['group_a']['default_rate']:.4f}")
    print(f"  Avg loan size: R{data['group_a']['avg_loan_size']:.2f}")
    print(f"  Processing time: {data['group_a']['processing_time']:.2f} hrs")
    print()
    print("Group B (treatment):")
    print(f"  Approved: {data['group_b']['approved']}/{N} ({data['group_b']['approval_rate']:.4f})")
    print(f"  Default rate: {data['group_b']['default_rate']:.4f}")
    print(f"  Avg loan size: R{data['group_b']['avg_loan_size']:.2f}")
    print(f"  Processing time: {data['group_b']['processing_time']:.2f} hrs")
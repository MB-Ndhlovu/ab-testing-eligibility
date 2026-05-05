"""Generate synthetic credit eligibility A/B test data."""

import numpy as np

def generate_data(n_total: int = 5000, seed: int = 42) -> dict:
    """Generate synthetic loan application data for A/B test.

    Args:
        n_total: Total number of applications (split evenly A/B).
        seed: Random seed for reproducibility.

    Returns:
        dict with arrays for each group and metric.
    """
    rng = np.random.default_rng(seed)
    n = n_total // 2

    # Group A (control): approval ~0.62, default ~0.11
    # Group B (treatment): approval ~0.71, default ~0.09
    group_a_approved = rng.binomial(1, 0.62, n)
    group_a_defaulted = (rng.binomial(1, 0.11, n) * group_a_approved)
    group_b_approved = rng.binomial(1, 0.71, n)
    group_b_defaulted = (rng.binomial(1, 0.09, n) * group_b_approved)

    # Loan sizes: log-normal, larger loans more likely to default
    mu, sigma = 9.5, 0.8
    group_a_loan_size = group_a_approved * np.exp(rng.normal(mu, sigma, n))
    group_b_loan_size = group_b_approved * np.exp(rng.normal(mu + 0.05, sigma, n))

    # Processing time in hours: right-skewed, add noise
    group_a_proc_time = rng.exponential(2.5, n) + rng.normal(0, 0.2, n)
    group_b_proc_time = rng.exponential(2.2, n) + rng.normal(0, 0.2, n)

    return {
        "group_a": {
            "approved": group_a_approved,
            "defaulted": group_a_defaulted,
            "loan_size": group_a_loan_size,
            "processing_time": np.clip(group_a_proc_time, 0.5, None),
        },
        "group_b": {
            "approved": group_b_approved,
            "defaulted": group_b_defaulted,
            "loan_size": group_b_loan_size,
            "processing_time": np.clip(group_b_proc_time, 0.5, None),
        },
        "n_per_group": n,
    }


def compute_group_stats(data: dict) -> dict:
    """Compute aggregate statistics per group."""
    stats = {}
    for group, d in [("A", data["group_a"]), ("B", data["group_b"])]:
        approved = d["approved"]
        defaulted = d["defaulted"]
        approved_sum = approved.sum()
        stats[group] = {
            "n": len(approved),
            "approval_rate": approved_sum / len(approved),
            "default_rate": defaulted.sum() / approved_sum if approved_sum > 0 else 0,
            "avg_loan_size": d["loan_size"][approved == 1].mean() if approved_sum > 0 else 0,
            "avg_processing_time": d["processing_time"].mean(),
        }
    return stats
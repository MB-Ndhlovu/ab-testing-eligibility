"""Generate synthetic loan applicant data for A/B test."""

import numpy as np

np.random.seed(42)

N_PER_GROUP = 2500

GROUP_A_APPROVAL_TARGET = 0.62
GROUP_A_DEFAULT_TARGET = 0.11
GROUP_B_APPROVAL_TARGET = 0.71
GROUP_B_DEFAULT_TARGET = 0.09


def generate_group(n: int, approval_target: float, default_target: float, seed_offset: int = 0) -> dict:
    """Generate loan applicant data for a group."""
    rng = np.random.RandomState(42 + seed_offset)

    approved = rng.random(n) < approval_target

    loan_sizes = np.zeros(n)
    for i in range(n):
        bucket = rng.random()
        if bucket < 0.5:
            loan_sizes[i] = rng.uniform(5000, 20000)
        elif bucket < 0.85:
            loan_sizes[i] = rng.uniform(20000, 100000)
        else:
            loan_sizes[i] = rng.uniform(100000, 500000)

    defaulted = rng.random(n) < (default_target + rng.normal(0, 0.015))
    defaulted = np.clip(defaulted, 0, 1)

    processing_times = rng.exponential(2.5, n) + rng.uniform(0.5, 4, n)

    return {
        'approved': approved,
        'loan_size': loan_sizes,
        'defaulted': defaulted,
        'processing_time': processing_times
    }


def compute_metrics(data: dict) -> dict:
    """Compute aggregate metrics from group data."""
    approved_mask = data['approved']
    n_total = len(data['approved'])
    n_approved = int(approved_mask.sum())

    default_rate = float(data['defaulted'][approved_mask].mean()) if n_approved > 0 else 0.0
    avg_loan = float(data['loan_size'][approved_mask].mean()) if n_approved > 0 else 0.0

    return {
        'n': n_total,
        'approval_rate': float(approved_mask.mean()),
        'default_rate': default_rate,
        'avg_loan_size': avg_loan,
        'avg_processing_time': float(data['processing_time'].mean())
    }


def generate_all_data():
    """Generate both groups and return metrics."""
    group_a_data = generate_group(N_PER_GROUP, GROUP_A_APPROVAL_TARGET, GROUP_A_DEFAULT_TARGET, seed_offset=0)
    group_b_data = generate_group(N_PER_GROUP, GROUP_B_APPROVAL_TARGET, GROUP_B_DEFAULT_TARGET, seed_offset=1)

    metrics_a = compute_metrics(group_a_data)
    metrics_b = compute_metrics(group_b_data)

    return metrics_a, metrics_b


if __name__ == '__main__':
    ma, mb = generate_all_data()
    print("Group A metrics:", ma)
    print("Group B metrics:", mb)
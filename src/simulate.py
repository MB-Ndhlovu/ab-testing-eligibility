import json
from src.data_generator import generate_credit_data, compute_group_stats
from src.statistical import analyze_metric


def run_simulation(seed=42):
    df = generate_credit_data(n=5000, seed=seed)
    stats = compute_group_stats(df)

    approval_result = analyze_metric(
        "approval_rate",
        n_a=stats["A"]["n"],
        rate_a=stats["A"]["approval_rate"],
        n_b=stats["B"]["n"],
        rate_b=stats["B"]["approval_rate"],
    )

    default_result = analyze_metric(
        "default_rate",
        n_a=stats["A"]["n"],
        rate_a=stats["A"]["default_rate"],
        n_b=stats["B"]["n"],
        rate_b=stats["B"]["default_rate"],
    )

    return {
        "group_stats": stats,
        "approval_rate_test": approval_result,
        "default_rate_test": default_result,
        "sample_size": 5000,
    }
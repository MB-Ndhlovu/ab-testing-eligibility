"""Run the A/B experiment simulation."""

import json
from src.data_generator import generate_data, compute_group_metrics
from src.statistical import two_proportion_ztest


def run_simulation(seed: int = 42) -> dict:
    """Run the full A/B experiment pipeline.

    Args:
        seed: Random seed for data generation.

    Returns:
        dict containing raw data, metrics, and statistical results.
    """
    df = generate_data(n=5000, seed=seed)

    metrics = compute_group_metrics(df)

    # Two-proportion z-test for approval rate
    approval_results = two_proportion_ztest(
        n_A=metrics["A"]["n"],
        x_A=int(metrics["A"]["approval_rate"] * metrics["A"]["n"]),
        n_B=metrics["B"]["n"],
        x_B=int(metrics["B"]["approval_rate"] * metrics["B"]["n"]),
    )

    # Two-proportion z-test for default rate
    default_results = two_proportion_ztest(
        n_A=metrics["A"]["n"],
        x_A=int(metrics["A"]["default_rate"] * metrics["A"]["n"]),
        n_B=metrics["B"]["n"],
        x_B=int(metrics["B"]["default_rate"] * metrics["B"]["n"]),
    )

    return {
        "data": df.to_dict(orient="records"),
        "metrics": metrics,
        "approval_test": approval_results,
        "default_test": default_results,
    }
from src.data_generator import generate_data, compute_group_stats
from src.statistical import test_metric

def run_simulation(n=5000, seed=42):
    df = generate_data(n=n, seed=seed)
    stats = compute_group_stats(df)

    n_a = stats["A"]["n"]
    n_b = stats["B"]["n"]

    approval_result = test_metric(
        "approval_rate",
        n_a, stats["A"]["approval_rate"],
        n_b, stats["B"]["approval_rate"],
    )

    default_result = test_metric(
        "default_rate",
        n_a, stats["A"]["default_rate"],
        n_b, stats["B"]["default_rate"],
    )

    return {
        "group_stats": stats,
        "approval_rate_test": approval_result,
        "default_rate_test": default_result,
        "seed": seed,
        "n": n,
    }

if __name__ == "__main__":
    result = run_simulation()
    print(result)
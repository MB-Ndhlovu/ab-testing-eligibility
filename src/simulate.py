from src.data_generator import generate_data
from src.statistical import test_metric

def run_simulation(n=5000, alpha=0.05):
    data = generate_data()
    n_a = n // 2
    n_b = n // 2

    approval_result = test_metric(
        data["group_a"], data["group_b"], "approval_rate", n_a, n_b, alpha
    )
    default_result = test_metric(
        data["group_a"], data["group_b"], "default_rate", n_a, n_b, alpha
    )

    summary = {
        "n_total": n,
        "n_group_a": n_a,
        "n_group_b": n_b,
        "alpha": alpha,
        "group_a": {
            "approval_rate": round(data["group_a"]["approval_rate"], 4),
            "default_rate": round(data["group_a"]["default_rate"], 4),
            "avg_loan_size": round(data["group_a"]["avg_loan_size"], 2),
            "avg_processing_time": round(data["group_a"]["avg_processing_time"], 2),
        },
        "group_b": {
            "approval_rate": round(data["group_b"]["approval_rate"], 4),
            "default_rate": round(data["group_b"]["default_rate"], 4),
            "avg_loan_size": round(data["group_b"]["avg_loan_size"], 2),
            "avg_processing_time": round(data["group_b"]["avg_processing_time"], 2),
        },
        "tests": {
            "approval_rate": approval_result,
            "default_rate": default_result,
        },
    }
    return summary

if __name__ == "__main__":
    result = run_simulation()
    print(result)
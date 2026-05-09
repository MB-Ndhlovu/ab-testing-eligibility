"""Run experiment simulation and compute treatment effects."""
from .data_generator import generate_data
from .statistical import test_metric

def run_simulation():
    data = generate_data()

    N = 5000
    approved_a = data["group_a"]["approved"]
    approved_b = data["group_b"]["approved"]
    defaults_a = data["group_a"]["defaults"]
    defaults_b = data["group_b"]["defaults"]

    approval_result = test_metric(N, approved_a, N, approved_b, "approval_rate", higher_is_better=True)
    default_result = test_metric(N, defaults_a, N, defaults_b, "default_rate", higher_is_better=False)

    results = {
        "sample_size": N,
        "group_a": data["group_a"],
        "group_b": data["group_b"],
        "approval_rate_test": approval_result,
        "default_rate_test": default_result,
    }

    return results

if __name__ == "__main__":
    r = run_simulation()
    print("=== Approval Rate Test ===")
    print(r["approval_rate_test"])
    print()
    print("=== Default Rate Test ===")
    print(r["default_rate_test"])
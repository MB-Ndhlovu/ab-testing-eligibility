import json
from src.simulate import run_simulation
from src.report import generate_report

def main():
    results = run_simulation(n=5000, alpha=0.05)
    results["tests"]["approval_rate"]["significant"] = bool(results["tests"]["approval_rate"]["significant"])
    results["tests"]["default_rate"]["significant"] = bool(results["tests"]["default_rate"]["significant"])
    report = generate_report(results)

    print(report)
    print()

    output_path = "/home/workspace/Projects/ab-testing-eligibility/results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"Results saved to {output_path}")

    return results

if __name__ == "__main__":
    main()
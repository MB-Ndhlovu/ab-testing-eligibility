import json
from src.simulate import run_simulation
from src.report import generate_report

def main():
    print("Running A/B test pipeline...")
    results = run_simulation(n=5000, seed=42)

    report = generate_report(results)
    print(report)

    with open("/home/workspace/Projects/ab-testing-eligibility/results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("\nResults saved to results.json")
    return results

if __name__ == "__main__":
    main()
import json
from src.data_generator import generate_credit_data
from src.simulate import run_experiment
from src.report import generate_report


def main():
    print("Generating synthetic credit eligibility data...")
    df = generate_credit_data(n=5000, seed=42)

    print("Running A/B experiment simulation...")
    results = run_experiment(df, alpha=0.05)

    print("\n" + generate_report(results))

    output_path = "/home/workspace/Projects/ab-testing-eligibility/results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=lambda o: float(o) if hasattr(o, 'item') else o)

    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    main()
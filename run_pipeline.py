"""Execute the full A/B test pipeline."""
import json
from src.data_generator import group_a_summary, group_b_summary
from src.simulate import run_simulation
from src.report import format_results, save_json

def main():
    print("Generating data...")
    from src import data_generator
    print(f"  Group A: n={group_a_summary['n']}, approval={group_a_summary['approval_rate']:.4f}, default={group_a_summary['default_rate']:.4f}")
    print(f"  Group B: n={group_b_summary['n']}, approval={group_b_summary['approval_rate']:.4f}, default={group_b_summary['default_rate']:.4f}")

    print("\nRunning simulation...")
    results = run_simulation()

    print("\n" + format_results(results))

    output_path = "/home/workspace/Projects/ab-testing-eligibility/results.json"
    save_json(results, output_path)
    print(f"\nResults saved to {output_path}")

if __name__ == "__main__":
    main()
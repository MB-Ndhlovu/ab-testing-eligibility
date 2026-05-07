"""Execute the full A/B test pipeline and save results."""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.simulate import run_simulation, compute_treatment_effects
from src.report import generate_summary_report, results_to_json

def save_json_results(results, filepath='results.json'):
    """Save results to JSON file."""
    with open(filepath, 'w') as f:
        json.dump(results_to_json(results), f, indent=2)
    print(f"\nResults saved to: {filepath}")

def main():
    print("Running A/B Test Pipeline...")
    print("-" * 40)
    
    # Run simulation
    results = run_simulation()
    
    # Compute treatment effects
    effects = compute_treatment_effects(results)
    
    # Generate and print report
    report = generate_summary_report(results)
    print(report)
    
    # Save results
    save_json_results(results)
    
    # Print treatment effects summary
    print("\nTREATMENT EFFECTS SUMMARY")
    print("-" * 40)
    print(f"  Approval Rate Lift: +{effects['approval_rate_lift']:.4f} ({effects['approval_rate_lift_pct']:.2f}%)")
    print(f"  Default Rate Change: {effects['default_rate_change']:.4f} ({effects['default_rate_change_pct']:.2f}%)")
    
    return results

if __name__ == '__main__':
    results = main()
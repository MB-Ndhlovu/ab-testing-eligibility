"""
Execute full A/B test pipeline.
"""

import json
from src.simulate import run_simulation
from src.report import generate_report

def main():
    print("Running A/B Test Pipeline...")
    print()
    
    results = run_simulation(seed=42, alpha=0.05)
    
    report = generate_report(results)
    print(report)
    
    # Save JSON
    output_path = "/home/workspace/Projects/ab-testing-eligibility/results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to: {output_path}")
    
    return results

if __name__ == "__main__":
    main()
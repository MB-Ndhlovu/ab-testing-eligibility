import json
import sys
import numpy as np
from src.simulate import run_simulation
from src.report import generate_report

def convert_types(obj):
    if isinstance(obj, dict):
        return {k: convert_types(v) for k, v in obj.items()}
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    return obj

def main():
    print("Running A/B test simulation...\n")
    results = run_simulation(seed=42)
    report = generate_report(results)
    print(report)

    results_clean = convert_types(results)
    with open('/home/workspace/Projects/ab-testing-eligibility/results.json', 'w') as f:
        json.dump(results_clean, f, indent=2)
    print("\nResults saved to results.json")

    return report, results_clean

if __name__ == '__main__':
    main()
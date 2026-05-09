import json
import numpy as np
from src.simulate import run_experiment
from src.report import generate_report

def make_serializable(obj):
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [make_serializable(v) for v in obj]
    elif isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    elif isinstance(obj, (np.integer, int)):
        return int(obj)
    elif isinstance(obj, (np.floating, float)):
        return float(obj)
    else:
        return obj

def main():
    print("Running A/B Test Experiment...")
    print("")
    results = run_experiment()

    report = generate_report(results)
    print(report)

    serializable = make_serializable(results)
    output_path = "/home/workspace/Projects/ab-testing-eligibility/results.json"
    with open(output_path, "w") as f:
        json.dump(serializable, f, indent=2)

    print(f"\nResults saved to: {output_path}")
    return results

if __name__ == "__main__":
    main()
"""Execute full A/B test pipeline."""
import json
import sys
import numpy as np
sys.path.insert(0, "/home/workspace/Projects/ab-testing-eligibility")

from src.simulate import run_simulation
from src.report import generate_report

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, (np.integer, np.floating)):
            return obj.item()
        return super().default(obj)

def main():
    print("Running A/B Test Pipeline...")
    print()

    results = run_simulation()

    print()
    report = generate_report(results)
    print()

    output_path = "/home/workspace/Projects/ab-testing-eligibility/results.json"
    with open(output_path, "w") as f:
        json.dump(results, f, indent=2, cls=NumpyEncoder)
    print(f"[Results JSON saved to {output_path}]")

    return results

if __name__ == "__main__":
    main()
import json
import sys
import numpy as np
sys.path.insert(0, "/home/workspace/Projects/ab-testing-eligibility")

from src.simulate import run_simulation
from src.report import generate_report

def main():
    print("Running A/B test simulation...\n")
    results = run_simulation()
    report = generate_report(results)
    print(report)

    out_path = "/home/workspace/Projects/ab-testing-eligibility/results.json"
    json_data = json.dumps(results, indent=2, default=float)
    with open(out_path, "w") as f:
        f.write(json_data)

    print(f"\nResults saved to {out_path}")
    return report, results

if __name__ == "__main__":
    main()
import json
import sys
sys.path.insert(0, "/home/workspace/Projects/ab-testing-eligibility")

from src.data_generator import df
from src.simulate import run_simulation
from src.report import generate_report

def main():
    results = run_simulation(df)
    report = generate_report(results)

    with open("/home/workspace/Projects/ab-testing-eligibility/results.json", "w") as f:
        json.dump(results, f, indent=2, default=lambda x: float(x) if hasattr(x, "item") else list(x) if isinstance(x, tuple) else x)

    print("\n[Pipeline complete] results saved to results.json")
    return results, report

if __name__ == "__main__":
    main()
"""Execute the full A/B testing pipeline."""

import json
import numpy as np
from src.simulate import run_simulation
from src.report import generate_report


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)


def main():
    print("Running A/B Test Simulation...")
    print("")

    results = run_simulation(n=5000, seed=42)

    report = generate_report(results)
    print(report)

    with open("results.json", "w") as f:
        json.dump(results, f, indent=2, cls=NumpyEncoder)

    print("Results saved to results.json")

    return results


if __name__ == "__main__":
    main()
import json
import sys
import os
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))

from src.simulate import run_simulation
from src.report import generate_report

def make_serializable(obj):
    """Convert numpy types for JSON serialization."""
    if isinstance(obj, (np.floating, float)):
        return float(obj)
    if isinstance(obj, (np.integer, int)):
        return int(obj)
    if isinstance(obj, (np.bool_, bool)):
        return bool(obj)
    if isinstance(obj, tuple):
        return list(obj)
    if isinstance(obj, dict):
        return {k: make_serializable(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [make_serializable(x) for x in obj]
    return obj

if __name__ == '__main__':
    print("Running A/B Test Pipeline...")
    print("=" * 60)

    results = run_simulation(seed=42, alpha=0.05)
    report = generate_report(results)

    print(report)

    output_path = os.path.join(os.path.dirname(__file__), 'results.json')
    with open(output_path, 'w') as f:
        json.dump(make_serializable(results), f, indent=2)

    print(f"\nResults saved to: {output_path}")
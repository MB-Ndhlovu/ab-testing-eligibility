#!/usr/bin/env python3
"""
A/B Testing Framework for Credit Eligibility — Pipeline Runner

Executes the full pipeline: generate data, run experiment, produce report, save JSON.
"""

import json
import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.simulate import run_experiment
from src.report import print_report


def save_json(results: dict, path: str) -> None:
    """Serialize results to JSON (convert numpy types for JSON compatibility)."""
    def default_serializer(obj):
        import numpy as np
        if isinstance(obj, np.bool_):
            return bool(obj)
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        raise TypeError(f"Object of type {type(obj)} is not JSON serializable")

    with open(path, 'w') as f:
        json.dump(results, f, indent=2, default=default_serializer)


def main():
    print("Running A/B Test Pipeline...\n")

    # Run experiment
    results = run_experiment(n=5000, seed=42)

    # Print human-readable report
    print_report(results)

    # Save JSON output
    output_dir = Path(__file__).parent
    json_path = output_dir / "results.json"
    save_json(results, str(json_path))
    print(f"\nResults saved to: {json_path}")

    return results


if __name__ == '__main__':
    main()
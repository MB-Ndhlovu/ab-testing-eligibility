import json
import os
from src.simulate import run_simulation
from src.report import generate_report

def main():
    print("Running A/B Test Pipeline...")
    print("")

    results = run_simulation()
    report = generate_report(results)

    print(report)

    # Save JSON
    output_path = os.path.join(os.path.dirname(__file__), 'results.json')
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2, default=float)

    print("")
    print(f"Results saved to: {output_path}")

if __name__ == "__main__":
    main()
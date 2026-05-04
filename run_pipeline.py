import json
from src.simulate import run_simulation
from src.report import generate_report

def main():
    print("Running A/B Test Simulation...")
    results = run_simulation(n=5000, alpha=0.05)
    
    report = generate_report(results)
    print(report)
    
    with open('/home/workspace/Projects/ab-testing-eligibility/results.json', 'w') as f:
        json.dump(results, f, indent=2, default=float)
    
    print("\nResults saved to results.json")
    return results

if __name__ == '__main__':
    main()
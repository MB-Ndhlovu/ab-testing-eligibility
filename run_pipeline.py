import os
from src.simulate import run_simulation
from src.report import generate_report, save_json

def main():
    results = run_simulation(seed=42)
    
    report = generate_report(results)
    print(report)
    
    out_path = os.path.join(os.path.dirname(__file__), 'results.json')
    save_json(results, out_path)
    print(f"\nResults saved to: {out_path}")
    
    return results

if __name__ == '__main__':
    main()
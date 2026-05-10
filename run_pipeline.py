import json
from src.simulate import run_experiment
from src.report import generate_report

def main():
    print("Running A/B Test Pipeline...")
    print()
    
    results = run_experiment(seed=42)
    
    report = generate_report(results)
    print(report)
    
    # Save JSON results
    with open('/home/workspace/Projects/ab-testing-eligibility/results.json', 'w') as f:
        # Convert numpy types to native Python for JSON serialization
        def convert(obj):
            if hasattr(obj, 'item'):
                return obj.item()
            return obj
        
        json_results = {}
        for k, v in results.items():
            if isinstance(v, dict):
                json_results[k] = {kk: convert(vv) for kk, vv in v.items()}
            else:
                json_results[k] = convert(v)
        
        json.dump(json_results, f, indent=2, default=str)
    
    print("\n💾 Results saved to results.json")
    
    return results

if __name__ == '__main__':
    main()
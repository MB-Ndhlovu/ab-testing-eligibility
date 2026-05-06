"""Execute the full A/B testing pipeline."""

from src.simulate import run as run_experiment
from src.report import print_and_save


def main():
    print("Running A/B experiment simulation...\n")
    results = run_experiment()
    report = print_and_save(results, "results.json")
    return results


if __name__ == "__main__":
    main()
# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (Group B) performs better than the current model (Group A). The key metrics are:

- **Approval Rate**: Higher is better (more loans approved)
- **Default Rate**: Lower is better (fewer loans defaulting)

## Methodology

We conduct a randomised A/B experiment:

1. **Control (Group A)**: Current eligibility model
2. **Treatment (Group B)**: New eligibility model

Each applicant is randomly assigned to either group, and their outcome (approved/denied, defaulted/not defaulted) is simulated based on group-specific probabilities with realistic noise added.

We use a **two-proportion z-test** to determine whether the observed differences are statistically significant at α = 0.05.

## Metrics Analysed

| Metric | Group A (Control) | Group B (Treatment) | Expected Direction |
|---|---|---|---|
| Approval Rate | ~62% | ~71% | B higher |
| Default Rate | ~11% | ~9% | B lower |

## Files

- `src/data_generator.py` — Generates 5 000 synthetic loan applications
- `src/statistical.py` — Two-proportion z-test, confidence intervals, power analysis
- `src/simulate.py` — Runs the experiment and computes treatment effects
- `src/report.py` — Produces a human-readable summary
- `run_pipeline.py` — Orchestrates the full pipeline
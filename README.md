# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test a new credit eligibility model against their current model. The goal is to determine whether the new model improves key business metrics — specifically approval rate and default rate — without introducing unacceptable risk.

- **Group A (Control)**: Current eligibility model
- **Group B (Treatment)**: New eligibility model

The new model is expected to be slightly better on both metrics: higher approval rate (more loans originated) and lower default rate (less credit risk).

## Methodology

1. **Data Generation**: Simulate 5,000 loan applications split evenly between control (A) and treatment (B) groups
2. **Outcome Simulation**: Each applicant receives a simulated outcome — approved/denied, default/no default, loan size, processing time
3. **Statistical Testing**: Two-proportion z-test for each metric, comparing groups A and B
4. **Reporting**: Confidence intervals, p-values, and statistical significance at α = 0.05

## Key Metrics

| Metric | Group A (Control) | Group B (Treatment) |
|--------|-------------------|---------------------|
| Approval Rate | ~62% | ~71% |
| Default Rate | ~11% | ~9% |

## Files

- `src/data_generator.py` — Synthetic data generation (5,000 rows, A/B split)
- `src/statistical.py` — Two-proportion z-test, CI, power analysis
- `src/simulate.py` — Experiment runner and treatment effect computation
- `src/report.py` — Formatted summary report
- `run_pipeline.py` — End-to-end execution script
- `requirements.txt` — Dependencies
# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test a new credit eligibility model against their current model. The new model (Group B) is hypothesized to:
- Increase approval rates (approve more worthy applicants)
- Decrease default rates (better at identifying risky borrowers)

We run a controlled A/B experiment to determine if the new model (treatment) outperforms the current model (control).

## Methodology

1. **Data Generation**: Simulate 5,000 loan applications split evenly between control (Group A) and treatment (Group B)
2. **Metrics Tracked**:
   - Approval Rate (primary)
   - Default Rate (primary)
   - Average Loan Size
   - Processing Time
3. **Statistical Testing**: Two-proportion z-test for each binary metric
4. **Reporting**: Full summary with z-statistics, p-values, 95% confidence intervals, and statistical conclusions

## Files

- `src/data_generator.py` — Synthetic data generation
- `src/statistical.py` — Statistical tests (z-test, CI, power, MDE)
- `src/simulate.py` — Experiment simulation and treatment effect computation
- `src/report.py` — Human-readable summary report
- `run_pipeline.py` — Orchestrates the full pipeline
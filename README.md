# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a **new credit eligibility model (Group B)** performs better than their **current model (Group A)**. The goal is to make data-driven decisions about adopting the new model by testing it on a sample of loan applications.

## Key Metrics

| Metric | Group A (Control) | Group B (Treatment) | Desired Direction |
|---|---|---|---|
| Approval Rate | ~62% | ~71% | Higher is better |
| Default Rate | ~11% | ~9% | Lower is better |
| Avg Loan Size | Simulated | Simulated | Contextual |
| Processing Time | Simulated | Simulated | Lower is better |

## Methodology

1. **Data Generation**: Simulate 5,000 loan applications split evenly between control and treatment groups with realistic noise.
2. **Statistical Testing**: Two-proportion z-tests for approval rate and default rate.
3. **Confidence Intervals**: 95% CI for the difference between group proportions.
4. **Power Analysis**: Evaluate statistical power and minimum detectable effect.
5. **Reporting**: Human-readable summary with actionable conclusions.

## Files

- `src/data_generator.py` — Generate synthetic loan application data
- `src/statistical.py` — Z-test, confidence intervals, power calculations
- `src/simulate.py` — Run experiment simulation
- `src/report.py` — Generate summary report
- `run_pipeline.py` — Execute full pipeline
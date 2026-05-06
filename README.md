# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (treatment group B) outperforms their current model (control group A). The key metrics are:

- **Approval Rate**: Higher is better — more loans approved
- **Default Rate**: Lower is better — fewer loans that go bad

## Methodology

1. **Synthetic Data Generation**: Simulate 5,000 loan applications split evenly between control (A) and treatment (B) groups
2. **Statistical Testing**: Two-proportion z-test for each metric
3. **Confidence Intervals**: 95% CI for the difference between groups
4. **Power Analysis**: Minimum detectable effect at 80% power

## Expected Outcomes

| Metric | Group A (Control) | Group B (Treatment) | Expected Effect |
|--------|-------------------|---------------------|------------------|
| Approval Rate | ~62% | ~71% | +9 pp |
| Default Rate | ~11% | ~9% | -2 pp |

## Files

- `src/data_generator.py` — Generate synthetic loan data
- `src/statistical.py` — Two-proportion z-test and power analysis
- `src/simulate.py` — Run experiment simulation
- `src/report.py` — Generate human-readable summary
- `run_pipeline.py` — Execute full pipeline
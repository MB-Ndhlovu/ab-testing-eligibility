# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (Group B) outperforms their current model (Group A). The key metrics are:

- **Approval Rate**: Higher is better (more loans originated)
- **Default Rate**: Lower is better (fewer losses)

## Methodology

1. **Generate synthetic data** for 5,000 applicants split evenly between Group A (control) and Group B (treatment)
2. **Simulate outcomes** using realistic base rates with added noise
3. **Run two-proportion z-tests** for each metric at α = 0.05
4. **Report** z-statistic, p-value, 95% CI, and statistical conclusion

## Expected Outcomes

| Metric | Group A (Control) | Group B (Treatment) |
|--------|-------------------|----------------------|
| Approval Rate | ~62% | ~71% |
| Default Rate | ~11% | ~9% |

## Files

- `src/data_generator.py` — Synthetic data generation
- `src/statistical.py` — Two-proportion z-test implementation
- `src/simulate.py` — Experiment simulation
- `src/report.py` — Summary report generation
- `run_pipeline.py` — Execute full pipeline
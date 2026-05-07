# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) outperforms their current model (Group A). The new model is expected to:
- Increase approval rates (approve more creditworthy applicants)
- Reduce default rates (better risk selection)

## Objective

Run a controlled A/B experiment to determine if the differences in approval rate and default rate between the two models are statistically significant at α = 0.05.

## Methodology

### Data Generation
- 5,000 synthetic applicants split evenly: 2,500 in Group A (control) and 2,500 in Group B (treatment)
- Group A (current model): approval_rate ≈ 0.62, default_rate ≈ 0.11
- Group B (new model): approval_rate ≈ 0.71, default_rate ≈ 0.09
- Realistic noise added via Bernoulli trials with specified probabilities

### Statistical Testing
Two-proportion z-test for each metric:
- **Approval Rate**: Tests whether the new model approves a significantly higher proportion of applicants
- **Default Rate**: Tests whether the new model achieves a significantly lower default rate

### Metrics Reported
For each metric:
- Observed rates for both groups
- Z-statistic
- Two-tailed p-value
- 95% confidence interval for the difference
- Statistical conclusion (significant / not significant)

## Files

- `src/data_generator.py` — Generates synthetic loan applicant data
- `src/statistical.py` — Two-proportion z-test, confidence intervals, power analysis
- `src/simulate.py` — Runs experiment simulation and computes treatment effects
- `src/report.py` — Generates a readable summary report
- `run_pipeline.py` — Executes the full pipeline end-to-end
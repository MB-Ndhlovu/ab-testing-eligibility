# A/B Testing Framework for Credit Eligibility

## Business Problem
A lender wants to test a new credit eligibility model (Group B) against their current model (Group A). The goal is to determine whether the new model improves approval rates and reduces default rates without introducing unacceptable risk.

## Methodology

### Experimental Design
- **Control Group (A)**: Current eligibility model with approval rate ~62% and default rate ~11%
- **Treatment Group (B)**: New eligibility model with approval rate ~71% and default rate ~9%
- **Sample Size**: 5,000 applicants (2,500 per group)
- **Key Metrics**: approval_rate, default_rate, avg_loan_size, processing_time

### Statistical Approach
Two-proportion z-test for each binary metric (approval_rate, default_rate):

1. **Null Hypothesis (H₀)**: No difference between Group A and Group B proportions
2. **Alternative Hypothesis (H₁)**: There is a difference between groups
3. **Significance Level**: α = 0.05
4. **Test Statistic**: Two-proportion z-test

### Reported Metrics
- z-statistic
- p-value (two-tailed)
- 95% Confidence Interval for the difference
- Statistical conclusion (significant / not significant)

## Files
- `src/data_generator.py` — Synthetic loan applicant data generation
- `src/statistical.py` — Two-proportion z-test, confidence intervals, power analysis
- `src/simulate.py` — Experiment simulation and treatment effect computation
- `src/report.py` — Human-readable summary report
- `run_pipeline.py` — End-to-end pipeline execution

## Usage
```bash
python run_pipeline.py
```

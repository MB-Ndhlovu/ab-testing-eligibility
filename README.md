# A/B Testing Framework for Credit Eligibility

## Business Problem
A lender wants to test a new credit eligibility model (Group B) against their current model (Group A). The goal is to determine whether the new model improves approval rates and reduces default rates without introducing statistical false positives.

## Methodology
- Generate synthetic data for 5,000 loan applicants split evenly into control (A) and treatment (B) groups
- Group A uses current eligibility rules: ~62% approval rate, ~11% default rate
- Group B uses new eligibility rules: ~71% approval rate, ~9% default rate
- Apply two-proportion z-test for each metric to detect statistically significant differences
- Report z-statistic, p-value, 95% confidence interval, and statistical conclusion at α=0.05

## Metrics
| Metric | Group A (Control) | Group B (Treatment) |
|---|---|---|
| Approval Rate | ~62% | ~71% |
| Default Rate | ~11% | ~9% |

## Files
- `src/data_generator.py` — Synthetic loan applicant data generation
- `src/statistical.py` — Two-proportion z-test, confidence intervals, power analysis
- `src/simulate.py` — Experiment runner and treatment effect computation
- `src/report.py` — Human-readable summary report
- `run_pipeline.py` — End-to-end pipeline execution
# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test a new credit eligibility model (Group B) against their current model (Group A). The goal is to determine whether the new model improves key business metrics — specifically **approval rate** and **default rate** — without increasing financial risk.

## Current State

- **Group A (Control):** Current eligibility model
  - Approval rate: ~62%
  - Default rate: ~11%
  - Avg loan size: $12,000–$18,000
  - Processing time: 3–7 days

- **Group B (Treatment):** New eligibility model
  - Target approval rate: ~71% (higher approvals)
  - Target default rate: ~9% (lower defaults)
  - Avg loan size: $13,000–$20,000
  - Processing time: 2–5 days

## Methodology

### Data Generation
- 5,000 synthetic loan applications split evenly between groups A and B (2,500 each)
- Realistic noise added to simulate real-world variance
- Each record includes: application_id, group, outcome (approved/denied), default flag, loan_size, processing_days

### Statistical Testing
A **two-proportion z-test** is used for each metric:

1. **Approval Rate** — Testing if the new model approves more loans
2. **Default Rate** — Testing if the new model has fewer defaults

For each test we compute:
- Observed proportions for each group
- Pooled proportion under null hypothesis
- Z-statistic
- Two-tailed p-value
- 95% Confidence Interval for the difference
- Statistical conclusion at α = 0.05

### Minimum Detectable Effect (MDE)
For a two-proportion z-test with:
- α = 0.05 (two-tailed)
- Power = 80%
- Baseline proportion (pA)
- Treatment proportion (pB)

The MDE tells us the smallest effect size the test can reliably detect given the sample size.

## Success Criteria

| Metric | Group A | Group B | Direction |
|--------|---------|---------|-----------|
| Approval Rate | ~62% | ~71% | ↑ Better |
| Default Rate | ~11% | ~9% | ↓ Better |

A result is **statistically significant** if p-value < 0.05, meaning we can reject the null hypothesis that the models perform identically.
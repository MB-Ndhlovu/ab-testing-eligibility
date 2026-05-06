# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender currently uses a credit eligibility model (Group A — control). They want to test a new model (Group B — treatment) that is expected to:
- Increase approval rates (approve more borrowers responsibly)
- Decrease default rates (better risk selection)

The goal is to run a statistically rigorous A/B experiment to determine whether the new model genuinely outperforms the current one, or if observed differences are just noise.

## Methodology

### Data Generation
- Synthetic dataset of 5,000 loan applications (2,500 per group)
- **Group A (Control)**: Existing eligibility model
  - Target approval rate: ~62%
  - Target default rate: ~11%
- **Group B (Treatment)**: New eligibility model
  - Target approval rate: ~71%
  - Target default rate: ~9%
- Realistic noise added so results are not perfectly clean

### Metrics Tracked per Group
| Metric | Description |
|---|---|
| Approval Rate | Proportion of applications approved |
| Default Rate | Proportion of approved loans that defaulted |
| Avg Loan Size | Mean approved loan amount |
| Processing Time | Mean days to process applications |

### Statistical Testing
- **Two-Proportion Z-Test** for approval_rate and default_rate
- **95% Confidence Interval** for the difference between groups
- **P-value** against α = 0.05
- **Statistical Power** calculation
- **Minimum Detectable Effect (MDE)** estimation

### Decision Rule
At α = 0.05:
- **p < 0.05**: Reject null hypothesis → statistically significant difference
- **p ≥ 0.05**: Fail to reject null hypothesis → no statistically significant difference
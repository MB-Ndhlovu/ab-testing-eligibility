# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test a new credit eligibility model against their current model. The new model (Group B) should:
- Approve more applicants (higher approval rate)
- Reduce defaults (lower default rate)

We run a controlled A/B experiment to determine if the new model is statistically superior.

## Methodology

1. **Data Generation**: Simulate 5,000 loan applications split evenly between control (A) and treatment (B)
2. **Metrics Tracked**:
   - Approval Rate: proportion of applicants approved
   - Default Rate: proportion of approved loans that go into default
   - Average Loan Size
   - Processing Time
3. **Statistical Test**: Two-proportion z-test for approval and default rates
4. **Reporting**: 95% confidence intervals, p-values, and statistical conclusions

## Hypotheses

- **Approval Rate**: H₀: p_B ≤ p_A vs H₁: p_B > p_A (one-sided)
- **Default Rate**: H₀: p_B ≥ p_A vs H₁: p_B < p_A (one-sided)
- **Significance Level**: α = 0.05
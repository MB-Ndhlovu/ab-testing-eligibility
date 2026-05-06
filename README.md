# A/B Testing Framework for Credit Eligibility

## Business Problem
A lender wants to test a new credit eligibility model (Group B) against their current model (Group A). The goal is to determine whether the new model improves key business metrics without increasing default risk.

## Key Metrics
- **Approval Rate**: Proportion of loan applications approved
- **Default Rate**: Proportion of approved loans that go into default
- **Average Loan Size**: Mean approved loan amount
- **Processing Time**: Average time to process applications

## Methodology
1. **Data Generation**: Simulate 5,000 loan applications split evenly between control (A) and treatment (B)
2. **Statistical Testing**: Two-proportion z-test for approval and default rates
3. **Confidence Intervals**: 95% CI for the difference in proportions
4. **Power Analysis**: Determine minimum detectable effect at 80% power

## Hypotheses
- **Approval Rate**: H₀: p_B ≤ p_A vs H₁: p_B > p_A (one-tailed)
- **Default Rate**: H₀: p_B ≥ p_A vs H₁: p_B < p_A (one-tailed, we want lower defaults)

## Success Criteria
- α = 0.05 significance level
- New model should improve approval rate without increasing default rate
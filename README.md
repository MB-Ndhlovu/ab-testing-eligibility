# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate a new credit eligibility model against the current model before full deployment. The new model (Group B) is expected to improve approval rates while reducing default rates compared to the current model (Group A).

## Methodology

### Experiment Design
- **Control Group (A)**: Current eligibility model
- **Treatment Group (B)**: New eligibility model
- **Sample Size**: 5,000 applicants (2,500 per group)

### Key Metrics
1. **Approval Rate**: Proportion of applicants approved
2. **Default Rate**: Proportion of approved loans that default
3. **Average Loan Size**: Mean loan amount approved
4. **Processing Time**: Average time to process applications

### Statistical Approach
- Two-proportion z-test for approval and default rates
- 95% Confidence Intervals for treatment effects
- Statistical significance at α = 0.05
- Power analysis for minimum detectable effects

## Expected Outcomes
- Group A (Control): ~62% approval rate, ~11% default rate
- Group B (Treatment): ~71% approval rate, ~9% default rate
- Realistic noise added to avoid perfectly clean results
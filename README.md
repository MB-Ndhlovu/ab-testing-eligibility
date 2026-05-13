# A/B Testing Framework for Credit Eligibility

## Business Problem
A lender wants to test a new credit eligibility model (Group B) against their current model (Group A). The goal is to determine whether the new model improves approval rates without significantly increasing default rates.

## Key Metrics
- **Approval Rate**: Proportion of loan applications approved
- **Default Rate**: Proportion of approved loans that default
- **Average Loan Size**: Mean loan amount disbursed
- **Processing Time**: Average time to process applications (hours)

## Methodology

### Data Generation
- 5,000 synthetic loan applications split evenly: 2,500 in Group A (control), 2,500 in Group B (treatment)
- Group A (current model): approval_rate ≈ 0.62, default_rate ≈ 0.11
- Group B (new model): approval_rate ≈ 0.71, default_rate ≈ 0.09
- Realistic noise added to simulate real-world variability

### Statistical Analysis
- Two-proportion z-test for approval_rate and default_rate
- 95% Confidence Intervals for the difference between groups
- Statistical significance at α = 0.05
- Power analysis to validate experimental design

### Output
- JSON results file with full statistical breakdown
- Readable summary report with conclusions
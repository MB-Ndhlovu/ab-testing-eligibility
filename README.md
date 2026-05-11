# A/B Testing Framework for Credit Eligibility

## Business Problem
A lender wants to test a new credit eligibility model against the current model. The goal is to determine whether the new model (Group B) improves approval rates and reduces default rates compared to the current model (Group A).

## Methodology
- **Two-Proportion Z-Test**: Used to compare approval and default rates between control (A) and treatment (B) groups.
- **95% Confidence Intervals**: Reported for the difference in proportions.
- **Statistical Significance**: Tested at α = 0.05.

## Metrics
1. **Approval Rate**: Higher is better for Group B.
2. **Default Rate**: Lower is better for Group B.

## Expected Outcomes
- Group A (Control): ~62% approval, ~11% default
- Group B (Treatment): ~71% approval, ~9% default
- Realistic noise added to simulate real-world data imperfection.
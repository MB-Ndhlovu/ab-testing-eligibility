# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (Group B) outperforms the current model (Group A) in two key metrics:
- **Approval Rate**: Higher is better — more loans approved increases revenue
- **Default Rate**: Lower is better — fewer defaults reduces loss

The goal is to determine whether the new model produces a statistically significant improvement, or if any observed difference is due to random noise.

## Methodology

### Experiment Design
- **Group A (Control)**: Current eligibility model
- **Group B (Treatment)**: New eligibility model
- **Sample size**: 5,000 applicants total (2,500 per group)
- **Metrics**: Approval rate, default rate, average loan size, processing time

### Statistical Approach
Two-proportion z-test for each binary metric:
- Null hypothesis (H₀): p_B - p_A = 0 (no difference)
- Alternative (H₁): p_B - p_A ≠ 0 (two-tailed)
- Significance level: α = 0.05

For each metric we compute:
1. **Z-statistic**: Measures how many standard errors the observed difference is from zero
2. **P-value**: Probability of observing this difference if H₀ is true
3. **95% Confidence Interval**: Range of plausible true differences
4. **Statistical conclusion**: Significant or not at α = 0.05

## Expected Outcomes

| Metric | Group A (Control) | Group B (Treatment) | Expected Lift |
|--------|-------------------|--------------------|---------------|
| Approval Rate | ~62% | ~71% | +9 pp |
| Default Rate | ~11% | ~9% | -2 pp |

Both metrics should show improvement in Group B, but noise is intentionally added so results aren't perfectly clean — reflecting real-world variability.
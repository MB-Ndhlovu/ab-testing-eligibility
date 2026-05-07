# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (treatment group B) improves outcomes compared to their current model (control group A).

**Key Metrics:**
- **Approval Rate**: Higher is better (more loans approved)
- **Default Rate**: Lower is better (fewer defaults)

**Hypothesis:**
- H0 (null): No difference between models
- H1 (alternative): Treatment B differs from control A

## Methodology

1. **Data Generation**: Simulate 5,000 loan applications split evenly into control (A) and treatment (B) groups
2. **Synthetic Outcomes**: Assign approval/default outcomes using probabilistic models with realistic noise
3. **Statistical Testing**: Two-proportion z-test for each metric
4. **Reporting**: Confidence intervals, p-values, and statistical conclusions at α=0.05

## Target Metrics

| Metric | Group A (Control) | Group B (Treatment) |
|--------|-------------------|---------------------|
| Approval Rate | ~62% | ~71% |
| Default Rate | ~11% | ~9% |

## Files

- `src/data_generator.py` — Generate synthetic loan data
- `src/statistical.py` — Z-test, confidence intervals, power analysis
- `src/simulate.py` — Run experiment simulation
- `src/report.py` — Generate summary report
- `run_pipeline.py` — Execute full pipeline
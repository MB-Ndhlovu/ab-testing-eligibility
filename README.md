# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (Group B) performs better than the current model (Group A). The goal is to make data-driven decisions about adopting the new model based on statistical evidence.

**Key Metrics:**
- **Approval Rate**: Higher is better (more loans approved)
- **Default Rate**: Lower is better (fewer defaults)
- **Average Loan Size**: Context metric
- **Processing Time**: Operational efficiency

## Methodology

1. **Randomized Experiment**: 5,000 synthetic loan applications randomly assigned to control (A) or treatment (B)
2. **Control Group (A)**: Current eligibility model — approval rate ~62%, default rate ~11%
3. **Treatment Group (B)**: New eligibility model — approval rate ~71%, default rate ~9%
4. **Statistical Test**: Two-proportion z-test for each metric
5. **Significance Level**: α = 0.05

## Success Criteria

The new model (B) is adopted if:
- Approval rate is significantly higher (beneficial)
- Default rate is not significantly higher (no added risk)
- Both conditions met → approve deployment

## Files

- `src/data_generator.py` — Generate synthetic loan data
- `src/statistical.py` — Statistical tests and confidence intervals
- `src/simulate.py` — Run experiment simulation
- `src/report.py` — Generate summary report
- `run_pipeline.py` — Execute full pipeline
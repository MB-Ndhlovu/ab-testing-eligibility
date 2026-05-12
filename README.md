# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (Group B) improves upon their current model (Group A). Specifically:

- **Group A (Control)**: Current eligibility rules → approval rate ~62%, default rate ~11%
- **Group B (Treatment)**: New eligibility rules → approval rate ~71%, default rate ~9%

The goal is to determine whether the new model is statistically significantly better on:
1. **Approval rate** — higher is better (more loans approved)
2. **Default rate** — lower is better (fewer defaults)

---

## Methodology

1. **Data Generation**: Simulate 5,000 loan applications per group with realistic noise
2. **Statistical Testing**: Two-proportion z-test for each metric
3. **Confidence Intervals**: 95% CI for the difference between groups
4. **Power Analysis**: Compute statistical power and minimum detectable effect

---

## Files

| File | Description |
|------|-------------|
| `src/data_generator.py` | Generates synthetic loan data for both groups |
| `src/statistical.py` | Two-proportion z-test, CI, power, MDE |
| `src/simulate.py` | Runs the experiment and computes treatment effects |
| `src/report.py` | Generates a readable summary report |
| `run_pipeline.py` | Executes the full pipeline end-to-end |
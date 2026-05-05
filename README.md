# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender currently uses a credit eligibility model (Group A - Control) and wants to test a new model (Group B - Treatment) that they believe will:
- Increase approval rates (more loans approved)
- Decrease default rates (fewer bad loans)

The question: Does the new model actually perform better, or is any observed difference due to random chance?

## Methodology

1. **Data Generation**: Simulate 5,000 loan applications split evenly between Control (A) and Treatment (B)
2. **Metrics Tracked**:
   - Approval Rate: Proportion of applications approved
   - Default Rate: Proportion of approved loans that go into default
   - Average Loan Size: Mean approved loan amount
   - Processing Time: Average time to process applications
3. **Statistical Testing**: Two-proportion z-test for approval and default rates
4. **Confidence Intervals**: 95% CI for the difference in proportions
5. **Power Analysis**: Minimum detectable effect at 80% power

## Expected Results

- Group A (Control): ~62% approval, ~11% default
- Group B (Treatment): ~71% approval, ~9% default
- Treatment should show statistically significant improvement

## Files

- `src/data_generator.py` - Synthetic data generation
- `src/statistical.py` - Statistical tests and power analysis
- `src/simulate.py` - Experiment simulation
- `src/report.py` - Results reporting
- `run_pipeline.py` - End-to-end pipeline execution
# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) performs better than their current model (Group A). The key metrics are:

- **Approval Rate**: Higher is better — more loans originated
- **Default Rate**: Lower is better — fewer defaulted loans

The goal is to make a data-driven decision: should the new model be deployed?

## Methodology

### Data Generation

We simulate 5,000 loan applications split evenly between control (A) and treatment (B):

- **Group A (Control)**: Current eligibility model
  - Target approval rate: ~62%
  - Target default rate: ~11%
  
- **Group B (Treatment)**: New eligibility model
  - Target approval rate: ~71%
  - Target default rate: ~9%

Realistic noise is added so results aren't perfectly clean.

### Statistical Testing

We use a **two-proportion z-test** to compare each metric between groups:

```
H₀: p_A = p_B (no difference)
H₁: p_A ≠ p_B (significant difference)
```

For each metric we report:
- Z-statistic
- P-value (two-tailed)
- 95% Confidence Interval for the difference
- Statistical conclusion at α = 0.05

### Additional Metrics

- **Statistical Power**: Probability of detecting a true effect
- **Minimum Detectable Effect (MDE)**: Smallest effect the test can reliably detect

## Project Structure

```
ab-testing-eligibility/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── data_generator.py   # Generate synthetic loan data
│   ├── statistical.py       # Z-test, CI, power, MDE
│   ├── simulate.py           # Run experiment simulation
│   └── report.py            # Generate summary report
└── run_pipeline.py          # Execute full pipeline
```

## Usage

```bash
pip install -r requirements.txt
python run_pipeline.py
```

## Success Criteria

The new model (B) should show:
1. Higher approval rate than A
2. Lower default rate than A
3. Statistical significance at α = 0.05 for both metrics
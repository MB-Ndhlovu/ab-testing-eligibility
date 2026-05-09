# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) outperforms the current model (Group A). The goal is to make data-driven decisions about adopting the new model by measuring its impact on key business metrics.

## Key Metrics

- **Approval Rate**: Percentage of loan applications approved. Higher is generally better for business revenue.
- **Default Rate**: Percentage of approved loans that default. Lower is better for risk management.
- **Average Loan Size**: Average loan amount disbursed.
- **Processing Time**: Average time to process a loan application.

## Methodology

### Data Generation

- Synthetic dataset of 5,000 loan applications split evenly between control (A) and treatment (B)
- Group A (Control): Current eligibility model
  - Approval rate: ~62%
  - Default rate: ~11%
- Group B (Treatment): New eligibility model
  - Approval rate: ~71% (improved)
  - Default rate: ~9% (improved)
- Realistic noise added to simulate real-world variation

### Statistical Analysis

Two-proportion z-test for each binary metric (approval_rate, default_rate):

- **Null Hypothesis (H₀)**: No difference between groups
- **Alternative (H₁)**: Significant difference exists
- **Significance Level**: α = 0.05
- **Confidence Interval**: 95%

Metrics computed:
- Z-statistic
- P-value
- 95% Confidence Interval for the difference
- Statistical power
- Minimum Detectable Effect (MDE)

## Files

```
ab-testing-eligibility/
├── README.md
├── requirements.txt
├── run_pipeline.py
└── src/
    ├── __init__.py
    ├── data_generator.py
    ├── statistical.py
    ├── simulate.py
    └── report.py
```

## Usage

```bash
pip install -r requirements.txt
python run_pipeline.py
```

## Conclusion Framework

Results are classified as:
- **Significant**: p-value < 0.05 — recommend adopting the new model if improvements are in desired direction
- **Not Significant**: p-value ≥ 0.05 — insufficient evidence to change current model

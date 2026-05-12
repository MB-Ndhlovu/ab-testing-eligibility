# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to test whether a new credit eligibility model (Group B) outperforms the current model (Group A). The goal is to determine if the new model:

- Increases **approval rate** (good for business)
- Decreases **default rate** (good for risk management)

## Methodology

### Data Generation
- **5,000 total applicants** split evenly between Group A (control) and Group B (treatment)
- Group A uses current eligibility rules: ~62% approval, ~11% default rate
- Group B uses new rules: ~71% approval, ~9% default rate
- Realistic noise added so results aren't perfectly clean

### Metrics Tracked
| Metric | Description |
|--------|-------------|
| `approval_rate` | Proportion of applicants approved |
| `default_rate` | Proportion of approved loans that default |
| `avg_loan_size` | Average loan amount (in rand) |
| `processing_time` | Average processing time per application (minutes) |

### Statistical Testing
- **Two-proportion z-test** for each metric
- **95% confidence intervals** for the difference between groups
- **α = 0.05** significance level
- Report: z-statistic, p-value, CI, and statistical conclusion

## File Structure
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
python run_pipeline.py
```
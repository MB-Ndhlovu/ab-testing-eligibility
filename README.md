# A/B Testing Framework for Credit Eligibility

## Overview
An A/B testing framework for evaluating a new credit eligibility model against the current model. The framework generates synthetic lending data, performs statistical hypothesis testing, and produces actionable reports.

## Business Problem
A lender wants to test a new credit eligibility model (Group B) against their current model (Group A). The goal is to determine whether the new model improves approval rates and/or reduces default rates before deploying to production.

## Methodology

### Experiment Design
- **Control Group (A)**: Current eligibility model
- **Treatment Group (B)**: New eligibility model
- **Sample Size**: 5,000 applicants (2,500 per group)

### Key Metrics
1. **Approval Rate**: Proportion of applicants approved
2. **Default Rate**: Proportion of approved loans that go into default
3. **Average Loan Size**: Mean approved loan amount
4. **Processing Time**: Average time to process applications

### Statistical Methods
- Two-proportion z-test for comparing approval and default rates
- 95% confidence intervals for the difference in proportions
- Statistical power analysis
- Minimum detectable effect (MDE) calculation

### Success Criteria
- α (significance level) = 0.05
- Statistically significant improvement in at least one key metric with no degradation in others

## Project Structure
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
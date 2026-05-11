# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) improves outcomes compared to the current model (Group A). The key metrics are:

- **Approval Rate**: Higher is better — more loans originated
- **Default Rate**: Lower is better — fewer losses from bad loans

The new model is expected to:
- Increase approval rate (approve more creditworthy applicants)
- Decrease default rate (better at identifying risk)

## Methodology

### Experiment Design
- **Control Group (A)**: Current eligibility model
- **Treatment Group (B)**: New eligibility model
- **Sample Size**: 5,000 applicants per group (10,000 total)
- **Allocation**: 50/50 split

### Synthetic Data Generation
Realistic loan application data with the following characteristics:

| Metric | Group A (Control) | Group B (Treatment) |
|--------|-------------------|---------------------|
| Approval Rate | ~62% | ~71% |
| Default Rate | ~11% | ~9% |
| Avg Loan Size | ~$15,000 | ~$15,500 |
| Processing Time | ~4.5 days | ~3.8 days |

Noise is added to simulate real-world variance (seasonal effects, applicant mix, regional differences).

### Statistical Analysis
- **Two-Proportion Z-Test** for approval rate and default rate
- **95% Confidence Intervals** for the difference between groups
- **Statistical Power** analysis to ensure adequate sample size
- **Minimum Detectable Effect (MDE)** calculation

### Decision Criteria
- Significance level: α = 0.05
- Null hypothesis (H₀): No difference between groups
- Alternative hypothesis (H₁): Significant difference exists
- Conclusion: Reject H₀ if p-value < 0.05

## Files

- `src/data_generator.py` — Synthetic data generation
- `src/statistical.py` — Statistical tests and power analysis
- `src/simulate.py` — Experiment simulation runner
- `src/report.py` — Results reporting
- `run_pipeline.py` — End-to-end pipeline execution

## Usage

```bash
pip install -r requirements.txt
python run_pipeline.py
```

Results are saved to `results.json` and printed to stdout.
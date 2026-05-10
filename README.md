# A/B Testing Framework for Credit Eligibility

## Business Problem

A lender wants to evaluate whether a new credit eligibility model (Group B) outperforms their current model (Group A). The framework allows them to:

- Test whether the new model increases approval rates without significantly affecting default rates
- Make data-driven decisions before full deployment
- Quantify uncertainty through confidence intervals and statistical significance

## Methodology

### Experiment Design

- **Control Group (A)**: Current eligibility model
- **Treatment Group (B)**: New eligibility model
- **Sample Size**: 5,000 applicants per group (10,000 total)
- **Primary Metrics**: Approval rate, Default rate
- **Secondary Metrics**: Average loan size, Processing time

### Statistical Approach

We use a **two-proportion z-test** to compare proportions between groups. This test is appropriate when:

1. Samples are independent
2. Sample sizes are large (n > 30)
3. Data follows a binomial distribution

### Key Statistics Reported

| Metric | Description |
|--------|-------------|
| Z-statistic | Standardized difference between proportions |
| P-value | Probability of observing this result by chance |
| 95% CI | Range likely to contain the true difference |
| Power | Probability of detecting a true effect |

### Decision Rule

- **Significance level (α)**: 0.05
- If p-value < 0.05: Reject null hypothesis → statistically significant difference
- If p-value ≥ 0.05: Fail to reject null hypothesis → no statistically significant difference

## Expected Results

Based on synthetic data generation:

| Metric | Group A (Control) | Group B (Treatment) |
|--------|-------------------|---------------------|
| Approval Rate | ~0.62 | ~0.71 |
| Default Rate | ~0.11 | ~0.09 |
| Avg Loan Size | ~R15,000 | ~R16,500 |
| Processing Time | ~45 min | ~38 min |

## Installation

```bash
pip install -r requirements.txt
```

## Usage

```bash
python run_pipeline.py
```

## Output

- Console: Summary report with statistical findings
- JSON: Full results saved to `results.json`
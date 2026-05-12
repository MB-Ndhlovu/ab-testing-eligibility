import numpy as np
from .data_generator import generate_data
from .statistical import two_proportion_ztest, confidence_interval

def run_simulation():
    """Run the A/B test experiment and compute results."""
    df = generate_data()

    group_a = df[df['group'] == 'A']
    group_b = df[df['group'] == 'B']

    n_a = len(group_a)
    n_b = len(group_b)

    # Approval rate
    approved_a = group_a['approved'].sum()
    approved_b = group_b['approved'].sum()

    # Default rate (only among approved)
    approved_loans_a = group_a[group_a['approved']]
    approved_loans_b = group_b[group_b['approved']]

    defaulted_a = approved_loans_a['defaulted'].sum()
    defaulted_b = approved_loans_b['defaulted'].sum()

    # Avg loan size (approved only)
    avg_loan_a = approved_loans_a['loan_amount'].mean()
    avg_loan_b = approved_loans_b['loan_amount'].mean()

    # Avg processing time (all applications)
    avg_time_a = group_a['processing_time'].mean()
    avg_time_b = group_b['processing_time'].mean()

    # Two-proportion z-tests
    approval_test = two_proportion_ztest(approved_a, n_a, approved_b, n_b)
    approval_ci = confidence_interval(approved_a, n_a, approved_b, n_b)

    default_test = two_proportion_ztest(defaulted_a, len(approved_loans_a),
                                        defaulted_b, len(approved_loans_b))
    default_ci = confidence_interval(defaulted_a, len(approved_loans_a),
                                     defaulted_b, len(approved_loans_b))

    alpha = 0.05

    results = {
        'sample_sizes': {'group_a': n_a, 'group_b': n_b},
        'approval_rate': {
            'group_a': approved_a / n_a,
            'group_b': approved_b / n_b,
            'difference': approval_test['difference'],
            'z_statistic': approval_test['z_statistic'],
            'p_value': approval_test['p_value'],
            'ci_lower': approval_ci['ci_lower'],
            'ci_upper': approval_ci['ci_upper'],
            'significant': approval_test['p_value'] < alpha,
        },
        'default_rate': {
            'group_a': defaulted_a / len(approved_loans_a),
            'group_b': defaulted_b / len(approved_loans_b),
            'difference': default_test['difference'],
            'z_statistic': default_test['z_statistic'],
            'p_value': default_test['p_value'],
            'ci_lower': default_ci['ci_lower'],
            'ci_upper': default_ci['ci_upper'],
            'significant': default_test['p_value'] < alpha,
        },
        'avg_loan_size': {
            'group_a': avg_loan_a,
            'group_b': avg_loan_b,
        },
        'avg_processing_time': {
            'group_a': avg_time_a,
            'group_b': avg_time_b,
        },
    }

    return results
from src.data_generator import generate_credit_data, compute_group_metrics
from src.statistical import two_proportion_z_test, confidence_interval, statistical_power

def run_simulation(seed=42):
    df = generate_credit_data(n=5000, seed=seed)
    metrics = compute_group_metrics(df)

    results = {}
    for metric in ['approval_rate', 'default_rate']:
        pA = metrics['A'][metric]
        pB = metrics['B'][metric]
        nA = metrics['A']['n']
        nB = metrics['B']['n']

        z, p_val = two_proportion_z_test(nA, pA, nB, pB)
        ci = confidence_interval(pA, pB, nA, nB)
        power = statistical_power(pA, pB, min(nA, nB))
        sig = p_val < 0.05

        results[metric] = {
            'group_a': round(pA, 4),
            'group_b': round(pB, 4),
            'z_statistic': round(z, 4),
            'p_value': round(p_val, 6),
            'ci_lower': round(ci[0], 4),
            'ci_upper': round(ci[1], 4),
            'significant': sig,
            'statistical_power': round(power, 4)
        }

    for group in ['A', 'B']:
        results[f'{group.lower()}_avg_loan_size'] = round(metrics[group]['avg_loan_size'], 2)
        results[f'{group.lower()}_avg_processing_time'] = round(metrics[group]['avg_processing_time'], 2)

    return results
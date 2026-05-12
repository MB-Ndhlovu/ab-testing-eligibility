from src.data_generator import generate_data, compute_group_stats
from src.statistical import two_proportion_ztest, confidence_interval, statistical_power

ALPHA = 0.05

def run_simulation():
    df = generate_data()
    stats_a = compute_group_stats(df, "A")
    stats_b = compute_group_stats(df, "B")

    results = {}

    for metric in ["approval_rate", "default_rate"]:
        n1 = stats_a["n"]
        p1 = stats_a[metric]
        n2 = stats_b["n"]
        p2 = stats_b[metric]

        z, p_value = two_proportion_ztest(n1, p1, n2, p2)
        ci_low, ci_high = confidence_interval(n1, p1, n2, p2, alpha=ALPHA)
        power = statistical_power(n1, p1, p2, alpha=ALPHA)
        significant = p_value < ALPHA

        results[metric] = {
            "group_a": p1,
            "group_b": p2,
            "treatment_effect": p2 - p1,
            "z_statistic": z,
            "p_value": p_value,
            "ci_95": [ci_low, ci_high],
            "power": power,
            "significant": significant,
        }

    n = stats_a["n"]
    results["avg_loan_size"] = {
        "group_a": stats_a["avg_loan_size"],
        "group_b": stats_b["avg_loan_size"],
        "treatment_effect": stats_b["avg_loan_size"] - stats_a["avg_loan_size"],
    }
    results["avg_processing_time"] = {
        "group_a": stats_a["avg_processing_time"],
        "group_b": stats_b["avg_processing_time"],
        "treatment_effect": stats_b["avg_processing_time"] - stats_a["avg_processing_time"],
    }

    return results
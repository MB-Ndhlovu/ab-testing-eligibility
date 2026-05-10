"""Run A/B test experiment simulation."""

from src.data_generator import generate_data
from src.statistical import analyze_metric


def run_experiment():
    """Execute the A/B test experiment and return results."""
    data = generate_data()

    results = {
        "sample_sizes": {
            "group_A": data["group_A"]["n"],
            "group_B": data["group_B"]["n"],
        },
        "group_A_summary": {
            "approval_rate": round(data["group_A"]["approval_rate"], 4),
            "default_rate": round(data["group_A"]["default_rate"], 4),
            "avg_loan_size": round(data["group_A"]["avg_loan_size"], 2),
            "avg_processing_time": round(data["group_A"]["avg_processing_time"], 2),
        },
        "group_B_summary": {
            "approval_rate": round(data["group_B"]["approval_rate"], 4),
            "default_rate": round(data["group_B"]["default_rate"], 4),
            "avg_loan_size": round(data["group_B"]["avg_loan_size"], 2),
            "avg_processing_time": round(data["group_B"]["avg_processing_time"], 2),
        },
    }

    # Analyze approval rate
    approval_analysis = analyze_metric(data, "approval_rate")
    results["approval_rate_analysis"] = {
        "group_A_rate": round(approval_analysis["group_A_rate"], 4),
        "group_B_rate": round(approval_analysis["group_B_rate"], 4),
        "treatment_effect": round(approval_analysis["treatment_effect"], 4),
        "z_statistic": round(approval_analysis["test"]["z_statistic"], 4),
        "p_value": round(approval_analysis["test"]["p_value"], 6),
        "ci_95": (round(approval_analysis["test"]["ci_95"][0], 4), round(approval_analysis["test"]["ci_95"][1], 4)),
        "significant": approval_analysis["test"]["significant"],
    }

    # Analyze default rate
    default_analysis = analyze_metric(data, "default_rate")
    results["default_rate_analysis"] = {
        "group_A_rate": round(default_analysis["group_A_rate"], 4),
        "group_B_rate": round(default_analysis["group_B_rate"], 4),
        "treatment_effect": round(default_analysis["treatment_effect"], 4),
        "z_statistic": round(default_analysis["test"]["z_statistic"], 4),
        "p_value": round(default_analysis["test"]["p_value"], 6),
        "ci_95": (round(default_analysis["test"]["ci_95"][0], 4), round(default_analysis["test"]["ci_95"][1], 4)),
        "significant": default_analysis["test"]["significant"],
    }

    return results
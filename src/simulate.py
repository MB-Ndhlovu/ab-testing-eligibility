"""
Experiment simulation: generate data and run statistical analysis.
"""
import json
from src.data_generator import generate_data, summarize
from src.statistical import run_analysis

def run_experiment():
    """
    Generate data, compute summary stats, run z-tests.
    Returns (summary_df, analysis_results, raw_dataframe).
    """
    df = generate_data()
    summary = summarize(df)

    n_A = int((df.group == "A").sum())
    n_B = int((df.group == "B").sum())

    p_approval_A = float(df[df.group == "A"]["approved"].mean())
    p_approval_B = float(df[df.group == "B"]["approved"].mean())

    # Default rate is computed only on approved loans
    approved_A = df[df.group == "A"]["approved"].sum()
    approved_B = df[df.group == "B"]["approved"].sum()
    defaults_A = float(df[df.group == "A"]["defaulted"].sum())
    defaults_B = float(df[df.group == "B"]["defaulted"].sum())

    p_default_A = defaults_A / approved_A if approved_A > 0 else 0.0
    p_default_B = defaults_B / approved_B if approved_B > 0 else 0.0

    analysis = run_analysis(
        n_A, p_approval_A, n_B, p_approval_B,
        n_A, p_default_A, n_B, p_default_B
    )

    return summary, analysis, df

def save_results(summary, analysis, path="results.json"):
    output = {
        "summary": summary.to_dict(orient="index"),
        "analysis": analysis,
    }
    with open(path, "w") as f:
        json.dump(output, f, indent=2, default=float)
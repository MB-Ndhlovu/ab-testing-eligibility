import numpy as np

def generate_data(n=5000, seed=42):
    np.random.seed(seed)
    group_a_n = n // 2
    group_b_n = n - group_a_n

    # Group A (control): approval ~62%, default among approved ~11%
    group_a_approved = np.random.binomial(1, 0.62, group_a_n)
    group_a_default = np.array([
        np.random.binomial(1, 0.11) if approved else 0
        for approved in group_a_approved
    ])

    # Group B (treatment): approval ~71%, default among approved ~9%
    group_b_approved = np.random.binomial(1, 0.71, group_b_n)
    group_b_default = np.array([
        np.random.binomial(1, 0.09) if approved else 0
        for approved in group_b_approved
    ])

    # Loan size (in thousands) — skewed distribution, larger for approved
    group_a_loan_size = np.where(
        group_a_approved == 1,
        np.random.lognormal(mean=4.2, sigma=0.6, size=group_a_n),
        np.random.lognormal(mean=3.5, sigma=0.7, size=group_a_n)
    )
    group_b_loan_size = np.where(
        group_b_approved == 1,
        np.random.lognormal(mean=4.3, sigma=0.55, size=group_b_n),
        np.random.lognormal(mean=3.6, sigma=0.65, size=group_b_n)
    )

    # Processing time in minutes
    group_a_proc_time = np.random.gamma(shape=3, scale=12, size=group_a_n) + np.random.normal(0, 3, group_a_n)
    group_b_proc_time = np.random.gamma(shape=3.5, scale=10, size=group_b_n) + np.random.normal(0, 2.5, group_b_n)
    group_a_proc_time = np.clip(group_a_proc_time, 5, 300)
    group_b_proc_time = np.clip(group_b_proc_time, 5, 300)

    # Combine into records
    records = []
    for i in range(group_a_n):
        records.append({
            "id": i + 1,
            "group": "A",
            "approved": int(group_a_approved[i]),
            "defaulted": int(group_a_default[i]),
            "loan_size": round(group_a_loan_size[i], 2),
            "processing_time": round(group_a_proc_time[i], 2)
        })

    offset = group_a_n
    for i in range(group_b_n):
        records.append({
            "id": offset + i + 1,
            "group": "B",
            "approved": int(group_b_approved[i]),
            "defaulted": int(group_b_default[i]),
            "loan_size": round(group_b_loan_size[i], 2),
            "processing_time": round(group_b_proc_time[i], 2)
        })

    return records

def compute_summary(records):
    from collections import defaultdict
    groups = defaultdict(list)
    for r in records:
        groups[r["group"]].append(r)

    summary = {}
    for g, recs in groups.items():
        n = len(recs)
        approved = [r for r in recs if r["approved"] == 1]
        defaulted = [r for r in approved if r["defaulted"] == 1]
        summary[g] = {
            "n": n,
            "approval_rate": len(approved) / n,
            "default_rate": len(defaulted) / len(approved) if approved else 0,
            "avg_loan_size": np.mean([r["loan_size"] for r in recs]),
            "avg_processing_time": np.mean([r["processing_time"] for r in recs])
        }
    return summary

if __name__ == "__main__":
    records = generate_data()
    summary = compute_summary(records)
    for g, s in summary.items():
        print(f"Group {g}: n={s['n']}, approval_rate={s['approval_rate']:.4f}, "
              f"default_rate={s['default_rate']:.4f}, "
              f"avg_loan_size={s['avg_loan_size']:.2f}, "
              f"avg_proc_time={s['avg_processing_time']:.2f}")
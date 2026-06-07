import pandas as pd

def build_report(results):

    rows = []

    for claim, verdict in results:
        rows.append({
            "Claim": claim,
            "Result": verdict
        })

    return pd.DataFrame(rows)

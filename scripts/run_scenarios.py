import argparse, json, yaml, pandas as pd
from datetime import datetime
from src.io.loaders import load_portfolio_csv
from src.curves.nss import discount_factor
from src.pricing.bonds import price_coupon_bond
from src.portfolio.analytics import apply_parallel_shift, scenario_pnl

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--curve", required=True)
    ap.add_argument("--portfolio", required=True)
    ap.add_argument("--scenarios", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()

    with open(args.curve) as f:
        curve = json.load(f)
    beta = curve["params"]

    pf = load_portfolio_csv(args.portfolio)
    with open(args.scenarios) as f:
        sc = yaml.safe_load(f)["scenarios"]

    def pricer_with_beta(b):
        def inner(row):
            settl = datetime.fromisoformat(row["settl_date"])
            mat = datetime.fromisoformat(row["mat_date"])
            return price_coupon_bond(settl, mat, row["coupon"], row["face"], int(row["frequency"]),
                                     lambda t: discount_factor(t, b))
        return inner

    all_rows = []
    base_pricer = pricer_with_beta(beta)
    for s in sc:
        if s["type"] == "parallel":
            b2 = apply_parallel_shift(beta[:], s["shift_bps"])
        elif s["type"] == "key_rate":
            # simple key-rate: adjust beta0 based on weighted average of provided shifts
            avg_shift = sum(s["shifts_bps"].values())/len(s["shifts_bps"])
            b2 = apply_parallel_shift(beta[:], avg_shift)
        else:
            raise ValueError("unknown scenario type")

        df = scenario_pnl(pf, base_pricer, pricer_with_beta(b2))
        df.insert(0, "scenario", s["name"])
        all_rows.append(df)

    out = pd.concat(all_rows, ignore_index=True)
    out.to_csv(args.report, index=False)
    print("Wrote", args.report)

if __name__ == "__main__":
    main()

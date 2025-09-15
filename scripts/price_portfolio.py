import argparse, json
import pandas as pd
from datetime import datetime
from src.io.loaders import load_portfolio_csv
from src.curves.nss import discount_factor
from src.pricing.bonds import price_coupon_bond, modified_duration, convexity

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--curve", required=True)
    ap.add_argument("--portfolio", required=True)
    ap.add_argument("--report", required=True)
    args = ap.parse_args()

    with open(args.curve) as f:
        curve = json.load(f)
    beta = curve["params"]

    def df_func(t):
        return discount_factor(t, beta)

    pf = load_portfolio_csv(args.portfolio)

    rows = []
    for _, r in pf.iterrows():
        settl = datetime.fromisoformat(r["settl_date"])
        mat = datetime.fromisoformat(r["mat_date"])
        price_fn = lambda bump: price_coupon_bond(settl, mat, r["coupon"], r["face"], int(r["frequency"]),
                                                  lambda t: discount_factor(t, [beta[0]+bump, *beta[1:]]))
        clean = price_fn(0.0)
        dur = modified_duration(price_fn)
        conv = convexity(price_fn)
        rows.append({**r.to_dict(), "model_price": clean, "mod_duration": dur, "convexity": conv})

    out = pd.DataFrame(rows)
    out.to_csv(args.report, index=False)
    print("Wrote", args.report)

if __name__ == "__main__":
    main()

import argparse, json
import numpy as np
from src.io.loaders import load_ust_csv
from src.curves.nss import fit_nss

TENOR_MAP = {
    "1M": 1/12, "3M": 3/12, "6M": 6/12, "1Y": 1.0, "2Y": 2.0, "3Y": 3.0,
    "5Y": 5.0, "7Y": 7.0, "10Y": 10.0, "20Y": 20.0, "30Y": 30.0
}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--method", choices=["nss"], default="nss")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    df = load_ust_csv(args.input)
    df = df[df["quote_type"]=="yield"].copy()
    df["tenor_years"] = df["tenor"].map(TENOR_MAP)
    df = df.dropna(subset=["tenor_years"])

    ten = df["tenor_years"].values
    y = df["value"].values
    beta = fit_nss(ten, y, beta0_init=float(y[-1]))

    with open(args.out,"w") as f:
        json.dump({"method":"nss","params": beta.tolist()}, f, indent=2)
    print("Saved curve to", args.out)

if __name__ == "__main__":
    main()

import numpy as np
import pandas as pd

def apply_parallel_shift(curve_params, shift_bps):
    beta = curve_params.copy()
    # Shift beta0 (long-term level) in decimal terms
    beta[0] += shift_bps/10000.0
    return beta

def scenario_pnl(portfolio_df, base_pricer, shock_pricer):
    rows = []
    for _, row in portfolio_df.iterrows():
        base_p = base_pricer(row)
        shock_p = shock_pricer(row)
        pnl = shock_p - base_p
        rows.append({**row.to_dict(), "base_price": base_p, "scenario_price": shock_p, "pnl": pnl})
    return pd.DataFrame(rows)

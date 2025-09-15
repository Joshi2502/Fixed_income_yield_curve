# Fixed Income Yield Curve Construction & Analytics

End-to-end toolkit to **construct yield curves**, **price bonds**, and compute **risk metrics**
(duration, convexity, DV01), with **scenario/stress testing** and an optional **interactive dashboard**.
Built with **Python** (NumPy/Pandas/SciPy/Plotly/Streamlit).

## Features
- Curve fitting: **Nelson–Siegel–Svensson (NSS)** and **cubic spline**.
- Instruments: Bills/Notes/Bonds (zero & coupon).
- Pricing & Risk: clean/dirty price, accrued interest, YTM, **DV01**, **duration**, **convexity**.
- Scenarios: parallel/steepener/flattener shifts; YAML-configured stress tests.
- Portfolio analytics: P&L attribution under scenarios.
- Data pipeline: ingest and validate UST data (CSV).
- Dashboard: Streamlit app for interactive exploration.

## Quickstart
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1) Fit curve from CSV
python scripts/build_curve.py   --input data/raw/ust_quotes.csv   --method nss   --out data/processed/curve_latest.json

# 2) Price & risk a portfolio
python scripts/price_portfolio.py   --curve data/processed/curve_latest.json   --portfolio data/examples/portfolio.csv   --report out/portfolio_risk.csv

# 3) Run scenarios
python scripts/run_scenarios.py   --curve data/processed/curve_latest.json   --portfolio data/examples/portfolio.csv   --scenarios configs/scenarios.yaml   --report out/scenario_pnl.csv

# 4) Launch dashboard
streamlit run src/dashboard/app.py
```

## Data
Sample UST yields are included in `data/raw/ust_quotes.csv`. Replace with your own data as needed.

## Testing
```bash
pytest -q
```

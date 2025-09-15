# Ensure project root is on sys.path when running on hosted platforms
import os, sys
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)


import json
import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
from src.curves.nss import nss_rate
from src.io.loaders import load_portfolio_csv

st.set_page_config(page_title="Yield Curve & FI Analytics", layout="wide")

st.title("Fixed Income Yield Curve Construction & Analytics")

curve_file = st.sidebar.text_input("Curve JSON", "data/processed/curve_latest.json")
portfolio_file = st.sidebar.text_input("Portfolio CSV", "data/examples/portfolio.csv")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Yield Curve")
    try:
        with open(curve_file) as f:
            curve = json.load(f)
        beta = curve["params"]
        ten = np.linspace(0.1, 30, 200)
        zr = nss_rate(ten, beta)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=ten, y=zr, mode="lines", name="NSS Zero Rate"))
        fig.update_layout(xaxis_title="Maturity (Years)", yaxis_title="Zero Rate", height=400)
        st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.warning(f"Load a curve JSON: {e}")

with col2:
    st.subheader("Portfolio Preview")
    try:
        pf = load_portfolio_csv(portfolio_file)
        st.dataframe(pf.head(20), use_container_width=True, height=400)
    except Exception as e:
        st.warning(f"Load a portfolio CSV: {e}")

st.markdown("---")
st.caption("Tip: use the CLI scripts to build a curve and run analytics, then refresh this dashboard.")

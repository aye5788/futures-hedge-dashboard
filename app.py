import streamlit as st
from logic.calculations import (
    calculate_beta_exposure,
    calculate_futures_notional,
    calculate_full_hedge_contracts,
)

st.set_page_config(layout="wide")
st.title("Futures Hedge Dashboard")

st.markdown("### Enter Portfolio Inputs")

col1, col2 = st.columns(2)

with col1:
    portfolio_value = st.number_input(
        "Total Portfolio Value ($)",
        min_value=0.0,
        value=100000.0,
        step=1000.0,
    )

    portfolio_beta = st.number_input(
        "Portfolio Beta",
        min_value=0.0,
        value=1.0,
        step=0.05,
    )

with col2:
    spx_level = st.number_input(
        "Current SPX Level",
        min_value=1000.0,
        value=5000.0,
        step=10.0,
    )

    mes_multiplier = st.number_input(
        "MES Multiplier",
        value=5.0,
        step=1.0,
    )

st.markdown("---")
st.markdown("### Futures Hedge Inputs")

futures_direction = st.selectbox("Direction", ["SHORT", "LONG"])

mes_contracts = st.number_input(
    "Number of MES Contracts",
    min_value=0,
    max_value=50,
    value=0,
    step=1,
)

st.markdown("---")
st.markdown("## Exposure Calculations")

beta_exposure = calculate_beta_exposure(portfolio_value, portfolio_beta)

futures_notional = calculate_futures_notional(
    mes_contracts, mes_multiplier, spx_level, futures_direction
)

net_exposure = beta_exposure + futures_notional

percent_hedged = (
    abs(futures_notional) / beta_exposure * 100
    if beta_exposure != 0
    else 0
)

full_hedge_contracts = calculate_full_hedge_contracts(
    beta_exposure, mes_multiplier, spx_level
)

col1, col2, col3 = st.columns(3)

col1.metric("Beta-Adjusted Exposure ($)", f"{beta_exposure:,.0f}")
col2.metric("Futures Notional ($)", f"{futures_notional:,.0f}")
col3.metric("Net Exposure ($)", f"{net_exposure:,.0f}")

st.markdown("### Hedge Diagnostics")

col4, col5 = st.columns(2)

col4.metric("Percent Hedged (%)", f"{percent_hedged:.1f}%")
col5.metric("Contracts for Full Hedge", f"{full_hedge_contracts:.2f}")

st.markdown("---")
st.markdown("### Interpretation")

if net_exposure > 0:
    st.info("You are net LONG market exposure.")
elif net_exposure < 0:
    st.warning("You are net SHORT market exposure.")
else:
    st.success("You are approximately market neutral.")


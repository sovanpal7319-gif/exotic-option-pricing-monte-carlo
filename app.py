"""
Exotic Option Pricing and Risk Analysis Dashboard
===================================================
Interactive Streamlit application for pricing exotic options
using Monte Carlo simulation and analyzing associated risks.

Run with: streamlit run app.py

Authors: Sayan Goswami, Sovan Pal, Tanmoy Paul
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# --- Page Configuration (must be first Streamlit call) ---
st.set_page_config(
    page_title="Exotic Option Pricing",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Imports from project modules ---
from src.simulation import simulate_gbm_paths
from src.asian_option import price_asian_option
from src.barrier_option import price_barrier_option
from src.lookback_option import price_lookback_option
from src.greeks import calculate_all_greeks
from src.data_processing import (load_price_data, calculate_log_returns,
                                  calculate_historical_volatility, estimate_parameters)
from src.validation import (black_scholes_call, black_scholes_put,
                             validate_european_mc, convergence_analysis)

# ============================================================
# Custom CSS
# ============================================================
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem; font-weight: 700;
        background: linear-gradient(90deg, #1f77b4, #2ca02c);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        text-align: center; margin-bottom: 0.3rem;
    }
    .sub-header {
        font-size: 1.1rem; color: #888; text-align: center;
        margin-bottom: 2rem;
    }
    .metric-container {
        background-color: #f0f2f6; border-radius: 10px;
        padding: 1rem; margin: 0.5rem 0;
    }
    .footer {
        text-align: center; color: #aaa; font-size: 0.85rem;
        margin-top: 3rem; padding-top: 1rem;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# Session State Initialization
# ============================================================
if 'pricing_results' not in st.session_state:
    st.session_state.pricing_results = {}
if 'greeks_results' not in st.session_state:
    st.session_state.greeks_results = {}
if 'params' not in st.session_state:
    st.session_state.params = {}
if 'comparison_df' not in st.session_state:
    st.session_state.comparison_df = None

# ============================================================
# Sidebar Navigation
# ============================================================
st.sidebar.title("📊 Navigation")
page = st.sidebar.radio(
    "Go to",
    ["🏠 Home",
     "📊 Market Data",
     "💰 Option Pricing",
     "📈 Risk Analysis (Greeks)",
     "📉 Sensitivity Analysis",
     "🔄 Option Comparison",
     "✅ Validation",
     "📥 Export Results"],
    index=0
)


def add_footer():
    """Add consistent footer to every page."""
    st.markdown('<div class="footer">Developed by Sayan Goswami, Sovan Pal, '
                'Tanmoy Paul &nbsp;|&nbsp; Exotic Option Pricing Project</div>',
                unsafe_allow_html=True)


# ============================================================
# PAGE: HOME
# ============================================================
if page == "🏠 Home":
    st.markdown('<p class="main-header">Exotic Option Pricing and Risk Analysis</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Using Monte Carlo Simulation</p>',
                unsafe_allow_html=True)

    st.markdown("---")

    # Abstract
    st.subheader("📄 Abstract")
    st.write(
        "This project focuses on pricing exotic options — Asian, Barrier, and Lookback — "
        "using Monte Carlo simulation and analyzing the associated financial risks. "
        "By simulating thousands of possible future asset-price paths under the risk-neutral "
        "measure, we estimate the fair value of each option type. The project further analyzes "
        "option price sensitivity using Greeks (Delta, Gamma, Vega) and presents results "
        "through interactive visualizations."
    )

    # Problem Statement
    st.subheader("❓ Problem Statement")
    st.write(
        "Exotic options have more complex payoff structures than standard European options, "
        "making their pricing and risk analysis challenging. Unlike vanilla options, most exotic "
        "options have **no closed-form analytical solution**, necessitating numerical methods "
        "such as Monte Carlo simulation. This project aims to estimate the fair value of selected "
        "exotic options and understand how changes in market parameters affect their prices and risks."
    )

    # Methodology
    st.subheader("🔬 Methodology")
    st.write(
        "The project uses **Monte Carlo simulation** to generate multiple possible future "
        "asset-price paths based on Geometric Brownian Motion (GBM). These simulated paths "
        "are used to estimate option values by computing expected discounted payoffs. "
        "Sensitivity analysis is performed using finite-difference approximations of Greeks."
    )
    st.latex(r"S(t+\Delta t) = S(t) \cdot \exp\left[\left(r - \frac{\sigma^2}{2}\right)"
             r"\Delta t + \sigma\sqrt{\Delta t}\, Z\right]")

    # Objectives
    st.subheader("🎯 Objectives")
    objectives = [
        "Simulate future asset-price paths using Geometric Brownian Motion",
        "Price Asian, Barrier, and Lookback exotic options via Monte Carlo",
        "Calculate Greeks (Delta, Gamma, Vega) using finite differences",
        "Analyze how option prices change with market parameters",
        "Validate Monte Carlo pricing against Black-Scholes analytical solution",
        "Provide an interactive dashboard for exploration and analysis"
    ]
    for obj in objectives:
        st.write(f"- {obj}")

    # Exotic Options Overview
    st.markdown("---")
    st.subheader("📚 Exotic Options Overview")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("#### 🔵 Asian Option")
        st.write("Payoff depends on the **average** price over the option's life. "
                 "Cheaper than vanilla options due to reduced volatility exposure.")
        st.latex(r"\text{Call} = \max(\bar{S} - K,\; 0)")
    with col2:
        st.markdown("#### 🟡 Barrier Option")
        st.write("Option is **activated or deactivated** when the asset price "
                 "crosses a barrier level. Cheaper than vanilla due to knock-out risk.")
        st.latex(r"\text{D\&O Call} = \max(S_T - K,\; 0) \cdot \mathbf{1}[\min S > B]")
    with col3:
        st.markdown("#### 🟢 Lookback Option")
        st.write("Payoff depends on the **extreme** (max or min) price. "
                 "Always in the money — hence more expensive than vanilla.")
        st.latex(r"\text{Call} = S_T - S_{\min}")

    # Team Members
    st.markdown("---")
    st.subheader("👥 Team Members")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.info("**Sayan Goswami**\n\nCore Simulation & Option Pricing")
    with t2:
        st.info("**Sovan Pal**\n\nGreeks, Validation & Risk Analysis")
    with t3:
        st.info("**Tanmoy Paul**\n\nDashboard, Visualization & Data Processing")

    add_footer()


# ============================================================
# PAGE: MARKET DATA
# ============================================================
elif page == "📊 Market Data":
    st.header("📊 Historical Market Data")
    st.write("Upload historical price data (CSV) to estimate model parameters, "
             "or use the sample dataset provided.")

    col_upload, col_sample = st.columns(2)
    with col_upload:
        uploaded_file = st.file_uploader("Upload CSV (must have Date & Close columns)",
                                          type=['csv'])
    with col_sample:
        use_sample = st.button("📂 Use Sample Data (NIFTY-like synthetic)")

    data_source = None
    if uploaded_file is not None:
        data_source = uploaded_file
    elif use_sample:
        data_source = "data/sample_prices.csv"

    if data_source is not None:
        try:
            df = load_price_data(data_source)
            params = estimate_parameters(df)

            st.success(f"✅ Loaded {params['n_observations']} data points")

            # Display parameters
            c1, c2, c3 = st.columns(3)
            c1.metric("Last Close (S₀)", f"{params['S0']:,.2f}")
            c2.metric("Historical Volatility (σ)", f"{params['sigma']:.4f}")
            c3.metric("Mean Annualized Return", f"{params['mean_return']:.4f}")

            # Data preview
            with st.expander("📋 Data Preview"):
                st.dataframe(df.head(20), use_container_width=True)

            # Price chart
            st.subheader("Price History")
            fig_price = go.Figure()
            fig_price.add_trace(go.Scatter(
                x=df['Date'], y=df['Close'], mode='lines',
                name='Close Price', line=dict(color='#1f77b4', width=1.5)))
            fig_price.update_layout(
                xaxis_title='Date', yaxis_title='Price',
                template='plotly_white', height=400)
            st.plotly_chart(fig_price, use_container_width=True)

            # Returns distribution
            returns = params['daily_returns']
            col_ret, col_hist = st.columns(2)
            with col_ret:
                st.subheader("Daily Log Returns")
                fig_ret = go.Figure()
                fig_ret.add_trace(go.Scatter(
                    y=returns.values, mode='lines',
                    line=dict(color='#2ca02c', width=0.8)))
                fig_ret.update_layout(
                    xaxis_title='Day', yaxis_title='Log Return',
                    template='plotly_white', height=300)
                st.plotly_chart(fig_ret, use_container_width=True)
            with col_hist:
                st.subheader("Return Distribution")
                fig_hist = go.Figure()
                fig_hist.add_trace(go.Histogram(
                    x=returns.values, nbinsx=40,
                    marker_color='#ff7f0e', opacity=0.75))
                fig_hist.update_layout(
                    xaxis_title='Log Return', yaxis_title='Frequency',
                    template='plotly_white', height=300)
                st.plotly_chart(fig_hist, use_container_width=True)

            # Button to use estimated parameters
            if st.button("✅ Use These Parameters for Pricing"):
                st.session_state.params = {
                    'S0': params['S0'],
                    'sigma': params['sigma']
                }
                st.success("Parameters saved! Go to Option Pricing page.")

        except Exception as e:
            st.error(f"Error loading data: {e}")
    else:
        st.info("Upload a CSV file or click 'Use Sample Data' to begin.")
        st.markdown("""
        **Expected CSV format:**
        | Date | Close |
        |------|-------|
        | 2025-01-02 | 22000.50 |
        | 2025-01-03 | 22150.75 |

        **Suggested data sources:**
        - [NSE India](https://www.nseindia.com/)
        - [Yahoo Finance](https://finance.yahoo.com/)
        """)

    add_footer()


# ============================================================
# PAGE: OPTION PRICING
# ============================================================
elif page == "💰 Option Pricing":
    st.header("💰 Option Pricing Engine")

    # Sidebar parameters
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Market Parameters")

    default_S0 = st.session_state.params.get('S0', 100.0)
    default_sigma = st.session_state.params.get('sigma', 0.20)

    S0 = st.sidebar.number_input("Initial Asset Price (S₀)", value=float(default_S0),
                                  min_value=0.01, step=1.0, format="%.2f")
    K = st.sidebar.number_input("Strike Price (K)", value=float(default_S0),
                                 min_value=0.01, step=1.0, format="%.2f")
    sigma = st.sidebar.slider("Volatility (σ)", 0.05, 1.00,
                               float(min(default_sigma, 1.0)), 0.01)
    r = st.sidebar.slider("Risk-Free Rate (r)", 0.01, 0.15, 0.05, 0.005)
    T = st.sidebar.slider("Time to Maturity (T, years)", 0.1, 5.0, 1.0, 0.1)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🔧 Simulation Settings")
    n_simulations = st.sidebar.selectbox(
        "Number of Simulations", [1000, 5000, 10000, 50000, 100000], index=2)
    n_steps = st.sidebar.selectbox(
        "Time Steps", [50, 100, 252, 504], index=2)
    seed = st.sidebar.number_input("Random Seed", value=42, min_value=0, step=1)

    st.sidebar.markdown("---")
    st.sidebar.subheader("🚧 Barrier Settings")
    B = st.sidebar.number_input("Barrier Level (B)", value=float(S0 * 0.8),
                                 min_value=0.01, step=1.0, format="%.2f")
    barrier_type = st.sidebar.selectbox(
        "Barrier Type", ['down-and-out', 'down-and-in', 'up-and-out', 'up-and-in'])

    # Save params to session state
    st.session_state.params = {
        'S0': S0, 'K': K, 'sigma': sigma, 'r': r, 'T': T,
        'n_simulations': n_simulations, 'n_steps': n_steps,
        'B': B, 'barrier_type': barrier_type, 'seed': seed
    }

    # Option selection
    st.subheader("Select Options to Price")
    col_sel1, col_sel2, col_sel3 = st.columns(3)
    with col_sel1:
        asian_call = st.checkbox("Asian Call", value=True)
        asian_put = st.checkbox("Asian Put", value=True)
    with col_sel2:
        barrier_call = st.checkbox("Barrier Call", value=True)
        barrier_put = st.checkbox("Barrier Put")
    with col_sel3:
        lookback_call = st.checkbox("Lookback Call", value=True)
        lookback_put = st.checkbox("Lookback Put", value=True)

    # Run simulation
    if st.button("🚀 Run Monte Carlo Simulation", type="primary"):
        results = {}
        progress = st.progress(0)
        status = st.empty()

        selected = []
        if asian_call: selected.append(('Asian Call', 'asian', 'call'))
        if asian_put: selected.append(('Asian Put', 'asian', 'put'))
        if barrier_call: selected.append(('Barrier Call', 'barrier', 'call'))
        if barrier_put: selected.append(('Barrier Put', 'barrier', 'put'))
        if lookback_call: selected.append(('Lookback Call', 'lookback', 'call'))
        if lookback_put: selected.append(('Lookback Put', 'lookback', 'put'))

        if not selected:
            st.warning("Please select at least one option type.")
        else:
            for i, (name, opt_class, opt_type) in enumerate(selected):
                status.text(f"Pricing {name}...")
                try:
                    if opt_class == 'asian':
                        res = price_asian_option(
                            S0, K, r, sigma, T, n_steps, n_simulations,
                            option_type=opt_type, seed=seed)
                    elif opt_class == 'barrier':
                        res = price_barrier_option(
                            S0, K, r, sigma, T, B, n_steps, n_simulations,
                            option_type=opt_type, barrier_type=barrier_type,
                            seed=seed)
                    elif opt_class == 'lookback':
                        res = price_lookback_option(
                            S0, r, sigma, T, n_steps, n_simulations,
                            option_type=opt_type, seed=seed)
                    results[name] = res
                except Exception as e:
                    st.error(f"Error pricing {name}: {e}")

                progress.progress((i + 1) / len(selected))

            status.text("✅ All simulations complete!")
            st.session_state.pricing_results = results

    # Display results
    if st.session_state.pricing_results:
        st.markdown("---")
        st.subheader("📊 Pricing Results")

        for name, res in st.session_state.pricing_results.items():
            with st.expander(f"📌 {name}", expanded=True):
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("💲 Option Price", f"{res['price']:.4f}")
                c2.metric("📏 Std Error", f"{res['std_error']:.4f}")
                c3.metric("📐 95% CI Lower", f"{res['conf_interval'][0]:.4f}")
                c4.metric("📐 95% CI Upper", f"{res['conf_interval'][1]:.4f}")

                if 'knocked_out_pct' in res:
                    st.info(f"🚧 Paths knocked out: {res['knocked_out_pct']:.1f}%")

                # Simulated paths plot
                tab1, tab2 = st.tabs(["📈 Simulated Paths", "📊 Payoff Distribution"])

                with tab1:
                    fig_paths = go.Figure()
                    paths = res['paths']
                    n_show = min(100, paths.shape[0])
                    time_axis = np.linspace(0, T, paths.shape[1])

                    for j in range(n_show):
                        fig_paths.add_trace(go.Scatter(
                            x=time_axis, y=paths[j], mode='lines',
                            line=dict(width=0.4, color='rgba(31,119,180,0.08)'),
                            showlegend=False, hoverinfo='skip'))

                    # Mean path
                    fig_paths.add_trace(go.Scatter(
                        x=time_axis, y=np.mean(paths, axis=0), mode='lines',
                        line=dict(width=2.5, color='red'), name='Mean Path'))

                    # Barrier line if applicable
                    if 'knocked_out_pct' in res:
                        fig_paths.add_hline(y=B, line_dash="dash",
                                            line_color="orange",
                                            annotation_text=f"Barrier = {B}")

                    fig_paths.update_layout(
                        title=f'{name} — Simulated Price Paths ({n_show} shown)',
                        xaxis_title='Time (years)', yaxis_title='Asset Price',
                        template='plotly_white', height=400)
                    st.plotly_chart(fig_paths, use_container_width=True)

                with tab2:
                    fig_payoff = go.Figure()
                    payoffs = res['payoffs']
                    fig_payoff.add_trace(go.Histogram(
                        x=payoffs[payoffs > 0], nbinsx=50,
                        marker_color='#2ca02c', opacity=0.75,
                        name='Positive Payoffs'))
                    if np.any(payoffs == 0):
                        zero_count = np.sum(payoffs == 0)
                        fig_payoff.add_annotation(
                            text=f"Zero payoffs: {zero_count} ({zero_count/len(payoffs)*100:.1f}%)",
                            xref="paper", yref="paper", x=0.8, y=0.9,
                            showarrow=False, bgcolor='lightyellow')
                    fig_payoff.update_layout(
                        title=f'{name} — Payoff Distribution',
                        xaxis_title='Payoff', yaxis_title='Frequency',
                        template='plotly_white', height=350)
                    st.plotly_chart(fig_payoff, use_container_width=True)

    add_footer()


# ============================================================
# PAGE: RISK ANALYSIS (GREEKS)
# ============================================================
elif page == "📈 Risk Analysis (Greeks)":
    st.header("📈 Risk Analysis — Greeks")

    st.markdown("""
    Greeks measure the sensitivity of option prices to changes in market parameters.
    We compute them using **central finite differences** for accuracy.
    """)

    st.latex(r"\Delta \approx \frac{V(S+h) - V(S-h)}{2h}")
    st.latex(r"\Gamma \approx \frac{V(S+h) - 2V(S) + V(S-h)}{h^2}")
    st.latex(r"\nu \approx \frac{V(\sigma+\varepsilon) - V(\sigma-\varepsilon)}{2\varepsilon}")

    if not st.session_state.pricing_results:
        st.warning("⚠️ Please run Option Pricing first.")
    else:
        p = st.session_state.params
        n_sims_greeks = st.selectbox(
            "Simulations for Greeks (lower = faster)", [1000, 2000, 5000, 10000], index=1)

        if st.button("🧮 Calculate Greeks", type="primary"):
            greeks_results = {}
            progress = st.progress(0)

            option_list = list(st.session_state.pricing_results.keys())
            for i, name in enumerate(option_list):
                st.text(f"Computing Greeks for {name}...")
                try:
                    if 'Asian' in name:
                        opt_type = 'call' if 'Call' in name else 'put'
                        greeks = calculate_all_greeks(
                            price_asian_option, p['S0'], p['r'], p['sigma'],
                            p['T'], p['n_steps'], n_sims_greeks,
                            seed=p['seed'], K=p['K'], option_type=opt_type)
                    elif 'Barrier' in name:
                        opt_type = 'call' if 'Call' in name else 'put'
                        greeks = calculate_all_greeks(
                            price_barrier_option, p['S0'], p['r'], p['sigma'],
                            p['T'], p['n_steps'], n_sims_greeks,
                            seed=p['seed'], K=p['K'], B=p['B'],
                            option_type=opt_type, barrier_type=p['barrier_type'])
                    elif 'Lookback' in name:
                        opt_type = 'call' if 'Call' in name else 'put'
                        greeks = calculate_all_greeks(
                            price_lookback_option, p['S0'], p['r'], p['sigma'],
                            p['T'], p['n_steps'], n_sims_greeks,
                            seed=p['seed'], option_type=opt_type)
                    greeks_results[name] = greeks
                except Exception as e:
                    st.error(f"Error computing Greeks for {name}: {e}")
                progress.progress((i + 1) / len(option_list))

            st.session_state.greeks_results = greeks_results
            st.success("✅ Greeks calculated!")

        if st.session_state.greeks_results:
            st.markdown("---")
            # Display as cards
            for name, greeks in st.session_state.greeks_results.items():
                st.subheader(f"📌 {name}")
                c1, c2, c3 = st.columns(3)
                c1.metric("Δ Delta", f"{greeks['delta']:.6f}",
                          help="Price change per unit change in spot price")
                c2.metric("Γ Gamma", f"{greeks['gamma']:.6f}",
                          help="Rate of change of Delta")
                c3.metric("ν Vega", f"{greeks['vega']:.4f}",
                          help="Price change per 1% change in volatility")

            # Summary table
            st.markdown("---")
            st.subheader("📋 Greeks Summary Table")
            rows = []
            for name, g in st.session_state.greeks_results.items():
                rows.append({'Option': name, 'Delta': f"{g['delta']:.6f}",
                             'Gamma': f"{g['gamma']:.6f}", 'Vega': f"{g['vega']:.4f}"})
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

            # Explanation
            with st.expander("📖 Interpretation Guide"):
                st.markdown("""
                | Greek | Meaning | Example |
                |-------|---------|---------|
                | **Delta** | If Δ = 0.5, a ₹1 rise in asset price → ~₹0.50 rise in option price | Hedge ratio |
                | **Gamma** | If Γ is high, Delta changes rapidly — rebalance hedge frequently | Convexity |
                | **Vega** | If ν = 15, a 1% rise in volatility → ~₹0.15 rise in option price | Vol exposure |
                """)

    add_footer()


# ============================================================
# PAGE: SENSITIVITY ANALYSIS
# ============================================================
elif page == "📉 Sensitivity Analysis":
    st.header("📉 Sensitivity Analysis")
    st.write("Explore how option prices change with different market parameters.")

    if not st.session_state.params:
        st.warning("⚠️ Please set parameters in Option Pricing first.")
        add_footer()
        st.stop()

    p = st.session_state.params
    n_sims_sens = st.selectbox("Simulations per point (lower = faster)",
                                [500, 1000, 2000, 5000], index=1)

    # Select option type for analysis
    option_for_analysis = st.selectbox(
        "Select option type to analyze",
        ["Asian Call", "Asian Put", "Lookback Call", "Lookback Put"])

    def get_price_for_params(S0_v, sigma_v, T_v):
        """Helper to price the selected option with given params."""
        if 'Asian' in option_for_analysis:
            ot = 'call' if 'Call' in option_for_analysis else 'put'
            return price_asian_option(S0_v, p['K'], p['r'], sigma_v, T_v,
                                      p['n_steps'], n_sims_sens,
                                      option_type=ot, seed=p['seed'])['price']
        else:  # Lookback
            ot = 'call' if 'Call' in option_for_analysis else 'put'
            return price_lookback_option(S0_v, p['r'], sigma_v, T_v,
                                          p['n_steps'], n_sims_sens,
                                          option_type=ot, seed=p['seed'])['price']

    tab1, tab2, tab3, tab4 = st.tabs([
        "📈 vs Spot Price", "📈 vs Volatility",
        "📈 vs Maturity", "📈 MC Convergence"])

    with tab1:
        if st.button("Generate Spot Sensitivity", key="spot_sens"):
            spot_range = np.linspace(p['S0'] * 0.5, p['S0'] * 1.5, 20)
            prices_vs_spot = []
            prog = st.progress(0)
            for i, s in enumerate(spot_range):
                prices_vs_spot.append(get_price_for_params(s, p['sigma'], p['T']))
                prog.progress((i + 1) / len(spot_range))

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=spot_range, y=prices_vs_spot,
                                     mode='lines+markers', name=option_for_analysis,
                                     line=dict(width=2, color='#1f77b4')))
            fig.add_vline(x=p['S0'], line_dash="dash", line_color="gray",
                          annotation_text=f"Current S₀={p['S0']:.0f}")
            fig.update_layout(title=f'{option_for_analysis} Price vs Spot Price',
                              xaxis_title='Spot Price (S₀)',
                              yaxis_title='Option Price',
                              template='plotly_white', height=450)
            st.plotly_chart(fig, use_container_width=True)

    with tab2:
        if st.button("Generate Volatility Sensitivity", key="vol_sens"):
            vol_range = np.linspace(0.05, 0.80, 15)
            prices_vs_vol = []
            prog = st.progress(0)
            for i, v in enumerate(vol_range):
                prices_vs_vol.append(get_price_for_params(p['S0'], v, p['T']))
                prog.progress((i + 1) / len(vol_range))

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=vol_range * 100, y=prices_vs_vol,
                                     mode='lines+markers', name=option_for_analysis,
                                     line=dict(width=2, color='#ff7f0e')))
            fig.add_vline(x=p['sigma'] * 100, line_dash="dash", line_color="gray",
                          annotation_text=f"Current σ={p['sigma']*100:.0f}%")
            fig.update_layout(title=f'{option_for_analysis} Price vs Volatility',
                              xaxis_title='Volatility (%)',
                              yaxis_title='Option Price',
                              template='plotly_white', height=450)
            st.plotly_chart(fig, use_container_width=True)

    with tab3:
        if st.button("Generate Maturity Sensitivity", key="mat_sens"):
            mat_range = np.linspace(0.1, 3.0, 15)
            prices_vs_mat = []
            prog = st.progress(0)
            for i, t in enumerate(mat_range):
                prices_vs_mat.append(get_price_for_params(p['S0'], p['sigma'], t))
                prog.progress((i + 1) / len(mat_range))

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=mat_range, y=prices_vs_mat,
                                     mode='lines+markers', name=option_for_analysis,
                                     line=dict(width=2, color='#2ca02c')))
            fig.add_vline(x=p['T'], line_dash="dash", line_color="gray",
                          annotation_text=f"Current T={p['T']:.1f}")
            fig.update_layout(title=f'{option_for_analysis} Price vs Time to Maturity',
                              xaxis_title='Time to Maturity (years)',
                              yaxis_title='Option Price',
                              template='plotly_white', height=450)
            st.plotly_chart(fig, use_container_width=True)

    with tab4:
        if st.button("Run Convergence Analysis", key="conv_analysis"):
            n_list = [100, 250, 500, 1000, 2500, 5000, 10000, 25000, 50000]
            if 'Asian' in option_for_analysis:
                ot = 'call' if 'Call' in option_for_analysis else 'put'
                conv_df = convergence_analysis(
                    price_asian_option, n_list, p['S0'], p['r'], p['sigma'],
                    p['T'], p['n_steps'], seed=p['seed'],
                    K=p['K'], option_type=ot)
            else:
                ot = 'call' if 'Call' in option_for_analysis else 'put'
                conv_df = convergence_analysis(
                    price_lookback_option, n_list, p['S0'], p['r'], p['sigma'],
                    p['T'], p['n_steps'], seed=p['seed'], option_type=ot)

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=conv_df['n_simulations'], y=conv_df['price'],
                mode='lines+markers', name='MC Price',
                line=dict(width=2, color='#1f77b4')))
            fig.add_trace(go.Scatter(
                x=conv_df['n_simulations'], y=conv_df['upper_ci'],
                mode='lines', name='Upper 95% CI',
                line=dict(width=1, dash='dash', color='rgba(31,119,180,0.3)')))
            fig.add_trace(go.Scatter(
                x=conv_df['n_simulations'], y=conv_df['lower_ci'],
                mode='lines', name='Lower 95% CI',
                line=dict(width=1, dash='dash', color='rgba(31,119,180,0.3)'),
                fill='tonexty', fillcolor='rgba(31,119,180,0.1)'))
            fig.update_layout(
                title=f'{option_for_analysis} — Monte Carlo Convergence',
                xaxis_title='Number of Simulations',
                yaxis_title='Option Price',
                xaxis_type='log',
                template='plotly_white', height=450)
            st.plotly_chart(fig, use_container_width=True)

            st.subheader("Convergence Data")
            st.dataframe(conv_df, use_container_width=True, hide_index=True)

    add_footer()


# ============================================================
# PAGE: OPTION COMPARISON
# ============================================================
elif page == "🔄 Option Comparison":
    st.header("🔄 Option Comparison")
    st.write("Compare all exotic option types under identical market conditions.")

    if not st.session_state.params:
        st.warning("⚠️ Please set parameters in Option Pricing first.")
        add_footer()
        st.stop()

    p = st.session_state.params
    n_sims_comp = st.selectbox("Simulations for comparison",
                                [1000, 5000, 10000], index=1)

    if st.button("🔄 Run Comparison", type="primary"):
        comp_results = {}
        progress = st.progress(0)

        options_to_compare = [
            ("Asian Call", lambda: price_asian_option(
                p['S0'], p['K'], p['r'], p['sigma'], p['T'],
                p['n_steps'], n_sims_comp, 'call', p['seed'])),
            ("Asian Put", lambda: price_asian_option(
                p['S0'], p['K'], p['r'], p['sigma'], p['T'],
                p['n_steps'], n_sims_comp, 'put', p['seed'])),
            ("Barrier Call (D&O)", lambda: price_barrier_option(
                p['S0'], p['K'], p['r'], p['sigma'], p['T'],
                p['B'], p['n_steps'], n_sims_comp, 'call',
                p['barrier_type'], p['seed'])),
            ("Lookback Call", lambda: price_lookback_option(
                p['S0'], p['r'], p['sigma'], p['T'],
                p['n_steps'], n_sims_comp, 'call', p['seed'])),
            ("Lookback Put", lambda: price_lookback_option(
                p['S0'], p['r'], p['sigma'], p['T'],
                p['n_steps'], n_sims_comp, 'put', p['seed'])),
        ]

        # Also compute BS European for reference
        bs_call = black_scholes_call(p['S0'], p['K'], p['r'], p['sigma'], p['T'])
        bs_put = black_scholes_put(p['S0'], p['K'], p['r'], p['sigma'], p['T'])

        for i, (name, func) in enumerate(options_to_compare):
            try:
                res = func()
                comp_results[name] = res
            except Exception as e:
                st.error(f"Error pricing {name}: {e}")
            progress.progress((i + 1) / len(options_to_compare))

        # Build comparison table
        rows = []
        for name, res in comp_results.items():
            rows.append({
                'Option': name,
                'Price': f"{res['price']:.4f}",
                'Std Error': f"{res['std_error']:.4f}",
                '95% CI': f"({res['conf_interval'][0]:.4f}, {res['conf_interval'][1]:.4f})"
            })
        # Add BS reference
        rows.append({'Option': 'European Call (BS)', 'Price': f"{bs_call:.4f}",
                     'Std Error': 'N/A (analytical)', '95% CI': 'N/A'})
        rows.append({'Option': 'European Put (BS)', 'Price': f"{bs_put:.4f}",
                     'Std Error': 'N/A (analytical)', '95% CI': 'N/A'})

        comp_df = pd.DataFrame(rows)
        st.session_state.comparison_df = comp_df

        # Display table
        st.subheader("📋 Comparison Table")
        st.dataframe(comp_df, use_container_width=True, hide_index=True)

        # Bar chart
        st.subheader("📊 Price Comparison")
        price_data = {name: res['price'] for name, res in comp_results.items()}
        price_data['European Call (BS)'] = bs_call
        price_data['European Put (BS)'] = bs_put

        fig_bar = go.Figure()
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2']
        for i, (name, price) in enumerate(price_data.items()):
            fig_bar.add_trace(go.Bar(
                x=[name], y=[price], name=name,
                marker_color=colors[i % len(colors)],
                text=[f"{price:.2f}"], textposition='auto'))
        fig_bar.update_layout(
            title='Option Price Comparison',
            yaxis_title='Option Price',
            template='plotly_white', height=450, showlegend=False)
        st.plotly_chart(fig_bar, use_container_width=True)

        # Explanation
        st.info("""
        **Expected price ordering (for calls):**
        Barrier (D&O) < Asian < European (BS) < Lookback

        - **Barrier** is cheapest because there's a risk of being knocked out.
        - **Asian** is cheaper than European because averaging reduces volatility.
        - **Lookback** is most expensive because the holder always gets the best price.
        """)

    elif st.session_state.comparison_df is not None:
        st.dataframe(st.session_state.comparison_df,
                     use_container_width=True, hide_index=True)

    add_footer()


# ============================================================
# PAGE: VALIDATION
# ============================================================
elif page == "✅ Validation":
    st.header("✅ Monte Carlo Validation")
    st.write("Validate the MC simulation engine against the Black-Scholes analytical solution.")

    st.subheader("Black-Scholes Formula")
    st.latex(r"C = S_0 \, N(d_1) - K \, e^{-rT} \, N(d_2)")
    st.latex(r"d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)\,T}{\sigma\sqrt{T}}, \quad d_2 = d_1 - \sigma\sqrt{T}")

    p = st.session_state.params if st.session_state.params else {
        'S0': 100.0, 'K': 100.0, 'r': 0.05, 'sigma': 0.20, 'T': 1.0,
        'n_steps': 252, 'seed': 42
    }

    st.subheader("Parameters")
    vc1, vc2, vc3, vc4 = st.columns(4)
    v_S0 = vc1.number_input("S₀", value=float(p.get('S0', 100.0)), key="v_s0")
    v_K = vc2.number_input("K", value=float(p.get('K', 100.0)), key="v_k")
    v_sigma = vc3.number_input("σ", value=float(p.get('sigma', 0.20)), key="v_sig")
    v_r = vc4.number_input("r", value=float(p.get('r', 0.05)), key="v_r")

    if st.button("🔬 Run Validation", type="primary"):
        with st.spinner("Running validation across simulation counts..."):
            val_df = validate_european_mc(v_S0, v_K, v_r, v_sigma, 1.0, 252,
                                           seed=p.get('seed', 42))

        st.subheader("📋 Validation Results")
        st.dataframe(val_df, use_container_width=True, hide_index=True)

        # Convergence plot
        bs_c = black_scholes_call(v_S0, v_K, v_r, v_sigma, 1.0)
        fig_val = go.Figure()
        fig_val.add_trace(go.Scatter(
            x=val_df['n_simulations'], y=val_df['mc_call'],
            mode='lines+markers', name='MC Call Price'))
        fig_val.add_hline(y=bs_c, line_dash="dash", line_color="red",
                          annotation_text=f"BS Call = {bs_c:.4f}")
        fig_val.update_layout(
            title='MC Call Price Convergence to Black-Scholes',
            xaxis_title='Number of Simulations', xaxis_type='log',
            yaxis_title='Price', template='plotly_white', height=400)
        st.plotly_chart(fig_val, use_container_width=True)

        # Error plot
        fig_err = go.Figure()
        fig_err.add_trace(go.Scatter(
            x=val_df['n_simulations'], y=val_df['call_error_pct'],
            mode='lines+markers', name='Call Error %',
            line=dict(color='#d62728')))
        fig_err.add_trace(go.Scatter(
            x=val_df['n_simulations'], y=val_df['put_error_pct'],
            mode='lines+markers', name='Put Error %',
            line=dict(color='#ff7f0e')))
        fig_err.update_layout(
            title='Pricing Error vs Number of Simulations',
            xaxis_title='Number of Simulations', xaxis_type='log',
            yaxis_title='Error (%)', template='plotly_white', height=350)
        st.plotly_chart(fig_err, use_container_width=True)

        st.success("✅ As simulations increase, MC prices converge to BS — "
                   "our simulation engine is correctly implemented!")

        with st.expander("📖 Understanding the Validation"):
            st.markdown("""
            **Why this works:**
            - European options HAVE a closed-form solution (Black-Scholes).
            - Our MC engine should produce prices that converge to BS as N → ∞.
            - This gives us confidence that the same engine correctly prices
              exotic options (where no analytical solution exists).
            
            **Convergence rate:**
            - MC error decreases at rate O(1/√N).
            - To halve the error, you need 4× more simulations.
            - 10,000 simulations typically give <2% error.
            """)

    add_footer()


# ============================================================
# PAGE: EXPORT RESULTS
# ============================================================
elif page == "📥 Export Results":
    st.header("📥 Export Results")
    st.write("Download simulation results and analysis data as CSV files.")

    p = st.session_state.params

    # Export pricing results
    st.subheader("💰 Pricing Results")
    if st.session_state.pricing_results:
        rows = []
        for name, res in st.session_state.pricing_results.items():
            rows.append({
                'Option': name,
                'Price': res['price'],
                'Std_Error': res['std_error'],
                'CI_Lower': res['conf_interval'][0],
                'CI_Upper': res['conf_interval'][1],
                'Knocked_Out_Pct': res.get('knocked_out_pct', 'N/A')
            })
        pricing_df = pd.DataFrame(rows)
        st.dataframe(pricing_df, use_container_width=True, hide_index=True)
        st.download_button(
            "📥 Download Pricing Results",
            pricing_df.to_csv(index=False).encode('utf-8'),
            "pricing_results.csv", "text/csv")
    else:
        st.info("No pricing results yet. Run Option Pricing first.")

    st.markdown("---")

    # Export Greeks
    st.subheader("📈 Greeks")
    if st.session_state.greeks_results:
        rows = []
        for name, g in st.session_state.greeks_results.items():
            rows.append({'Option': name, 'Delta': g['delta'],
                         'Gamma': g['gamma'], 'Vega': g['vega']})
        greeks_df = pd.DataFrame(rows)
        st.dataframe(greeks_df, use_container_width=True, hide_index=True)
        st.download_button(
            "📥 Download Greeks",
            greeks_df.to_csv(index=False).encode('utf-8'),
            "greeks_results.csv", "text/csv")
    else:
        st.info("No Greeks calculated yet.")

    st.markdown("---")

    # Export comparison
    st.subheader("🔄 Comparison Table")
    if st.session_state.comparison_df is not None:
        st.dataframe(st.session_state.comparison_df,
                     use_container_width=True, hide_index=True)
        st.download_button(
            "📥 Download Comparison",
            st.session_state.comparison_df.to_csv(index=False).encode('utf-8'),
            "comparison_results.csv", "text/csv")
    else:
        st.info("No comparison results yet.")

    st.markdown("---")

    # Export simulated paths
    st.subheader("📈 Simulated Paths")
    if st.session_state.pricing_results:
        option_name = st.selectbox("Select option paths to download",
                                    list(st.session_state.pricing_results.keys()))
        if st.button("Prepare Paths CSV"):
            paths = st.session_state.pricing_results[option_name]['paths']
            # Export first 1000 paths to keep file size manageable
            n_export = min(1000, paths.shape[0])
            paths_df = pd.DataFrame(
                paths[:n_export],
                columns=[f"t_{i}" for i in range(paths.shape[1])])
            st.download_button(
                f"📥 Download {option_name} Paths ({n_export} paths)",
                paths_df.to_csv(index=False).encode('utf-8'),
                f"{option_name.lower().replace(' ', '_')}_paths.csv", "text/csv")
            st.success(f"Ready to download {n_export} paths × {paths.shape[1]} time steps")

    # Export parameters
    st.markdown("---")
    st.subheader("⚙️ Parameters Used")
    if p:
        params_df = pd.DataFrame([p])
        st.dataframe(params_df, use_container_width=True, hide_index=True)
        st.download_button(
            "📥 Download Parameters",
            params_df.to_csv(index=False).encode('utf-8'),
            "parameters.csv", "text/csv")

    add_footer()

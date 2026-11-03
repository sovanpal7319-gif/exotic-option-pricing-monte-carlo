# 📊 Exotic Option Pricing and Risk Analysis Using Monte Carlo Simulation

A complete quantitative finance project that prices exotic options (Asian, Barrier, Lookback) using Monte Carlo simulation, analyzes risk through Greeks, and provides an interactive Streamlit dashboard.

## 👥 Team Members

| Name | Role |
|------|------|
| **Sayan Goswami** | Core Simulation & Option Pricing |
| **Sovan Pal** | Greeks, Validation & Risk Analysis |
| **Tanmoy Paul** | Dashboard, Visualization & Data Processing |

## ✨ Features

- **Monte Carlo Simulation** — Geometric Brownian Motion path generation
- **Asian Option Pricing** — Arithmetic-average call and put
- **Barrier Option Pricing** — Down-and-Out, Down-and-In, Up-and-Out, Up-and-In
- **Lookback Option Pricing** — Floating-strike call and put
- **Greeks Calculation** — Delta, Gamma, Vega via central finite differences
- **Black-Scholes Validation** — Verify MC engine against analytical solution
- **Interactive Dashboard** — Professional Streamlit UI with 8 pages
- **Sensitivity Analysis** — Price vs spot, volatility, maturity
- **Convergence Analysis** — MC estimation error vs simulation count
- **CSV Export** — Download all results and simulated paths
- **Historical Data Support** — Upload CSV from NSE/Yahoo Finance

## 📁 Project Structure

```
exotic_option_pricing/
├── app.py                    # Streamlit dashboard (main entry point)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
│
├── src/                      # Core modules
│   ├── __init__.py
│   ├── simulation.py         # GBM path generation engine
│   ├── asian_option.py       # Asian option pricing
│   ├── barrier_option.py     # Barrier option pricing
│   ├── lookback_option.py    # Lookback option pricing
│   ├── greeks.py             # Greeks (Delta, Gamma, Vega)
│   ├── data_processing.py    # CSV loading & parameter estimation
│   └── validation.py         # Black-Scholes validation
│
├── data/
│   └── sample_prices.csv     # Sample synthetic price data
│
├── tests/                    # Test suite
│   ├── test_simulation.py
│   ├── test_options.py
│   └── test_greeks.py
│
└── reports/
    ├── project_report.md     # Academic project report
    └── presentation_outline.md
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Steps

```bash
# 1. Navigate to the project directory
cd exotic_option_pricing

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the dashboard
streamlit run app.py

# 4. Open browser at http://localhost:8501
```

## 🧪 Running Tests

```bash
cd exotic_option_pricing
pip install pytest
python -m pytest tests/ -v
```

## 📖 Mathematical Background

### Geometric Brownian Motion (Risk-Neutral)

$$S(t+\Delta t) = S(t) \cdot \exp\left[\left(r - \frac{\sigma^2}{2}\right)\Delta t + \sigma\sqrt{\Delta t}\, Z\right]$$

### Monte Carlo Estimator

$$\hat{V} = e^{-rT} \cdot \frac{1}{N}\sum_{i=1}^{N} \text{Payoff}_i$$

### Option Payoffs

| Option | Call Payoff | Put Payoff |
|--------|------------|------------|
| **Asian** | max(Avg(S) - K, 0) | max(K - Avg(S), 0) |
| **Barrier (D&O)** | max(S_T - K, 0) · I[min(S) > B] | max(K - S_T, 0) · I[min(S) > B] |
| **Lookback** | S_T - S_min | S_max - S_T |

### Greeks (Finite Differences)

| Greek | Formula |
|-------|---------|
| Delta | [V(S+h) - V(S-h)] / (2h) |
| Gamma | [V(S+h) - 2V(S) + V(S-h)] / h² |
| Vega | [V(σ+ε) - V(σ-ε)] / (2ε) |

## 🛠️ Technologies

- **Python** — Programming language
- **NumPy** — Numerical computation & simulation
- **Pandas** — Data processing
- **SciPy** — Statistical functions (normal CDF for Black-Scholes)
- **Plotly** — Interactive visualizations
- **Streamlit** — Web dashboard framework

## 📊 Dashboard Pages

1. **🏠 Home** — Project overview, team, and exotic options introduction
2. **📊 Market Data** — Upload CSV, estimate volatility from historical data
3. **💰 Option Pricing** — Configure parameters and run Monte Carlo simulation
4. **📈 Risk Analysis** — Calculate and display Greeks
5. **📉 Sensitivity Analysis** — Price sensitivity to spot, vol, maturity
6. **🔄 Option Comparison** — Side-by-side comparison of all option types
7. **✅ Validation** — Black-Scholes benchmark comparison
8. **📥 Export Results** — Download all results as CSV

## ⚠️ Disclaimer

- Simulated prices are **NOT** predictions of future market prices.
- Sample data is **synthetic** (generated via GBM), not real market data.
- This project is for **educational purposes** only.
- The GBM model assumes constant volatility and no dividends.

## 📜 License

MIT License — Free for educational and academic use.


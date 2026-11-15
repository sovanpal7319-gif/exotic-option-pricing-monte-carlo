# 📊 Exotic Option Pricing and Risk Analysis Using Monte Carlo Simulation

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-FF4B4B?logo=streamlit&logoColor=white)
![NumPy](https://img.shields.io/badge/NumPy-1.24%2B-013243?logo=numpy&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Tests](https://img.shields.io/badge/Tests-36%20passed-brightgreen)

A complete quantitative finance project that prices exotic options (Asian, Barrier, Lookback) using Monte Carlo simulation, analyzes risk through Greeks, and provides an interactive Streamlit dashboard.


## ✨ Features

- **Monte Carlo Simulation** — Geometric Brownian Motion path generation with antithetic variates
- **Asian Option Pricing** — Arithmetic-average call and put
- **Barrier Option Pricing** — Down-and-Out, Down-and-In, Up-and-Out, Up-and-In (call & put)
- **Lookback Option Pricing** — Floating-strike call and put
- **Greeks Calculation** — Delta, Gamma, Vega via central finite differences
- **Black-Scholes Validation** — Verify MC engine against analytical solution
- **Interactive Dashboard** — Professional Streamlit UI with 8 pages
- **Sensitivity Analysis** — Price vs spot, volatility, maturity
- **Convergence Analysis** — MC estimation error vs simulation count
- **CSV Export** — Download all results and simulated paths
- **Historical Data Support** — Upload CSV from NSE India / Yahoo Finance

---

## 📁 Project Structure

```
exotic_option_pricing/
│
├── app.py                        # Streamlit dashboard (main entry point)
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── LICENSE                       # MIT License
│
├── src/                          # Core pricing modules
│   ├── __init__.py               # Package exports
│   ├── simulation.py             # GBM path generation engine
│   ├── asian_option.py           # Asian option pricing
│   ├── barrier_option.py         # Barrier option pricing
│   ├── lookback_option.py        # Lookback option pricing
│   ├── greeks.py                 # Greeks (Delta, Gamma, Vega)
│   ├── data_processing.py        # CSV loading & volatility estimation
│   └── validation.py             # Black-Scholes validation & convergence
│
├── data/
│   └── sample_prices.csv         # Sample synthetic price data (for testing)
│
├── tests/                        # Unit test suite (36 tests)
│   ├── __init__.py
│   ├── test_simulation.py        # GBM path tests
│   ├── test_options.py           # Option pricing tests
│   └── test_greeks.py            # Greeks calculation tests
│
└── reports/                      # Academic documentation
    ├── project_report.md         # Full project report (21 sections)
    └── presentation_outline.md   # 25-slide outline + viva Q&A
```

---

## 🚀 Installation & Usage

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/exotic-option-pricing.git
cd exotic-option-pricing

# Install dependencies
pip install -r requirements.txt

# Launch the dashboard
streamlit run app.py
```

The dashboard will open at **http://localhost:8501**

### Running Tests

```bash
python -m pytest tests/ -v
```

---

## 📊 Dashboard Pages

| Page | Description |
|------|-------------|
| 🏠 **Home** | Project overview, abstract, team members |
| 📊 **Market Data** | Upload historical CSV, estimate volatility |
| 💰 **Option Pricing** | Configure parameters, run Monte Carlo simulation |
| 📈 **Risk Analysis** | Calculate and display Delta, Gamma, Vega |
| 📉 **Sensitivity** | Price sensitivity to spot, volatility, maturity |
| 🔄 **Comparison** | Side-by-side comparison of all option types |
| ✅ **Validation** | Black-Scholes benchmark convergence proof |
| 📥 **Export** | Download all results as CSV |

---

## 📖 Mathematical Background

### Geometric Brownian Motion (Risk-Neutral)

$$S(t+\Delta t) = S(t) \cdot \exp\left[\left(r - \frac{\sigma^2}{2}\right)\Delta t + \sigma\sqrt{\Delta t}\, Z\right]$$

where $Z \sim \mathcal{N}(0,1)$, $r$ is the risk-free rate, and $\sigma$ is the volatility.

### Monte Carlo Estimator

$$\hat{V} = e^{-rT} \cdot \frac{1}{N}\sum_{i=1}^{N} \text{Payoff}_i \quad \pm \quad 1.96 \times \frac{\hat{\sigma}}{\sqrt{N}}$$

### Option Payoffs

| Option Type | Call Payoff | Put Payoff |
|-------------|------------|------------|
| **Asian** (arithmetic avg.) | $\max(\bar{S} - K,\; 0)$ | $\max(K - \bar{S},\; 0)$ |
| **Barrier** (down-and-out) | $\max(S_T - K,\; 0) \cdot \mathbf{1}[\min S > B]$ | $\max(K - S_T,\; 0) \cdot \mathbf{1}[\min S > B]$ |
| **Lookback** (floating strike) | $S_T - S_{\min}$ | $S_{\max} - S_T$ |

### Greeks (Central Finite Differences)

| Greek | Formula | Interpretation |
|-------|---------|----------------|
| **Delta (Δ)** | $\frac{V(S+h) - V(S-h)}{2h}$ | Price sensitivity to spot |
| **Gamma (Γ)** | $\frac{V(S+h) - 2V(S) + V(S-h)}{h^2}$ | Curvature of Delta |
| **Vega (ν)** | $\frac{V(\sigma+\varepsilon) - V(\sigma-\varepsilon)}{2\varepsilon}$ | Sensitivity to volatility |

---

## 🛠️ Technology Stack

| Technology | Purpose |
|------------|---------|
| **Python** | Programming language |
| **NumPy** | Numerical computation & simulation |
| **Pandas** | Data processing & CSV handling |
| **SciPy** | Statistical functions (normal CDF for Black-Scholes) |
| **Plotly** | Interactive visualizations |
| **Streamlit** | Web dashboard framework |

---

## 📈 Sample Results

Parameters: $S_0 = 100$, $K = 100$, $r = 5\%$, $\sigma = 20\%$, $T = 1$ year, $N = 10{,}000$

| Option | Price | Std Error |
|--------|-------|-----------|
| Asian Call | 5.70 | 0.079 |
| Asian Put | 3.44 | 0.054 |
| Barrier Call (D&O, B=80) | 10.14 | 0.145 |
| Lookback Call | 16.51 | 0.144 |
| Lookback Put | 13.46 | 0.099 |
| European Call (Black-Scholes) | 10.45 | — |

**Price ordering:** Barrier < Asian < European < Lookback ✅

---

## ⚠️ Disclaimer

- Simulated prices are **NOT** predictions of future market prices.
- Sample data (`data/sample_prices.csv`) is **synthetic** (GBM-generated), not real market data.
- This project is for **educational and academic purposes** only.
- The GBM model assumes constant volatility, no dividends, and continuous trading.

---

## 📚 References

1. Black, F., & Scholes, M. (1973). *The Pricing of Options and Corporate Liabilities.* Journal of Political Economy.
2. Boyle, P. P. (1977). *Options: A Monte Carlo Approach.* Journal of Financial Economics.
3. Hull, J. C. (2018). *Options, Futures, and Other Derivatives* (10th ed.). Pearson.
4. Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering.* Springer.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

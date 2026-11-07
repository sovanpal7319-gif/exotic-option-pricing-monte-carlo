# Exotic Option Pricing and Risk Analysis Using Monte Carlo Simulation

**Project Report**

**Team Members:** Sayan Goswami, Sovan Pal, Tanmoy Paul

---

## 1. Introduction

Financial derivatives are contracts whose value is derived from the price of an underlying asset, such as a stock, index, commodity, or currency. Among derivatives, **options** grant the holder the right — but not the obligation — to buy or sell the underlying asset at a predetermined price (the strike price) on or before a specified date (the maturity date).

While standard European and American options are widely traded and well understood, the financial industry has developed a rich class of **exotic options** with more complex payoff structures. These exotic options are designed to meet specific hedging or speculative needs that standard options cannot efficiently address.

This project focuses on three important types of exotic options:

1. **Asian options** — payoff depends on the average price over the option's lifetime
2. **Barrier options** — payoff depends on whether the price crosses a predetermined barrier level
3. **Lookback options** — payoff depends on the maximum or minimum price during the option's lifetime

Unlike standard European options, most exotic options have **no closed-form analytical solution**. This makes numerical methods — particularly Monte Carlo simulation — essential for pricing them.

The project demonstrates the practical application of mathematical and quantitative techniques in option pricing and risk analysis, using Python as the implementation platform and providing an interactive dashboard for exploration.

---

## 2. Abstract

This project implements a comprehensive framework for pricing exotic options and analyzing their associated financial risks using Monte Carlo simulation. We simulate thousands of possible future asset-price paths using Geometric Brownian Motion (GBM) under the risk-neutral measure, and use these paths to estimate the fair value of Asian (arithmetic-average), Barrier (knock-in and knock-out), and Lookback (floating-strike) options. The project further analyzes option price sensitivity using the Greeks — Delta, Gamma, and Vega — computed via central finite-difference approximations. An interactive Streamlit dashboard provides parameter configuration, real-time pricing, sensitivity analysis, option comparison, and Black-Scholes validation. All results are exportable as CSV files. The implementation is validated by comparing Monte Carlo European option prices against the Black-Scholes analytical solution, confirming convergence at rate $O(1/\sqrt{N})$. The project demonstrates that Monte Carlo simulation is a flexible and powerful tool for pricing path-dependent derivatives where analytical solutions do not exist.

---

## 3. Problem Statement

Standard European options can be priced using the Black-Scholes formula, which provides a closed-form analytical solution. However, **exotic options** have more complex payoff structures that depend on the entire price path — not just the terminal price — making their pricing significantly more challenging.

Specifically:

- **Asian options** require computing the average of all prices along the path. The arithmetic average of lognormal variables does not follow a known distribution, so no exact closed-form solution exists.
- **Barrier options** require monitoring whether the price crosses a barrier at any point during the option's life, introducing path dependency.
- **Lookback options** require tracking the running maximum or minimum of the price path.

These complexities mean that analytical pricing is either impossible or extremely difficult for most exotic options. **Monte Carlo simulation** provides a flexible numerical approach that can handle arbitrary payoff structures by simulating many possible future scenarios.

The project aims to:
1. Estimate the fair value of selected exotic options
2. Understand how changes in market parameters affect option prices
3. Measure and visualize the associated financial risks

---

## 4. Objectives

1. Implement a Monte Carlo simulation engine based on Geometric Brownian Motion under the risk-neutral measure
2. Price arithmetic-average Asian call and put options
3. Price barrier options (Down-and-Out, Down-and-In, Up-and-Out, Up-and-In) for both calls and puts
4. Price floating-strike Lookback call and put options
5. Calculate Greeks (Delta, Gamma, Vega) using central finite-difference approximations
6. Analyze how option prices change with different market parameters (spot price, volatility, maturity)
7. Validate the Monte Carlo implementation against the Black-Scholes analytical solution
8. Develop an interactive dashboard for exploration, comparison, and export of results

---

## 5. Literature and Conceptual Background

### 5.1 History of Option Pricing

The modern theory of option pricing began with the seminal work of **Black and Scholes (1973)** and **Merton (1973)**, who derived a closed-form formula for European option prices under certain assumptions (constant volatility, no dividends, continuous trading, lognormal asset prices). This formula revolutionized finance and earned Scholes and Merton the 1997 Nobel Prize in Economics.

The Black-Scholes model assumes that the asset price follows a **Geometric Brownian Motion** (GBM):

$$dS = \mu \, S \, dt + \sigma \, S \, dW$$

where $\mu$ is the drift (expected return), $\sigma$ is the volatility, and $dW$ is a Wiener process (Brownian motion).

### 5.2 Monte Carlo Methods in Finance

**Boyle (1977)** was the first to apply Monte Carlo simulation to option pricing. The idea is simple but powerful:

1. Simulate many possible future price paths
2. Calculate the option payoff for each path
3. Take the average payoff
4. Discount to present value

Monte Carlo methods are particularly valuable for **path-dependent options** (where the payoff depends on the entire price trajectory, not just the terminal price) and for **high-dimensional problems** (options on multiple assets).

### 5.3 Exotic Options

Exotic options are non-standard options with payoff structures more complex than plain vanilla calls and puts. They were developed to meet specific hedging and trading needs. Key references include **Hull (2018)** for a comprehensive treatment and **Wilmott (2006)** for quantitative perspectives.

### 5.4 Risk-Neutral Pricing

The **Fundamental Theorem of Asset Pricing** states that in an arbitrage-free market, there exists a probability measure — the **risk-neutral measure** — under which all asset prices are martingales when discounted at the risk-free rate. Under this measure:

$$\text{Option Price} = e^{-rT} \, \mathbb{E}^Q[\text{Payoff}]$$

This is the theoretical foundation for Monte Carlo pricing: we simulate under the risk-neutral measure (using drift $r$ instead of $\mu$) and discount expected payoffs at the risk-free rate.

### 5.5 Key References

1. Black, F., & Scholes, M. (1973). *The Pricing of Options and Corporate Liabilities.* Journal of Political Economy.
2. Boyle, P. P. (1977). *Options: A Monte Carlo Approach.* Journal of Financial Economics.
3. Hull, J. C. (2018). *Options, Futures, and Other Derivatives* (10th ed.). Pearson.
4. Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering.* Springer.

---

## 6. Financial Mathematics

### 6.1 Geometric Brownian Motion

In the **real world**, the asset price follows:

$$dS = \mu \, S \, dt + \sigma \, S \, dW$$

Under the **risk-neutral measure**, we replace the real-world drift $\mu$ with the risk-free rate $r$:

$$dS = r \, S \, dt + \sigma \, S \, dW$$

**Why do we use $r$ instead of $\mu$?**

The key insight of risk-neutral pricing is that the actual expected return of the asset ($\mu$) does not matter for derivative pricing. Under the risk-neutral measure, all assets earn the risk-free rate in expectation. This allows us to compute expected payoffs and discount them at $r$. The mathematics works because of the Fundamental Theorem of Asset Pricing — in an arbitrage-free complete market, this risk-neutral price equals the unique fair price of the derivative.

**Discretized Simulation Formula:**

Using **Itô's lemma** to solve the SDE, we get the exact discrete-time formula:

$$S(t + \Delta t) = S(t) \cdot \exp\left[\left(r - \frac{\sigma^2}{2}\right)\Delta t + \sigma \sqrt{\Delta t} \, Z\right]$$

where $Z \sim \mathcal{N}(0, 1)$ is a standard normal random variable.

**Understanding each term:**

- $r \, \Delta t$: the risk-free drift over one time step
- $-\frac{\sigma^2}{2} \, \Delta t$: the **Itô correction** — this ensures that the expected value of $S(t+\Delta t)$ equals $S(t) \cdot e^{r \Delta t}$. Without this correction, the exponential of the diffusion term would cause an upward bias.
- $\sigma \sqrt{\Delta t} \, Z$: the random component, scaled by volatility and the square root of the time step

### 6.2 Monte Carlo Estimation

The Monte Carlo estimator for the option price is:

$$\hat{V} = e^{-rT} \cdot \frac{1}{N} \sum_{i=1}^{N} \text{Payoff}_i$$

**Standard Error:**

$$SE = \frac{\hat{\sigma}_{\text{payoff}}}{\sqrt{N}}$$

where $\hat{\sigma}_{\text{payoff}}$ is the sample standard deviation of the discounted payoffs.

**95% Confidence Interval:**

$$\hat{V} \pm 1.96 \times SE$$

**Convergence Rate:**

By the Central Limit Theorem, the MC estimator converges at rate $O(1/\sqrt{N})$. This means:
- To halve the error, you need **4 times** more simulations
- 10,000 simulations typically give errors within 2% of the true price
- 100,000 simulations give errors within about 0.6%

### 6.3 Asian Option Pricing

**Definition:** An Asian option's payoff depends on the average price of the underlying asset over a specified set of monitoring dates.

**Arithmetic Average:** Given $M$ monitoring dates $t_1, t_2, \ldots, t_M$:

$$\bar{S} = \frac{1}{M} \sum_{j=1}^{M} S(t_j)$$

**Payoffs:**

| Type | Formula |
|------|---------|
| **Call** | $\max(\bar{S} - K, 0)$ |
| **Put** | $\max(K - \bar{S}, 0)$ |

**Why is there no closed-form solution?**

The geometric average of lognormal variables is lognormal, so geometric-average Asian options have analytical solutions. However, the **arithmetic** average of lognormal variables does **not** follow a known distribution. This is why Monte Carlo simulation is the standard method for arithmetic-average Asian options.

**Why are Asian options cheaper than European options?**

The averaging process reduces the effective volatility of the payoff variable. Since option prices increase with volatility (higher uncertainty → higher option value), the reduced effective volatility makes Asian options cheaper. In simple terms, it is harder for the average to be extreme than for a single terminal price to be extreme.

**Practical use:** Asian options are common in commodity and foreign exchange markets, where they protect against price manipulation near the expiry date.

### 6.4 Barrier Option Pricing

**Definition:** A barrier option is activated or deactivated when the underlying asset price crosses a predetermined barrier level $B$.

**Four Types:**

| Type | Condition | Effect |
|------|-----------|--------|
| **Down-and-Out** | Price falls to or below $B$ | Option is knocked out (worthless) |
| **Down-and-In** | Price falls to or below $B$ | Option is activated |
| **Up-and-Out** | Price rises to or above $B$ | Option is knocked out (worthless) |
| **Up-and-In** | Price rises to or above $B$ | Option is activated |

**Down-and-Out Call Payoff:**

$$\text{Payoff} = \max(S_T - K, 0) \cdot \mathbf{1}\left[\min_{j=0,\ldots,M} S(t_j) > B\right]$$

where $\mathbf{1}[\cdot]$ is the indicator function — it equals 1 if the condition is true, 0 otherwise.

**In-Out Parity:**

$$\text{Knock-In Price} + \text{Knock-Out Price} = \text{Vanilla Price}$$

This parity relation holds because either the barrier is hit (knock-in active) or it is not hit (knock-out active), but never both. Together, they cover all possible scenarios, which is exactly the vanilla option.

**Why are barrier options cheaper?**

Because there is a chance the option gets knocked out (for knock-out types) or never activated (for knock-in types), reducing the expected payoff compared to a vanilla option.

### 6.5 Lookback Option Pricing

**Definition:** A lookback option's payoff depends on the maximum or minimum price achieved during the option's lifetime.

**Floating-Strike Lookback:**

| Type | Payoff | Interpretation |
|------|--------|----------------|
| **Call** | $S_T - S_{\min}$ | Buy at the lowest price, sell at expiry |
| **Put** | $S_{\max} - S_T$ | Sell at the highest price, buy back at expiry |

**Key Property: Always In the Money**

- For a call: $S_T \geq S_{\min}$ always, so $S_T - S_{\min} \geq 0$
- For a put: $S_{\max} \geq S_T$ always, so $S_{\max} - S_T \geq 0$

This guarantee makes lookback options more expensive than any fixed-strike option.

**Why are lookback options expensive?**

The holder effectively gets the benefit of "perfect hindsight" — buying at the lowest point or selling at the highest point. This is an extremely valuable right, so lookback options command a significant premium.

### 6.6 Greeks

Greeks measure how the option price responds to small changes in market parameters. They are essential for **hedging** (reducing risk) and **risk management**.

**Delta ($\Delta$) — Sensitivity to Asset Price:**

$$\Delta = \frac{\partial V}{\partial S} \approx \frac{V(S + h) - V(S - h)}{2h}$$

where $h = 0.01 \times S_0$ (1% of the current price).

*Interpretation:* If $\Delta = 0.5$, then a ₹1 increase in the asset price causes approximately a ₹0.50 increase in the option price. Delta is also the **hedge ratio** — to create a delta-neutral portfolio, hold $\Delta$ units of the underlying asset for each option sold.

**Gamma ($\Gamma$) — Sensitivity of Delta:**

$$\Gamma = \frac{\partial^2 V}{\partial S^2} \approx \frac{V(S + h) - 2V(S) + V(S - h)}{h^2}$$

*Interpretation:* Gamma measures how quickly Delta changes. High Gamma means the hedge must be rebalanced frequently. Gamma is always positive for long option positions (convexity).

**Vega ($\nu$) — Sensitivity to Volatility:**

$$\nu = \frac{\partial V}{\partial \sigma} \approx \frac{V(\sigma + \varepsilon) - V(\sigma - \varepsilon)}{2\varepsilon}$$

where $\varepsilon = 0.01$ (1 percentage point).

*Interpretation:* If $\nu = 15$, then a 1 percentage point increase in volatility causes approximately a ₹0.15 increase in the option price. Vega is always positive for long options — higher volatility increases option value.

**Why numerical (finite difference) Greeks?**

For exotic options, there are no closed-form expressions for Greeks. We must compute them numerically by "bumping" a parameter, re-pricing, and computing the slope. We use **central finite differences** because they provide $O(h^2)$ accuracy, which is better than forward differences ($O(h)$ accuracy).

**Important:** We use the **same random seed** for all bumped prices. This ensures that price differences come from the parameter change, not from different random draws — dramatically reducing noise in the Greek estimates.

---

## 7. Methodology

The overall methodology follows these steps:

1. **Parameter Selection:** Choose market parameters — initial price ($S_0$), strike ($K$), risk-free rate ($r$), volatility ($\sigma$), maturity ($T$), and barrier ($B$) if applicable.

2. **Path Simulation:** Generate $N$ (typically 10,000–100,000) price paths using the discretized GBM formula with $M$ time steps each.

3. **Payoff Calculation:** For each simulated path, compute the option payoff according to the specific exotic option type.

4. **Discounting:** Discount each payoff to present value using the factor $e^{-rT}$.

5. **Price Estimation:** The option price is the average of the discounted payoffs, with standard error and confidence interval.

6. **Greeks Calculation:** Re-price the option with bumped parameters to estimate Delta, Gamma, and Vega.

7. **Validation:** Compare Monte Carlo European option prices against the Black-Scholes analytical solution to verify the simulation engine.

8. **Sensitivity Analysis:** Vary parameters systematically and plot how the option price responds.

---

## 8. Monte Carlo Simulation Implementation

### Algorithm

```
Input: S0, r, sigma, T, n_steps, n_simulations, seed
Output: paths array of shape (n_simulations, n_steps + 1)

1. Set dt = T / n_steps
2. Initialize random number generator with seed
3. Generate Z matrix of shape (n_simulations, n_steps) from N(0,1)
4. Compute drift = (r - sigma²/2) * dt
5. Compute diffusion = sigma * sqrt(dt) * Z
6. Compute log_returns = drift + diffusion
7. Compute cumulative_log_returns = cumsum(log_returns, axis=1)
8. Prepend column of zeros (for t=0)
9. Compute paths = S0 * exp(cumulative_log_returns)
10. Return paths
```

**Key implementation decisions:**

- **Vectorized operations:** All random numbers are generated at once ($N \times M$ matrix), and path construction uses NumPy's cumulative sum. This avoids slow Python for-loops and leverages optimized C/Fortran libraries.
- **Reproducible seeds:** We use `np.random.RandomState(seed)` to ensure identical results across runs.
- **Cumulative sum of log-returns:** Instead of multiplying step-by-step, we sum log-returns and exponentiate once. This is numerically more stable and faster.

---

## 9. Asian Option Pricing

### Implementation

1. Simulate $N$ paths, each with $M$ time steps
2. For each path, compute the arithmetic average: $\bar{S}_i = \frac{1}{M}\sum_{j=1}^{M} S_i(t_j)$
   - We average over monitoring dates $t_1$ through $t_M$ (excluding the initial price $S_0$)
3. Compute payoff: $\text{Payoff}_i = \max(\bar{S}_i - K, 0)$ for calls
4. Discount: $V = e^{-rT} \cdot \frac{1}{N}\sum_{i=1}^{N} \text{Payoff}_i$

### Example Walkthrough

With $S_0 = 100$, $K = 100$, $r = 0.05$, $\sigma = 0.20$, $T = 1$ year, and 10,000 simulations:

- The Asian call price is typically around ₹5.5–6.5 (compared to ~₹10.45 for a European call)
- The lower price reflects the reduced effective volatility from averaging

---

## 10. Barrier Option Pricing

### Implementation

1. Simulate $N$ paths
2. For each path, check if the barrier condition is triggered at any monitoring date
3. For **Down-and-Out**: if $\min_j S(t_j) \leq B$, the option is knocked out (payoff = 0)
4. For surviving paths, compute vanilla payoff: $\max(S_T - K, 0)$
5. Discount the average payoff

### Impact of Barrier Level

- **Barrier close to $S_0$:** Many paths get knocked out → very cheap option
- **Barrier far below $S_0$:** Few paths get knocked out → price approaches European option price
- As $B \to 0$: knock-out probability → 0, barrier price → vanilla price
- As $B \to S_0$: knock-out probability → 100%, barrier price → 0

---

## 11. Lookback Option Pricing

### Implementation

1. Simulate $N$ paths
2. For each path, find $S_{\min} = \min_j S(t_j)$ and $S_{\max} = \max_j S(t_j)$
3. For **call**: $\text{Payoff}_i = S_T^{(i)} - S_{\min}^{(i)}$
4. For **put**: $\text{Payoff}_i = S_{\max}^{(i)} - S_T^{(i)}$
5. All payoffs are non-negative by construction
6. Discount the average payoff

### Impact of Path Resolution

More time steps (finer monitoring) generally **increases** the lookback option price because:
- More observations → higher probability of capturing extreme prices
- The true continuous maximum/minimum is always at least as extreme as any discrete sample

---

## 12. Greeks and Risk Analysis

### Implementation

For each Greek, we re-price the option with bumped parameters while keeping the **same random seed** to minimize noise.

**Delta calculation example:**
```
h = 0.01 * S0        # Bump = 1% of spot
V_up = Price(S0 + h)  # Price with spot bumped up
V_down = Price(S0 - h) # Price with spot bumped down
Delta = (V_up - V_down) / (2 * h)
```

**Typical results** for an ATM Asian Call ($S_0 = K = 100$, $\sigma = 20\%$, $T = 1$yr):
- Delta ≈ 0.55 (positive — call gains value when spot rises)
- Gamma ≈ 0.02 (positive — Delta increases as spot rises)
- Vega ≈ 15–20 (positive — option gains value when volatility rises)

---

## 13. Dataset Description

### Historical Data Usage

The application supports uploading historical price data in CSV format from sources such as:
- **NSE India** (https://www.nseindia.com/)
- **Yahoo Finance** (https://finance.yahoo.com/)

The data is used to **estimate realistic model parameters** — specifically the initial asset price ($S_0$) and historical volatility ($\sigma$).

### Volatility Estimation

From historical closing prices, we compute:

1. **Daily log returns:** $r_t = \ln(S_t / S_{t-1})$
2. **Daily volatility:** $\sigma_{\text{daily}} = \text{std}(r_t)$
3. **Annualized volatility:** $\sigma = \sigma_{\text{daily}} \times \sqrt{252}$

where 252 is the typical number of trading days per year.

### Important Distinction

| Data Type | Source | Description |
|-----------|--------|-------------|
| **Historical data** | Real market CSV | Actual past prices |
| **Estimated parameters** | Derived from historical data | $S_0$, $\sigma$ |
| **Simulated paths** | Generated by GBM | Possible future scenarios — NOT predictions |

### Sample Data

A sample synthetic dataset (`data/sample_prices.csv`) is provided for testing. This data is generated using GBM and is **clearly not real market data**. Users should use real data from NSE or Yahoo Finance for meaningful analysis.

---

## 14. System Architecture

```
┌──────────────────────────────────────────────────────────┐
│                    Streamlit Dashboard                    │
│  ┌──────┐ ┌──────────┐ ┌────────┐ ┌──────────┐ ┌──────┐│
│  │ Home │ │ Mkt Data │ │Pricing │ │ Greeks   │ │Export ││
│  └──┬───┘ └─────┬────┘ └───┬────┘ └────┬─────┘ └──┬───┘│
│     │           │           │           │          │     │
└─────┼───────────┼───────────┼───────────┼──────────┼─────┘
      │           │           │           │          │
┌─────┴───────────┴───────────┴───────────┴──────────┴─────┐
│                    Source Modules (src/)                   │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ simulation │  │ asian_option │  │ barrier_option   │  │
│  └────────────┘  └──────────────┘  └──────────────────┘  │
│  ┌────────────┐  ┌──────────────┐  ┌──────────────────┐  │
│  │ lookback   │  │   greeks     │  │ data_processing  │  │
│  └────────────┘  └──────────────┘  └──────────────────┘  │
│  ┌────────────┐                                          │
│  │ validation │                                          │
│  └────────────┘                                          │
└──────────────────────────────────────────────────────────┘
      │           │           │           │
┌─────┴───────────┴───────────┴───────────┴────────────────┐
│          Python Libraries: NumPy, Pandas, SciPy,         │
│                      Plotly, Streamlit                    │
└──────────────────────────────────────────────────────────┘
```

### Technology Stack Justification

| Technology | Reason |
|------------|--------|
| **Python** | De facto standard for quantitative finance, rich ecosystem |
| **NumPy** | Vectorized numerical operations, fast random number generation |
| **Pandas** | Data loading, cleaning, tabular operations |
| **SciPy** | Normal CDF for Black-Scholes (scipy.stats.norm) |
| **Plotly** | Interactive charts with hover, zoom, pan capabilities |
| **Streamlit** | Rapid web dashboard development, widgets, session state |

---

## 15. Implementation Details

### Code Organization

Each module has a single responsibility:
- `simulation.py` — knows nothing about options; just generates price paths
- Each option module (`asian_option.py`, etc.) — imports simulation, knows its payoff formula
- `greeks.py` — generic; accepts any pricing function and bumps parameters
- `validation.py` — compares MC against analytical solutions
- `data_processing.py` — handles real-world data loading and parameter estimation
- `app.py` — orchestrates everything through the Streamlit UI

### Key Design Decision: Generic Greeks

The Greeks module accepts a **callable** pricing function as input. This means the same `calculate_delta` function works for Asian, Barrier, and Lookback options without any code changes. The extra parameters (strike, barrier, option type) are passed through `**kwargs`.

### Error Handling

- Input validation at the start of every pricing function
- Barrier level validation (down barriers must be below spot, up barriers above)
- Graceful error handling in the dashboard with user-friendly error messages
- Numerical edge cases: clamping negative prices, handling zero-division

---

## 16. Results and Analysis

### Sample Results (S₀ = 100, K = 100, r = 5%, σ = 20%, T = 1 year, N = 10,000)

| Option Type | Price | Std Error | 95% CI |
|-------------|-------|-----------|--------|
| Asian Call | ~5.80 | ~0.07 | (5.66, 5.94) |
| Asian Put | ~3.95 | ~0.05 | (3.85, 4.05) |
| Barrier Call (D&O, B=80) | ~8.50 | ~0.12 | (8.26, 8.74) |
| Lookback Call | ~16.50 | ~0.12 | (16.26, 16.74) |
| Lookback Put | ~12.80 | ~0.10 | (12.60, 13.00) |
| European Call (BS) | 10.45 | — | — |
| European Put (BS) | 5.57 | — | — |

*Note: MC results vary slightly with seed. Values are approximate.*

### Key Observations

1. **Price Ordering (Calls):** Barrier (D&O) < Asian < European < Lookback
   - Barrier is cheapest due to knock-out risk
   - Asian is cheaper than European due to averaging
   - Lookback is most expensive due to perfect hindsight

2. **Volatility Effect:** All exotic option prices increase with volatility, but lookback options are most sensitive (highest Vega).

3. **Convergence:** MC prices converge to stable values by ~10,000 simulations, with standard errors below 2% of the price.

---

## 17. Validation

### Black-Scholes Comparison

We validate our MC engine by pricing **European** call and put options — for which the Black-Scholes formula provides exact analytical prices.

**Validation Results (S₀ = 100, K = 100, r = 5%, σ = 20%, T = 1 year):**

| N (simulations) | MC Call | BS Call | Error (%) |
|-----------------|---------|---------|-----------|
| 100 | ~10.5 | 10.45 | ~5% |
| 1,000 | ~10.3 | 10.45 | ~1.5% |
| 10,000 | ~10.42 | 10.45 | ~0.3% |
| 50,000 | ~10.44 | 10.45 | ~0.1% |

The error decreases at rate $O(1/\sqrt{N})$, confirming correct implementation.

### Property Verification

| Property | Expected | Verified |
|----------|----------|----------|
| Asian Call < European Call | Yes | ✅ |
| Barrier Call (D&O) < European Call | Yes | ✅ |
| Lookback Call > European Call (ATM) | Yes | ✅ |
| Lookback payoffs ≥ 0 | Yes | ✅ |
| All prices ≥ 0 | Yes | ✅ |
| Higher σ → Higher price | Yes | ✅ |
| Risk-neutral E[S_T] ≈ S₀·e^(rT) | Yes | ✅ |

---

## 18. Limitations

1. **Constant Volatility:** GBM assumes volatility is constant. In reality, volatility changes over time (volatility smile/skew). Stochastic volatility models like Heston would be more realistic.

2. **No Dividends:** The model assumes the underlying asset pays no dividends. For stocks that pay dividends, the model would need adjustment.

3. **No Transaction Costs:** Real trading involves bid-ask spreads, commissions, and market impact. These are ignored.

4. **Discrete Monitoring:** We check barrier conditions only at discrete time steps, not continuously. This can underestimate the probability of barrier breach (the "barrier monitoring bias").

5. **Slow Convergence:** MC convergence at $O(1/\sqrt{N})$ is slow — to halve the error requires 4× more simulations. Advanced variance reduction techniques (control variates, importance sampling) could improve this.

6. **No Jumps:** GBM produces continuous paths — no sudden jumps. Real asset prices can jump (earnings announcements, crashes). Jump-diffusion models (Merton, 1976) address this.

7. **Model Risk:** The entire pricing framework assumes GBM is the correct model. If the true price dynamics differ significantly, all prices will be biased.

8. **Finite Difference Greeks:** Numerical Greeks are noisy and depend on bump size. Pathwise derivatives or likelihood ratio methods could be more efficient.

---

## 19. Conclusion

This project successfully demonstrates the application of Monte Carlo simulation to price exotic options and analyze their risk profiles. We implemented a complete pricing framework for Asian, Barrier, and Lookback options with an interactive dashboard that allows users to:

- Configure market parameters and simulate thousands of price paths
- Compare prices across different exotic option types
- Analyze risk through Greeks (Delta, Gamma, Vega)
- Validate the simulation engine against analytical Black-Scholes solutions
- Export all results for further analysis

The key findings confirm theoretical expectations:
- Asian options are cheaper than European options due to volatility reduction from averaging
- Barrier options are cheaper due to knock-out risk
- Lookback options are most expensive due to the guarantee of buying at the minimum or selling at the maximum
- Monte Carlo prices converge to analytical solutions at the expected $O(1/\sqrt{N})$ rate

The project demonstrates that Monte Carlo simulation is a powerful, flexible tool for pricing derivatives with complex payoff structures where analytical solutions do not exist.

---

## 20. Future Scope

1. **Stochastic Volatility Models:** Implement the Heston model where volatility itself is random, producing more realistic option prices.

2. **Jump-Diffusion Models:** Add Merton's jump-diffusion model to capture sudden price movements.

3. **Variance Reduction:** Implement control variates (using geometric Asian option as control) and importance sampling to improve convergence.

4. **GPU Acceleration:** Use CUDA/CuPy for massive parallelization of path simulation on GPUs.

5. **More Exotic Options:** Extend to Rainbow options (multiple assets), Basket options, Cliquet options, and Range accruals.

6. **American Option Pricing:** Implement the Longstaff-Schwartz (Least Squares Monte Carlo) algorithm for early exercise.

7. **Real-Time Data Integration:** Connect to live market data feeds for real-time parameter estimation and pricing.

8. **Machine Learning:** Use neural networks for fast approximate pricing or for model calibration.

9. **Multi-Asset Options:** Extend to options on multiple correlated assets using Cholesky decomposition for correlated random variables.

---

## 21. References

1. Black, F., & Scholes, M. (1973). The Pricing of Options and Corporate Liabilities. *Journal of Political Economy*, 81(3), 637–654.

2. Boyle, P. P. (1977). Options: A Monte Carlo Approach. *Journal of Financial Economics*, 4(3), 323–338.

3. Hull, J. C. (2018). *Options, Futures, and Other Derivatives* (10th ed.). Pearson Education.

4. Glasserman, P. (2003). *Monte Carlo Methods in Financial Engineering*. Springer-Verlag.

5. Wilmott, P. (2006). *Paul Wilmott on Quantitative Finance* (2nd ed.). John Wiley & Sons.

6. Shreve, S. E. (2004). *Stochastic Calculus for Finance II: Continuous-Time Models*. Springer.

7. Merton, R. C. (1973). Theory of Rational Option Pricing. *Bell Journal of Economics and Management Science*, 4(1), 141–183.

8. Cox, J. C., Ross, S. A., & Rubinstein, M. (1979). Option Pricing: A Simplified Approach. *Journal of Financial Economics*, 7(3), 229–263.

9. Longstaff, F. A., & Schwartz, E. S. (2001). Valuing American Options by Simulation: A Simple Least-Squares Approach. *Review of Financial Studies*, 14(1), 113–147.

10. Kemna, A. G. Z., & Vorst, A. C. F. (1990). A Pricing Method for Options Based on Average Asset Values. *Journal of Banking & Finance*, 14(1), 113–129.

---

*End of Project Report*

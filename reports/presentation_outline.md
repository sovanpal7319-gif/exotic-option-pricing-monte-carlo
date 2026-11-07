k# Presentation Outline

## Exotic Option Pricing and Risk Analysis Using Monte Carlo Simulation

**Presenters:** Sayan Goswami, Sovan Pal, Tanmoy Paul

**Estimated Duration:** 20–25 minutes + Q&A

---

## Slide 1: Title Slide

**Title:** Exotic Option Pricing and Risk Analysis Using Monte Carlo Simulation

**Visual:** Project title with finance-themed imagery

**Key Points:**
- Team members: Sayan Goswami, Sovan Pal, Tanmoy Paul
- Course name and semester (fill in)
- Date of presentation

---

## Slide 2: Agenda

**Key Points:**
1. Introduction & Motivation
2. Problem Statement
3. Objectives
4. Financial Mathematics
5. Monte Carlo Simulation
6. Asian, Barrier, and Lookback Options
7. Greeks and Risk Analysis
8. Dashboard Demo
9. Results & Validation
10. Conclusion & Future Scope

---

## Slide 3: Introduction

**Title:** What Are Exotic Options?

**Key Points:**
- Options are derivatives — contracts whose value derives from an underlying asset
- **Vanilla options**: payoff depends only on the final price (European call/put)
- **Exotic options**: payoff depends on the entire price PATH
- Three types we study: Asian, Barrier, Lookback

**Visual:** Simple diagram showing vanilla vs exotic payoff dependency

**Speaker Notes:**
"Options give the holder the right but not the obligation to buy or sell an asset. Standard options only care about the price at expiry. Exotic options care about what happens DURING the option's lifetime — the average price, whether a barrier was crossed, or the maximum/minimum achieved."

---

## Slide 4: Motivation

**Title:** Why Monte Carlo Simulation?

**Key Points:**
- Black-Scholes gives closed-form solutions for European options
- Exotic options have NO closed-form solution (for most types)
- Monte Carlo: simulate many possible futures, compute average payoff
- Flexible — works for ANY payoff structure
- Used extensively in industry (investment banks, hedge funds)

**Speaker Notes:**
"We can't use Black-Scholes for exotic options because their payoffs depend on the entire price path, not just the terminal price. Monte Carlo is the go-to method in industry because it's extremely flexible — you can price any derivative by defining its payoff rule."

---

## Slide 5: Problem Statement

**Title:** The Challenge

**Key Points:**
- Exotic options have complex, path-dependent payoff structures
- No closed-form analytical solutions for most exotic options
- Need to estimate fair values using numerical methods
- Need to understand risk sensitivity (how price changes with market conditions)

**Visual:** Table comparing European vs Exotic option complexity

---

## Slide 6: Objectives

**Title:** Project Objectives

**Key Points:**
1. Build a Monte Carlo simulation engine using GBM
2. Price Asian, Barrier, and Lookback options
3. Calculate Greeks (Delta, Gamma, Vega)
4. Validate against Black-Scholes (for European options)
5. Analyze sensitivity to market parameters
6. Create an interactive dashboard

---

## Slide 7: Financial Mathematics — GBM

**Title:** Geometric Brownian Motion

**Key Points:**
- Asset price model under risk-neutral measure:

$$S(t+\Delta t) = S(t) \cdot \exp\left[\left(r - \frac{\sigma^2}{2}\right)\Delta t + \sigma\sqrt{\Delta t}\, Z\right]$$

- $r$ = risk-free rate (NOT the expected return $\mu$)
- $\sigma$ = volatility
- $Z \sim N(0,1)$ = random shock
- $-\sigma^2/2$ = Itô correction (prevents bias)

**Visual:** GBM formula with annotated terms

**Speaker Notes:**
"We use the RISK-NEUTRAL measure, meaning we replace the real-world expected return mu with the risk-free rate r. This is justified by the Fundamental Theorem of Asset Pricing — under this measure, we can discount expected payoffs at the risk-free rate to get the fair option price. The sigma-squared-over-two term is a correction from Itô's lemma that ensures the expected price equals S₀ times e^(rT)."

---

## Slide 8: Risk-Neutral Pricing

**Title:** Why Risk-Neutral?

**Key Points:**
- **Real world:** Assets have different expected returns (risky stocks vs bonds)
- **Risk-neutral world:** ALL assets earn the risk-free rate in expectation
- Option price = discounted expected payoff under risk-neutral measure:

$$V = e^{-rT} \cdot \mathbb{E}^Q[\text{Payoff}]$$

- The actual expected return μ does NOT affect the option price!
- This is the foundation of derivative pricing theory

**Speaker Notes:**
"This is one of the most important insights in financial mathematics. The expected return of the stock does not matter for option pricing. Two stocks with the same volatility but different expected returns will have the same option prices. We use risk-neutral pricing because it eliminates the need to estimate expected returns, which are very hard to estimate reliably."

---

## Slide 9: Monte Carlo Method

**Title:** Monte Carlo Simulation — How It Works

**Key Points:**
1. **Simulate** thousands of price paths using GBM
2. **Calculate** option payoff for each path
3. **Average** all payoffs
4. **Discount** to present value: $V = e^{-rT} \cdot \frac{1}{N}\sum \text{Payoff}_i$

**Visual:** Diagram showing fan of simulated paths converging to an average

**Speaker Notes:**
"Monte Carlo is conceptually simple. We ask: 'If I simulate 10,000 possible futures, what is the average payoff?' Then we discount that average to today's value. The Law of Large Numbers guarantees that as N gets large, our estimate converges to the true price. The convergence rate is 1/√N — to halve the error, we need 4 times more simulations."

---

## Slide 10: Asian Option

**Title:** Asian Option — Average-Based Payoff

**Key Points:**
- Payoff depends on the AVERAGE price over the option's life
- Arithmetic average: $\bar{S} = \frac{1}{M}\sum S(t_j)$
- Call: $\max(\bar{S} - K, 0)$
- Put: $\max(K - \bar{S}, 0)$
- **Cheaper than European** because averaging reduces volatility
- No closed-form for arithmetic average → Monte Carlo is needed

**Visual:** Price path with average line drawn, showing payoff

**Speaker Notes:**
"Asian options are popular in commodity markets. By using the average price, they protect against price manipulation near expiry. They're cheaper than European options because the average of a volatile series is less volatile than any individual point in that series."

---

## Slide 11: Asian Option — Results

**Title:** Asian Option Pricing Results

**Key Points:**
- Show sample pricing results (price, std error, confidence interval)
- Compare Asian call vs European call (BS)
- Show simulated paths with average price line
- Show payoff distribution histogram

**Visual:** Side-by-side: paths plot + payoff histogram

---

## Slide 12: Barrier Option

**Title:** Barrier Option — Knock-In/Knock-Out

**Key Points:**
- Option is activated or killed when price crosses barrier B
- **Down-and-Out Call:** Knocked out if price ≤ B at any time

$$\text{Payoff} = \max(S_T - K, 0) \times \mathbf{1}[\min S > B]$$

- Four types: Down-Out, Down-In, Up-Out, Up-In
- **Cheaper than European** due to knock-out risk
- In-Out Parity: Knock-In + Knock-Out = Vanilla

**Visual:** Price path crossing barrier, option killed

**Speaker Notes:**
"Barrier options add a condition: if the price crosses a certain level, the option either dies (knock-out) or comes alive (knock-in). The knock-out risk makes them cheaper. An important result is In-Out Parity: the knock-in and knock-out versions together cover all possible scenarios, so their sum equals the vanilla option price."

---

## Slide 13: Barrier Option — Results

**Title:** Barrier Option Results

**Key Points:**
- Show paths plot with barrier line
- Knocked-out paths highlighted
- Percentage of paths knocked out
- Price comparison with European option

**Visual:** Paths plot with dashed barrier line, red paths = knocked out

---

## Slide 14: Lookback Option

**Title:** Lookback Option — Perfect Hindsight

**Key Points:**
- Payoff depends on the maximum or minimum price during the option's life
- **Floating-strike Call:** $S_T - S_{\min}$ (buy at the lowest price)
- **Floating-strike Put:** $S_{\max} - S_T$ (sell at the highest price)
- **Always in the money** (payoff ≥ 0)
- **Most expensive** exotic option due to perfect hindsight guarantee

**Visual:** Price path with S_min and S_max marked

**Speaker Notes:**
"Lookback options give you the benefit of perfect hindsight — you effectively buy at the lowest price or sell at the highest price during the option's life. This is an incredibly valuable right, so lookback options are the most expensive of the three exotic types we study. They're always in the money because, by definition, S_T is at least S_min and at most S_max."

---

## Slide 15: Lookback Option — Results

**Title:** Lookback Option Results

**Key Points:**
- All payoffs are non-negative (verified)
- Price significantly higher than European ATM option
- Higher volatility → even higher lookback price

**Visual:** Payoff distribution (no zero bin!)

---

## Slide 16: Greeks — Definition

**Title:** Greeks — Measuring Risk

**Key Points:**

| Greek | Formula | Meaning |
|-------|---------|---------|
| **Delta (Δ)** | $\frac{V(S+h) - V(S-h)}{2h}$ | Price sensitivity to spot |
| **Gamma (Γ)** | $\frac{V(S+h) - 2V(S) + V(S-h)}{h^2}$ | How fast Delta changes |
| **Vega (ν)** | $\frac{V(\sigma+\varepsilon) - V(\sigma-\varepsilon)}{2\varepsilon}$ | Sensitivity to volatility |

- We use **central finite differences** for $O(h^2)$ accuracy
- Same random seed for bumped prices to reduce noise

**Speaker Notes:**
"Greeks tell us how risky our option position is. Delta tells us how much the option price changes when the underlying moves — it's the hedge ratio. Gamma tells us how quickly Delta changes — high Gamma means we need to rebalance our hedge frequently. Vega tells us how exposed we are to changes in volatility."

---

## Slide 17: Greeks — Results

**Title:** Greeks Results Summary

**Key Points:**
- Table of Delta, Gamma, Vega for each option type
- Delta positive for calls, negative for puts
- Vega always positive (higher vol → higher price)
- Lookback has highest Vega (most sensitive to volatility)

**Visual:** Bar chart comparing Greeks across option types

---

## Slide 18: Dashboard Demo — Overview

**Title:** Interactive Dashboard

**Key Points:**
- Built with Streamlit (Python web framework)
- 8 pages: Home, Market Data, Pricing, Greeks, Sensitivity, Comparison, Validation, Export
- Configure all parameters via sidebar
- Real-time pricing and visualization
- Export results as CSV

**Visual:** Screenshot of the Home page

**Speaker Notes:**
"Let me walk you through our dashboard. [Live demo or screenshots]"

---

## Slide 19: Dashboard Demo — Pricing

**Title:** Pricing in Action

**Key Points:**
- User selects option types (checkboxes)
- Sets market parameters (sidebar)
- Clicks "Run Simulation"
- Results shown: price, std error, confidence interval
- Interactive Plotly charts: paths, payoff distributions

**Visual:** Screenshot of Option Pricing page with results

---

## Slide 20: Results Summary

**Title:** Results Comparison

**Key Points:**
- **Price ordering:** Barrier (D&O) < Asian < European < Lookback
- All results consistent with financial theory
- MC prices converge to BS prices for European options
- Standard errors decrease with more simulations

**Visual:** Comparison bar chart of all option prices

| Option | Price | Relative to European |
|--------|-------|---------------------|
| Barrier (D&O) Call | ~8.50 | Cheaper (knock-out risk) |
| Asian Call | ~5.80 | Cheaper (averaging) |
| European Call | 10.45 | Benchmark (BS) |
| Lookback Call | ~16.50 | More expensive (hindsight) |

---

## Slide 21: Validation

**Title:** Validating Our Engine

**Key Points:**
- Compare MC European option prices to Black-Scholes
- Error < 1% at 10,000 simulations
- Convergence rate $O(1/\sqrt{N})$ confirmed
- All theoretical properties verified (36 tests pass)

**Visual:** Convergence plot (MC price vs N, with BS reference line)

**Speaker Notes:**
"We validate our simulation engine by pricing European options — for which we know the exact answer from Black-Scholes. Our Monte Carlo prices converge to the BS price, confirming our engine is correctly implemented. We then trust this same engine to price exotic options where no analytical solution exists."

---

## Slide 22: Key Findings

**Title:** Key Findings

**Key Points:**
1. Monte Carlo simulation successfully prices all three exotic option types
2. Asian options are ~45% cheaper than European options (averaging effect)
3. Barrier options are cheaper due to knock-out risk — price depends strongly on barrier level
4. Lookback options are ~60% more expensive than European options (hindsight premium)
5. Greeks confirm expected risk sensitivities
6. 10,000 simulations provide sufficient accuracy (<2% standard error)

---

## Slide 23: Limitations

**Title:** Model Limitations

**Key Points:**
- **Constant volatility** assumption (real markets have volatility smile)
- **No dividends** modeled
- **Discrete monitoring** (slight underestimation of barrier breach probability)
- **Slow convergence** ($O(1/\sqrt{N})$) — need 4× more sims to halve error
- **No jumps** in price (GBM paths are continuous)
- **Model risk** — GBM may not capture real market dynamics

---

## Slide 24: Future Scope

**Title:** Future Extensions

**Key Points:**
- **Stochastic volatility** (Heston model)
- **Jump-diffusion** (Merton model)
- **Variance reduction** (control variates, importance sampling)
- **GPU acceleration** for faster simulation
- **American options** (Longstaff-Schwartz algorithm)
- **Multi-asset options** (Rainbow, Basket)
- **Machine learning** for fast approximate pricing

---

## Slide 25: Thank You & Q&A

**Title:** Thank You!

**Key Points:**
- Project demonstrates practical application of quantitative finance techniques
- Complete working implementation with interactive dashboard
- All code available in the project repository

**Team:**
- Sayan Goswami — Core Simulation & Pricing
- Sovan Pal — Greeks, Validation & Risk Analysis
- Tanmoy Paul — Dashboard & Visualization

---

---

## Common Viva Questions and Answers

### Q1: Why do we use risk-neutral pricing instead of real-world drift?
**A:** Under the risk-neutral measure, all assets earn the risk-free rate in expectation. This allows us to discount expected payoffs at the risk-free rate to get the fair (no-arbitrage) option price. The actual expected return μ of the stock does not affect the option price — this is a fundamental result of the Fundamental Theorem of Asset Pricing. Using risk-neutral pricing eliminates the need to estimate expected returns, which are very difficult to estimate reliably.

### Q2: Why is the Asian option cheaper than the European option?
**A:** The Asian option payoff depends on the average price, and averaging reduces volatility. Since option prices increase with volatility (higher uncertainty → higher option value), the reduced effective volatility makes the Asian option cheaper. Mathematically, Var(average) < Var(terminal price).

### Q3: What happens if you increase the number of simulations?
**A:** The option price estimate becomes more precise — the standard error decreases as $1/\sqrt{N}$. The price converges to the true value. However, the convergence is slow: to halve the error, you need 4 times more simulations. There are diminishing returns beyond about 50,000–100,000 simulations for most practical purposes.

### Q4: How does the barrier level affect the option price?
**A:** For a down-and-out option: as the barrier level B increases (approaches S₀), more paths are knocked out, so the option becomes cheaper. As B decreases (moves far from S₀), fewer paths are knocked out, and the option price approaches the vanilla European option price. At the extreme: B→0 gives vanilla price; B→S₀ gives price near zero.

### Q5: Why are lookback options always in the money?
**A:** By definition, the lookback call payoff is $S_T - S_{\min}$. Since $S_T$ is a value from the path and $S_{\min}$ is the minimum of all values on the path (including $S_T$), we always have $S_T \geq S_{\min}$, so the payoff is always $\geq 0$. Similarly for puts: $S_{\max} \geq S_T$ always.

### Q6: What is the convergence rate of Monte Carlo simulation?
**A:** $O(1/\sqrt{N})$, where N is the number of simulations. This comes from the Central Limit Theorem — the standard error of the mean is $\sigma/\sqrt{N}$. This is independent of the dimension of the problem, which is a key advantage of Monte Carlo over other numerical methods for high-dimensional problems.

### Q7: What is Itô's lemma and why does it matter here?
**A:** Itô's lemma is the chain rule for stochastic calculus. When we apply $\ln()$ to the SDE $dS = rS\,dt + \sigma S\,dW$, Itô's lemma gives us $d(\ln S) = (r - \sigma^2/2)dt + \sigma\,dW$. The extra $-\sigma^2/2$ term (Itô correction) does not appear in ordinary calculus — it arises because the Wiener process has non-zero quadratic variation. This correction ensures unbiased simulation.

### Q8: What is the difference between arithmetic and geometric averaging?
**A:** Arithmetic average: $\bar{S} = \frac{1}{M}\sum S_j$. Geometric average: $\bar{S}_G = \left(\prod S_j\right)^{1/M}$. The geometric average of lognormal variables is lognormal, so geometric-average Asian options have closed-form solutions. The arithmetic average does not have a known distribution, requiring numerical methods. In practice, arithmetic averaging is more common because it's simpler and more intuitive.

### Q9: Why do we use central finite differences for Greeks?
**A:** Central differences use both $f(x+h)$ and $f(x-h)$, giving accuracy of $O(h^2)$. Forward differences (using only $f(x+h)$ and $f(x)$) have accuracy of only $O(h)$. For the same bump size h, central differences give much more accurate Greek estimates. We also use the same random seed for all bumped prices to ensure that differences come from the parameter change, not from different random draws.

### Q10: What are the limitations of the GBM model?
**A:** GBM assumes: (1) constant volatility — real markets show volatility smiles/skews; (2) continuous paths — real prices can jump; (3) normally distributed log returns — real returns have fat tails; (4) no transaction costs or market impact; (5) constant risk-free rate; (6) no dividends. Despite these limitations, GBM is widely used as a baseline model because of its mathematical tractability.

### Q11: What is the In-Out parity for barrier options?
**A:** Knock-In Price + Knock-Out Price = Vanilla Price. This holds because either the barrier is hit (knock-in is active, knock-out is dead) or it is not (knock-out is active, knock-in is dead). Together, they cover all scenarios, which is exactly what the vanilla option covers.

### Q12: Why do we use the same random seed when computing Greeks?
**A:** Using the same seed means the same random numbers are generated for both bumped and unbumped prices. This ensures that any price difference is due to the parameter bump, not due to different random draws. Without this, the Greek estimates would be extremely noisy because random fluctuations would dominate the small signal from the parameter change.

### Q13: What is a Wiener process (Brownian motion)?
**A:** A Wiener process $W(t)$ is a continuous-time stochastic process with four properties: (1) $W(0) = 0$; (2) independent increments; (3) $W(t) - W(s) \sim N(0, t-s)$ for $t > s$; (4) continuous paths. It is the fundamental building block of stochastic calculus and financial mathematics.

### Q14: How would you price an American option?
**A:** American options allow early exercise, which standard Monte Carlo cannot handle directly (because MC goes forward in time, but early exercise requires backward decisions). The **Longstaff-Schwartz algorithm** (Least Squares Monte Carlo) solves this by using regression to estimate the continuation value at each time step, then comparing it to immediate exercise value.

### Q15: What is the Black-Scholes formula?
**A:** For a European call: $C = S_0 N(d_1) - K e^{-rT} N(d_2)$, where $d_1 = \frac{\ln(S_0/K) + (r + \sigma^2/2)T}{\sigma\sqrt{T}}$ and $d_2 = d_1 - \sigma\sqrt{T}$. $N(\cdot)$ is the standard normal CDF. For puts, we use put-call parity: $P = C - S_0 + Ke^{-rT}$.

### Q16: What variance reduction techniques could improve your results?
**A:** (1) **Antithetic variates:** For each random draw Z, also use -Z, producing negatively correlated pairs that reduce variance. (2) **Control variates:** Use a related quantity with known expectation (e.g., geometric Asian option) to reduce variance. (3) **Importance sampling:** Change the probability distribution to sample more from important regions.

### Q17: How do you estimate historical volatility?
**A:** We compute daily log returns $r_t = \ln(S_t/S_{t-1})$, then calculate their standard deviation $\sigma_{\text{daily}}$, and annualize: $\sigma = \sigma_{\text{daily}} \times \sqrt{252}$, where 252 is the number of trading days per year.

### Q18: What is Delta hedging?
**A:** Delta hedging means holding $\Delta$ units of the underlying asset for each option sold. This neutralizes the first-order sensitivity to price changes. For example, if Delta = 0.5, sell 1 call and buy 0.5 shares. The portfolio is then approximately insensitive to small changes in the stock price. However, the hedge must be rebalanced as Delta changes (measured by Gamma).

### Q19: Why is Vega always positive for long options?
**A:** Higher volatility means more uncertainty about the future price. For an option holder, this is valuable because options have asymmetric payoffs — you benefit from large moves in one direction but your loss is limited (you can let the option expire worthless). More volatility → higher chance of large payoffs → higher option value.

### Q20: How does time to maturity affect exotic option prices?
**A:** Generally, longer maturity increases option prices because: (1) more time for favorable price movements; (2) more time for averaging (Asian), barrier events (Barrier), and extreme prices (Lookback). However, the relationship isn't always monotonic for barrier options — longer maturity also means more chance of knock-out.

### Q21: What is the difference between European and American options?
**A:** European options can only be exercised at maturity. American options can be exercised at any time before maturity. This early exercise right makes American options at least as valuable as European options ($V_{\text{American}} \geq V_{\text{European}}$).

### Q22: Why don't we use Black-Scholes for exotic options?
**A:** Black-Scholes assumes the payoff depends only on the terminal price $S_T$. Exotic options have path-dependent payoffs — they depend on the entire price trajectory. The averaging (Asian), barrier monitoring (Barrier), and extreme-tracking (Lookback) cannot be captured by a simple terminal-price formula.

### Q23: What is the role of the risk-free rate in option pricing?
**A:** The risk-free rate r appears in two places: (1) as the drift in the risk-neutral GBM ($r$ replaces $\mu$); (2) as the discount factor ($e^{-rT}$). Higher r increases call prices (higher drift → higher expected terminal price) and decreases put prices. It also reduces the present value of the strike price.

### Q24: Can Monte Carlo simulation give negative option prices?
**A:** In theory, individual discounted payoffs are always ≥ 0, so the average should be ≥ 0. However, with very few simulations, statistical noise could theoretically cause the confidence interval to include negative values. The point estimate (average) should always be non-negative. We clamp prices to zero as a safety measure.

### Q25: What would you improve if you had more time?
**A:** Priority improvements: (1) Stochastic volatility (Heston model) for more realistic pricing; (2) Control variates using geometric Asian option as control for Asian pricing; (3) Continuous barrier monitoring correction (Broadie-Glasserman-Kou adjustment); (4) GPU acceleration for 100× faster simulation; (5) Real-time data integration from exchange APIs.

---

*End of Presentation Outline*

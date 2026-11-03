"""
Asian Option Pricing Module
============================
Prices arithmetic-average Asian options using Monte Carlo simulation.

Asian options are path-dependent options whose payoff depends on the
AVERAGE price of the underlying asset over a specified period, rather
than just the terminal price.

Types Implemented:
    Arithmetic-Average Asian Call:
        Payoff = max(A - K, 0)
    
    Arithmetic-Average Asian Put:
        Payoff = max(K - A, 0)

    where A = (1/M) * Σ S(t_j)  is the arithmetic average over M
    monitoring dates, and K is the strike price.

Key Properties:
    - Asian options are CHEAPER than equivalent European options because
      averaging reduces the effective volatility of the payoff.
    - There is NO closed-form solution for arithmetic-average Asian options
      (unlike geometric-average), making Monte Carlo the standard method.
    - Commonly used in commodity and FX markets where averaging protects
      against price manipulation near expiry.

Monitoring Dates:
    In our implementation, every time step is a monitoring date.
    The average is computed over S(t_1), S(t_2), ..., S(t_M) where
    M = n_steps. We exclude S(0) = S0 from the average, as is standard.

Authors: Sayan Goswami, Sovan Pal, Tanmoy Paul
"""

import numpy as np
from .simulation import simulate_gbm_paths


def price_asian_option(S0: float, K: float, r: float, sigma: float, T: float,
                       n_steps: int, n_simulations: int,
                       option_type: str = 'call', seed: int = 42) -> dict:
    """
    Price an arithmetic-average Asian option using Monte Carlo simulation.

    Algorithm:
        1. Simulate N price paths using GBM.
        2. For each path, compute the arithmetic average of prices
           at all monitoring dates (time steps 1 through M).
        3. Compute the payoff for each path.
        4. Discount the average payoff to present value.
        5. Estimate standard error and confidence interval.

    Parameters
    ----------
    S0 : float
        Initial asset price.
    K : float
        Strike price (must be > 0).
    r : float
        Risk-free interest rate (annualized).
    sigma : float
        Volatility (annualized).
    T : float
        Time to maturity in years.
    n_steps : int
        Number of time steps (= number of monitoring dates).
    n_simulations : int
        Number of Monte Carlo simulation paths.
    option_type : str
        'call' or 'put'.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    dict
        'price'          : Discounted expected payoff (the option price).
        'std_error'      : Standard error of the Monte Carlo estimate.
        'conf_interval'  : (lower, upper) 95% confidence interval.
        'payoffs'        : np.ndarray of raw payoffs per path (undiscounted).
        'paths'          : np.ndarray of simulated price paths.
        'average_prices' : np.ndarray of arithmetic average price per path.
    """
    # --- Input validation ---
    if K <= 0:
        raise ValueError(f"Strike price K must be positive, got {K}")
    if option_type not in ('call', 'put'):
        raise ValueError(f"option_type must be 'call' or 'put', got '{option_type}'")

    # Step 1: Simulate price paths
    # paths shape: (n_simulations, n_steps + 1)
    paths = simulate_gbm_paths(S0, r, sigma, T, n_steps, n_simulations, seed)

    # Step 2: Compute arithmetic average of each path
    # We average over monitoring dates: columns 1 to n_steps (exclude initial S0)
    # This represents the average price observed during the option's life
    average_prices = np.mean(paths[:, 1:], axis=1)  # Shape: (n_simulations,)

    # Step 3: Compute payoffs
    if option_type == 'call':
        # Asian Call Payoff: max(Average - K, 0)
        payoffs = np.maximum(average_prices - K, 0.0)
    else:
        # Asian Put Payoff: max(K - Average, 0)
        payoffs = np.maximum(K - average_prices, 0.0)

    # Step 4: Discount payoffs to present value
    # V = e^(-rT) * E[Payoff]
    discount_factor = np.exp(-r * T)
    discounted_payoffs = discount_factor * payoffs

    # Step 5: Calculate option price and statistics
    price = np.mean(discounted_payoffs)

    # Standard error: std of discounted payoffs / sqrt(N)
    # This measures the precision of our Monte Carlo estimate
    std_error = np.std(discounted_payoffs, ddof=1) / np.sqrt(n_simulations)

    # 95% confidence interval using Central Limit Theorem
    # As N → ∞, the MC estimate is approximately normally distributed
    conf_interval = (price - 1.96 * std_error, price + 1.96 * std_error)

    return {
        'price': float(price),
        'std_error': float(std_error),
        'conf_interval': (float(conf_interval[0]), float(conf_interval[1])),
        'payoffs': payoffs,
        'paths': paths,
        'average_prices': average_prices
    }

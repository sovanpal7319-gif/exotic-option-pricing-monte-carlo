"""
Lookback Option Pricing Module
================================
Prices floating-strike lookback options using Monte Carlo simulation.

Lookback options are path-dependent options whose payoff depends on the
MAXIMUM or MINIMUM price achieved by the underlying asset during the
option's lifetime.

Floating-Strike Lookback Options:
    Call Payoff: S_T - S_min
        The holder buys at the lowest price observed during the option's life.
        This is equivalent to "buying at the bottom."
    
    Put Payoff: S_max - S_T
        The holder sells at the highest price observed during the option's life.
        This is equivalent to "selling at the top."

Key Properties:
    - Lookback options are ALWAYS in the money (payoff ≥ 0) because:
        * For calls: S_T ≥ S_min by definition, so S_T - S_min ≥ 0
        * For puts: S_max ≥ S_T by definition, so S_max - S_T ≥ 0
    - This guarantee makes lookback options MORE EXPENSIVE than vanilla options.
    - The maximum and minimum are taken over all monitoring dates (time steps).
    - More time steps (finer monitoring) generally increases the option value
      as extreme prices are more likely to be captured.

Authors: Sayan Goswami, Sovan Pal, Tanmoy Paul
"""

import numpy as np
from .simulation import simulate_gbm_paths


def price_lookback_option(S0: float, r: float, sigma: float, T: float,
                          n_steps: int, n_simulations: int,
                          option_type: str = 'call', seed: int = 42) -> dict:
    """
    Price a floating-strike lookback option using Monte Carlo simulation.

    Algorithm:
        1. Simulate N price paths using GBM.
        2. For each path, find the minimum price (for calls) or
           maximum price (for puts) across all time steps.
        3. Compute payoffs using the floating-strike formula.
        4. Discount average payoff to present value.
        5. Calculate standard error and confidence interval.

    Note: No strike price K is needed — the strike is determined by
    the path itself (floating strike).

    Parameters
    ----------
    S0 : float
        Initial asset price.
    r : float
        Risk-free interest rate (annualized).
    sigma : float
        Volatility (annualized).
    T : float
        Time to maturity in years.
    n_steps : int
        Number of time steps (monitoring dates).
    n_simulations : int
        Number of Monte Carlo paths.
    option_type : str
        'call' or 'put'.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    dict
        'price'      : Option price (discounted expected payoff).
        'std_error'  : Standard error of MC estimate.
        'conf_interval' : (lower, upper) 95% CI.
        'payoffs'    : np.ndarray of payoffs per path (undiscounted).
        'paths'      : Simulated price paths.
        'path_mins'  : Minimum price per path.
        'path_maxs'  : Maximum price per path.
    """
    # --- Input validation ---
    if option_type not in ('call', 'put'):
        raise ValueError(f"option_type must be 'call' or 'put', got '{option_type}'")

    # Step 1: Simulate price paths
    paths = simulate_gbm_paths(S0, r, sigma, T, n_steps, n_simulations, seed)

    # Step 2: Find path extremes across ALL time steps (including S0)
    # The lookback examines the entire path from start to finish
    path_mins = np.min(paths, axis=1)   # Minimum price per path
    path_maxs = np.max(paths, axis=1)   # Maximum price per path

    # Terminal prices
    S_T = paths[:, -1]

    # Step 3: Compute payoffs
    if option_type == 'call':
        # Lookback Call: S_T - S_min
        # "Buy at the lowest price, sell at expiry"
        payoffs = S_T - path_mins
    else:
        # Lookback Put: S_max - S_T
        # "Sell at the highest price, buy back at expiry"
        payoffs = path_maxs - S_T

    # Payoffs should always be non-negative (by definition)
    # Small numerical errors might occur, so we clamp
    payoffs = np.maximum(payoffs, 0.0)

    # Step 4: Discount and compute statistics
    discount_factor = np.exp(-r * T)
    discounted_payoffs = discount_factor * payoffs

    price = np.mean(discounted_payoffs)
    std_error = np.std(discounted_payoffs, ddof=1) / np.sqrt(n_simulations)
    conf_interval = (price - 1.96 * std_error, price + 1.96 * std_error)

    return {
        'price': float(price),
        'std_error': float(std_error),
        'conf_interval': (float(conf_interval[0]), float(conf_interval[1])),
        'payoffs': payoffs,
        'paths': paths,
        'path_mins': path_mins,
        'path_maxs': path_maxs
    }

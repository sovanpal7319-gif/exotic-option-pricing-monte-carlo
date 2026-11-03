"""
Barrier Option Pricing Module
===============================
Prices barrier options using Monte Carlo simulation.

Barrier options are path-dependent options that are either activated
(knock-in) or deactivated (knock-out) when the underlying asset price
crosses a predetermined barrier level B during the option's lifetime.

Types Implemented:
    Down-and-Out: Option is knocked out (becomes worthless) if the asset
                  price touches or falls BELOW barrier B at any monitoring date.
    Down-and-In:  Option is activated only if the price touches or falls
                  BELOW barrier B. (Complementary to Down-and-Out.)
    Up-and-Out:   Option is knocked out if the price touches or rises
                  ABOVE barrier B.
    Up-and-In:    Option is activated only if the price touches or rises
                  ABOVE barrier B.

Payoff Examples (Down-and-Out Call):
    Payoff = max(S_T - K, 0) * I[min(S(t_j)) > B]
    
    where I[.] is the indicator function:
        I = 1 if the barrier was NEVER breached (option survives)
        I = 0 if the barrier was breached at any point (knocked out)

Barrier Parity:
    Down-and-In + Down-and-Out = Vanilla Option
    Up-and-In + Up-and-Out = Vanilla Option

    This means the sum of a knock-in and knock-out barrier option
    with the same parameters equals the corresponding vanilla option.

Key Properties:
    - Barrier options are CHEAPER than vanilla options because there is
      a chance the option gets knocked out.
    - The closer the barrier is to the initial price, the more likely
      knock-out occurs, and the cheaper the option.

Monitoring:
    In practice, barriers can be monitored continuously or at discrete
    dates. Our implementation uses discrete monitoring at each time step.

Authors: Sayan Goswami, Sovan Pal, Tanmoy Paul
"""

import numpy as np
from .simulation import simulate_gbm_paths


def price_barrier_option(S0: float, K: float, r: float, sigma: float, T: float,
                         B: float, n_steps: int, n_simulations: int,
                         option_type: str = 'call',
                         barrier_type: str = 'down-and-out',
                         seed: int = 42) -> dict:
    """
    Price a barrier option using Monte Carlo simulation.

    Algorithm:
        1. Simulate N price paths using GBM.
        2. For each path, check if the barrier condition is triggered
           at any monitoring date.
        3. Apply the barrier logic to determine which paths have active payoffs.
        4. Compute payoffs, discount, and calculate statistics.

    Parameters
    ----------
    S0 : float
        Initial asset price.
    K : float
        Strike price.
    r : float
        Risk-free interest rate (annualized).
    sigma : float
        Volatility (annualized).
    T : float
        Time to maturity in years.
    B : float
        Barrier level.
    n_steps : int
        Number of time steps (monitoring dates).
    n_simulations : int
        Number of Monte Carlo paths.
    option_type : str
        'call' or 'put'.
    barrier_type : str
        One of: 'down-and-out', 'down-and-in', 'up-and-out', 'up-and-in'.
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    dict
        'price'           : Option price (discounted expected payoff).
        'std_error'       : Standard error of MC estimate.
        'conf_interval'   : (lower, upper) 95% CI.
        'payoffs'         : np.ndarray of payoffs per path.
        'paths'           : Simulated price paths.
        'knocked_out_pct' : Percentage of paths knocked out (or not activated).
    """
    # --- Input validation ---
    if K <= 0:
        raise ValueError(f"Strike price K must be positive, got {K}")
    if B <= 0:
        raise ValueError(f"Barrier B must be positive, got {B}")
    if option_type not in ('call', 'put'):
        raise ValueError(f"option_type must be 'call' or 'put', got '{option_type}'")

    valid_barrier_types = ('down-and-out', 'down-and-in', 'up-and-out', 'up-and-in')
    if barrier_type not in valid_barrier_types:
        raise ValueError(f"barrier_type must be one of {valid_barrier_types}, got '{barrier_type}'")

    # Validate barrier level relative to initial price
    if 'down' in barrier_type and B >= S0:
        raise ValueError(
            f"For '{barrier_type}', barrier B ({B}) must be below S0 ({S0})")
    if 'up' in barrier_type and B <= S0:
        raise ValueError(
            f"For '{barrier_type}', barrier B ({B}) must be above S0 ({S0})")

    # Step 1: Simulate price paths
    paths = simulate_gbm_paths(S0, r, sigma, T, n_steps, n_simulations, seed)

    # Step 2: Determine barrier breaches
    # Check ALL time steps (columns 0 through n_steps) for barrier crossings
    if 'down' in barrier_type:
        # Barrier is breached if price falls to or below B at any step
        path_mins = np.min(paths, axis=1)         # Min price per path
        barrier_hit = (path_mins <= B)             # True if barrier was touched
    else:  # 'up' barrier
        # Barrier is breached if price rises to or above B at any step
        path_maxs = np.max(paths, axis=1)          # Max price per path
        barrier_hit = (path_maxs >= B)             # True if barrier was touched

    # Step 3: Determine which paths have active payoffs
    if 'out' in barrier_type:
        # Knock-out: option is alive only if barrier was NOT hit
        option_alive = ~barrier_hit
    else:  # 'in' barrier
        # Knock-in: option is alive only if barrier WAS hit
        option_alive = barrier_hit

    # Step 4: Compute terminal payoffs
    S_T = paths[:, -1]  # Terminal asset prices

    if option_type == 'call':
        vanilla_payoff = np.maximum(S_T - K, 0.0)
    else:
        vanilla_payoff = np.maximum(K - S_T, 0.0)

    # Apply barrier condition: zero payoff for knocked-out / not-activated paths
    payoffs = vanilla_payoff * option_alive.astype(float)

    # Step 5: Discount and compute statistics
    discount_factor = np.exp(-r * T)
    discounted_payoffs = discount_factor * payoffs

    price = np.mean(discounted_payoffs)
    std_error = np.std(discounted_payoffs, ddof=1) / np.sqrt(n_simulations)
    conf_interval = (price - 1.96 * std_error, price + 1.96 * std_error)

    # Calculate knocked-out percentage
    if 'out' in barrier_type:
        knocked_out_pct = float(np.mean(barrier_hit) * 100)
    else:
        # For knock-in, report percentage NOT activated
        knocked_out_pct = float(np.mean(~barrier_hit) * 100)

    return {
        'price': float(max(price, 0.0)),
        'std_error': float(std_error),
        'conf_interval': (float(conf_interval[0]), float(conf_interval[1])),
        'payoffs': payoffs,
        'paths': paths,
        'knocked_out_pct': knocked_out_pct
    }

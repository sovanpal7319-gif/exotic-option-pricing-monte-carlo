"""
Monte Carlo Simulation Engine
=============================
Simulates future asset-price paths using Geometric Brownian Motion (GBM)
under the risk-neutral measure.

Mathematical Background:
    Under the risk-neutral measure, the asset price follows:
        dS = r * S * dt + sigma * S * dW

    Discretized (exact solution using Itô's lemma):
        S(t+dt) = S(t) * exp[(r - sigma²/2)*dt + sigma*sqrt(dt)*Z]

    where:
        S(t)  = Asset price at time t
        r     = Risk-free interest rate (annualized)
        sigma = Volatility (annualized)
        dt    = Time step size (T / n_steps)
        Z     = Standard normal random variable ~ N(0, 1)
        W     = Wiener process (Brownian motion)

Why Risk-Neutral Pricing?
    Under the Fundamental Theorem of Asset Pricing, the fair price of a
    derivative is the discounted expected payoff under the risk-neutral
    measure. In this measure, all assets earn the risk-free rate r in
    expectation, allowing us to discount expected payoffs at r.
    We replace the real-world drift mu with r — the actual expected
    return of the asset does not matter for pricing.

Authors: Sayan Goswami, Sovan Pal, Tanmoy Paul
"""

import numpy as np


def simulate_gbm_paths(S0: float, r: float, sigma: float, T: float,
                       n_steps: int, n_simulations: int,
                       seed: int = 42) -> np.ndarray:
    """
    Simulate asset price paths using Geometric Brownian Motion.

    Uses vectorized NumPy operations for efficiency. All random numbers
    are generated at once, then cumulative products build the paths.

    Parameters
    ----------
    S0 : float
        Initial asset price (must be > 0).
    r : float
        Risk-free interest rate (annualized, e.g. 0.05 for 5%).
    sigma : float
        Volatility (annualized, e.g. 0.20 for 20%).
    T : float
        Time to maturity in years (must be > 0).
    n_steps : int
        Number of discrete time steps (must be > 0).
    n_simulations : int
        Number of Monte Carlo paths to generate (must be > 0).
    seed : int
        Random seed for reproducibility.

    Returns
    -------
    np.ndarray
        Array of shape (n_simulations, n_steps + 1).
        Column 0 is S0 for every path.
        Columns 1..n_steps are the simulated prices at each time step.
    """
    # --- Input validation ---
    if S0 <= 0:
        raise ValueError(f"Initial price S0 must be positive, got {S0}")
    if sigma <= 0:
        raise ValueError(f"Volatility sigma must be positive, got {sigma}")
    if T <= 0:
        raise ValueError(f"Time to maturity T must be positive, got {T}")
    if n_steps <= 0:
        raise ValueError(f"Number of steps must be positive, got {n_steps}")
    if n_simulations <= 0:
        raise ValueError(f"Number of simulations must be positive, got {n_simulations}")

    dt = T / n_steps  # Size of each time step

    # Use RandomState for reproducibility across different NumPy versions
    rng = np.random.RandomState(seed)

    # Generate all standard normal random variables at once
    # Shape: (n_simulations, n_steps)
    Z = rng.standard_normal((n_simulations, n_steps))

    # Calculate log-returns for each step using the GBM formula:
    #   ln(S(t+dt)/S(t)) = (r - sigma²/2)*dt + sigma*sqrt(dt)*Z
    #
    # The term (r - sigma²/2) is the drift correction from Itô's lemma.
    # Without -sigma²/2, the discrete simulation would overestimate prices.
    drift = (r - 0.5 * sigma ** 2) * dt
    diffusion = sigma * np.sqrt(dt) * Z

    # Log-returns for each step
    log_returns = drift + diffusion  # Shape: (n_simulations, n_steps)

    # Build price paths using cumulative sum of log-returns
    # S(t) = S0 * exp(sum of log-returns up to t)
    cumulative_log_returns = np.cumsum(log_returns, axis=1)

    # Prepend zeros for the initial time (log-return of 0 → price = S0)
    cumulative_log_returns = np.concatenate(
        [np.zeros((n_simulations, 1)), cumulative_log_returns], axis=1
    )

    # Convert log-returns to prices
    paths = S0 * np.exp(cumulative_log_returns)  # Shape: (n_simulations, n_steps+1)

    return paths


def simulate_gbm_paths_antithetic(S0: float, r: float, sigma: float, T: float,
                                   n_steps: int, n_simulations: int,
                                   seed: int = 42) -> np.ndarray:
    """
    Simulate GBM paths using antithetic variates for variance reduction.

    Antithetic variates technique:
        For each set of random draws Z, we also use -Z.
        This generates negatively correlated path pairs, reducing
        the variance of the Monte Carlo estimator.

        If N simulations are requested, we generate N/2 paths with Z
        and N/2 paths with -Z, producing N total paths.

    Parameters
    ----------
    S0, r, sigma, T, n_steps, n_simulations, seed :
        Same as simulate_gbm_paths.

    Returns
    -------
    np.ndarray
        Array of shape (n_simulations, n_steps + 1).
    """
    if S0 <= 0:
        raise ValueError(f"Initial price S0 must be positive, got {S0}")
    if sigma <= 0:
        raise ValueError(f"Volatility sigma must be positive, got {sigma}")
    if T <= 0:
        raise ValueError(f"Time to maturity T must be positive, got {T}")

    dt = T / n_steps
    half_sims = n_simulations // 2

    rng = np.random.RandomState(seed)
    Z = rng.standard_normal((half_sims, n_steps))

    drift = (r - 0.5 * sigma ** 2) * dt
    diffusion_pos = sigma * np.sqrt(dt) * Z
    diffusion_neg = sigma * np.sqrt(dt) * (-Z)  # Antithetic draws

    # Positive paths
    log_returns_pos = drift + diffusion_pos
    cum_pos = np.cumsum(log_returns_pos, axis=1)
    cum_pos = np.concatenate([np.zeros((half_sims, 1)), cum_pos], axis=1)
    paths_pos = S0 * np.exp(cum_pos)

    # Antithetic (negative) paths
    log_returns_neg = drift + diffusion_neg
    cum_neg = np.cumsum(log_returns_neg, axis=1)
    cum_neg = np.concatenate([np.zeros((half_sims, 1)), cum_neg], axis=1)
    paths_neg = S0 * np.exp(cum_neg)

    # Combine both sets
    paths = np.concatenate([paths_pos, paths_neg], axis=0)

    # If n_simulations is odd, add one more path
    if n_simulations % 2 == 1:
        extra_Z = rng.standard_normal((1, n_steps))
        extra_log = drift + sigma * np.sqrt(dt) * extra_Z
        extra_cum = np.concatenate([np.zeros((1, 1)), np.cumsum(extra_log, axis=1)], axis=1)
        extra_path = S0 * np.exp(extra_cum)
        paths = np.concatenate([paths, extra_path], axis=0)

    return paths

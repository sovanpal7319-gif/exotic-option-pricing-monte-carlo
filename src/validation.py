"""
Validation Module
==================
Validates Monte Carlo pricing against analytical solutions (Black-Scholes)
and performs convergence analysis.

Black-Scholes Formula (1973):
    For European options on a non-dividend-paying asset:

    Call Price: C = S0 * N(d1) - K * e^(-rT) * N(d2)
    Put Price:  P = K * e^(-rT) * N(-d2) - S0 * N(-d1)

    where:
        d1 = [ln(S0/K) + (r + σ²/2)*T] / (σ√T)
        d2 = d1 - σ√T
        N(.) = Standard normal cumulative distribution function

Validation Strategy:
    1. Price European call and put options using Monte Carlo simulation.
    2. Compare MC prices with Black-Scholes analytical prices.
    3. As number of simulations increases, MC prices should converge
       to BS prices (Law of Large Numbers).
    4. The convergence rate is O(1/√N) — to halve the error, we need
       4× more simulations.

This validation gives confidence that our simulation engine is correct,
which then supports pricing exotic options (where no analytical solution
exists).

Authors: Sayan Goswami, Sovan Pal, Tanmoy Paul
"""

import numpy as np
import pandas as pd
from scipy.stats import norm
from .simulation import simulate_gbm_paths


def black_scholes_call(S0: float, K: float, r: float,
                       sigma: float, T: float) -> float:
    """
    Analytical Black-Scholes price for a European call option.

    Formula:
        C = S0 * N(d1) - K * exp(-rT) * N(d2)

        d1 = [ln(S0/K) + (r + σ²/2)*T] / (σ√T)
        d2 = d1 - σ√T

    Parameters
    ----------
    S0 : float
        Current asset price.
    K : float
        Strike price.
    r : float
        Risk-free interest rate.
    sigma : float
        Volatility.
    T : float
        Time to maturity.

    Returns
    -------
    float
        Black-Scholes call price.
    """
    if T <= 0 or sigma <= 0:
        # At expiry or zero vol, option has intrinsic value only
        return max(S0 - K * np.exp(-r * max(T, 0)), 0.0)

    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call_price = S0 * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    return float(call_price)


def black_scholes_put(S0: float, K: float, r: float,
                      sigma: float, T: float) -> float:
    """
    Analytical Black-Scholes price for a European put option.

    Formula:
        P = K * exp(-rT) * N(-d2) - S0 * N(-d1)

    Uses put-call parity: P = C - S0 + K*exp(-rT)

    Parameters
    ----------
    Same as black_scholes_call.

    Returns
    -------
    float
        Black-Scholes put price.
    """
    if T <= 0 or sigma <= 0:
        return max(K * np.exp(-r * max(T, 0)) - S0, 0.0)

    d1 = (np.log(S0 / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)
    return float(put_price)


def price_european_mc(S0: float, K: float, r: float, sigma: float, T: float,
                      n_steps: int, n_simulations: int,
                      option_type: str = 'call', seed: int = 42) -> dict:
    """
    Price a European option using Monte Carlo simulation.

    This is used for VALIDATION: comparing MC results against
    the Black-Scholes analytical solution.

    European Call Payoff: max(S_T - K, 0)
    European Put Payoff:  max(K - S_T, 0)

    Only the terminal price S_T matters (not the path).

    Parameters
    ----------
    S0, K, r, sigma, T, n_steps, n_simulations, option_type, seed :
        Standard pricing parameters.

    Returns
    -------
    dict
        'price', 'std_error', 'conf_interval'
    """
    paths = simulate_gbm_paths(S0, r, sigma, T, n_steps, n_simulations, seed)
    S_T = paths[:, -1]

    if option_type == 'call':
        payoffs = np.maximum(S_T - K, 0.0)
    else:
        payoffs = np.maximum(K - S_T, 0.0)

    discount_factor = np.exp(-r * T)
    discounted_payoffs = discount_factor * payoffs

    price = np.mean(discounted_payoffs)
    std_error = np.std(discounted_payoffs, ddof=1) / np.sqrt(n_simulations)
    conf_interval = (price - 1.96 * std_error, price + 1.96 * std_error)

    return {
        'price': float(price),
        'std_error': float(std_error),
        'conf_interval': (float(conf_interval[0]), float(conf_interval[1]))
    }


def validate_european_mc(S0: float, K: float, r: float, sigma: float,
                         T: float, n_steps: int,
                         n_simulations_list: list = None,
                         seed: int = 42) -> pd.DataFrame:
    """
    Compare Monte Carlo European option prices against Black-Scholes
    for various simulation counts.

    This demonstrates convergence: as N increases, MC prices approach
    the true BS prices, with error decreasing at rate O(1/√N).

    Parameters
    ----------
    S0, K, r, sigma, T, n_steps : float/int
        Market parameters.
    n_simulations_list : list of int
        Simulation counts to test (default: [100, 500, 1000, 5000, 10000, 50000]).
    seed : int
        Random seed.

    Returns
    -------
    pd.DataFrame
        Columns: n_simulations, mc_call, mc_put, bs_call, bs_put,
                 call_error_pct, put_error_pct, call_std_error, put_std_error
    """
    if n_simulations_list is None:
        n_simulations_list = [100, 500, 1000, 5000, 10000, 50000]

    # Analytical Black-Scholes prices
    bs_call = black_scholes_call(S0, K, r, sigma, T)
    bs_put = black_scholes_put(S0, K, r, sigma, T)

    results = []
    for n_sims in n_simulations_list:
        mc_call_result = price_european_mc(S0, K, r, sigma, T, n_steps,
                                           n_sims, 'call', seed)
        mc_put_result = price_european_mc(S0, K, r, sigma, T, n_steps,
                                          n_sims, 'put', seed)

        # Percentage error relative to BS price
        call_err_pct = abs(mc_call_result['price'] - bs_call) / bs_call * 100 if bs_call > 0 else 0
        put_err_pct = abs(mc_put_result['price'] - bs_put) / bs_put * 100 if bs_put > 0 else 0

        results.append({
            'n_simulations': n_sims,
            'mc_call': round(mc_call_result['price'], 4),
            'mc_put': round(mc_put_result['price'], 4),
            'bs_call': round(bs_call, 4),
            'bs_put': round(bs_put, 4),
            'call_error_pct': round(call_err_pct, 2),
            'put_error_pct': round(put_err_pct, 2),
            'call_std_error': round(mc_call_result['std_error'], 4),
            'put_std_error': round(mc_put_result['std_error'], 4)
        })

    return pd.DataFrame(results)


def convergence_analysis(pricing_func, n_simulations_list: list,
                         S0: float, r: float, sigma: float,
                         T: float, n_steps: int,
                         seed: int = 42, **kwargs) -> pd.DataFrame:
    """
    Analyze Monte Carlo convergence by running pricing at increasing
    simulation counts.

    This helps understand:
    1. How quickly the MC estimate stabilizes.
    2. How standard error decreases with more simulations.
    3. How the confidence interval narrows.

    Parameters
    ----------
    pricing_func : callable
        Option pricing function with standard interface.
    n_simulations_list : list of int
        Increasing simulation counts to test.
    S0, r, sigma, T, n_steps, seed :
        Standard parameters.
    **kwargs :
        Additional args for pricing_func (K, B, option_type, etc.).

    Returns
    -------
    pd.DataFrame
        Columns: n_simulations, price, std_error, lower_ci, upper_ci
    """
    results = []
    for n_sims in n_simulations_list:
        result = pricing_func(S0, r=r, sigma=sigma, T=T,
                              n_steps=n_steps, n_simulations=n_sims,
                              seed=seed, **kwargs)

        results.append({
            'n_simulations': n_sims,
            'price': round(result['price'], 4),
            'std_error': round(result['std_error'], 4),
            'lower_ci': round(result['conf_interval'][0], 4),
            'upper_ci': round(result['conf_interval'][1], 4)
        })

    return pd.DataFrame(results)

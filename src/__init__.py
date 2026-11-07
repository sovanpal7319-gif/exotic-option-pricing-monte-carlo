"""
Exotic Option Pricing – Source Package
======================================
Core modules for Monte Carlo simulation of exotic option pricing
and risk analysis.

Modules:
    simulation      – GBM path generation engine
    asian_option    – Arithmetic-average Asian call/put
    barrier_option  – Knock-in / knock-out barrier options
    lookback_option – Floating-strike lookback call/put
    greeks          – Delta, Gamma, Vega via finite differences
    data_processing – CSV loading & parameter estimation
    validation      – Black-Scholes benchmark & convergence

Authors: Sayan Goswami, Sovan Pal, Tanmoy Paul
"""

from .simulation import simulate_gbm_paths, simulate_gbm_paths_antithetic
from .asian_option import price_asian_option
from .barrier_option import price_barrier_option
from .lookback_option import price_lookback_option
from .greeks import calculate_delta, calculate_gamma, calculate_vega, calculate_all_greeks
from .data_processing import (
    load_price_data,
    calculate_log_returns,
    calculate_historical_volatility,
    estimate_parameters,
    create_sample_data,
)
from .validation import (
    black_scholes_call,
    black_scholes_put,
    price_european_mc,
    validate_european_mc,
    convergence_analysis,
)

__all__ = [
    "simulate_gbm_paths",
    "simulate_gbm_paths_antithetic",
    "price_asian_option",
    "price_barrier_option",
    "price_lookback_option",
    "calculate_delta",
    "calculate_gamma",
    "calculate_vega",
    "calculate_all_greeks",
    "load_price_data",
    "calculate_log_returns",
    "calculate_historical_volatility",
    "estimate_parameters",
    "create_sample_data",
    "black_scholes_call",
    "black_scholes_put",
    "price_european_mc",
    "validate_european_mc",
    "convergence_analysis",
]

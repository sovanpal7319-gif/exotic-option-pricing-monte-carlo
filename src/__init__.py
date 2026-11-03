"""
Exotic Option Pricing – Source Package
======================================
Core modules for Monte Carlo pricing of exotic options.
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

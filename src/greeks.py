"""
Greeks Calculation Module
=========================
Calculates option price sensitivities (Greeks) using finite differences.

Greeks measure how the option price changes when a market parameter
changes, holding all other parameters constant. They are essential
for risk management and hedging.

Greeks Implemented:
    Delta (Δ) = ∂V/∂S
        Sensitivity of option price to changes in the underlying asset price.
        Interpretation: If Delta = 0.5, a $1 increase in asset price causes
        a ~$0.50 increase in option price.
        Range: [0, 1] for calls, [-1, 0] for puts (approximately).
        Used for: Delta hedging — hold Delta units of the asset to neutralize
        price risk.

    Gamma (Γ) = ∂²V/∂S²
        Rate of change of Delta with respect to asset price.
        Interpretation: If Gamma is high, Delta changes rapidly and the
        hedge must be rebalanced frequently.
        Always positive for long option positions.
        Used for: Assessing rebalancing frequency and convexity risk.

    Vega (ν) = ∂V/∂σ
        Sensitivity of option price to changes in volatility.
        Interpretation: If Vega = 15, a 1% increase in volatility causes
        a ~$0.15 increase in option price.
        Always positive for long options (higher vol → higher option value).
        Used for: Managing volatility exposure.

Numerical Method: Central Finite Differences
    We use central differences because they provide O(h²) accuracy,
    which is superior to forward differences (O(h) accuracy).

    Central difference for first derivative:
        f'(x) ≈ [f(x+h) - f(x-h)] / (2h)

    Central difference for second derivative:
        f''(x) ≈ [f(x+h) - 2f(x) + f(x-h)] / h²

    Bump sizes:
        - For Delta/Gamma: h = 1% of S0 (h = 0.01 * S0)
        - For Vega: ε = 0.01 (1 percentage point of volatility)

    Using the SAME random seed for all bumped prices ensures that
    differences come from parameter changes, not random noise.

Authors: Sayan Goswami, Sovan Pal, Tanmoy Paul
"""

import numpy as np


def calculate_delta(pricing_func, S0: float, r: float, sigma: float,
                    T: float, n_steps: int, n_simulations: int,
                    h_pct: float = 0.01, seed: int = 42, **kwargs) -> float:
    """
    Calculate Delta using central finite difference.

    Delta ≈ [V(S0 + h) - V(S0 - h)] / (2h)

    Parameters
    ----------
    pricing_func : callable
        Option pricing function. Must accept S0 as first positional arg,
        plus keyword args r, sigma, T, n_steps, n_simulations, seed.
        Must return a dict with 'price' key.
    S0 : float
        Current asset price.
    r, sigma, T, n_steps, n_simulations, seed :
        Parameters passed to pricing_func.
    h_pct : float
        Bump size as fraction of S0 (default: 0.01 = 1%).
    **kwargs :
        Additional keyword arguments for pricing_func (e.g., K, B, option_type).

    Returns
    -------
    float
        Estimated Delta.
    """
    h = h_pct * S0  # Absolute bump size

    # Price with S0 bumped up and down, using SAME seed for noise cancellation
    price_up = pricing_func(S0 + h, r=r, sigma=sigma, T=T,
                            n_steps=n_steps, n_simulations=n_simulations,
                            seed=seed, **kwargs)['price']
    price_down = pricing_func(S0 - h, r=r, sigma=sigma, T=T,
                              n_steps=n_steps, n_simulations=n_simulations,
                              seed=seed, **kwargs)['price']

    delta = (price_up - price_down) / (2 * h)
    return float(delta)


def calculate_gamma(pricing_func, S0: float, r: float, sigma: float,
                    T: float, n_steps: int, n_simulations: int,
                    h_pct: float = 0.01, seed: int = 42, **kwargs) -> float:
    """
    Calculate Gamma using central finite difference.

    Gamma ≈ [V(S0 + h) - 2V(S0) + V(S0 - h)] / h²

    Parameters
    ----------
    Same as calculate_delta.

    Returns
    -------
    float
        Estimated Gamma.
    """
    h = h_pct * S0

    price_up = pricing_func(S0 + h, r=r, sigma=sigma, T=T,
                            n_steps=n_steps, n_simulations=n_simulations,
                            seed=seed, **kwargs)['price']
    price_mid = pricing_func(S0, r=r, sigma=sigma, T=T,
                             n_steps=n_steps, n_simulations=n_simulations,
                             seed=seed, **kwargs)['price']
    price_down = pricing_func(S0 - h, r=r, sigma=sigma, T=T,
                              n_steps=n_steps, n_simulations=n_simulations,
                              seed=seed, **kwargs)['price']

    gamma = (price_up - 2 * price_mid + price_down) / (h ** 2)
    return float(gamma)


def calculate_vega(pricing_func, S0: float, r: float, sigma: float,
                   T: float, n_steps: int, n_simulations: int,
                   epsilon: float = 0.01, seed: int = 42, **kwargs) -> float:
    """
    Calculate Vega using central finite difference.

    Vega ≈ [V(σ + ε) - V(σ - ε)] / (2ε)

    Note: Vega is typically quoted as the price change for a 1 percentage
    point change in volatility.

    Parameters
    ----------
    pricing_func : callable
        Option pricing function.
    epsilon : float
        Volatility bump size (default: 0.01 = 1 percentage point).
    Other parameters same as calculate_delta.

    Returns
    -------
    float
        Estimated Vega.
    """
    # Ensure sigma - epsilon stays positive
    sigma_up = sigma + epsilon
    sigma_down = max(sigma - epsilon, 0.001)
    actual_epsilon = (sigma_up - sigma_down) / 2.0

    price_up = pricing_func(S0, r=r, sigma=sigma_up, T=T,
                            n_steps=n_steps, n_simulations=n_simulations,
                            seed=seed, **kwargs)['price']
    price_down = pricing_func(S0, r=r, sigma=sigma_down, T=T,
                              n_steps=n_steps, n_simulations=n_simulations,
                              seed=seed, **kwargs)['price']

    vega = (price_up - price_down) / (2 * actual_epsilon)
    return float(vega)


def calculate_all_greeks(pricing_func, S0: float, r: float, sigma: float,
                         T: float, n_steps: int, n_simulations: int,
                         seed: int = 42, **kwargs) -> dict:
    """
    Calculate all Greeks (Delta, Gamma, Vega) for a given option.

    This is a convenience function that calls calculate_delta,
    calculate_gamma, and calculate_vega and returns all results
    in a single dictionary.

    Parameters
    ----------
    pricing_func : callable
        Option pricing function with standard interface.
    S0, r, sigma, T, n_steps, n_simulations, seed :
        Standard pricing parameters.
    **kwargs :
        Additional arguments for pricing_func (K, B, option_type, etc.).

    Returns
    -------
    dict
        'delta' : float — price sensitivity to asset price
        'gamma' : float — second-order sensitivity to asset price
        'vega'  : float — sensitivity to volatility
    """
    delta = calculate_delta(pricing_func, S0, r, sigma, T,
                            n_steps, n_simulations, seed=seed, **kwargs)
    gamma = calculate_gamma(pricing_func, S0, r, sigma, T,
                            n_steps, n_simulations, seed=seed, **kwargs)
    vega = calculate_vega(pricing_func, S0, r, sigma, T,
                          n_steps, n_simulations, seed=seed, **kwargs)

    return {
        'delta': delta,
        'gamma': gamma,
        'vega': vega
    }

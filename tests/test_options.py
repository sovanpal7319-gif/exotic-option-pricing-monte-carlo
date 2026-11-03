"""
Tests for Exotic Option Pricing Modules.
Validates payoff calculations, price properties, and convergence.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from src.asian_option import price_asian_option
from src.barrier_option import price_barrier_option
from src.lookback_option import price_lookback_option
from src.validation import black_scholes_call, black_scholes_put


class TestAsianOption:
    """Tests for Asian option pricing."""

    def setup_method(self):
        self.S0 = 100.0
        self.K = 100.0
        self.r = 0.05
        self.sigma = 0.20
        self.T = 1.0
        self.n_steps = 252
        self.n_sims = 10000
        self.seed = 42

    def test_call_price_positive(self):
        result = price_asian_option(self.S0, self.K, self.r, self.sigma, self.T,
                                     self.n_steps, self.n_sims, 'call', self.seed)
        assert result['price'] > 0

    def test_put_price_positive(self):
        result = price_asian_option(self.S0, self.K, self.r, self.sigma, self.T,
                                     self.n_steps, self.n_sims, 'put', self.seed)
        assert result['price'] > 0

    def test_asian_cheaper_than_european(self):
        """Asian call should be cheaper than European call."""
        asian = price_asian_option(self.S0, self.K, self.r, self.sigma, self.T,
                                    self.n_steps, self.n_sims, 'call', self.seed)
        european = black_scholes_call(self.S0, self.K, self.r, self.sigma, self.T)
        assert asian['price'] < european * 1.1

    def test_result_keys(self):
        result = price_asian_option(self.S0, self.K, self.r, self.sigma, self.T,
                                     self.n_steps, self.n_sims, 'call', self.seed)
        for key in ['price', 'std_error', 'conf_interval', 'payoffs', 'paths']:
            assert key in result

    def test_confidence_interval(self):
        result = price_asian_option(self.S0, self.K, self.r, self.sigma, self.T,
                                     self.n_steps, self.n_sims, 'call', self.seed)
        assert result['conf_interval'][0] <= result['price'] <= result['conf_interval'][1]

    def test_deep_itm_call(self):
        result = price_asian_option(self.S0, 50.0, self.r, self.sigma, self.T,
                                     self.n_steps, self.n_sims, 'call', self.seed)
        assert result['price'] > 30

    def test_deep_otm_call(self):
        result = price_asian_option(self.S0, 200.0, self.r, self.sigma, self.T,
                                     self.n_steps, self.n_sims, 'call', self.seed)
        assert result['price'] < 5


class TestBarrierOption:
    """Tests for Barrier option pricing."""

    def setup_method(self):
        self.S0 = 100.0
        self.K = 100.0
        self.r = 0.05
        self.sigma = 0.20
        self.T = 1.0
        self.B = 80.0
        self.n_steps = 252
        self.n_sims = 10000
        self.seed = 42

    def test_down_out_call_nonnegative(self):
        result = price_barrier_option(self.S0, self.K, self.r, self.sigma, self.T,
                                       self.B, self.n_steps, self.n_sims,
                                       'call', 'down-and-out', self.seed)
        assert result['price'] >= 0

    def test_down_out_cheaper_than_european(self):
        barrier = price_barrier_option(self.S0, self.K, self.r, self.sigma, self.T,
                                        self.B, self.n_steps, self.n_sims,
                                        'call', 'down-and-out', self.seed)
        european = black_scholes_call(self.S0, self.K, self.r, self.sigma, self.T)
        assert barrier['price'] <= european * 1.05

    def test_knocked_out_percentage(self):
        result = price_barrier_option(self.S0, self.K, self.r, self.sigma, self.T,
                                       self.B, self.n_steps, self.n_sims,
                                       'call', 'down-and-out', self.seed)
        assert 0 < result['knocked_out_pct'] < 100

    def test_high_barrier_many_knockouts(self):
        result = price_barrier_option(self.S0, self.K, self.r, self.sigma, self.T,
                                       B=99.0, n_steps=self.n_steps,
                                       n_simulations=self.n_sims,
                                       option_type='call',
                                       barrier_type='down-and-out', seed=self.seed)
        assert result['knocked_out_pct'] > 50

    def test_low_barrier_approaches_european(self):
        barrier = price_barrier_option(self.S0, self.K, self.r, self.sigma, self.T,
                                        B=10.0, n_steps=self.n_steps,
                                        n_simulations=self.n_sims,
                                        option_type='call',
                                        barrier_type='down-and-out', seed=self.seed)
        european = black_scholes_call(self.S0, self.K, self.r, self.sigma, self.T)
        assert abs(barrier['price'] - european) / european < 0.15

    def test_result_keys(self):
        result = price_barrier_option(self.S0, self.K, self.r, self.sigma, self.T,
                                       self.B, self.n_steps, self.n_sims,
                                       'call', 'down-and-out', self.seed)
        for key in ['price', 'std_error', 'conf_interval', 'payoffs', 'paths', 'knocked_out_pct']:
            assert key in result


class TestLookbackOption:
    """Tests for Lookback option pricing."""

    def setup_method(self):
        self.S0 = 100.0
        self.r = 0.05
        self.sigma = 0.20
        self.T = 1.0
        self.n_steps = 252
        self.n_sims = 10000
        self.seed = 42

    def test_call_price_positive(self):
        result = price_lookback_option(self.S0, self.r, self.sigma, self.T,
                                        self.n_steps, self.n_sims, 'call', self.seed)
        assert result['price'] > 0

    def test_put_price_positive(self):
        result = price_lookback_option(self.S0, self.r, self.sigma, self.T,
                                        self.n_steps, self.n_sims, 'put', self.seed)
        assert result['price'] > 0

    def test_lookback_more_expensive_than_european_atm(self):
        lookback = price_lookback_option(self.S0, self.r, self.sigma, self.T,
                                          self.n_steps, self.n_sims, 'call', self.seed)
        european = black_scholes_call(self.S0, self.S0, self.r, self.sigma, self.T)
        assert lookback['price'] > european * 0.9

    def test_all_payoffs_nonnegative(self):
        result = price_lookback_option(self.S0, self.r, self.sigma, self.T,
                                        self.n_steps, self.n_sims, 'call', self.seed)
        assert np.all(result['payoffs'] >= -1e-10)

    def test_higher_vol_higher_price(self):
        low_vol = price_lookback_option(self.S0, self.r, 0.10, self.T,
                                         self.n_steps, self.n_sims, 'call', self.seed)
        high_vol = price_lookback_option(self.S0, self.r, 0.40, self.T,
                                          self.n_steps, self.n_sims, 'call', self.seed)
        assert high_vol['price'] > low_vol['price']

    def test_result_keys(self):
        result = price_lookback_option(self.S0, self.r, self.sigma, self.T,
                                        self.n_steps, self.n_sims, 'call', self.seed)
        for key in ['price', 'std_error', 'conf_interval', 'payoffs', 'paths']:
            assert key in result


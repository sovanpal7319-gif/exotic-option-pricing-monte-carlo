"""
Tests for Greeks Calculation Module.
Validates finite difference approximations.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from src.greeks import calculate_delta, calculate_gamma, calculate_vega, calculate_all_greeks
from src.asian_option import price_asian_option
from src.lookback_option import price_lookback_option


class TestGreeks:
    """Tests for Greeks via finite differences."""

    def setup_method(self):
        self.S0 = 100.0
        self.K = 100.0
        self.r = 0.05
        self.sigma = 0.20
        self.T = 1.0
        self.n_steps = 100
        self.n_sims = 10000
        self.seed = 42

    def test_delta_positive_for_call(self):
        delta = calculate_delta(price_asian_option, self.S0, self.r, self.sigma,
                                self.T, self.n_steps, self.n_sims, seed=self.seed,
                                K=self.K, option_type='call')
        assert delta > 0

    def test_delta_negative_for_put(self):
        delta = calculate_delta(price_asian_option, self.S0, self.r, self.sigma,
                                self.T, self.n_steps, self.n_sims, seed=self.seed,
                                K=self.K, option_type='put')
        assert delta < 0

    def test_delta_bounded(self):
        delta = calculate_delta(price_asian_option, self.S0, self.r, self.sigma,
                                self.T, self.n_steps, self.n_sims, seed=self.seed,
                                K=self.K, option_type='call')
        assert -1.5 <= delta <= 1.5

    def test_gamma_positive(self):
        gamma = calculate_gamma(price_asian_option, self.S0, self.r, self.sigma,
                                self.T, self.n_steps, self.n_sims, seed=self.seed,
                                K=self.K, option_type='call')
        assert gamma > -0.05  # Allow MC noise

    def test_vega_positive(self):
        vega = calculate_vega(price_asian_option, self.S0, self.r, self.sigma,
                              self.T, self.n_steps, self.n_sims, seed=self.seed,
                              K=self.K, option_type='call')
        assert vega > 0

    def test_all_greeks_returns_dict(self):
        greeks = calculate_all_greeks(price_asian_option, self.S0, self.r, self.sigma,
                                       self.T, self.n_steps, self.n_sims, seed=self.seed,
                                       K=self.K, option_type='call')
        assert 'delta' in greeks
        assert 'gamma' in greeks
        assert 'vega' in greeks

    def test_lookback_delta_positive(self):
        delta = calculate_delta(price_lookback_option, self.S0, self.r, self.sigma,
                                self.T, self.n_steps, self.n_sims, seed=self.seed,
                                option_type='call')
        assert delta > 0

    def test_lookback_vega_positive(self):
        vega = calculate_vega(price_lookback_option, self.S0, self.r, self.sigma,
                              self.T, self.n_steps, self.n_sims, seed=self.seed,
                              option_type='call')
        assert vega > 0


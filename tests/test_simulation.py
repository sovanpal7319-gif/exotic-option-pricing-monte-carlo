"""
Tests for the Monte Carlo Simulation Engine.
Verifies GBM path properties and statistical correctness.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import numpy as np
import pytest
from src.simulation import simulate_gbm_paths, simulate_gbm_paths_antithetic


class TestGBMSimulation:
    """Test suite for GBM path simulation."""

    def setup_method(self):
        """Common test parameters."""
        self.S0 = 100.0
        self.r = 0.05
        self.sigma = 0.20
        self.T = 1.0
        self.n_steps = 252
        self.n_simulations = 10000
        self.seed = 42

    def test_output_shape(self):
        """Paths array should have shape (n_simulations, n_steps + 1)."""
        paths = simulate_gbm_paths(self.S0, self.r, self.sigma, self.T,
                                    self.n_steps, self.n_simulations, self.seed)
        assert paths.shape == (self.n_simulations, self.n_steps + 1)

    def test_initial_price(self):
        """All paths should start at S0."""
        paths = simulate_gbm_paths(self.S0, self.r, self.sigma, self.T,
                                    self.n_steps, self.n_simulations, self.seed)
        np.testing.assert_array_almost_equal(paths[:, 0], self.S0)

    def test_positive_prices(self):
        """All simulated prices should be positive (GBM property)."""
        paths = simulate_gbm_paths(self.S0, self.r, self.sigma, self.T,
                                    self.n_steps, self.n_simulations, self.seed)
        assert np.all(paths > 0)

    def test_reproducibility(self):
        """Same seed should produce identical paths."""
        paths1 = simulate_gbm_paths(self.S0, self.r, self.sigma, self.T,
                                     self.n_steps, self.n_simulations, self.seed)
        paths2 = simulate_gbm_paths(self.S0, self.r, self.sigma, self.T,
                                     self.n_steps, self.n_simulations, self.seed)
        np.testing.assert_array_equal(paths1, paths2)

    def test_risk_neutral_drift(self):
        """Under risk-neutral measure, E[S_T] should be approx S0 * exp(r*T)."""
        n_sims = 50000
        paths = simulate_gbm_paths(self.S0, self.r, self.sigma, self.T,
                                    self.n_steps, n_sims, self.seed)
        expected_final = self.S0 * np.exp(self.r * self.T)
        mean_final = np.mean(paths[:, -1])
        assert abs(mean_final - expected_final) / expected_final < 0.01

    def test_different_seeds(self):
        """Different seeds should produce different paths."""
        paths1 = simulate_gbm_paths(self.S0, self.r, self.sigma, self.T,
                                     self.n_steps, 100, seed=42)
        paths2 = simulate_gbm_paths(self.S0, self.r, self.sigma, self.T,
                                     self.n_steps, 100, seed=123)
        assert not np.array_equal(paths1, paths2)

    def test_volatility_effect(self):
        """Higher volatility should produce wider distribution of final prices."""
        paths_low = simulate_gbm_paths(self.S0, self.r, 0.10, self.T,
                                        self.n_steps, self.n_simulations, self.seed)
        paths_high = simulate_gbm_paths(self.S0, self.r, 0.40, self.T,
                                         self.n_steps, self.n_simulations, self.seed)
        assert np.std(paths_high[:, -1]) > np.std(paths_low[:, -1])

    def test_invalid_inputs(self):
        """Negative or zero inputs should raise ValueError."""
        with pytest.raises(ValueError):
            simulate_gbm_paths(-100, self.r, self.sigma, self.T,
                                self.n_steps, self.n_simulations, self.seed)
        with pytest.raises(ValueError):
            simulate_gbm_paths(self.S0, self.r, -0.1, self.T,
                                self.n_steps, self.n_simulations, self.seed)

    def test_antithetic(self):
        """Antithetic paths should have correct shape."""
        paths = simulate_gbm_paths_antithetic(
            self.S0, self.r, self.sigma, self.T,
            self.n_steps, self.n_simulations, self.seed)
        assert paths.shape == (self.n_simulations, self.n_steps + 1)
        assert np.all(paths > 0)
        np.testing.assert_array_almost_equal(paths[:, 0], self.S0)


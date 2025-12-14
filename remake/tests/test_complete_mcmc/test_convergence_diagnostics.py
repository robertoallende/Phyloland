"""
Test Convergence Diagnostics - Subunit 6.2
Validate ESS calculation and convergence monitoring match phyloland
"""

import pytest
import numpy as np
from phyloland.mcmc.convergence_diagnostics import ConvergenceDiagnostics, ConvergenceMonitor
from phyloland.mcmc.convergent_mcmc import ConvergentMCMC

class TestConvergenceDiagnostics:
    """Test convergence diagnostics functionality"""
    
    @pytest.fixture
    def diagnostics(self):
        """Create convergence diagnostics for testing"""
        return ConvergenceDiagnostics(ess_threshold=200)
        
    @pytest.fixture
    def monitor(self, diagnostics):
        """Create convergence monitor for testing"""
        return ConvergenceMonitor(diagnostics, check_frequency=100)
        
    @pytest.fixture
    def banza_data(self):
        """Hawaiian islands test data"""
        locations = [
            (21.3099, -157.8581),  # Oahu
            (20.7984, -156.3319),  # Maui  
            (19.5429, -155.6659),  # Big Island
            (22.0964, -159.5261),  # Kauai
        ]
        location_names = ["Oahu", "Maui", "BigIsland", "Kauai"]
        tree = None
        return tree, locations, location_names
        
    def test_autocorrelation_calculation(self, diagnostics):
        """Test autocorrelation function calculation"""
        # Create test samples with known autocorrelation
        np.random.seed(42)
        n = 1000
        samples = np.random.normal(0, 1, n)
        
        # Calculate autocorrelation
        autocorr = diagnostics.calculate_autocorrelation(samples)
        
        # Should start at 1.0 (lag 0)
        assert np.isclose(autocorr[0], 1.0)
        
        # Should decrease for independent samples
        assert len(autocorr) > 10
        assert all(np.isfinite(autocorr))
        
    def test_ess_calculation_basic(self, diagnostics):
        """Test basic ESS calculation"""
        # Independent samples should have ESS ≈ n
        np.random.seed(42)
        independent_samples = np.random.normal(0, 1, 1000)
        ess_indep = diagnostics.calculate_ess(independent_samples)
        
        # Should be close to sample size for independent samples
        assert ess_indep > 500  # At least half the samples
        assert ess_indep <= 1000  # Can't exceed sample size
        
        # Highly correlated samples should have low ESS
        correlated_samples = np.cumsum(np.random.normal(0, 0.1, 1000))
        ess_corr = diagnostics.calculate_ess(correlated_samples)
        
        # Should be much lower than independent case
        assert ess_corr < ess_indep / 2
        
    def test_ess_edge_cases(self, diagnostics):
        """Test ESS calculation edge cases"""
        # Empty samples
        ess_empty = diagnostics.calculate_ess(np.array([]))
        assert ess_empty == 0.0
        
        # Very short samples
        ess_short = diagnostics.calculate_ess(np.array([1.0, 2.0]))
        assert ess_short == 0.0
        
        # Constant samples
        ess_constant = diagnostics.calculate_ess(np.ones(100))
        assert ess_constant >= 1.0
        
    def test_rhat_calculation(self, diagnostics):
        """Test Gelman-Rubin R-hat statistic"""
        np.random.seed(42)
        
        # Identical chains should have R-hat ≈ 1
        chain1 = np.random.normal(0, 1, 1000)
        chain2 = chain1 + np.random.normal(0, 0.01, 1000)  # Nearly identical
        rhat_good = diagnostics.calculate_rhat([chain1, chain2])
        
        assert 0.9 <= rhat_good <= 1.1
        
        # Very different chains should have R-hat > 1
        chain3 = np.random.normal(5, 1, 1000)  # Different mean
        rhat_bad = diagnostics.calculate_rhat([chain1, chain3])
        
        assert rhat_bad > 1.1
        
    def test_parameter_convergence_check(self, diagnostics):
        """Test convergence checking for individual parameters"""
        # Well-mixed samples (should converge)
        np.random.seed(42)
        good_samples = np.random.normal(0, 1, 1000)
        result_good = diagnostics.check_parameter_convergence(good_samples)
        
        assert 'ess' in result_good
        assert 'converged' in result_good
        assert result_good['ess'] > 0
        assert result_good['ess_threshold'] == 200
        
        # Poorly mixed samples (should not converge)
        poor_samples = np.repeat([1, 2], 500)  # Alternating pattern
        result_poor = diagnostics.check_parameter_convergence(poor_samples)
        
        assert result_poor['ess'] < result_good['ess']
        
    def test_convergence_monitor_frequency(self, monitor):
        """Test convergence checking frequency"""
        # Should check at specified intervals
        assert not monitor.should_check_convergence(50)   # Too early
        assert monitor.should_check_convergence(100)      # First check
        assert not monitor.should_check_convergence(150)  # Too soon
        assert monitor.should_check_convergence(200)      # Second check
        
    def test_convergence_monitor_multi_parameter(self, monitor):
        """Test convergence checking across multiple parameters"""
        # Create sample data
        samples_dict = {
            'sigma1': list(np.random.normal(1.0, 0.1, 1000)),
            'sigma2': list(np.random.normal(0.5, 0.05, 1000)),
            'lambda': list(np.random.normal(0.8, 0.1, 100)),  # Fewer samples
            'Lambda': list(np.random.normal(2.0, 0.2, 1000))
        }
        
        results = monitor.check_convergence(samples_dict)
        
        # Should have results for all parameters
        assert len(results) == 4
        for param in ['sigma1', 'sigma2', 'lambda', 'Lambda']:
            assert param in results
            assert 'ess' in results[param]
            assert 'converged' in results[param]
            
        # Lambda should not converge (too few samples)
        assert not results['lambda']['converged']
        
    def test_convergence_summary(self, monitor):
        """Test convergence summary generation"""
        # Mock convergence results
        results = {
            'sigma1': {'ess': 250.0, 'ess_threshold': 200, 'converged': True},
            'sigma2': {'ess': 150.0, 'ess_threshold': 200, 'converged': False},
        }
        
        summary = monitor.get_convergence_summary(results)
        
        assert "sigma1" in summary
        assert "sigma2" in summary
        assert "✓" in summary  # Converged parameter
        assert "✗" in summary  # Non-converged parameter
        assert "RUNNING" in summary  # Overall status
        
    def test_convergent_mcmc_initialization(self, banza_data):
        """Test ConvergentMCMC initialization"""
        tree, locations, location_names = banza_data
        
        mcmc = ConvergentMCMC(tree, locations, location_names, 
                             ess_threshold=150, check_frequency=50)
        
        assert mcmc.diagnostics.ess_threshold == 150
        assert mcmc.monitor.check_frequency == 50
        assert hasattr(mcmc, 'convergence_history')
        
    def test_convergent_mcmc_fixed_steps(self, banza_data):
        """Test fixed-step MCMC with convergence monitoring"""
        tree, locations, location_names = banza_data
        
        mcmc = ConvergentMCMC(tree, locations, location_names, ess_threshold=50)
        
        # Run short MCMC
        result = mcmc.run_fixed_steps(n_steps=200, burnin=50, thin=5)
        
        # Verify result structure
        assert 'samples' in result
        assert 'converged' in result
        assert 'total_steps' in result
        assert 'final_diagnostics' in result
        
        # Should have collected samples
        assert len(result['samples']['sigma1']) > 0
        
    def test_convergent_mcmc_until_convergence(self, banza_data):
        """Test MCMC with automatic stopping"""
        tree, locations, location_names = banza_data
        
        # Use low threshold for quick convergence in test
        mcmc = ConvergentMCMC(tree, locations, location_names, 
                             ess_threshold=10, check_frequency=50)
        
        # Run until convergence (should be quick with low threshold)
        result = mcmc.run_until_convergence(max_steps=1000, burnin=100, 
                                          thin=2, min_samples=50)
        
        # Verify result structure
        assert 'converged' in result
        assert 'convergence_step' in result
        assert 'convergence_history' in result
        assert 'final_diagnostics' in result
        
        # Should have convergence history
        assert len(result['convergence_history']) > 0
        
    def test_final_diagnostics(self, banza_data):
        """Test final diagnostics collection"""
        tree, locations, location_names = banza_data
        
        mcmc = ConvergentMCMC(tree, locations, location_names)
        mcmc.run_fixed_steps(n_steps=200, burnin=50, thin=5)
        
        diagnostics = mcmc.get_final_diagnostics()
        
        # Should have ESS for all parameters
        assert 'final_ess' in diagnostics
        assert 'sigma1' in diagnostics['final_ess']
        assert 'sigma2' in diagnostics['final_ess']
        assert 'lambda' in diagnostics['final_ess']
        assert 'Lambda' in diagnostics['final_ess']
        
        # All ESS values should be positive
        for ess in diagnostics['final_ess'].values():
            assert ess > 0

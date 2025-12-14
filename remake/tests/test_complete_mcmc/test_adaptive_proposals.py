"""
Test Adaptive Parameter Proposals - Subunit 6.1
Validate adaptive MCMC proposals match phyloland efficiency
"""

import pytest
import numpy as np
from phyloland.mcmc.adaptive_proposals import AdaptiveProposer, ParameterProposer
from phyloland.mcmc.advanced_mcmc import AdvancedMCMC

class TestAdaptiveProposals:
    """Test adaptive proposal mechanisms"""
    
    @pytest.fixture
    def adaptive_proposer(self):
        """Create adaptive proposer for testing"""
        return AdaptiveProposer(target_acceptance=0.44)
        
    @pytest.fixture
    def parameter_proposer(self, adaptive_proposer):
        """Create parameter proposer for testing"""
        return ParameterProposer(adaptive_proposer)
        
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
        
    def test_adaptive_proposer_initialization(self, adaptive_proposer):
        """Test adaptive proposer initializes correctly"""
        assert adaptive_proposer.target_acceptance == 0.44
        assert len(adaptive_proposer.step_sizes) == 0
        
        # Initialize parameter
        adaptive_proposer.initialize_parameter('sigma1', 0.1)
        assert 'sigma1' in adaptive_proposer.step_sizes
        assert adaptive_proposer.step_sizes['sigma1'] == 0.1
        assert adaptive_proposer.acceptance_counts['sigma1'] == 0
        
    def test_step_size_adaptation(self, adaptive_proposer):
        """Test Robbins-Monro step size adaptation"""
        adaptive_proposer.initialize_parameter('sigma1', 0.1)
        initial_step = adaptive_proposer.step_sizes['sigma1']
        
        # High acceptance should increase step size
        for i in range(100):
            adaptive_proposer.adapt_step_size('sigma1', True, i)
            
        assert adaptive_proposer.step_sizes['sigma1'] > initial_step
        
        # Reset and test low acceptance
        adaptive_proposer.initialize_parameter('sigma2', 0.1)
        initial_step = adaptive_proposer.step_sizes['sigma2']
        
        for i in range(100):
            adaptive_proposer.adapt_step_size('sigma2', False, i)
            
        assert adaptive_proposer.step_sizes['sigma2'] < initial_step
        
    def test_parameter_proposals_positivity(self, parameter_proposer):
        """Test parameter proposals maintain positivity"""
        # Initialize proposer
        parameter_proposer.adaptive_proposer.initialize_parameter('sigma1', 0.1)
        parameter_proposer.adaptive_proposer.initialize_parameter('sigma2', 0.1)
        parameter_proposer.adaptive_proposer.initialize_parameter('lambda', 0.1)
        parameter_proposer.adaptive_proposer.initialize_parameter('tau', 0.1)
        
        # Test sigma proposals
        for _ in range(100):
            sigma1, sigma2 = parameter_proposer.propose_sigma(1.0, 0.5)
            assert sigma1 > 0
            assert sigma2 > 0
            
        # Test lambda proposals
        for _ in range(100):
            lambda_val = parameter_proposer.propose_lambda(0.8)
            assert lambda_val > 0
            
        # Test tau proposals
        for _ in range(100):
            tau = parameter_proposer.propose_tau(2.0)
            assert tau > 0
            
    def test_log_jacobians(self, parameter_proposer):
        """Test log Jacobian calculations for log-space proposals"""
        # Test sigma Jacobian
        jacobian = parameter_proposer.log_jacobian_sigma(1.0, 0.5)
        expected = np.log(1.0) + np.log(0.5)
        assert np.isclose(jacobian, expected)
        
        # Test lambda Jacobian
        jacobian = parameter_proposer.log_jacobian_lambda(0.8)
        expected = np.log(0.8)
        assert np.isclose(jacobian, expected)
        
        # Test tau Jacobian
        jacobian = parameter_proposer.log_jacobian_tau(2.0)
        expected = np.log(2.0)
        assert np.isclose(jacobian, expected)
        
    def test_advanced_mcmc_initialization(self, banza_data):
        """Test AdvancedMCMC initializes with adaptive proposals"""
        tree, locations, location_names = banza_data
        
        # Test with adaptive proposals
        mcmc = AdvancedMCMC(tree, locations, location_names, adaptive_proposals=True)
        assert mcmc.adaptive_proposals == True
        assert hasattr(mcmc, 'adaptive_proposer')
        assert hasattr(mcmc, 'parameter_proposer')
        
        # Test without adaptive proposals
        mcmc_basic = AdvancedMCMC(tree, locations, location_names, adaptive_proposals=False)
        assert mcmc_basic.adaptive_proposals == False
        
    def test_adaptive_mcmc_run(self, banza_data):
        """Test adaptive MCMC runs without errors"""
        tree, locations, location_names = banza_data
        
        mcmc = AdvancedMCMC(tree, locations, location_names, adaptive_proposals=True)
        
        # Run short MCMC
        samples = mcmc.run_adaptive_mcmc(n_steps=200, burnin=50, thin=5)
        
        # Verify samples collected
        assert len(samples['sigma1']) > 0
        assert len(samples['sigma2']) > 0
        assert len(samples['lambda']) > 0
        assert len(samples['Lambda']) > 0
        
        # Verify parameters remain positive
        assert all(s > 0 for s in samples['sigma1'])
        assert all(s > 0 for s in samples['sigma2'])
        assert all(s > 0 for s in samples['lambda'])
        assert all(s > 0 for s in samples['Lambda'])
        
    def test_adaptation_diagnostics(self, banza_data):
        """Test adaptation diagnostics are collected"""
        tree, locations, location_names = banza_data
        
        mcmc = AdvancedMCMC(tree, locations, location_names, adaptive_proposals=True)
        mcmc.run_adaptive_mcmc(n_steps=100, burnin=20, thin=5)
        
        diagnostics = mcmc.get_adaptation_diagnostics()
        
        # Verify diagnostics for all parameters
        for param in ['sigma1', 'sigma2', 'lambda', 'Lambda']:
            assert param in diagnostics
            assert 'acceptance_rate' in diagnostics[param]
            assert 'final_step_size' in diagnostics[param]
            assert 'total_proposals' in diagnostics[param]
            
            # Verify reasonable values
            assert 0 <= diagnostics[param]['acceptance_rate'] <= 1
            assert diagnostics[param]['final_step_size'] > 0
            assert diagnostics[param]['total_proposals'] > 0
            
    def test_acceptance_rate_targeting(self, banza_data):
        """Test acceptance rates converge toward target"""
        tree, locations, location_names = banza_data
        
        mcmc = AdvancedMCMC(tree, locations, location_names, adaptive_proposals=True)
        mcmc.run_adaptive_mcmc(n_steps=1000, burnin=200, thin=10)
        
        diagnostics = mcmc.get_adaptation_diagnostics()
        
        # Check acceptance rates are reasonable (not necessarily exact due to short run)
        for param in ['sigma1', 'sigma2', 'lambda', 'Lambda']:
            acc_rate = diagnostics[param]['acceptance_rate']
            # Should be between 10% and 80% for reasonable adaptation
            assert 0.1 <= acc_rate <= 0.8, f"{param} acceptance rate {acc_rate} outside reasonable range"
            
    def test_proposal_ratio_computation(self, banza_data):
        """Test proposal ratio computation includes Jacobians"""
        tree, locations, location_names = banza_data
        
        mcmc = AdvancedMCMC(tree, locations, location_names, adaptive_proposals=True)
        
        current_params = (1.0, 0.5, 0.8, 2.0)
        proposed_params = (1.1, 0.6, 0.9, 2.2)
        
        # Compute proposal ratio
        ratio = mcmc.compute_proposal_ratio(current_params, proposed_params)
        
        # Should be finite
        assert np.isfinite(ratio)
        
        # Test without adaptive proposals (should be 0)
        mcmc_basic = AdvancedMCMC(tree, locations, location_names, adaptive_proposals=False)
        ratio_basic = mcmc_basic.compute_proposal_ratio(current_params, proposed_params)
        assert ratio_basic == 0.0

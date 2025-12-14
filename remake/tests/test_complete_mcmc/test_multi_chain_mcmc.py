"""
Test Multi-Chain MCMC - Subunit 6.3
Validate multi-chain execution and cross-chain diagnostics match phyloland
"""

import pytest
import numpy as np
from phyloland.mcmc.multi_chain_mcmc import CrossChainDiagnostics, MultiChainMonitor, MultiChainMCMC

class TestMultiChainMCMC:
    """Test multi-chain MCMC functionality"""
    
    @pytest.fixture
    def cross_chain_diagnostics(self):
        """Create cross-chain diagnostics for testing"""
        return CrossChainDiagnostics(rhat_threshold=1.1)
        
    @pytest.fixture
    def multi_chain_monitor(self):
        """Create multi-chain monitor for testing"""
        return MultiChainMonitor(ess_threshold=50, rhat_threshold=1.1, check_frequency=100)
        
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
        
    def test_rhat_calculation_identical_chains(self, cross_chain_diagnostics):
        """Test R-hat calculation for identical chains"""
        np.random.seed(42)
        
        # Identical chains should have R-hat ≈ 1
        chain1 = np.random.normal(0, 1, 1000)
        chain2 = chain1.copy()  # Identical
        
        rhat = cross_chain_diagnostics.calculate_rhat([chain1, chain2])
        assert np.isclose(rhat, 1.0, atol=0.01)
        
    def test_rhat_calculation_different_chains(self, cross_chain_diagnostics):
        """Test R-hat calculation for different chains"""
        np.random.seed(42)
        
        # Different chains should have R-hat > 1
        chain1 = np.random.normal(0, 1, 1000)
        chain2 = np.random.normal(2, 1, 1000)  # Different mean
        
        rhat = cross_chain_diagnostics.calculate_rhat([chain1, chain2])
        assert rhat > 1.1
        
    def test_rhat_calculation_converged_chains(self, cross_chain_diagnostics):
        """Test R-hat for chains that should converge"""
        np.random.seed(42)
        
        # Chains with slight differences should have reasonable R-hat
        base_chain = np.random.normal(0, 1, 1000)
        chain1 = base_chain + np.random.normal(0, 0.1, 1000)
        chain2 = base_chain + np.random.normal(0, 0.1, 1000)
        
        rhat = cross_chain_diagnostics.calculate_rhat([chain1, chain2])
        assert 0.9 <= rhat <= 1.2  # Should be reasonable
        
    def test_rhat_edge_cases(self, cross_chain_diagnostics):
        """Test R-hat calculation edge cases"""
        # Single chain
        chain1 = np.random.normal(0, 1, 100)
        rhat_single = cross_chain_diagnostics.calculate_rhat([chain1])
        assert rhat_single == 1.0
        
        # Empty chains
        rhat_empty = cross_chain_diagnostics.calculate_rhat([])
        assert rhat_empty == 1.0
        
        # Very short chains
        short_chain1 = np.array([1.0, 2.0])
        short_chain2 = np.array([1.5, 2.5])
        rhat_short = cross_chain_diagnostics.calculate_rhat([short_chain1, short_chain2])
        assert rhat_short == np.inf
        
    def test_rhat_all_parameters(self, cross_chain_diagnostics):
        """Test R-hat calculation for all parameters"""
        # Mock multi-chain samples
        all_chain_samples = {
            'sigma1': [
                [1.0, 1.1, 1.2] * 100,  # Chain 1
                [1.05, 1.15, 1.25] * 100  # Chain 2
            ],
            'sigma2': [
                [0.8, 0.9, 1.0] * 100,
                [0.85, 0.95, 1.05] * 100
            ],
            'lambda': [
                [0.7, 0.8, 0.9] * 100,
                [2.0, 2.1, 2.2] * 100  # Very different - should have high R-hat
            ]
        }
        
        rhat_results = cross_chain_diagnostics.calculate_rhat_all_parameters(all_chain_samples)
        
        # Should have R-hat for all parameters
        assert 'sigma1' in rhat_results
        assert 'sigma2' in rhat_results
        assert 'lambda' in rhat_results
        
        # Lambda should have high R-hat due to different chains
        assert rhat_results['lambda'] > 1.5
        
    def test_chain_mixing_assessment(self, cross_chain_diagnostics):
        """Test comprehensive chain mixing assessment"""
        # Mock samples with good and poor mixing
        all_chain_samples = {
            'good_param': [
                list(np.random.normal(1.0, 0.1, 200)),
                list(np.random.normal(1.0, 0.1, 200))
            ],
            'poor_param': [
                list(np.random.normal(1.0, 0.1, 200)),
                list(np.random.normal(3.0, 0.1, 200))  # Different mean
            ]
        }
        
        mixing_results = cross_chain_diagnostics.assess_chain_mixing(all_chain_samples)
        
        # Should assess mixing for both parameters
        assert 'good_param' in mixing_results
        assert 'poor_param' in mixing_results
        
        # Good parameter should show good mixing
        assert mixing_results['good_param']['chains_mixed'] == True
        
        # Poor parameter should show poor mixing
        assert mixing_results['poor_param']['chains_mixed'] == False
        
    def test_multi_chain_monitor_convergence_check(self, multi_chain_monitor):
        """Test multi-chain convergence checking"""
        # Mock multi-chain samples
        all_chain_samples = {
            'sigma1': [
                list(np.random.normal(1.0, 0.1, 100)),  # Chain 1
                list(np.random.normal(1.0, 0.1, 100))   # Chain 2
            ],
            'sigma2': [
                list(np.random.normal(0.8, 0.05, 100)),
                list(np.random.normal(0.8, 0.05, 100))
            ]
        }
        
        convergence_results = multi_chain_monitor.check_multi_chain_convergence(all_chain_samples)
        
        # Should have convergence info for all parameters
        assert 'sigma1' in convergence_results
        assert 'sigma2' in convergence_results
        
        for param, result in convergence_results.items():
            assert 'min_ess' in result
            assert 'ess_converged' in result
            assert 'rhat' in result
            assert 'rhat_converged' in result
            assert 'converged' in result
            
    def test_multi_chain_monitor_convergence_criteria(self, multi_chain_monitor):
        """Test multi-chain convergence criteria (both ESS and R-hat)"""
        # Create samples that meet ESS but not R-hat
        np.random.seed(42)
        good_samples = list(np.random.normal(1.0, 0.1, 1000))  # High ESS
        bad_samples = list(np.random.normal(3.0, 0.1, 1000))   # High ESS but different mean
        
        all_chain_samples = {
            'test_param': [good_samples, bad_samples]
        }
        
        convergence_results = multi_chain_monitor.check_multi_chain_convergence(all_chain_samples)
        
        result = convergence_results['test_param']
        
        # Should have high ESS but poor R-hat
        assert result['ess_converged'] == True  # High ESS
        assert result['rhat_converged'] == False  # Poor R-hat
        assert result['converged'] == False  # Overall not converged
        
    def test_multi_chain_mcmc_initialization(self, banza_data):
        """Test MultiChainMCMC initialization"""
        tree, locations, location_names = banza_data
        
        mcmc = MultiChainMCMC(tree, locations, location_names, 
                             n_chains=3, ess_threshold=50, rhat_threshold=1.2)
        
        assert mcmc.n_chains == 3
        assert len(mcmc.chains) == 3
        assert mcmc.monitor.ess_diagnostics.ess_threshold == 50
        assert mcmc.monitor.cross_chain_diagnostics.rhat_threshold == 1.2
        
    def test_overdispersed_initialization(self, banza_data):
        """Test overdispersed chain initialization"""
        tree, locations, location_names = banza_data
        
        mcmc = MultiChainMCMC(tree, locations, location_names, n_chains=4)
        mcmc.initialize_chains_overdispersed()
        
        # Check that chains have different starting values
        starting_values = []
        for chain in mcmc.chains:
            values = (chain.sigma1, chain.sigma2, chain.lambda_param, chain.Lambda)
            starting_values.append(values)
            
        # All values should be positive
        for values in starting_values:
            assert all(v > 0 for v in values)
            
        # Values should be different across chains
        assert len(set(starting_values)) > 1  # At least some different values
        
    def test_chain_sample_collection(self, banza_data):
        """Test collection of samples from multiple chains"""
        tree, locations, location_names = banza_data
        
        mcmc = MultiChainMCMC(tree, locations, location_names, n_chains=2)
        
        # Mock chain results
        chain_results = [
            {'samples': {'sigma1': [1.0, 1.1], 'sigma2': [0.8, 0.9]}},
            {'samples': {'sigma1': [1.2, 1.3], 'sigma2': [0.7, 0.8]}}
        ]
        
        all_samples = mcmc._collect_chain_samples(chain_results)
        
        # Should have samples from both chains
        assert 'sigma1' in all_samples
        assert 'sigma2' in all_samples
        assert len(all_samples['sigma1']) == 2  # Two chains
        assert len(all_samples['sigma2']) == 2  # Two chains
        
        # Check sample values
        assert all_samples['sigma1'][0] == [1.0, 1.1]  # Chain 1
        assert all_samples['sigma1'][1] == [1.2, 1.3]  # Chain 2
        
    def test_multi_chain_run_short(self, banza_data):
        """Test short multi-chain MCMC run"""
        tree, locations, location_names = banza_data
        
        # Use very low thresholds for quick test
        mcmc = MultiChainMCMC(tree, locations, location_names, 
                             n_chains=2, ess_threshold=5, rhat_threshold=2.0)
        
        # Run very short chains
        result = mcmc.run_parallel_chains(max_steps=100, burnin=20, 
                                        thin=2, min_samples=10)
        
        # Verify result structure
        assert 'chain_results' in result
        assert 'all_chain_samples' in result
        assert 'multi_chain_converged' in result
        assert 'final_convergence' in result
        assert 'n_chains' in result
        
        # Should have results from both chains
        assert len(result['chain_results']) == 2
        assert result['n_chains'] == 2

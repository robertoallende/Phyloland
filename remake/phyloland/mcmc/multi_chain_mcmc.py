"""
Multi-Chain MCMC Implementation
Parallel chain execution with cross-chain diagnostics matching phyloland
"""

import numpy as np
from typing import List, Dict, Tuple, Optional
from concurrent.futures import ProcessPoolExecutor, as_completed
import copy
from .convergent_mcmc import ConvergentMCMC
from .convergence_diagnostics import ConvergenceDiagnostics

class CrossChainDiagnostics:
    """Cross-chain convergence diagnostics with R-hat calculation"""
    
    def __init__(self, rhat_threshold: float = 1.1):
        """Initialize cross-chain diagnostics
        
        Args:
            rhat_threshold: R-hat threshold for convergence (phyloland default: 1.1)
        """
        self.rhat_threshold = rhat_threshold
        
    def calculate_rhat(self, chains: List[np.ndarray]) -> float:
        """Calculate Gelman-Rubin R-hat statistic matching phyloland"""
        if len(chains) < 2:
            return 1.0
            
        n_chains = len(chains)
        chain_length = min(len(chain) for chain in chains)
        
        if chain_length < 10:
            return np.inf
            
        # Truncate all chains to same length
        chains_array = np.array([chain[:chain_length] for chain in chains])
        
        # Calculate between and within chain variance
        chain_means = np.mean(chains_array, axis=1)
        overall_mean = np.mean(chain_means)
        
        # Between-chain variance (B)
        B = chain_length * np.var(chain_means, ddof=1) if n_chains > 1 else 0.0
        
        # Within-chain variance (W)
        chain_vars = np.var(chains_array, axis=1, ddof=1)
        W = np.mean(chain_vars)
        
        # Pooled variance estimate
        if chain_length > 1:
            var_plus = ((chain_length - 1) * W + B) / chain_length
        else:
            var_plus = W
            
        # R-hat statistic
        if W > 0:
            rhat = np.sqrt(var_plus / W)
        else:
            rhat = 1.0
            
        return rhat
        
    def calculate_rhat_all_parameters(self, all_chain_samples: Dict[str, List[List[float]]]) -> Dict[str, float]:
        """Calculate R-hat for all parameters across chains"""
        rhat_results = {}
        
        for param_name, param_chains in all_chain_samples.items():
            if param_name != 'likelihood' and len(param_chains) > 1:
                # Convert to numpy arrays
                chains_arrays = [np.array(chain) for chain in param_chains if len(chain) > 0]
                if len(chains_arrays) >= 2:
                    rhat_results[param_name] = self.calculate_rhat(chains_arrays)
                else:
                    rhat_results[param_name] = np.inf
            else:
                rhat_results[param_name] = 1.0
                
        return rhat_results
        
    def assess_chain_mixing(self, all_chain_samples: Dict[str, List[List[float]]]) -> Dict[str, Dict]:
        """Comprehensive chain mixing assessment"""
        mixing_results = {}
        rhat_results = self.calculate_rhat_all_parameters(all_chain_samples)
        
        for param_name, rhat_value in rhat_results.items():
            mixing_results[param_name] = {
                'rhat': rhat_value,
                'rhat_threshold': self.rhat_threshold,
                'chains_mixed': rhat_value <= self.rhat_threshold,
                'n_chains': len(all_chain_samples.get(param_name, []))
            }
            
        return mixing_results

class MultiChainMonitor:
    """Enhanced convergence monitoring for multiple chains"""
    
    def __init__(self, ess_threshold: int = 200, rhat_threshold: float = 1.1, check_frequency: int = 1000):
        """Initialize multi-chain monitor
        
        Args:
            ess_threshold: ESS threshold for within-chain convergence
            rhat_threshold: R-hat threshold for between-chain convergence
            check_frequency: How often to check convergence
        """
        self.ess_diagnostics = ConvergenceDiagnostics(ess_threshold)
        self.cross_chain_diagnostics = CrossChainDiagnostics(rhat_threshold)
        self.check_frequency = check_frequency
        self.last_check = 0
        
    def should_check_convergence(self, iteration: int) -> bool:
        """Determine if convergence should be checked"""
        if iteration - self.last_check >= self.check_frequency:
            self.last_check = iteration
            return True
        return False
        
    def check_multi_chain_convergence(self, all_chain_samples: Dict[str, List[List[float]]]) -> Dict[str, Dict]:
        """Check both ESS and R-hat convergence for all parameters"""
        convergence_results = {}
        
        # Calculate ESS for each chain and parameter
        for param_name, param_chains in all_chain_samples.items():
            if param_name != 'likelihood':
                # ESS for each chain
                chain_ess = []
                for chain_samples in param_chains:
                    if len(chain_samples) > 10:
                        ess = self.ess_diagnostics.calculate_ess(np.array(chain_samples))
                        chain_ess.append(ess)
                    else:
                        chain_ess.append(0.0)
                        
                # R-hat across chains
                if len(param_chains) >= 2:
                    chains_arrays = [np.array(chain) for chain in param_chains if len(chain) > 10]
                    if len(chains_arrays) >= 2:
                        rhat = self.cross_chain_diagnostics.calculate_rhat(chains_arrays)
                    else:
                        rhat = np.inf
                else:
                    rhat = 1.0
                    
                # Combined convergence criteria
                min_ess = min(chain_ess) if chain_ess else 0.0
                ess_converged = min_ess >= self.ess_diagnostics.ess_threshold
                rhat_converged = rhat <= self.cross_chain_diagnostics.rhat_threshold
                
                convergence_results[param_name] = {
                    'min_ess': min_ess,
                    'ess_threshold': self.ess_diagnostics.ess_threshold,
                    'ess_converged': ess_converged,
                    'rhat': rhat,
                    'rhat_threshold': self.cross_chain_diagnostics.rhat_threshold,
                    'rhat_converged': rhat_converged,
                    'converged': ess_converged and rhat_converged,
                    'n_chains': len(param_chains)
                }
                
        return convergence_results
        
    def all_parameters_converged(self, convergence_results: Dict[str, Dict]) -> bool:
        """Check if all parameters have converged (both ESS and R-hat)"""
        if not convergence_results:
            return False
            
        return all(result['converged'] for result in convergence_results.values())
        
    def get_convergence_summary(self, convergence_results: Dict[str, Dict]) -> str:
        """Generate multi-chain convergence summary"""
        if not convergence_results:
            return "No convergence data available"
            
        lines = ["Multi-Chain Convergence Status:"]
        for param, result in convergence_results.items():
            ess_status = "✓" if result['ess_converged'] else "✗"
            rhat_status = "✓" if result['rhat_converged'] else "✗"
            overall_status = "✓" if result['converged'] else "✗"
            
            lines.append(f"  {param}: ESS={result['min_ess']:.1f}/{result['ess_threshold']} {ess_status}, "
                        f"R̂={result['rhat']:.3f}/{result['rhat_threshold']} {rhat_status} → {overall_status}")
            
        all_converged = self.all_parameters_converged(convergence_results)
        overall_status = "ALL CONVERGED" if all_converged else "RUNNING"
        lines.append(f"Overall: {overall_status}")
        
        return "\n".join(lines)

class MultiChainMCMC:
    """Multi-chain MCMC with cross-chain diagnostics"""
    
    def __init__(self, tree, locations, location_names, 
                 n_chains: int = 4,
                 ess_threshold: int = 200,
                 rhat_threshold: float = 1.1,
                 check_frequency: int = 1000,
                 adaptive_proposals: bool = True):
        """Initialize multi-chain MCMC
        
        Args:
            tree: Phylogenetic tree
            locations: Geographic locations  
            location_names: Location names
            n_chains: Number of independent chains
            ess_threshold: ESS threshold for convergence
            rhat_threshold: R-hat threshold for convergence
            check_frequency: Convergence checking frequency
            adaptive_proposals: Use adaptive proposals
        """
        self.tree = tree
        self.locations = locations
        self.location_names = location_names
        self.n_chains = n_chains
        
        # Create individual MCMC instances for each chain
        self.chains = []
        for i in range(n_chains):
            chain = ConvergentMCMC(tree, locations, location_names,
                                 ess_threshold=ess_threshold,
                                 check_frequency=check_frequency,
                                 adaptive_proposals=adaptive_proposals)
            self.chains.append(chain)
            
        # Multi-chain monitoring
        self.monitor = MultiChainMonitor(ess_threshold, rhat_threshold, check_frequency)
        self.convergence_history = []
        
    def initialize_chains_overdispersed(self, base_params: Optional[Tuple] = None):
        """Initialize chains with overdispersed starting values"""
        if base_params is None:
            base_params = (1.0, 0.8, 1.0, 2.0)  # Default starting values
            
        sigma1_base, sigma2_base, lambda_base, Lambda_base = base_params
        
        # Overdispersed initialization (phyloland style)
        np.random.seed(42)  # For reproducible initialization
        
        for i, chain in enumerate(self.chains):
            # Add random perturbations to base parameters
            perturbation = 0.5  # 50% perturbation range
            
            chain.sigma1 = sigma1_base * (1 + np.random.uniform(-perturbation, perturbation))
            chain.sigma2 = sigma2_base * (1 + np.random.uniform(-perturbation, perturbation))
            chain.lambda_param = lambda_base * (1 + np.random.uniform(-perturbation, perturbation))
            chain.Lambda = Lambda_base * (1 + np.random.uniform(-perturbation, perturbation))
            
            # Ensure positivity
            chain.sigma1 = max(0.1, chain.sigma1)
            chain.sigma2 = max(0.1, chain.sigma2)
            chain.lambda_param = max(0.1, chain.lambda_param)
            chain.Lambda = max(0.1, chain.Lambda)
            
    def run_parallel_chains(self, max_steps: int = 100000, 
                          burnin: int = 10000, 
                          thin: int = 10,
                          min_samples: int = 1000) -> Dict:
        """Run multiple chains until convergence with cross-chain monitoring"""
        
        # Initialize chains with overdispersed starting values
        self.initialize_chains_overdispersed()
        
        print(f"Starting {self.n_chains} chains with multi-chain convergence monitoring")
        print(f"ESS threshold: {self.monitor.ess_diagnostics.ess_threshold}")
        print(f"R-hat threshold: {self.monitor.cross_chain_diagnostics.rhat_threshold}")
        
        # Run chains independently (simplified - not truly parallel for now)
        chain_results = []
        for i, chain in enumerate(self.chains):
            print(f"\nRunning chain {i+1}/{self.n_chains}...")
            result = chain.run_until_convergence(max_steps, burnin, thin, min_samples)
            chain_results.append(result)
            
        # Collect all chain samples
        all_chain_samples = self._collect_chain_samples(chain_results)
        
        # Final multi-chain convergence assessment
        final_convergence = self.monitor.check_multi_chain_convergence(all_chain_samples)
        all_converged = self.monitor.all_parameters_converged(final_convergence)
        
        print(f"\n=== Final Multi-Chain Assessment ===")
        print(self.monitor.get_convergence_summary(final_convergence))
        
        return {
            'chain_results': chain_results,
            'all_chain_samples': all_chain_samples,
            'multi_chain_converged': all_converged,
            'final_convergence': final_convergence,
            'n_chains': self.n_chains
        }
        
    def _collect_chain_samples(self, chain_results: List[Dict]) -> Dict[str, List[List[float]]]:
        """Collect samples from all chains by parameter"""
        all_samples = {}
        
        # Initialize parameter lists
        if chain_results:
            first_samples = chain_results[0]['samples']
            for param_name in first_samples.keys():
                all_samples[param_name] = []
                
        # Collect samples from each chain
        for result in chain_results:
            samples = result['samples']
            for param_name, param_samples in samples.items():
                all_samples[param_name].append(param_samples)
                
        return all_samples

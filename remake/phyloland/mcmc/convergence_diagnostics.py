"""
Convergence Diagnostics for MCMC
Implements ESS calculation and convergence monitoring matching phyloland
"""

import numpy as np
from typing import Dict, List, Tuple, Optional

class ConvergenceDiagnostics:
    """ESS calculation and convergence diagnostics matching phyloland"""
    
    def __init__(self, ess_threshold: int = 200):
        """Initialize convergence diagnostics
        
        Args:
            ess_threshold: Minimum ESS required for convergence (phyloland default: 200)
        """
        self.ess_threshold = ess_threshold
        
    def calculate_autocorrelation(self, samples: np.ndarray, max_lag: Optional[int] = None) -> np.ndarray:
        """Calculate autocorrelation function matching phyloland method"""
        n = len(samples)
        if max_lag is None:
            max_lag = min(n // 4, 200)  # Phyloland-style windowing
            
        # Center the samples
        centered = samples - np.mean(samples)
        
        # Calculate autocorrelation using FFT (efficient)
        padded = np.zeros(2 * n)
        padded[:n] = centered
        
        fft_result = np.fft.fft(padded)
        autocorr_fft = np.fft.ifft(fft_result * np.conj(fft_result)).real
        
        # Normalize and extract relevant lags
        autocorr = autocorr_fft[:max_lag + 1] / autocorr_fft[0]
        
        return autocorr
        
    def calculate_ess(self, samples: np.ndarray) -> float:
        """Calculate Effective Sample Size using autocorrelation method"""
        if len(samples) < 10:
            return 0.0
            
        # Handle constant samples (zero variance)
        if np.var(samples) == 0:
            return float(len(samples))  # All samples are independent if constant
            
        # Calculate autocorrelation
        autocorr = self.calculate_autocorrelation(samples)
        
        # Handle NaN/inf in autocorrelation
        if not np.all(np.isfinite(autocorr)):
            return 1.0
            
        # Find first negative autocorrelation (phyloland method)
        cutoff = 1
        for i in range(1, len(autocorr)):
            if autocorr[i] <= 0:
                cutoff = i
                break
            cutoff = i
            
        # Sum autocorrelations up to cutoff
        if cutoff > 1:
            autocorr_sum = 1 + 2 * np.sum(autocorr[1:cutoff])
        else:
            autocorr_sum = 1.0
            
        # ESS formula matching phyloland
        ess = len(samples) / max(autocorr_sum, 1.0)
        
        return max(ess, 1.0)  # ESS should be at least 1
        
    def calculate_rhat(self, chains: List[np.ndarray]) -> float:
        """Calculate Gelman-Rubin statistic for multiple chains"""
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
        
        # Between-chain variance
        B = chain_length * np.var(chain_means, ddof=1)
        
        # Within-chain variance
        chain_vars = np.var(chains_array, axis=1, ddof=1)
        W = np.mean(chain_vars)
        
        # Pooled variance estimate
        var_plus = ((chain_length - 1) * W + B) / chain_length
        
        # R-hat statistic
        if W > 0:
            rhat = np.sqrt(var_plus / W)
        else:
            rhat = 1.0
            
        return rhat
        
    def check_parameter_convergence(self, samples: np.ndarray) -> Dict[str, float]:
        """Check convergence for a single parameter"""
        ess = self.calculate_ess(samples)
        converged = ess >= self.ess_threshold
        
        return {
            'ess': ess,
            'ess_threshold': self.ess_threshold,
            'converged': converged,
            'n_samples': len(samples)
        }

class ConvergenceMonitor:
    """Real-time convergence monitoring during MCMC"""
    
    def __init__(self, diagnostics: ConvergenceDiagnostics, check_frequency: int = 1000):
        """Initialize convergence monitor
        
        Args:
            diagnostics: ConvergenceDiagnostics instance
            check_frequency: How often to check convergence (iterations)
        """
        self.diagnostics = diagnostics
        self.check_frequency = check_frequency
        self.last_check = 0
        
    def should_check_convergence(self, iteration: int) -> bool:
        """Determine if convergence should be checked at this iteration"""
        if iteration - self.last_check >= self.check_frequency:
            self.last_check = iteration
            return True
        return False
        
    def check_convergence(self, samples_dict: Dict[str, List[float]]) -> Dict[str, Dict]:
        """Check convergence for all parameters"""
        convergence_results = {}
        
        for param_name, samples in samples_dict.items():
            if len(samples) > 10:  # Need minimum samples for ESS
                samples_array = np.array(samples)
                convergence_results[param_name] = self.diagnostics.check_parameter_convergence(samples_array)
            else:
                convergence_results[param_name] = {
                    'ess': 0.0,
                    'ess_threshold': self.diagnostics.ess_threshold,
                    'converged': False,
                    'n_samples': len(samples)
                }
                
        return convergence_results
        
    def all_parameters_converged(self, convergence_results: Dict[str, Dict]) -> bool:
        """Check if all parameters have converged"""
        if not convergence_results:
            return False
            
        return all(result['converged'] for result in convergence_results.values())
        
    def get_convergence_summary(self, convergence_results: Dict[str, Dict]) -> str:
        """Generate human-readable convergence summary"""
        if not convergence_results:
            return "No convergence data available"
            
        lines = ["Convergence Status:"]
        for param, result in convergence_results.items():
            status = "✓" if result['converged'] else "✗"
            lines.append(f"  {param}: ESS={result['ess']:.1f}/{result['ess_threshold']} {status}")
            
        all_converged = self.all_parameters_converged(convergence_results)
        overall_status = "ALL CONVERGED" if all_converged else "RUNNING"
        lines.append(f"Overall: {overall_status}")
        
        return "\n".join(lines)

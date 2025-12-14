"""
Adaptive Parameter Proposals for MCMC
Implements Robbins-Monro adaptive algorithm matching phyloland efficiency
"""

import numpy as np
from typing import Tuple, Dict, Any

class AdaptiveProposer:
    """Adaptive parameter proposal mechanism using Robbins-Monro algorithm"""
    
    def __init__(self, target_acceptance: float = 0.44):
        """Initialize adaptive proposer
        
        Args:
            target_acceptance: Target acceptance rate (0.44 optimal for univariate)
        """
        self.target_acceptance = target_acceptance
        self.step_sizes = {}
        self.acceptance_counts = {}
        self.proposal_counts = {}
        
    def initialize_parameter(self, param_name: str, initial_step_size: float = 0.1):
        """Initialize tracking for a parameter"""
        self.step_sizes[param_name] = initial_step_size
        self.acceptance_counts[param_name] = 0
        self.proposal_counts[param_name] = 0
        
    def adapt_step_size(self, param_name: str, accepted: bool, iteration: int):
        """Adapt step size using Robbins-Monro algorithm"""
        if param_name not in self.step_sizes:
            self.initialize_parameter(param_name)
            
        self.proposal_counts[param_name] += 1
        if accepted:
            self.acceptance_counts[param_name] += 1
            
        # Robbins-Monro adaptation during burnin
        if iteration < 10000:  # Adapt during burnin phase
            current_rate = self.acceptance_counts[param_name] / self.proposal_counts[param_name]
            adaptation_rate = 1.0 / (iteration + 1)**0.6  # Decreasing adaptation
            
            if current_rate > self.target_acceptance:
                self.step_sizes[param_name] *= (1 + adaptation_rate)
            else:
                self.step_sizes[param_name] *= (1 - adaptation_rate)
                
            # Keep step size reasonable
            self.step_sizes[param_name] = np.clip(self.step_sizes[param_name], 1e-6, 10.0)
            
    def get_acceptance_rate(self, param_name: str) -> float:
        """Get current acceptance rate for parameter"""
        if self.proposal_counts[param_name] == 0:
            return 0.0
        return self.acceptance_counts[param_name] / self.proposal_counts[param_name]

class ParameterProposer:
    """Parameter-specific proposal mechanisms"""
    
    def __init__(self, adaptive_proposer: AdaptiveProposer):
        self.adaptive_proposer = adaptive_proposer
        
    def propose_sigma(self, current_sigma1: float, current_sigma2: float) -> Tuple[float, float]:
        """Propose new dispersal parameters (log-space for positivity)"""
        step1 = self.adaptive_proposer.step_sizes.get('sigma1', 0.1)
        step2 = self.adaptive_proposer.step_sizes.get('sigma2', 0.1)
        
        # Log-space proposals to ensure positivity with bounds
        log_sigma1 = np.log(max(current_sigma1, 1e-6))  # Prevent log(0)
        log_sigma2 = np.log(max(current_sigma2, 1e-6))  # Prevent log(0)
        
        new_log_sigma1 = log_sigma1 + np.random.normal(0, step1)
        new_log_sigma2 = log_sigma2 + np.random.normal(0, step2)
        
        # Apply bounds to prevent extreme values
        new_log_sigma1 = np.clip(new_log_sigma1, np.log(1e-6), np.log(100))
        new_log_sigma2 = np.clip(new_log_sigma2, np.log(1e-6), np.log(100))
        
        return np.exp(new_log_sigma1), np.exp(new_log_sigma2)
        
    def propose_lambda(self, current_lambda: float) -> float:
        """Propose new competition parameter (log-space for positivity)"""
        step = self.adaptive_proposer.step_sizes.get('lambda', 0.1)
        
        log_lambda = np.log(max(current_lambda, 1e-6))  # Prevent log(0)
        new_log_lambda = log_lambda + np.random.normal(0, step)
        
        # Apply bounds to prevent extreme values
        new_log_lambda = np.clip(new_log_lambda, np.log(1e-6), np.log(100))
        
        return np.exp(new_log_lambda)
        
    def propose_tau(self, current_tau: float) -> float:
        """Propose new rate parameter (log-space for positivity)"""
        step = self.adaptive_proposer.step_sizes.get('tau', 0.1)
        
        log_tau = np.log(max(current_tau, 1e-6))  # Prevent log(0)
        new_log_tau = log_tau + np.random.normal(0, step)
        
        # Apply bounds to prevent extreme values
        new_log_tau = np.clip(new_log_tau, np.log(1e-6), np.log(100))
        
        return np.exp(new_log_tau)
        
    def log_jacobian_sigma(self, sigma1: float, sigma2: float) -> float:
        """Log Jacobian for log-space sigma proposals"""
        return np.log(sigma1) + np.log(sigma2)
        
    def log_jacobian_lambda(self, lambda_val: float) -> float:
        """Log Jacobian for log-space lambda proposal"""
        return np.log(lambda_val)
        
    def log_jacobian_tau(self, tau: float) -> float:
        """Log Jacobian for log-space tau proposal"""
        return np.log(tau)

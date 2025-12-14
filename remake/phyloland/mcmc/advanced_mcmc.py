"""
Advanced MCMC with Adaptive Proposals
Extends BanzaMCMC with adaptive parameter proposals matching phyloland efficiency
"""

import numpy as np
from .banza_mcmc import BanzaMCMC
from .adaptive_proposals import AdaptiveProposer, ParameterProposer

class AdvancedMCMC(BanzaMCMC):
    """Enhanced MCMC with adaptive proposals"""
    
    def __init__(self, tree, locations, location_names, adaptive_proposals=True):
        super().__init__(tree, locations, location_names)
        
        self.adaptive_proposals = adaptive_proposals
        if adaptive_proposals:
            self.adaptive_proposer = AdaptiveProposer(target_acceptance=0.44)
            self.parameter_proposer = ParameterProposer(self.adaptive_proposer)
            
            # Initialize parameters
            self.adaptive_proposer.initialize_parameter('sigma1', 0.1)
            self.adaptive_proposer.initialize_parameter('sigma2', 0.1)
            self.adaptive_proposer.initialize_parameter('lambda', 0.1)
            self.adaptive_proposer.initialize_parameter('Lambda', 0.1)
            
    def propose_parameters_adaptive(self, current_params):
        """Propose new parameters using adaptive mechanism"""
        sigma1, sigma2, lambda_param, Lambda = current_params
        
        if not self.adaptive_proposals:
            return self.propose_parameters(current_params)
            
        # Propose each parameter independently
        new_sigma1, new_sigma2 = self.parameter_proposer.propose_sigma(sigma1, sigma2)
        new_lambda = self.parameter_proposer.propose_lambda(lambda_param)
        new_Lambda = self.parameter_proposer.propose_tau(Lambda)
        
        return (new_sigma1, new_sigma2, new_lambda, new_Lambda)
        
    def compute_proposal_ratio(self, current_params, proposed_params):
        """Compute proposal ratio including Jacobians for log-space proposals"""
        if not self.adaptive_proposals:
            return 0.0  # Symmetric proposals
            
        curr_sigma1, curr_sigma2, curr_lambda, curr_Lambda = current_params
        prop_sigma1, prop_sigma2, prop_lambda, prop_Lambda = proposed_params
        
        # Log Jacobians for log-space proposals
        curr_jacobian = (self.parameter_proposer.log_jacobian_sigma(curr_sigma1, curr_sigma2) +
                        self.parameter_proposer.log_jacobian_lambda(curr_lambda) +
                        self.parameter_proposer.log_jacobian_tau(curr_Lambda))
                        
        prop_jacobian = (self.parameter_proposer.log_jacobian_sigma(prop_sigma1, prop_sigma2) +
                        self.parameter_proposer.log_jacobian_lambda(prop_lambda) +
                        self.parameter_proposer.log_jacobian_tau(prop_Lambda))
                        
        return prop_jacobian - curr_jacobian
        
    def run_adaptive_mcmc(self, n_steps=50000, burnin=10000, thin=10):
        """Run MCMC with adaptive proposals"""
        current_params = (self.sigma1, self.sigma2, self.lambda_param, self.Lambda)
        current_loglik = self.log_likelihood(*current_params)
        
        accepted_counts = {'sigma1': 0, 'sigma2': 0, 'lambda': 0, 'Lambda': 0}
        
        for step in range(n_steps):
            # Propose new parameters
            proposed_params = self.propose_parameters_adaptive(current_params)
            proposed_loglik = self.log_likelihood(*proposed_params)
            
            # Compute acceptance probability
            log_ratio = (proposed_loglik - current_loglik + 
                        self.compute_proposal_ratio(current_params, proposed_params))
            
            # Accept or reject
            if np.log(np.random.random()) < log_ratio:
                current_params = proposed_params
                current_loglik = proposed_loglik
                
                # Track acceptances for each parameter
                if self.adaptive_proposals:
                    accepted_counts['sigma1'] += 1
                    accepted_counts['sigma2'] += 1
                    accepted_counts['lambda'] += 1
                    accepted_counts['Lambda'] += 1
                    
            # Adapt step sizes
            if self.adaptive_proposals:
                accepted = (current_params == proposed_params)
                self.adaptive_proposer.adapt_step_size('sigma1', accepted, step)
                self.adaptive_proposer.adapt_step_size('sigma2', accepted, step)
                self.adaptive_proposer.adapt_step_size('lambda', accepted, step)
                self.adaptive_proposer.adapt_step_size('Lambda', accepted, step)
                
            # Store samples after burnin
            if step >= burnin and step % thin == 0:
                self.samples['sigma1'].append(current_params[0])
                self.samples['sigma2'].append(current_params[1])
                self.samples['lambda'].append(current_params[2])
                self.samples['Lambda'].append(current_params[3])
                self.samples['likelihood'].append(current_loglik)
                
            # Progress reporting
            if step % 5000 == 0 and self.adaptive_proposals:
                print(f"Step {step}:")
                for param in ['sigma1', 'sigma2', 'lambda', 'Lambda']:
                    acc_rate = self.adaptive_proposer.get_acceptance_rate(param)
                    step_size = self.adaptive_proposer.step_sizes[param]
                    print(f"  {param}: acceptance={acc_rate:.3f}, step_size={step_size:.4f}")
                    
        return self.samples
        
    def get_adaptation_diagnostics(self):
        """Get diagnostic information about adaptive proposals"""
        if not self.adaptive_proposals:
            return {}
            
        diagnostics = {}
        for param in ['sigma1', 'sigma2', 'lambda', 'Lambda']:
            diagnostics[param] = {
                'acceptance_rate': self.adaptive_proposer.get_acceptance_rate(param),
                'final_step_size': self.adaptive_proposer.step_sizes[param],
                'total_proposals': self.adaptive_proposer.proposal_counts[param]
            }
            
        return diagnostics

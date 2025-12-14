"""
Convergent MCMC with Automatic Stopping
Extends AdvancedMCMC with convergence monitoring and phyloland-style automatic stopping
"""

import numpy as np
from typing import Dict, Optional
from .advanced_mcmc import AdvancedMCMC
from .convergence_diagnostics import ConvergenceDiagnostics, ConvergenceMonitor

class ConvergentMCMC(AdvancedMCMC):
    """MCMC with automatic convergence detection and stopping"""
    
    def __init__(self, tree, locations, location_names, 
                 ess_threshold: int = 200, 
                 check_frequency: int = 1000,
                 adaptive_proposals: bool = True):
        """Initialize convergent MCMC
        
        Args:
            tree: Phylogenetic tree
            locations: Geographic locations
            location_names: Location names
            ess_threshold: ESS threshold for convergence (phyloland ess_lim)
            check_frequency: How often to check convergence
            adaptive_proposals: Use adaptive proposals from Subunit 6.1
        """
        super().__init__(tree, locations, location_names, adaptive_proposals)
        
        self.diagnostics = ConvergenceDiagnostics(ess_threshold)
        self.monitor = ConvergenceMonitor(self.diagnostics, check_frequency)
        self.convergence_history = []
        
    def run_until_convergence(self, max_steps: int = 100000, 
                            burnin: int = 10000, 
                            thin: int = 10,
                            min_samples: int = 1000) -> Dict:
        """Run MCMC until convergence or max steps (phyloland-style)"""
        
        current_params = (self.sigma1, self.sigma2, self.lambda_param, self.Lambda)
        current_loglik = self.log_likelihood(*current_params)
        
        converged = False
        convergence_step = None
        
        print(f"Starting MCMC with ESS threshold: {self.diagnostics.ess_threshold}")
        print(f"Will check convergence every {self.monitor.check_frequency} steps")
        
        for step in range(max_steps):
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
                
            # Check convergence
            if (step >= burnin + min_samples and 
                self.monitor.should_check_convergence(step)):
                
                convergence_results = self.monitor.check_convergence(self.samples)
                self.convergence_history.append({
                    'step': step,
                    'results': convergence_results
                })
                
                # Print convergence status
                if step % (self.monitor.check_frequency * 5) == 0:  # Every 5th check
                    print(f"\nStep {step}:")
                    print(self.monitor.get_convergence_summary(convergence_results))
                    
                # Check if converged
                if self.monitor.all_parameters_converged(convergence_results):
                    converged = True
                    convergence_step = step
                    print(f"\n🎉 CONVERGENCE ACHIEVED at step {step}!")
                    print(self.monitor.get_convergence_summary(convergence_results))
                    break
                    
        # Final status
        if not converged:
            print(f"\n⚠️  Maximum steps ({max_steps}) reached without convergence")
            if self.convergence_history:
                final_results = self.convergence_history[-1]['results']
                print(self.monitor.get_convergence_summary(final_results))
        
        return {
            'samples': self.samples,
            'converged': converged,
            'convergence_step': convergence_step,
            'total_steps': step + 1,
            'convergence_history': self.convergence_history,
            'final_diagnostics': self.get_final_diagnostics()
        }
        
    def get_final_diagnostics(self) -> Dict:
        """Get comprehensive final diagnostics"""
        if not self.samples['sigma1']:
            return {}
            
        # Calculate final ESS for all parameters
        final_ess = {}
        for param, samples in self.samples.items():
            if param != 'likelihood' and samples:
                samples_array = np.array(samples)
                final_ess[param] = self.diagnostics.calculate_ess(samples_array)
                
        # Get adaptation diagnostics if available
        adaptation_diag = {}
        if self.adaptive_proposals:
            adaptation_diag = self.get_adaptation_diagnostics()
            
        return {
            'final_ess': final_ess,
            'ess_threshold': self.diagnostics.ess_threshold,
            'adaptation_diagnostics': adaptation_diag,
            'n_samples': len(self.samples['sigma1']),
            'convergence_checks': len(self.convergence_history)
        }
        
    def run_fixed_steps(self, n_steps: int = 50000, burnin: int = 10000, thin: int = 10) -> Dict:
        """Run MCMC for fixed number of steps (for comparison with phyloland)"""
        # Use parent class method but add convergence monitoring
        samples = self.run_adaptive_mcmc(n_steps, burnin, thin)
        
        # Check final convergence status
        final_convergence = self.monitor.check_convergence(samples)
        converged = self.monitor.all_parameters_converged(final_convergence)
        
        return {
            'samples': samples,
            'converged': converged,
            'convergence_step': None,
            'total_steps': n_steps,
            'final_convergence': final_convergence,
            'final_diagnostics': self.get_final_diagnostics()
        }

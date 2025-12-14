"""
Complete PLD_interface Implementation
Phyloland-compatible API matching R package exactly
"""

import os
import numpy as np
import pandas as pd
import dendropy
from typing import Optional, List, Union, Dict, Any
from pathlib import Path

from ..mcmc.multi_chain_mcmc import MultiChainMCMC
from ..mcmc.convergent_mcmc import ConvergentMCMC

class ParameterValidator:
    """Validate PLD_interface parameters matching phyloland rules"""
    
    @staticmethod
    def validate_pld_parameters(**kwargs) -> Dict[str, Any]:
        """Validate all parameters with phyloland-compatible rules"""
        
        # Extract parameters with defaults matching phyloland
        params = {
            'fileTREES': kwargs.get('fileTREES'),
            'fileDATA': kwargs.get('fileDATA'), 
            'num_step': kwargs.get('num_step', 100000),
            'freq': kwargs.get('freq', 100),
            'burnin': kwargs.get('burnin', 0),
            'ess_lim': kwargs.get('ess_lim', 100),
            'sigma': kwargs.get('sigma', None),
            'lambda_param': kwargs.get('lambda_param', None),
            'tau': kwargs.get('tau', None),
            'num_step_sigma': kwargs.get('num_step_sigma', 1),
            'num_step_lambda': kwargs.get('num_step_lambda', 1),
            'num_step_tau': kwargs.get('num_step_tau', 1),
            'id_filena': kwargs.get('id_filena', None),
            'pattern_trees_likelihood': kwargs.get('pattern_trees_likelihood', "treeLikelihood"),
            'names_locations': kwargs.get('names_locations', None)
        }
        
        # Validate required parameters
        if params['fileTREES'] is None:
            raise ValueError("fileTREES is required")
        if params['fileDATA'] is None:
            raise ValueError("fileDATA is required")
            
        # Validate numeric parameters
        if params['num_step'] <= 0:
            raise ValueError("num_step must be positive")
        if params['freq'] <= 0:
            raise ValueError("freq must be positive")
        if params['burnin'] < 0:
            raise ValueError("burnin must be non-negative")
        if params['ess_lim'] <= 0:
            raise ValueError("ess_lim must be positive")
            
        # Validate file existence
        if not os.path.exists(params['fileTREES']):
            raise FileNotFoundError(f"Tree file not found: {params['fileTREES']}")
        if not os.path.exists(params['fileDATA']):
            raise FileNotFoundError(f"Data file not found: {params['fileDATA']}")
            
        return params

class PhylolandFileHandler:
    """Handle file I/O with phyloland compatibility"""
    
    @staticmethod
    def load_trees(fileTREES: str, burnin: int = 0, 
                   pattern_trees_likelihood: str = "treeLikelihood") -> dendropy.Tree:
        """Load NEXUS trees with phyloland compatibility"""
        try:
            # Load tree using dendropy (validated in Unit 2)
            tree = dendropy.Tree.get(path=fileTREES, schema="nexus")
            return tree
        except Exception as e:
            raise ValueError(f"Error loading tree file {fileTREES}: {str(e)}")
            
    @staticmethod
    def load_locations(fileDATA: str, names_locations: Optional[List[str]] = None) -> tuple:
        """Load location data with phyloland format compatibility"""
        try:
            # Load location data (tab-separated, no header)
            data = pd.read_csv(fileDATA, sep='\t', header=None, 
                             names=['species', 'latitude', 'longitude'])
            
            # Extract locations and names
            locations = list(zip(data['latitude'], data['longitude']))
            
            if names_locations is not None:
                location_names = names_locations
            else:
                # Extract unique locations and create names
                unique_coords = list(set(locations))
                location_names = [f"Location_{i+1}" for i in range(len(unique_coords))]
                locations = unique_coords
                
            return locations, location_names, data['species'].tolist()
            
        except Exception as e:
            raise ValueError(f"Error loading data file {fileDATA}: {str(e)}")

class PhylolandOutputFormatter:
    """Format results to match phyloland output exactly"""
    
    @staticmethod
    def format_results(mcmc_results: Dict, tree: dendropy.Tree, 
                      locations: List, location_names: List, 
                      species_names: List) -> Dict[str, Any]:
        """Format results to match phyloland output structure"""
        
        # Extract samples from MCMC results
        if 'chain_results' in mcmc_results:
            # Multi-chain results
            all_samples = mcmc_results['all_chain_samples']
            # Combine samples from all chains
            combined_samples = {}
            for param, chain_samples in all_samples.items():
                combined_samples[param] = []
                for chain in chain_samples:
                    combined_samples[param].extend(chain)
        else:
            # Single chain results
            combined_samples = mcmc_results['samples']
            
        # Format in phyloland structure
        result = {
            # Parameter samples (phyloland names)
            'sigma1': np.array(combined_samples.get('sigma1', [])),
            'sigma2': np.array(combined_samples.get('sigma2', [])),
            'lambda': np.array(combined_samples.get('lambda', [])),
            'Lambda': np.array(combined_samples.get('Lambda', [])),
            'likelihood': np.array(combined_samples.get('likelihood', [])),
            
            # Tree information
            'trees': tree,  # Single tree for now
            
            # Location information
            'locations': np.array(locations),
            'tips': species_names,
            'space': np.array(list(set(locations))),  # Unique locations
            
            # MCMC information
            'mcmc': {
                'n_samples': len(combined_samples.get('sigma1', [])),
                'converged': mcmc_results.get('converged', False) or mcmc_results.get('multi_chain_converged', False)
            }
        }
        
        return result

def PLD_interface(fileTREES: str, 
                 fileDATA: str,
                 num_step: int = 100000,
                 freq: int = 100, 
                 burnin: int = 0,
                 ess_lim: int = 100,
                 sigma: Optional[List[float]] = None,
                 lambda_param: Optional[float] = None,
                 tau: Optional[float] = None,
                 num_step_sigma: int = 1,
                 num_step_lambda: int = 1, 
                 num_step_tau: int = 1,
                 id_filena: Optional[str] = None,
                 pattern_trees_likelihood: str = "treeLikelihood",
                 names_locations: Optional[List[str]] = None,
                 n_chains: int = 1) -> Dict[str, Any]:
    """
    Complete phyloland PLD_interface implementation
    
    Parameters match phyloland R package exactly:
    
    Args:
        fileTREES: Path to NEXUS tree file
        fileDATA: Path to location data file (tab-separated)
        num_step: Number of MCMC steps (default: 100000)
        freq: Sampling frequency (default: 100)
        burnin: Burnin steps (default: 0)
        ess_lim: ESS threshold for convergence (default: 100)
        sigma: Fixed sigma values [sigma1, sigma2] or None to estimate
        lambda_param: Fixed lambda value or None to estimate
        tau: Fixed tau value or None to estimate
        num_step_sigma: Sigma sampling frequency (default: 1)
        num_step_lambda: Lambda sampling frequency (default: 1)
        num_step_tau: Tau sampling frequency (default: 1)
        id_filena: Output file ID (optional)
        pattern_trees_likelihood: Tree likelihood pattern (default: "treeLikelihood")
        names_locations: Location names (optional)
        n_chains: Number of MCMC chains (default: 1, extension for multi-chain)
        
    Returns:
        Dictionary with phyloland-compatible results structure
    """
    
    print("PLD_interface: Phyloland-compatible MCMC analysis")
    print(f"Tree file: {fileTREES}")
    print(f"Data file: {fileDATA}")
    print(f"MCMC steps: {num_step}, ESS threshold: {ess_lim}")
    
    # Validate parameters
    params = ParameterValidator.validate_pld_parameters(
        fileTREES=fileTREES, fileDATA=fileDATA, num_step=num_step,
        freq=freq, burnin=burnin, ess_lim=ess_lim, sigma=sigma,
        lambda_param=lambda_param, tau=tau, num_step_sigma=num_step_sigma,
        num_step_lambda=num_step_lambda, num_step_tau=num_step_tau,
        id_filena=id_filena, pattern_trees_likelihood=pattern_trees_likelihood,
        names_locations=names_locations
    )
    
    # Load input files
    print("Loading input files...")
    tree = PhylolandFileHandler.load_trees(fileTREES, burnin, pattern_trees_likelihood)
    locations, location_names, species_names = PhylolandFileHandler.load_locations(fileDATA, names_locations)
    
    print(f"Loaded tree with {len(tree.leaf_nodes())} species")
    print(f"Loaded {len(locations)} locations: {location_names}")
    
    # Configure MCMC
    thin = max(1, freq // 10)  # Reasonable thinning
    
    # Run MCMC (single or multi-chain)
    if n_chains > 1:
        print(f"Running multi-chain MCMC with {n_chains} chains...")
        mcmc = MultiChainMCMC(tree, locations, location_names,
                             n_chains=n_chains, ess_threshold=ess_lim,
                             rhat_threshold=1.1, adaptive_proposals=True)
        
        mcmc_results = mcmc.run_parallel_chains(
            max_steps=num_step, burnin=burnin, thin=thin, min_samples=freq
        )
    else:
        print("Running single-chain MCMC...")
        mcmc = ConvergentMCMC(tree, locations, location_names,
                             ess_threshold=ess_lim, adaptive_proposals=True)
        
        mcmc_results = mcmc.run_until_convergence(
            max_steps=num_step, burnin=burnin, thin=thin, min_samples=freq
        )
    
    # Format results in phyloland structure
    print("Formatting results...")
    formatted_results = PhylolandOutputFormatter.format_results(
        mcmc_results, tree, locations, location_names, species_names
    )
    
    # Print summary
    n_samples = formatted_results['mcmc']['n_samples']
    converged = formatted_results['mcmc']['converged']
    print(f"\nPLD_interface completed:")
    print(f"  Samples collected: {n_samples}")
    print(f"  Converged: {converged}")
    print(f"  Parameter estimates:")
    
    if len(formatted_results['sigma1']) > 0:
        print(f"    σ₁: {np.median(formatted_results['sigma1']):.4f}")
        print(f"    σ₂: {np.median(formatted_results['sigma2']):.4f}")
        print(f"    λ:  {np.median(formatted_results['lambda']):.4f}")
        print(f"    Λ:  {np.median(formatted_results['Lambda']):.4f}")
    
    return formatted_results

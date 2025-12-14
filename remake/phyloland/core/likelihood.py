"""Phylogenetic likelihood calculation for phylogeographic inference"""

import numpy as np
import pandas as pd
import dendropy
from pathlib import Path
from .dispersal import DispersalKernel
from .rate_matrix import RateMatrixBuilder

class PhylogeneticLikelihood:
    """Complete phylogenetic likelihood calculation using optimized rate infrastructure"""
    
    def __init__(self, tree_file, location_file):
        """Initialize with tree and location data
        
        Args:
            tree_file: Path to Nexus tree file
            location_file: Path to tab-delimited location file
        """
        self.tree_file = Path(tree_file)
        self.location_file = Path(location_file)
        
        # Load data
        self._load_tree()
        self._load_locations()
        
        # Initialize rate calculation infrastructure (from subunits 4.1 + 4.2)
        self.dispersal_kernel = DispersalKernel(self.locations)
        self.rate_matrix_builder = RateMatrixBuilder(self.dispersal_kernel)
        
    def _load_tree(self):
        """Load phylogenetic tree from Nexus file"""
        self.tree = dendropy.Tree.get(
            path=str(self.tree_file),
            schema="nexus"
        )
        
        # Extract tip information
        self.tip_names = [leaf.taxon.label for leaf in self.tree.leaf_node_iter()]
        self.n_tips = len(self.tip_names)
        
    def _load_locations(self):
        """Load location data from tab-delimited file"""
        location_data = pd.read_csv(
            self.location_file, 
            sep="\t", 
            header=None, 
            names=["species", "latitude", "longitude"]
        )
        
        # Extract coordinates as tuples
        self.locations = list(zip(location_data["latitude"], location_data["longitude"]))
        self.n_locations = len(self.locations)
        
    def get_rate_matrix(self, sigma1, sigma2, Lambda):
        """Get rate matrix using optimized infrastructure from subunits 4.1 + 4.2
        
        Args:
            sigma1, sigma2: Dispersal parameters
            Lambda: Overall dispersal rate
            
        Returns:
            n×n rate matrix
        """
        return self.rate_matrix_builder.build_matrix(sigma1, sigma2, Lambda)
        
    def calculate_likelihood_components(self, sigma1, sigma2, Lambda):
        """Calculate basic likelihood components for validation
        
        Args:
            sigma1, sigma2, Lambda: Model parameters
            
        Returns:
            dict with likelihood components
        """
        # Get rate matrix using optimized infrastructure
        rate_matrix = self.get_rate_matrix(sigma1, sigma2, Lambda)
        
        # Calculate basic components
        total_rate = np.sum(rate_matrix)
        diagonal_rate = Lambda / self.n_locations
        
        return {
            'total_rate': total_rate,
            'diagonal_rate': diagonal_rate,
            'rate_matrix': rate_matrix
        }
        
    def calculate_simplified_likelihood(self, sigma1, sigma2, Lambda):
        """Calculate simplified likelihood for testing (not full phylogenetic likelihood)
        
        Note: This is a simplified version for infrastructure testing.
        Full phylogenetic likelihood requires complex tree traversal and 
        continuous-time Markov chain calculations.
        
        Args:
            sigma1, sigma2, Lambda: Model parameters
            
        Returns:
            Simplified log-likelihood value
        """
        # Get rate matrix
        rate_matrix = self.get_rate_matrix(sigma1, sigma2, Lambda)
        
        # Match R calculation exactly
        total_rate = np.sum(rate_matrix)
        diagonal_rate = Lambda / self.n_locations
        
        # Get off-diagonal rates (exclude diagonal elements)
        off_diagonal_rates = []
        for i in range(self.n_locations):
            for j in range(self.n_locations):
                if i != j and rate_matrix[i, j] > 0:
                    off_diagonal_rates.append(rate_matrix[i, j])
        
        # Simple likelihood: -total_rate + sum(log(off_diagonal_rates))
        # Match R: log_likelihood <- -total_rate + sum(log(off_diagonal_rates[off_diagonal_rates > 0]))
        log_likelihood = -total_rate + np.sum(np.log(off_diagonal_rates))
        
        return log_likelihood

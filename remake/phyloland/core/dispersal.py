"""Optimized dispersal kernel calculations for phylogeographic inference"""

import numpy as np

class DispersalKernel:
    """Efficient dispersal kernel calculation for realistic datasets"""
    
    def __init__(self, locations):
        """Initialize with location coordinates
        
        Args:
            locations: List of (latitude, longitude) tuples
        """
        self.locations = np.array(locations)
        self.n_locations = len(locations)
        
        # Precompute coordinate arrays for vectorized operations
        self.lats = self.locations[:, 0]
        self.lons = self.locations[:, 1]
        
    def calculate_matrix(self, sigma1, sigma2):
        """Calculate complete n×n dispersal kernel matrix using vectorized operations
        
        Args:
            sigma1: Latitude dispersal parameter
            sigma2: Longitude dispersal parameter
            
        Returns:
            n×n numpy array with kernel values
        """
        # Use broadcasting to compute all pairwise differences efficiently
        lat_diff = self.lats[:, np.newaxis] - self.lats[np.newaxis, :]
        lon_diff = self.lons[:, np.newaxis] - self.lons[np.newaxis, :]
        
        # Vectorized kernel calculation: f(x,y) = exp(-Σ(xi-yi)²/2σi²)
        kernel_matrix = np.exp(-(lat_diff**2 / (2 * sigma1**2) + 
                                lon_diff**2 / (2 * sigma2**2)))
        
        return kernel_matrix
        
    def calculate_pairwise(self, i, j, sigma1, sigma2):
        """Calculate single pairwise kernel value for validation/debugging
        
        Args:
            i, j: Location indices
            sigma1, sigma2: Dispersal parameters
            
        Returns:
            Single kernel value
        """
        lat_diff = self.lats[i] - self.lats[j]
        lon_diff = self.lons[i] - self.lons[j]
        
        kernel = np.exp(-(lat_diff**2 / (2 * sigma1**2) + 
                         lon_diff**2 / (2 * sigma2**2)))
        
        return kernel

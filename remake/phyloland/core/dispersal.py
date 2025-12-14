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
        
    def calculate_pairwise_distance(self, i, j):
        """Calculate distance between two location indices
        
        Args:
            i, j: Location indices
            
        Returns:
            Distance in kilometers
        """
        lat1, lon1 = self.lats[i], self.lons[i]
        lat2, lon2 = self.lats[j], self.lons[j]
        
        # Convert to radians
        lat1_r = np.radians(lat1)
        lat2_r = np.radians(lat2)
        lon1_r = np.radians(lon1)
        lon2_r = np.radians(lon2)
        
        # Great circle distance (same as R distkm)
        dlon = lon2_r - lon1_r
        dlat = lat2_r - lat1_r
        a = np.sin(dlat/2)**2 + np.cos(lat1_r) * np.cos(lat2_r) * np.sin(dlon/2)**2
        c = 2 * np.arcsin(np.sqrt(a))
        
        # Earth radius in km (same as R)
        R = 6378.137
        distance = R * c
        
        return distance
        
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

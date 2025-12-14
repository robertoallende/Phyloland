"""Base case implementations for phylogeographic inference"""

import dendropy
import pandas as pd
import numpy as np
from pathlib import Path

class SingleLocationCase:
    """Trivial phylogeographic case: single tip, single location"""
    
    def __init__(self, tree_file, location_file):
        """Initialize with tree and location data"""
        self.tree_file = Path(tree_file)
        self.location_file = Path(location_file)
        
        # Load and validate data
        self._load_tree()
        self._load_locations()
        self._validate_data()
        
    def _load_tree(self):
        """Load tree from Nexus file"""
        self.tree = dendropy.Tree.get(
            path=str(self.tree_file),
            schema="nexus"
        )
        
        # Extract tip information
        self.tip_names = [leaf.taxon.label for leaf in self.tree.leaf_node_iter()]
        self.n_tips = len(self.tip_names)
        
    def _load_locations(self):
        """Load location data from tab-delimited file"""
        # Read tab-delimited file: species, latitude, longitude
        location_data = pd.read_csv(
            self.location_file, 
            sep="\t", 
            header=None, 
            names=["species", "latitude", "longitude"]
        )
        
        # Extract coordinates as tuples
        self.locations = list(zip(location_data["latitude"], location_data["longitude"]))
        self.n_locations = len(self.locations)
        
    def _validate_data(self):
        """Validate tree and location data consistency"""
        if self.n_tips != self.n_locations:
            raise ValueError(f"Mismatch: {self.n_tips} tips, {self.n_locations} locations")
            
        # For single location case, should be exactly 1 of each
        if self.n_tips != 1 or self.n_locations != 1:
            raise ValueError(f"Single location case requires 1 tip and 1 location")
            
    def calculate_likelihood(self):
        """Calculate likelihood for single location case"""
        # Trivial case: no dispersal events possible
        # Observed data is certain, likelihood = 1.0
        return 1.0
        
    @property
    def n_dispersal_events(self):
        """Number of dispersal events (0 for single location)"""
        return 0


class TwoLocationCase:
    """Minimal dispersal case: 2 tips, 2 locations, 1 dispersal event"""
    
    def __init__(self, tree_file, location_file):
        """Initialize with tree and location data"""
        self.tree_file = Path(tree_file)
        self.location_file = Path(location_file)
        
        # Load and validate data
        self._load_tree()
        self._load_locations()
        self._validate_data()
        
    def _load_tree(self):
        """Load tree from Nexus file"""
        self.tree = dendropy.Tree.get(
            path=str(self.tree_file),
            schema="nexus"
        )
        
        # Extract tip information
        self.tip_names = [leaf.taxon.label for leaf in self.tree.leaf_node_iter()]
        self.n_tips = len(self.tip_names)
        
    def _load_locations(self):
        """Load location data from tab-delimited file"""
        # Read tab-delimited file: species, latitude, longitude
        location_data = pd.read_csv(
            self.location_file, 
            sep="\t", 
            header=None, 
            names=["species", "latitude", "longitude"]
        )
        
        # Extract coordinates as tuples
        self.locations = list(zip(location_data["latitude"], location_data["longitude"]))
        self.n_locations = len(self.locations)
        
    def _validate_data(self):
        """Validate tree and location data consistency"""
        if self.n_tips != self.n_locations:
            raise ValueError(f"Mismatch: {self.n_tips} tips, {self.n_locations} locations")
            
        # For two location case, should be exactly 2 of each
        if self.n_tips != 2 or self.n_locations != 2:
            raise ValueError(f"Two location case requires 2 tips and 2 locations")
            
    def calculate_distance(self, loc1, loc2):
        """Calculate geographic distance using great circle formula (matches R distkm)"""
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        
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
        
    def dispersal_kernel(self, loc1, loc2, sigma):
        """Calculate dispersal kernel f(x,y) = exp(-Σ(xi-yi)²/2σi²)"""
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        sigma1, sigma2 = sigma
        
        # Multivariate normal kernel
        kernel = np.exp(-((lat1-lat2)**2/(2*sigma1**2) + (lon1-lon2)**2/(2*sigma2**2)))
        return kernel
        
    def build_rate_matrix(self, sigma):
        """Build 2×2 dispersal rate matrix"""
        # Calculate dispersal kernel between locations
        f12 = self.dispersal_kernel(self.locations[0], self.locations[1], sigma)
        
        # Rate matrix: Fij = f(i,j) / (m * f(i,i))
        # For 2 locations: m=2, f(i,i)=1
        F12 = f12 / 2
        F21 = F12  # Symmetric
        F11 = 1/2  # Self-dispersal
        F22 = 1/2
        
        rate_matrix = np.array([
            [F11, F12],
            [F21, F22]
        ])
        
        return rate_matrix
        
    @property
    def n_dispersal_events(self):
        """Number of dispersal events (1 for two location case)"""
        return 1


class NoCompetitionCase:
    """Multi-location case with no competition: λ = 1, δj = 1 always"""
    
    def __init__(self, tree_file, location_file):
        """Initialize with tree and location data"""
        self.tree_file = Path(tree_file)
        self.location_file = Path(location_file)
        self.lambda_comp = 1.0  # No competition constraint
        
        # Load and validate data
        self._load_tree()
        self._load_locations()
        self._validate_data()
        
    def _load_tree(self):
        """Load tree from Nexus file"""
        self.tree = dendropy.Tree.get(
            path=str(self.tree_file),
            schema="nexus"
        )
        
        # Extract tip information
        self.tip_names = [leaf.taxon.label for leaf in self.tree.leaf_node_iter()]
        self.n_tips = len(self.tip_names)
        
    def _load_locations(self):
        """Load location data from tab-delimited file"""
        # Read tab-delimited file: species, latitude, longitude
        location_data = pd.read_csv(
            self.location_file, 
            sep="\t", 
            header=None, 
            names=["species", "latitude", "longitude"]
        )
        
        # Extract coordinates as tuples
        self.locations = list(zip(location_data["latitude"], location_data["longitude"]))
        self.n_locations = len(self.locations)
        
    def _validate_data(self):
        """Validate tree and location data consistency"""
        if self.n_tips != self.n_locations:
            raise ValueError(f"Mismatch: {self.n_tips} tips, {self.n_locations} locations")
            
    def calculate_distance(self, loc1, loc2):
        """Calculate geographic distance using great circle formula (matches R distkm)"""
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        
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
        
    def dispersal_kernel(self, loc1, loc2, sigma):
        """Calculate dispersal kernel f(x,y) = exp(-Σ(xi-yi)²/2σi²)"""
        lat1, lon1 = loc1
        lat2, lon2 = loc2
        sigma1, sigma2 = sigma
        
        # Multivariate normal kernel
        kernel = np.exp(-((lat1-lat2)**2/(2*sigma1**2) + (lon1-lon2)**2/(2*sigma2**2)))
        return kernel
        
    def build_rate_matrix(self, sigma):
        """Build n×n dispersal rate matrix with no competition"""
        n = self.n_locations
        rate_matrix = np.zeros((n, n))
        
        for i in range(n):
            for j in range(n):
                if i != j:
                    # Off-diagonal: Fij = f(i,j) / m
                    kernel_ij = self.dispersal_kernel(self.locations[i], self.locations[j], sigma)
                    rate_matrix[i, j] = kernel_ij / n
                else:
                    # Diagonal: self-dispersal = 1/m
                    rate_matrix[i, j] = 1.0 / n
                    
        return rate_matrix
        
    def get_competition_factors(self):
        """Get competition factors (all = 1.0 for no competition case)"""
        return [1.0] * self.n_locations
        
    @property
    def n_dispersal_events(self):
        """Number of dispersal events (n-1 internal nodes)"""
        return self.n_tips - 1

"""Efficient rate matrix construction for phylogeographic inference"""

import numpy as np

class RateMatrixBuilder:
    """Scalable rate matrix construction using optimized dispersal kernels"""
    
    def __init__(self, dispersal_kernel):
        """Initialize with DispersalKernel from subunit 4.1
        
        Args:
            dispersal_kernel: DispersalKernel instance for kernel calculations
        """
        self.dispersal_kernel = dispersal_kernel
        self.n_locations = dispersal_kernel.n_locations
        
    def build_matrix(self, sigma1, sigma2, Lambda):
        """Build complete n×n dispersal rate matrix with proper normalization
        
        Args:
            sigma1, sigma2: Dispersal parameters
            Lambda: Overall dispersal rate parameter
            
        Returns:
            n×n numpy array with rate values: Rij = Lambda * Fij
        """
        # Get kernel matrix from optimized calculation (subunit 4.1)
        kernel_matrix = self.dispersal_kernel.calculate_matrix(sigma1, sigma2)
        
        # Apply rate matrix normalization: Fij = f(i,j) / m
        # Then scale by Lambda: Rij = Lambda * Fij
        rate_matrix = Lambda * kernel_matrix / self.n_locations
        
        return rate_matrix
        
    def validate_properties(self, rate_matrix, Lambda):
        """Validate mathematical properties of rate matrix for debugging
        
        Args:
            rate_matrix: Rate matrix to validate
            Lambda: Expected Lambda parameter
            
        Returns:
            dict with validation results
        """
        n = self.n_locations
        
        # Check diagonal values should be Lambda/n
        diagonal_values = np.diag(rate_matrix)
        expected_diagonal = Lambda / n
        diagonal_correct = np.allclose(diagonal_values, expected_diagonal)
        
        # Check matrix is non-negative
        non_negative = np.all(rate_matrix >= 0)
        
        # Calculate row sums
        row_sums = np.sum(rate_matrix, axis=1)
        
        # Total rate
        total_rate = np.sum(rate_matrix)
        
        return {
            'diagonal_correct': diagonal_correct,
            'non_negative': non_negative,
            'diagonal_value': expected_diagonal,
            'mean_row_sum': np.mean(row_sums),
            'total_rate': total_rate,
            'matrix_shape': rate_matrix.shape
        }

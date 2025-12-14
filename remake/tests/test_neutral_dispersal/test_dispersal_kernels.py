"""Test dispersal kernel implementation - subunit 4.1"""

import numpy as np
import pandas as pd
import pytest
import time
from pathlib import Path

# Load reference data
TEST_DATA_DIR = Path(__file__).parent.parent.parent.parent / "test_data"
reference = pd.read_csv(TEST_DATA_DIR / "reference" / "dispersal_kernel_reference.csv").iloc[0]
kernel_matrix = pd.read_csv(TEST_DATA_DIR / "reference" / "dispersal_kernel_matrix.csv")
key_pairs = pd.read_csv(TEST_DATA_DIR / "reference" / "dispersal_kernel_pairs.csv")

def test_full_banza_kernel_matrix():
    """Test 21×21 kernel matrix matches R exactly"""
    from phyloland.core.dispersal import DispersalKernel
    
    # Load Banza locations
    locations_file = TEST_DATA_DIR / "banza" / "locations_Banza.txt"
    locations_data = pd.read_csv(locations_file, sep="\t", header=None, 
                                names=["species", "latitude", "longitude"])
    
    # Create dispersal kernel calculator
    locations = list(zip(locations_data["latitude"], locations_data["longitude"]))
    kernel_calc = DispersalKernel(locations)
    
    # Calculate kernel matrix
    sigma1, sigma2 = reference["sigma1"], reference["sigma2"]
    py_matrix = kernel_calc.calculate_matrix(sigma1, sigma2)
    
    # Reshape reference matrix from flat format
    n = int(reference["n_locations"])
    r_matrix = kernel_matrix["kernel_value"].values.reshape(n, n)
    
    # Compare matrices
    np.testing.assert_allclose(py_matrix, r_matrix, rtol=1e-12)
    
    # Check matrix properties
    assert py_matrix.shape == (n, n)
    assert np.all(np.diag(py_matrix) == 1.0)  # Diagonal should be 1.0

def test_key_pairwise_kernels():
    """Test specific pairwise kernel values match R"""
    from phyloland.core.dispersal import DispersalKernel
    
    # Load Banza locations
    locations_file = TEST_DATA_DIR / "banza" / "locations_Banza.txt"
    locations_data = pd.read_csv(locations_file, sep="\t", header=None, 
                                names=["species", "latitude", "longitude"])
    
    locations = list(zip(locations_data["latitude"], locations_data["longitude"]))
    kernel_calc = DispersalKernel(locations)
    
    sigma1, sigma2 = reference["sigma1"], reference["sigma2"]
    
    # Test key pairs from R reference
    for _, pair in key_pairs.iterrows():
        i, j = pair["from_idx"] - 1, pair["to_idx"] - 1  # Convert to 0-based
        expected = pair["kernel_value"]
        
        # Calculate pairwise kernel
        actual = kernel_calc.calculate_pairwise(i, j, sigma1, sigma2)
        
        np.testing.assert_allclose(actual, expected, rtol=1e-12)

def test_kernel_performance():
    """Test computation time < 1ms for 21×21 matrix"""
    from phyloland.core.dispersal import DispersalKernel
    
    # Load Banza locations
    locations_file = TEST_DATA_DIR / "banza" / "locations_Banza.txt"
    locations_data = pd.read_csv(locations_file, sep="\t", header=None, 
                                names=["species", "latitude", "longitude"])
    
    locations = list(zip(locations_data["latitude"], locations_data["longitude"]))
    kernel_calc = DispersalKernel(locations)
    
    sigma1, sigma2 = reference["sigma1"], reference["sigma2"]
    
    # Warm up
    kernel_calc.calculate_matrix(sigma1, sigma2)
    
    # Time the calculation
    start_time = time.time()
    for _ in range(10):  # Average over multiple runs
        kernel_calc.calculate_matrix(sigma1, sigma2)
    end_time = time.time()
    
    avg_time = (end_time - start_time) / 10
    
    # Should be < 1ms (0.001 seconds)
    assert avg_time < 0.001, f"Kernel calculation took {avg_time:.4f}s, should be < 0.001s"

def test_parameter_sensitivity():
    """Test kernel behavior across σ parameter ranges"""
    from phyloland.core.dispersal import DispersalKernel
    
    # Use simple 2-location case for parameter testing
    locations = [(21.0, -157.0), (22.0, -159.0)]  # Oahu, Kauai
    kernel_calc = DispersalKernel(locations)
    
    # Test different sigma values
    test_cases = [
        (0.1, 0.1),   # Small sigma - sharp kernel
        (1.0, 1.0),   # Medium sigma
        (5.0, 5.0),   # Large sigma - broad kernel
    ]
    
    for sigma1, sigma2 in test_cases:
        matrix = kernel_calc.calculate_matrix(sigma1, sigma2)
        
        # Basic properties should hold
        assert matrix.shape == (2, 2)
        assert np.all(np.diag(matrix) == 1.0)
        assert np.all(matrix >= 0.0)
        assert np.all(matrix <= 1.0)
        
        # Smaller sigma should give smaller off-diagonal values
        if sigma1 < 1.0:
            assert matrix[0, 1] < 0.5  # Should be small for distant locations

def test_numerical_precision():
    """Test accuracy with extreme parameter values"""
    from phyloland.core.dispersal import DispersalKernel
    
    # Use simple case
    locations = [(21.0, -157.0), (21.0, -157.0)]  # Identical locations
    kernel_calc = DispersalKernel(locations)
    
    # Test with various sigma values
    for sigma1, sigma2 in [(0.01, 0.01), (10.0, 10.0)]:
        matrix = kernel_calc.calculate_matrix(sigma1, sigma2)
        
        # Identical locations should always give kernel = 1.0
        assert np.allclose(matrix, 1.0, rtol=1e-12)

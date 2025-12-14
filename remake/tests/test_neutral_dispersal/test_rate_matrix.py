"""Test rate matrix construction - subunit 4.2"""

import numpy as np
import pandas as pd
import pytest
import time
from pathlib import Path

# Load reference data
TEST_DATA_DIR = Path(__file__).parent.parent.parent.parent / "test_data"
reference = pd.read_csv(TEST_DATA_DIR / "reference" / "rate_matrix_reference.csv").iloc[0]
rate_matrix = pd.read_csv(TEST_DATA_DIR / "reference" / "rate_matrix_matrix.csv")
key_pairs = pd.read_csv(TEST_DATA_DIR / "reference" / "rate_matrix_pairs.csv")

def test_full_banza_rate_matrix():
    """Test 21×21 rate matrix matches R exactly"""
    from phyloland.core.rate_matrix import RateMatrixBuilder
    from phyloland.core.dispersal import DispersalKernel
    
    # Load Banza locations
    locations_file = TEST_DATA_DIR / "banza" / "locations_Banza.txt"
    locations_data = pd.read_csv(locations_file, sep="\t", header=None, 
                                names=["species", "latitude", "longitude"])
    
    # Create rate matrix builder
    locations = list(zip(locations_data["latitude"], locations_data["longitude"]))
    kernel_calc = DispersalKernel(locations)
    rate_builder = RateMatrixBuilder(kernel_calc)
    
    # Build rate matrix
    sigma1, sigma2 = reference["sigma1"], reference["sigma2"]
    Lambda = reference["Lambda"]
    py_matrix = rate_builder.build_matrix(sigma1, sigma2, Lambda)
    
    # Reshape reference matrix from flat format
    n = int(reference["n_locations"])
    r_matrix = rate_matrix["rate_value"].values.reshape(n, n)
    
    # Compare matrices
    np.testing.assert_allclose(py_matrix, r_matrix, rtol=1e-12)
    
    # Check matrix properties
    assert py_matrix.shape == (n, n)

def test_rate_matrix_properties():
    """Test mathematical properties (normalization, scaling)"""
    from phyloland.core.rate_matrix import RateMatrixBuilder
    from phyloland.core.dispersal import DispersalKernel
    
    # Load Banza locations
    locations_file = TEST_DATA_DIR / "banza" / "locations_Banza.txt"
    locations_data = pd.read_csv(locations_file, sep="\t", header=None, 
                                names=["species", "latitude", "longitude"])
    
    locations = list(zip(locations_data["latitude"], locations_data["longitude"]))
    kernel_calc = DispersalKernel(locations)
    rate_builder = RateMatrixBuilder(kernel_calc)
    
    sigma1, sigma2 = reference["sigma1"], reference["sigma2"]
    Lambda = reference["Lambda"]
    matrix = rate_builder.build_matrix(sigma1, sigma2, Lambda)
    
    n = int(reference["n_locations"])
    
    # Check diagonal values (should be Lambda/n)
    expected_diagonal = Lambda / n
    np.testing.assert_allclose(np.diag(matrix), expected_diagonal, rtol=1e-12)
    
    # Check matrix is non-negative
    assert np.all(matrix >= 0)
    
    # Check total rate matches R
    total_rate = np.sum(matrix)
    np.testing.assert_allclose(total_rate, reference["total_rate"], rtol=1e-12)

def test_key_pairwise_rates():
    """Test specific pairwise rate values match R"""
    from phyloland.core.rate_matrix import RateMatrixBuilder
    from phyloland.core.dispersal import DispersalKernel
    
    # Load Banza locations
    locations_file = TEST_DATA_DIR / "banza" / "locations_Banza.txt"
    locations_data = pd.read_csv(locations_file, sep="\t", header=None, 
                                names=["species", "latitude", "longitude"])
    
    locations = list(zip(locations_data["latitude"], locations_data["longitude"]))
    kernel_calc = DispersalKernel(locations)
    rate_builder = RateMatrixBuilder(kernel_calc)
    
    sigma1, sigma2 = reference["sigma1"], reference["sigma2"]
    Lambda = reference["Lambda"]
    matrix = rate_builder.build_matrix(sigma1, sigma2, Lambda)
    
    # Test key pairs from R reference
    for _, pair in key_pairs.iterrows():
        i, j = pair["from_idx"] - 1, pair["to_idx"] - 1  # Convert to 0-based
        expected = pair["rate_value"]
        actual = matrix[i, j]
        
        np.testing.assert_allclose(actual, expected, rtol=1e-12)

def test_rate_matrix_performance():
    """Test construction time < 10ms for 21×21 matrix"""
    from phyloland.core.rate_matrix import RateMatrixBuilder
    from phyloland.core.dispersal import DispersalKernel
    
    # Load Banza locations
    locations_file = TEST_DATA_DIR / "banza" / "locations_Banza.txt"
    locations_data = pd.read_csv(locations_file, sep="\t", header=None, 
                                names=["species", "latitude", "longitude"])
    
    locations = list(zip(locations_data["latitude"], locations_data["longitude"]))
    kernel_calc = DispersalKernel(locations)
    rate_builder = RateMatrixBuilder(kernel_calc)
    
    sigma1, sigma2 = reference["sigma1"], reference["sigma2"]
    Lambda = reference["Lambda"]
    
    # Warm up
    rate_builder.build_matrix(sigma1, sigma2, Lambda)
    
    # Time the calculation
    start_time = time.time()
    for _ in range(10):  # Average over multiple runs
        rate_builder.build_matrix(sigma1, sigma2, Lambda)
    end_time = time.time()
    
    avg_time = (end_time - start_time) / 10
    
    # Should be < 10ms (0.01 seconds)
    assert avg_time < 0.01, f"Rate matrix construction took {avg_time:.4f}s, should be < 0.01s"

def test_parameter_scaling():
    """Test Λ parameter scaling behavior"""
    from phyloland.core.rate_matrix import RateMatrixBuilder
    from phyloland.core.dispersal import DispersalKernel
    
    # Use simple 2-location case for parameter testing
    locations = [(21.0, -157.0), (22.0, -159.0)]  # Oahu, Kauai
    kernel_calc = DispersalKernel(locations)
    rate_builder = RateMatrixBuilder(kernel_calc)
    
    sigma1, sigma2 = 1.0, 1.0
    
    # Get base matrix with Lambda = 1.0
    base_matrix = rate_builder.build_matrix(sigma1, sigma2, 1.0)
    
    # Test different Lambda values
    for Lambda in [0.5, 2.0, 5.0]:
        matrix = rate_builder.build_matrix(sigma1, sigma2, Lambda)
        
        # Diagonal should be Lambda/n
        expected_diagonal = Lambda / 2
        np.testing.assert_allclose(np.diag(matrix), expected_diagonal, rtol=1e-12)
        
        # Matrix should scale linearly with Lambda
        expected_matrix = base_matrix * Lambda
        np.testing.assert_allclose(matrix, expected_matrix, rtol=1e-12)

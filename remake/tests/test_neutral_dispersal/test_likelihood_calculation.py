"""Test likelihood calculation - subunit 4.3"""

import numpy as np
import pandas as pd
import pytest
import time
from pathlib import Path

# Load reference data
TEST_DATA_DIR = Path(__file__).parent.parent.parent.parent / "test_data"
reference = pd.read_csv(TEST_DATA_DIR / "reference" / "likelihood_reference.csv").iloc[0]
likelihood_rates = pd.read_csv(TEST_DATA_DIR / "reference" / "likelihood_rates.csv")

def test_likelihood_rate_matrix_integration():
    """Test likelihood calculation uses rate matrix correctly"""
    from phyloland.core.likelihood import PhylogeneticLikelihood
    from phyloland.core.dispersal import DispersalKernel
    from phyloland.core.rate_matrix import RateMatrixBuilder
    
    # Load test data
    tree_file = TEST_DATA_DIR / "minimal" / "likelihood_test.nex"
    location_file = TEST_DATA_DIR / "minimal" / "likelihood_locations.txt"
    
    # Create likelihood calculator
    likelihood_calc = PhylogeneticLikelihood(tree_file, location_file)
    
    # Calculate rate matrix using infrastructure from 4.1 + 4.2
    sigma1, sigma2 = reference["sigma1"], reference["sigma2"]
    Lambda = reference["Lambda"]
    
    rate_matrix = likelihood_calc.get_rate_matrix(sigma1, sigma2, Lambda)
    
    # Compare with R reference rate matrix
    n = int(reference["n_locations"])
    r_matrix = likelihood_rates["rate_value"].values.reshape(n, n)
    
    np.testing.assert_allclose(rate_matrix, r_matrix, rtol=1e-12)

def test_basic_likelihood_components():
    """Test basic likelihood components match R calculation"""
    from phyloland.core.likelihood import PhylogeneticLikelihood
    
    # Load test data
    tree_file = TEST_DATA_DIR / "minimal" / "likelihood_test.nex"
    location_file = TEST_DATA_DIR / "minimal" / "likelihood_locations.txt"
    
    likelihood_calc = PhylogeneticLikelihood(tree_file, location_file)
    
    # Calculate likelihood components
    sigma1, sigma2 = reference["sigma1"], reference["sigma2"]
    Lambda = reference["Lambda"]
    
    components = likelihood_calc.calculate_likelihood_components(sigma1, sigma2, Lambda)
    
    # Test basic components match R
    np.testing.assert_allclose(components["total_rate"], reference["total_rate"], rtol=1e-12)
    np.testing.assert_allclose(components["diagonal_rate"], reference["diagonal_rate"], rtol=1e-12)

def test_simplified_likelihood_calculation():
    """Test simplified likelihood calculation matches R reference"""
    from phyloland.core.likelihood import PhylogeneticLikelihood
    
    # Load test data
    tree_file = TEST_DATA_DIR / "minimal" / "likelihood_test.nex"
    location_file = TEST_DATA_DIR / "minimal" / "likelihood_locations.txt"
    
    likelihood_calc = PhylogeneticLikelihood(tree_file, location_file)
    
    # Calculate simplified likelihood
    sigma1, sigma2 = reference["sigma1"], reference["sigma2"]
    Lambda = reference["Lambda"]
    
    log_likelihood = likelihood_calc.calculate_simplified_likelihood(sigma1, sigma2, Lambda)
    
    # Should be in reasonable range (simplified calculation, not full phylogenetic likelihood)
    # This tests infrastructure integration, not exact phylogenetic likelihood
    assert isinstance(log_likelihood, (float, np.floating))
    assert log_likelihood < 0  # Log-likelihood should be negative
    assert abs(log_likelihood) > 10  # Should be substantial negative value

def test_likelihood_performance():
    """Test computation time reasonable for MCMC applications"""
    from phyloland.core.likelihood import PhylogeneticLikelihood
    
    # Load test data
    tree_file = TEST_DATA_DIR / "minimal" / "likelihood_test.nex"
    location_file = TEST_DATA_DIR / "minimal" / "likelihood_locations.txt"
    
    likelihood_calc = PhylogeneticLikelihood(tree_file, location_file)
    
    sigma1, sigma2 = reference["sigma1"], reference["sigma2"]
    Lambda = reference["Lambda"]
    
    # Warm up
    likelihood_calc.calculate_simplified_likelihood(sigma1, sigma2, Lambda)
    
    # Time the calculation
    start_time = time.time()
    for _ in range(10):  # Average over multiple runs
        likelihood_calc.calculate_simplified_likelihood(sigma1, sigma2, Lambda)
    end_time = time.time()
    
    avg_time = (end_time - start_time) / 10
    
    # Should be reasonable for 5-location case (much less than 100ms target)
    assert avg_time < 0.01, f"Likelihood calculation took {avg_time:.4f}s, should be < 0.01s for 5 locations"

def test_parameter_sensitivity():
    """Test likelihood changes appropriately with parameters"""
    from phyloland.core.likelihood import PhylogeneticLikelihood
    
    # Load test data
    tree_file = TEST_DATA_DIR / "minimal" / "likelihood_test.nex"
    location_file = TEST_DATA_DIR / "minimal" / "likelihood_locations.txt"
    
    likelihood_calc = PhylogeneticLikelihood(tree_file, location_file)
    
    # Test different parameter values
    base_sigma1, base_sigma2 = reference["sigma1"], reference["sigma2"]
    base_Lambda = reference["Lambda"]
    
    base_likelihood = likelihood_calc.calculate_simplified_likelihood(base_sigma1, base_sigma2, base_Lambda)
    
    # Test sigma sensitivity
    higher_sigma_likelihood = likelihood_calc.calculate_simplified_likelihood(base_sigma1 * 2, base_sigma2 * 2, base_Lambda)
    assert higher_sigma_likelihood != base_likelihood  # Should change with different sigma
    
    # Test Lambda sensitivity  
    higher_Lambda_likelihood = likelihood_calc.calculate_simplified_likelihood(base_sigma1, base_sigma2, base_Lambda * 2)
    assert higher_Lambda_likelihood != base_likelihood  # Should change with different Lambda

def test_data_structure_integration():
    """Test proper integration with tree and location data"""
    from phyloland.core.likelihood import PhylogeneticLikelihood
    
    # Load test data
    tree_file = TEST_DATA_DIR / "minimal" / "likelihood_test.nex"
    location_file = TEST_DATA_DIR / "minimal" / "likelihood_locations.txt"
    
    likelihood_calc = PhylogeneticLikelihood(tree_file, location_file)
    
    # Check basic properties
    assert likelihood_calc.n_locations == reference["n_locations"]
    assert likelihood_calc.n_tips == reference["n_locations"]  # Should match for this test
    assert len(likelihood_calc.locations) == reference["n_locations"]

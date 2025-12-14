"""Test algorithm validation against phyloland - subunit 5.3"""

import numpy as np
import pandas as pd
import pytest
from pathlib import Path

# Load phyloland algorithm reference data
TEST_DATA_DIR = Path(__file__).parent.parent.parent.parent / "test_data"

def test_fixed_distance_calculation_vs_phyloland():
    """Test fixed Python distance calculation matches phyloland distkm exactly"""
    from phyloland.core.dispersal import DispersalKernel
    
    # Load Banza locations
    locations_file = TEST_DATA_DIR / "banza" / "locations_Banza.txt"
    locations_data = pd.read_csv(locations_file, sep="\t", header=None, 
                                names=["species", "latitude", "longitude"])
    
    locations = list(zip(locations_data["latitude"], locations_data["longitude"]))
    kernel_calc = DispersalKernel(locations)
    
    # Load phyloland distances
    phyloland_distances = pd.read_csv(TEST_DATA_DIR / "phyloland_reference" / "phyloland_distances.csv")
    
    # Test key distance pairs against phyloland
    n = len(locations)
    phyloland_matrix = phyloland_distances["distance_km"].values.reshape(n, n)
    
    # Calculate Python distances with fixed formula
    python_distances = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                python_distances[i, j] = kernel_calc.calculate_pairwise_distance(i, j)
    
    # Should now match phyloland exactly
    mask = phyloland_matrix > 0
    differences = np.abs(python_distances[mask] - phyloland_matrix[mask])
    max_diff = np.max(differences)
    
    print(f"\nDistance correction results:")
    print(f"Max absolute difference: {max_diff:.2e} km")
    print(f"Max relative difference: {np.max(differences / phyloland_matrix[mask]):.2e}")
    
    # Should be much better now with phyloland formula
    np.testing.assert_allclose(python_distances[mask], phyloland_matrix[mask], rtol=1e-12)

def test_corrected_components_vs_phyloland():
    """Test that corrected distances fix kernel and rate calculations"""
    from phyloland.core.dispersal import DispersalKernel
    from phyloland.core.rate_matrix import RateMatrixBuilder
    
    # Load Banza locations
    locations_file = TEST_DATA_DIR / "banza" / "locations_Banza.txt"
    locations_data = pd.read_csv(locations_file, sep="\t", header=None, 
                                names=["species", "latitude", "longitude"])
    
    locations = list(zip(locations_data["latitude"], locations_data["longitude"]))
    kernel_calc = DispersalKernel(locations)
    rate_builder = RateMatrixBuilder(kernel_calc)
    
    # Load phyloland reference data
    phyloland_kernels = pd.read_csv(TEST_DATA_DIR / "phyloland_reference" / "phyloland_kernels.csv")
    phyloland_rates = pd.read_csv(TEST_DATA_DIR / "phyloland_reference" / "phyloland_rates.csv")
    
    # Use same parameters
    sigma1, sigma2, Lambda = 0.5, 0.8, 2.5
    
    # Calculate with corrected distances
    python_kernel = kernel_calc.calculate_matrix(sigma1, sigma2)
    python_rates = rate_builder.build_matrix(sigma1, sigma2, Lambda)
    
    # Get phyloland matrices
    n = len(locations)
    phyloland_kernel = phyloland_kernels["kernel_value"].values.reshape(n, n)
    phyloland_rate_matrix = phyloland_rates["rate_value"].values.reshape(n, n)
    
    # Should match exactly now
    np.testing.assert_allclose(python_kernel, phyloland_kernel, rtol=1e-12)
    np.testing.assert_allclose(python_rates, phyloland_rate_matrix, rtol=1e-12)

def test_algorithm_parameter_validation():
    """Test algorithm handles phyloland parameter ranges correctly"""
    from phyloland.core.likelihood import PhylogeneticLikelihood
    
    # Load algorithm summary
    algorithm_file = TEST_DATA_DIR / "phyloland_reference" / "phyloland_algorithm_summary.csv"
    if not algorithm_file.exists():
        pytest.skip("Phyloland algorithm summary not available")
    
    algorithm_summary = pd.read_csv(algorithm_file).iloc[0]
    
    # Test with phyloland parameters
    tree_file = TEST_DATA_DIR / "banza" / "tree_Banza.nex"
    location_file = TEST_DATA_DIR / "banza" / "locations_Banza.txt"
    
    likelihood_calc = PhylogeneticLikelihood(tree_file, location_file)
    
    # Use phyloland parameters
    sigma1 = algorithm_summary["final_sigma1"]
    sigma2 = algorithm_summary["final_sigma2"]
    Lambda = algorithm_summary["final_lambda"]
    
    # Should handle phyloland parameters without errors
    components = likelihood_calc.calculate_likelihood_components(sigma1, sigma2, Lambda)
    
    assert components is not None
    assert "total_rate" in components
    assert "diagonal_rate" in components

def test_scientific_parameter_ranges():
    """Test algorithm works across realistic phylogeographic parameter ranges"""
    from phyloland.core.dispersal import DispersalKernel
    from phyloland.core.rate_matrix import RateMatrixBuilder
    
    # Use simple test case
    locations = [(21.0, -157.0), (22.0, -159.0)]  # Oahu, Kauai
    kernel_calc = DispersalKernel(locations)
    rate_builder = RateMatrixBuilder(kernel_calc)
    
    # Test realistic phylogeographic parameter ranges
    test_params = [
        (0.1, 0.1, 0.5),   # Small dispersal, low rate
        (0.5, 0.8, 2.5),   # Phyloland Banza parameters
        (1.0, 1.2, 5.0),   # Larger dispersal, higher rate
        (2.0, 1.5, 10.0)   # Very large dispersal
    ]
    
    for sigma1, sigma2, Lambda in test_params:
        # Should work without errors
        kernel_matrix = kernel_calc.calculate_matrix(sigma1, sigma2)
        rate_matrix = rate_builder.build_matrix(sigma1, sigma2, Lambda)
        
        # Basic validation
        assert kernel_matrix.shape == (2, 2)
        assert rate_matrix.shape == (2, 2)
        assert np.all(kernel_matrix >= 0)
        assert np.all(rate_matrix >= 0)
        assert np.allclose(np.diag(kernel_matrix), 1.0)

def test_phyloland_algorithm_integration():
    """Test complete algorithm integration matches phyloland approach"""
    from phyloland.core.dispersal import DispersalKernel
    from phyloland.core.rate_matrix import RateMatrixBuilder
    from phyloland.core.likelihood import PhylogeneticLikelihood
    
    # Test complete integration with Banza subset
    tree_file = TEST_DATA_DIR / "minimal" / "five_tips.nex"
    location_file = TEST_DATA_DIR / "minimal" / "five_locations.txt"
    
    # Test complete workflow
    likelihood_calc = PhylogeneticLikelihood(tree_file, location_file)
    
    # Use phyloland-style parameters
    sigma1, sigma2, Lambda = 0.5, 0.8, 2.5
    
    # Get components
    rate_matrix = likelihood_calc.get_rate_matrix(sigma1, sigma2, Lambda)
    components = likelihood_calc.calculate_likelihood_components(sigma1, sigma2, Lambda)
    simplified_likelihood = likelihood_calc.calculate_simplified_likelihood(sigma1, sigma2, Lambda)
    
    # Validate integration
    assert rate_matrix.shape == (5, 5)
    assert "total_rate" in components
    assert isinstance(simplified_likelihood, (float, np.floating))
    assert simplified_likelihood < 0  # Log-likelihood should be negative

def test_phyloland_reference_data_completeness():
    """Test phyloland reference data is complete for algorithm validation"""
    # Check required files exist
    required_files = [
        "phyloland_distances.csv",
        "phyloland_kernels.csv", 
        "phyloland_rates.csv",
        "phyloland_component_summary.csv",
        "phyloland_algorithm_summary.csv"
    ]
    
    phyloland_ref_dir = TEST_DATA_DIR / "phyloland_reference"
    
    for filename in required_files:
        filepath = phyloland_ref_dir / filename
        assert filepath.exists(), f"Required phyloland reference file missing: {filename}"
    
    # Check data quality
    algorithm_summary = pd.read_csv(phyloland_ref_dir / "phyloland_algorithm_summary.csv")
    assert len(algorithm_summary) > 0, "Algorithm summary is empty"
    assert algorithm_summary["n_species"].iloc[0] == 21, "Expected 21 species in Banza dataset"

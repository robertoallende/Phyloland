"""Test two locations base case - subunit 3.2"""

import numpy as np
import pandas as pd
import pytest
from pathlib import Path

# Load reference data
TEST_DATA_DIR = Path(__file__).parent.parent.parent.parent / "test_data"
reference = pd.read_csv(TEST_DATA_DIR / "reference" / "two_locations_reference.csv").iloc[0]

def test_two_locations_geographic_distance():
    """Test geographic distance calculation matches R distkm"""
    from phyloland.core.base_cases import TwoLocationCase
    
    tree_file = TEST_DATA_DIR / "minimal" / "two_tips.nex"
    location_file = TEST_DATA_DIR / "minimal" / "two_locations.txt"
    
    case = TwoLocationCase(tree_file, location_file)
    
    # Calculate distance between Oahu and Kauai
    distance = case.calculate_distance(case.locations[0], case.locations[1])
    
    # Should match R distkm calculation
    np.testing.assert_allclose(distance, reference["distance_km"], rtol=1e-10)

def test_dispersal_kernel_calculation():
    """Test dispersal kernel f(x,y) matches R computation"""
    from phyloland.core.base_cases import TwoLocationCase
    
    tree_file = TEST_DATA_DIR / "minimal" / "two_tips.nex"
    location_file = TEST_DATA_DIR / "minimal" / "two_locations.txt"
    
    case = TwoLocationCase(tree_file, location_file)
    
    # Calculate dispersal kernel with default sigma
    sigma = [reference["sigma1"], reference["sigma2"]]
    kernel_value = case.dispersal_kernel(case.locations[0], case.locations[1], sigma)
    
    # Should match R calculation
    np.testing.assert_allclose(kernel_value, reference["dispersal_kernel"], rtol=1e-12)

def test_rate_matrix_construction():
    """Test 2×2 rate matrix matches R computation"""
    from phyloland.core.base_cases import TwoLocationCase
    
    tree_file = TEST_DATA_DIR / "minimal" / "two_tips.nex"
    location_file = TEST_DATA_DIR / "minimal" / "two_locations.txt"
    
    case = TwoLocationCase(tree_file, location_file)
    
    # Build rate matrix
    sigma = [reference["sigma1"], reference["sigma2"]]
    rate_matrix = case.build_rate_matrix(sigma)
    
    # Check matrix values match R
    np.testing.assert_allclose(rate_matrix[0, 1], reference["rate_F12"], rtol=1e-12)
    np.testing.assert_allclose(rate_matrix[1, 0], reference["rate_F21"], rtol=1e-12)
    np.testing.assert_allclose(rate_matrix[0, 0], reference["rate_F11"], rtol=1e-12)
    np.testing.assert_allclose(rate_matrix[1, 1], reference["rate_F22"], rtol=1e-12)

def test_two_locations_data_structures():
    """Test tree and location data processing"""
    from phyloland.core.base_cases import TwoLocationCase
    
    tree_file = TEST_DATA_DIR / "minimal" / "two_tips.nex"
    location_file = TEST_DATA_DIR / "minimal" / "two_locations.txt"
    
    case = TwoLocationCase(tree_file, location_file)
    
    # Check basic properties
    assert case.n_tips == reference["n_tips"]
    assert case.n_locations == reference["n_locations"]
    assert case.n_dispersal_events == reference["n_dispersal_events"]
    
    # Check data loaded correctly
    assert len(case.tip_names) == 2
    assert "tip1" in case.tip_names
    assert "tip2" in case.tip_names
    assert len(case.locations) == 2

"""Test no competition base case - subunit 3.3"""

import numpy as np
import pandas as pd
import pytest
from pathlib import Path

# Load reference data
TEST_DATA_DIR = Path(__file__).parent.parent.parent.parent / "test_data"
reference = pd.read_csv(TEST_DATA_DIR / "reference" / "no_competition_reference.csv").iloc[0]
distances = pd.read_csv(TEST_DATA_DIR / "reference" / "no_competition_distances.csv")
kernels = pd.read_csv(TEST_DATA_DIR / "reference" / "no_competition_kernels.csv")
rates = pd.read_csv(TEST_DATA_DIR / "reference" / "no_competition_rates.csv")

def test_multi_location_distances():
    """Test all pairwise distances match R distkm calculations"""
    from phyloland.core.base_cases import NoCompetitionCase
    
    tree_file = TEST_DATA_DIR / "minimal" / "five_tips.nex"
    location_file = TEST_DATA_DIR / "minimal" / "five_locations.txt"
    
    case = NoCompetitionCase(tree_file, location_file)
    
    # Test key distance pairs
    # Oahu-Kauai (indices 0,1)
    oahu_kauai = case.calculate_distance(case.locations[0], case.locations[1])
    expected = distances[(distances["from"]==1) & (distances["to"]==2)]["distance_km"].iloc[0]
    np.testing.assert_allclose(oahu_kauai, expected, rtol=1e-10)
    
    # Oahu-Maui (indices 0,2)  
    oahu_maui = case.calculate_distance(case.locations[0], case.locations[2])
    expected = distances[(distances["from"]==1) & (distances["to"]==3)]["distance_km"].iloc[0]
    np.testing.assert_allclose(oahu_maui, expected, rtol=1e-10)

def test_multi_location_kernels():
    """Test dispersal kernels for all location pairs match R"""
    from phyloland.core.base_cases import NoCompetitionCase
    
    tree_file = TEST_DATA_DIR / "minimal" / "five_tips.nex"
    location_file = TEST_DATA_DIR / "minimal" / "five_locations.txt"
    
    case = NoCompetitionCase(tree_file, location_file)
    
    # Test kernel calculations
    sigma = [reference["sigma1"], reference["sigma2"]]
    
    # Oahu-Kauai kernel
    kernel_01 = case.dispersal_kernel(case.locations[0], case.locations[1], sigma)
    expected = kernels[(kernels["from"]==1) & (kernels["to"]==2)]["kernel_value"].iloc[0]
    np.testing.assert_allclose(kernel_01, expected, rtol=1e-12)

def test_five_by_five_rate_matrix():
    """Test 5×5 rate matrix construction matches R"""
    from phyloland.core.base_cases import NoCompetitionCase
    
    tree_file = TEST_DATA_DIR / "minimal" / "five_tips.nex"
    location_file = TEST_DATA_DIR / "minimal" / "five_locations.txt"
    
    case = NoCompetitionCase(tree_file, location_file)
    
    # Build rate matrix
    sigma = [reference["sigma1"], reference["sigma2"]]
    rate_matrix = case.build_rate_matrix(sigma)
    
    # Test key rate values
    # Rate[0,1] (Oahu->Kauai)
    expected_01 = rates[(rates["from"]==1) & (rates["to"]==2)]["rate_value"].iloc[0]
    np.testing.assert_allclose(rate_matrix[0, 1], expected_01, rtol=1e-12)
    
    # Self-dispersal rate[0,0]
    expected_00 = rates[(rates["from"]==1) & (rates["to"]==1)]["rate_value"].iloc[0]
    np.testing.assert_allclose(rate_matrix[0, 0], expected_00, rtol=1e-12)

def test_no_competition_constraint():
    """Test δj = 1 always (no competition effects)"""
    from phyloland.core.base_cases import NoCompetitionCase
    
    tree_file = TEST_DATA_DIR / "minimal" / "five_tips.nex"
    location_file = TEST_DATA_DIR / "minimal" / "five_locations.txt"
    
    case = NoCompetitionCase(tree_file, location_file)
    
    # All competition factors should be 1.0
    competition_factors = case.get_competition_factors()
    assert all(factor == 1.0 for factor in competition_factors)
    assert case.lambda_comp == reference["lambda_comp"]

def test_multi_location_data_structures():
    """Test 5-tip tree and 5-location data processing"""
    from phyloland.core.base_cases import NoCompetitionCase
    
    tree_file = TEST_DATA_DIR / "minimal" / "five_tips.nex"
    location_file = TEST_DATA_DIR / "minimal" / "five_locations.txt"
    
    case = NoCompetitionCase(tree_file, location_file)
    
    # Check basic properties
    assert case.n_tips == reference["n_tips"]
    assert case.n_locations == reference["n_locations"]
    assert case.n_dispersal_events == reference["n_dispersal_events"]
    
    # Check data loaded correctly
    assert len(case.tip_names) == 5
    assert len(case.locations) == 5
    expected_tips = ["tip1", "tip2", "tip3", "tip4", "tip5"]
    assert all(tip in case.tip_names for tip in expected_tips)

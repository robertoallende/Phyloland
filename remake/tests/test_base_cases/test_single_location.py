"""Test single location base case - subunit 3.1"""

import pandas as pd
import pytest
from pathlib import Path

# Load reference data
TEST_DATA_DIR = Path(__file__).parent.parent.parent.parent / "test_data"
reference = pd.read_csv(TEST_DATA_DIR / "reference" / "single_location_reference.csv").iloc[0]

def test_single_location_likelihood():
    """Test trivial case produces likelihood = 1"""
    from phyloland.core.base_cases import SingleLocationCase
    
    # Load test data
    tree_file = TEST_DATA_DIR / "minimal" / "single_tip.nex"
    location_file = TEST_DATA_DIR / "minimal" / "single_location.txt"
    
    # Create case
    case = SingleLocationCase(tree_file, location_file)
    
    # Calculate likelihood
    likelihood = case.calculate_likelihood()
    
    # Should match R reference (= 1.0)
    assert likelihood == reference["likelihood"]
    assert likelihood == 1.0

def test_single_location_parameters():
    """Test parameter handling with no dispersal events"""
    from phyloland.core.base_cases import SingleLocationCase
    
    tree_file = TEST_DATA_DIR / "minimal" / "single_tip.nex"
    location_file = TEST_DATA_DIR / "minimal" / "single_location.txt"
    
    case = SingleLocationCase(tree_file, location_file)
    
    # Check basic properties
    assert case.n_tips == reference["n_tips"]
    assert case.n_locations == reference["n_locations"] 
    assert case.n_dispersal_events == reference["n_dispersal_events"]

def test_single_location_data_structures():
    """Test tree and location data processing"""
    from phyloland.core.base_cases import SingleLocationCase
    
    tree_file = TEST_DATA_DIR / "minimal" / "single_tip.nex"
    location_file = TEST_DATA_DIR / "minimal" / "single_location.txt"
    
    case = SingleLocationCase(tree_file, location_file)
    
    # Check data loaded correctly
    assert len(case.tip_names) == 1
    assert case.tip_names[0] == "tip1"
    assert len(case.locations) == 1
    assert case.locations[0] == (21.0, -157.0)

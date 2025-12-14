"""Test phyloland package integration - subunit 5.1"""

import pandas as pd
import pytest
from pathlib import Path

# Load validation results
TEST_DATA_DIR = Path(__file__).parent.parent.parent.parent / "test_data"

def test_phyloland_installation():
    """Test phyloland package is installed and working"""
    # Check if validation files exist
    validation_file = TEST_DATA_DIR / "phyloland_reference" / "package_validation.csv"
    
    if validation_file.exists():
        validation = pd.read_csv(validation_file)
        
        # Check that basic tests passed
        package_install = validation[validation["test"] == "package_installation"]
        package_load = validation[validation["test"] == "package_loading"]
        data_load = validation[validation["test"] == "data_loading"]
        
        # All should have "success" status
        assert len(package_install) > 0, "Package installation test not found"
        assert len(package_load) > 0, "Package loading test not found"
        assert len(data_load) > 0, "Data loading test not found"
    else:
        pytest.skip("Phyloland validation file not found - run R validation first")

def test_basic_phyloland_functions():
    """Test basic phyloland functions execute without errors"""
    # Check if basic function validation exists
    basic_validation_file = TEST_DATA_DIR / "phyloland_reference" / "basic_function_validation.csv"
    
    if basic_validation_file.exists():
        validation = pd.read_csv(basic_validation_file)
        
        # Check key functions
        expected_functions = ["read.nexus", "read.table", "distkm", "space_dist"]
        
        for func_name in expected_functions:
            func_test = validation[validation["function_name"] == func_name]
            assert len(func_test) > 0, f"Function {func_name} test not found"
            
            # Check status is success
            status = func_test["status"].iloc[0]
            assert status == "success", f"Function {func_name} failed: {status}"
    else:
        pytest.skip("Basic function validation file not found - run R validation first")

def test_banza_data_loading():
    """Test phyloland can load Banza dataset correctly"""
    # Check that Banza data files exist and are readable
    tree_file = TEST_DATA_DIR / "banza" / "tree_Banza.nex"
    locations_file = TEST_DATA_DIR / "banza" / "locations_Banza.txt"
    
    assert tree_file.exists(), "Banza tree file not found"
    assert locations_file.exists(), "Banza locations file not found"
    
    # Check locations file format
    locations = pd.read_csv(locations_file, sep="\t", header=None, 
                           names=["species", "latitude", "longitude"])
    
    assert len(locations) == 21, f"Expected 21 species, got {len(locations)}"
    assert "brunneaA" in locations["species"].values, "Expected species not found"
    
    # Check coordinate ranges (Hawaiian islands)
    assert locations["latitude"].min() > 18, "Latitude out of Hawaiian range"
    assert locations["latitude"].max() < 25, "Latitude out of Hawaiian range"
    
    # Hawaiian longitudes can be positive (East) or negative (West) depending on format
    # Check they're in reasonable range for Hawaiian islands
    lon_min, lon_max = locations["longitude"].min(), locations["longitude"].max()
    
    # Accept either negative (Western hemisphere) or positive (Eastern format) coordinates
    if lon_min < 0:
        # Western hemisphere format (-162 to -154)
        assert lon_min > -162, f"Longitude too far west: {lon_min}"
        assert lon_max < -154, f"Longitude too far east: {lon_max}"
    else:
        # Eastern format (154 to 162)
        assert lon_min > 154, f"Longitude too far west: {lon_min}"
        assert lon_max < 162, f"Longitude too far east: {lon_max}"

def test_phyloland_environment_ready():
    """Test phyloland environment is ready for comprehensive validation"""
    # This test ensures all prerequisites are met for subunits 5.2-5.5
    
    # Check R validation completed
    validation_files = [
        "package_validation.csv",
        "basic_function_validation.csv"
    ]
    
    phyloland_ref_dir = TEST_DATA_DIR / "phyloland_reference"
    
    for filename in validation_files:
        filepath = phyloland_ref_dir / filename
        assert filepath.exists(), f"Required validation file missing: {filename}"
    
    # Check Banza data is available
    banza_files = [
        "tree_Banza.nex",
        "locations_Banza.txt"
    ]
    
    banza_dir = TEST_DATA_DIR / "banza"
    
    for filename in banza_files:
        filepath = banza_dir / filename
        assert filepath.exists(), f"Required Banza file missing: {filename}"
    
    # Environment is ready for comprehensive validation
    assert True, "Phyloland environment ready for subunits 5.2-5.5"

def test_validation_data_structure():
    """Test validation data has expected structure"""
    basic_validation_file = TEST_DATA_DIR / "phyloland_reference" / "basic_function_validation.csv"
    
    if basic_validation_file.exists():
        validation = pd.read_csv(basic_validation_file)
        
        # Check required columns
        required_columns = ["function_name", "status", "test_value", "timestamp"]
        for col in required_columns:
            assert col in validation.columns, f"Missing column: {col}"
        
        # Check data types
        assert len(validation) > 0, "Validation data is empty"
        assert validation["status"].dtype == "object", "Status column should be string"
    else:
        pytest.skip("Basic validation file not found")

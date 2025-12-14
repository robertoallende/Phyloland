"""Test pandas file I/O equivalence to R read.table"""

import pandas as pd
import numpy as np
from pathlib import Path

# Load reference data
TEST_DATA_DIR = Path(__file__).parent.parent.parent.parent / "test_data"
r_data = pd.read_csv(TEST_DATA_DIR / "reference" / "io_data_reference.csv")
r_structure = pd.read_csv(TEST_DATA_DIR / "reference" / "io_structure_reference.csv")

def test_csv_data_equivalence():
    """Test pandas reads same data values as R read.table"""
    # Read with pandas using same approach as R
    py_data = pd.read_csv(TEST_DATA_DIR / "banza" / "locations_Banza.txt", 
                         sep="\t", header=None, 
                         names=["species", "latitude", "longitude"])
    
    # Check dimensions match
    assert py_data.shape == r_data.shape
    
    # Check species names match exactly
    assert list(py_data["species"]) == list(r_data["species"])
    
    # Check coordinates within precision tolerance
    np.testing.assert_allclose(py_data["latitude"], r_data["latitude"], rtol=1e-10)
    np.testing.assert_allclose(py_data["longitude"], r_data["longitude"], rtol=1e-10)

def test_column_structure():
    """Test column names and count match R parsing"""
    py_data = pd.read_csv(TEST_DATA_DIR / "banza" / "locations_Banza.txt", 
                         sep="\t", header=None, 
                         names=["species", "latitude", "longitude"])
    
    # Check column names
    assert list(py_data.columns) == list(r_data.columns)
    
    # Check row and column counts
    expected_rows = int(r_structure[r_structure["column"] == "species"]["row_count"].iloc[0])
    expected_cols = int(r_structure[r_structure["column"] == "species"]["col_count"].iloc[0])
    
    assert py_data.shape[0] == expected_rows
    assert py_data.shape[1] == expected_cols

def test_numeric_precision():
    """Test coordinate precision within tolerance"""
    py_data = pd.read_csv(TEST_DATA_DIR / "banza" / "locations_Banza.txt", 
                         sep="\t", header=None, 
                         names=["species", "latitude", "longitude"])
    
    # Test specific coordinate values for precision
    first_lat = py_data["latitude"].iloc[0]
    first_lon = py_data["longitude"].iloc[0]
    
    r_first_lat = r_data["latitude"].iloc[0]
    r_first_lon = r_data["longitude"].iloc[0]
    
    # High precision for geographic coordinates
    assert abs(first_lat - r_first_lat) < 1e-10
    assert abs(first_lon - r_first_lon) < 1e-10

def test_data_types():
    """Test data types are appropriate for phylogeographic analysis"""
    py_data = pd.read_csv(TEST_DATA_DIR / "banza" / "locations_Banza.txt", 
                         sep="\t", header=None, 
                         names=["species", "latitude", "longitude"])
    
    # Species should be string-like
    assert py_data["species"].dtype == object
    
    # Coordinates should be numeric
    assert np.issubdtype(py_data["latitude"].dtype, np.floating)
    assert np.issubdtype(py_data["longitude"].dtype, np.floating)

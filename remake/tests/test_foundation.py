"""Tests to validate Unit 01: Foundation implementation."""

import pytest
from pathlib import Path


def test_package_structure():
    """Verify all modules can be imported and package metadata is correct."""
    import phyloland
    import phyloland.core
    import phyloland.mcmc
    import phyloland.utils
    import phyloland.data
    
    # Check package metadata
    assert phyloland.__version__ == "0.1.0"
    assert "Phyloland" in phyloland.__doc__
    assert "phylogeographic" in phyloland.__doc__


def test_module_docstrings():
    """Verify all modules have proper documentation."""
    import phyloland.core
    import phyloland.mcmc
    import phyloland.utils
    import phyloland.data
    
    assert "Core algorithm" in phyloland.core.__doc__
    assert "MCMC engine" in phyloland.mcmc.__doc__
    assert "Utility functions" in phyloland.utils.__doc__
    assert "Sample data" in phyloland.data.__doc__


def test_shared_data_access(test_data_dir, banza_data_dir):
    """Verify shared test data is accessible and contains expected files."""
    # Test data directory exists
    assert test_data_dir.exists()
    assert test_data_dir.is_dir()
    
    # Banza data directory exists
    assert banza_data_dir.exists()
    assert banza_data_dir.is_dir()
    
    # Required Banza files exist
    locations_file = banza_data_dir / "locations_Banza.txt"
    tree_file = banza_data_dir / "tree_Banza.nex"
    
    assert locations_file.exists()
    assert tree_file.exists()
    
    # Files are not empty
    assert locations_file.stat().st_size > 0
    assert tree_file.stat().st_size > 0


def test_reference_data_directory(reference_data_dir):
    """Verify reference data directory exists for future R validation outputs."""
    assert reference_data_dir.exists()
    assert reference_data_dir.is_dir()


def test_test_directory_structure():
    """Verify test directory structure is properly organized."""
    test_dir = Path(__file__).parent
    
    # Main test directories exist
    assert (test_dir / "test_dependencies").exists()
    assert (test_dir / "test_core").exists()
    assert (test_dir / "test_integration").exists()
    
    # conftest.py exists
    assert (test_dir / "conftest.py").exists()


def test_dependencies_importable():
    """Verify all required dependencies can be imported."""
    # Core scientific stack
    import numpy
    import scipy
    import pandas
    
    # Phylogenetic trees
    import dendropy
    
    # Testing framework
    import pytest
    
    # Optional dependencies
    import matplotlib
    import numba
    
    # Basic functionality test
    assert numpy.array([1, 2, 3]).sum() == 6
    assert len(pandas.DataFrame({'a': [1, 2]})) == 2

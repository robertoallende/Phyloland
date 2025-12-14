"""
Test PLD_interface - Subunit 6.4
Validate complete phyloland API compatibility
"""

import pytest
import numpy as np
import tempfile
import os
from pathlib import Path
from phyloland.interface import PLD_interface

class TestPLDInterface:
    """Test complete PLD_interface functionality"""
    
    @pytest.fixture
    def temp_files(self):
        """Create temporary test files"""
        # Create temporary directory
        temp_dir = tempfile.mkdtemp()
        
        # Create mock NEXUS tree file
        tree_content = """#NEXUS
BEGIN TREES;
    TREE tree1 = ((A:0.1,B:0.1):0.1,(C:0.1,D:0.1):0.1);
END;"""
        
        tree_file = os.path.join(temp_dir, "test_tree.nex")
        with open(tree_file, 'w') as f:
            f.write(tree_content)
            
        # Create mock location data file
        location_content = """A\t21.3099\t-157.8581
B\t20.7984\t-156.3319
C\t19.5429\t-155.6659
D\t22.0964\t-159.5261"""
        
        data_file = os.path.join(temp_dir, "test_data.txt")
        with open(data_file, 'w') as f:
            f.write(location_content)
            
        return tree_file, data_file, temp_dir
        
    def test_pld_interface_parameter_validation(self, temp_files):
        """Test parameter validation matching phyloland"""
        tree_file, data_file, temp_dir = temp_files
        
        # Test required parameters
        with pytest.raises(ValueError, match="fileTREES is required"):
            PLD_interface(fileTREES=None, fileDATA=data_file)
            
        with pytest.raises(ValueError, match="fileDATA is required"):
            PLD_interface(fileTREES=tree_file, fileDATA=None)
            
        # Test numeric parameter validation
        with pytest.raises(ValueError, match="num_step must be positive"):
            PLD_interface(tree_file, data_file, num_step=0)
            
        with pytest.raises(ValueError, match="freq must be positive"):
            PLD_interface(tree_file, data_file, freq=0)
            
        with pytest.raises(ValueError, match="burnin must be non-negative"):
            PLD_interface(tree_file, data_file, burnin=-1)
            
        with pytest.raises(ValueError, match="ess_lim must be positive"):
            PLD_interface(tree_file, data_file, ess_lim=0)
            
    def test_pld_interface_file_validation(self, temp_files):
        """Test file existence validation"""
        tree_file, data_file, temp_dir = temp_files
        
        # Test non-existent tree file
        with pytest.raises(FileNotFoundError, match="Tree file not found"):
            PLD_interface("nonexistent_tree.nex", data_file)
            
        # Test non-existent data file  
        with pytest.raises(FileNotFoundError, match="Data file not found"):
            PLD_interface(tree_file, "nonexistent_data.txt")
            
    def test_pld_interface_basic_run(self, temp_files):
        """Test basic PLD_interface execution"""
        tree_file, data_file, temp_dir = temp_files
        
        # Run with minimal parameters for quick test
        result = PLD_interface(
            fileTREES=tree_file,
            fileDATA=data_file,
            num_step=100,
            freq=10,
            burnin=20,
            ess_lim=5  # Low threshold for quick convergence
        )
        
        # Verify result structure matches phyloland
        assert 'sigma1' in result
        assert 'sigma2' in result
        assert 'lambda' in result
        assert 'Lambda' in result
        assert 'likelihood' in result
        assert 'trees' in result
        assert 'locations' in result
        assert 'tips' in result
        assert 'space' in result
        assert 'mcmc' in result
        
        # Verify MCMC info
        assert 'n_samples' in result['mcmc']
        assert 'converged' in result['mcmc']
        
    def test_pld_interface_parameter_arrays(self, temp_files):
        """Test parameter arrays are numpy arrays"""
        tree_file, data_file, temp_dir = temp_files
        
        result = PLD_interface(tree_file, data_file, num_step=50, ess_lim=1)
        
        # All parameter results should be numpy arrays
        assert isinstance(result['sigma1'], np.ndarray)
        assert isinstance(result['sigma2'], np.ndarray)
        assert isinstance(result['lambda'], np.ndarray)
        assert isinstance(result['Lambda'], np.ndarray)
        assert isinstance(result['likelihood'], np.ndarray)
        
    def test_pld_interface_location_handling(self, temp_files):
        """Test location data handling"""
        tree_file, data_file, temp_dir = temp_files
        
        # Test with custom location names
        location_names = ["Oahu", "Maui", "BigIsland", "Kauai"]
        result = PLD_interface(tree_file, data_file, num_step=50, ess_lim=1,
                              names_locations=location_names)
        
        # Should have location information
        assert 'locations' in result
        assert 'space' in result
        assert len(result['locations']) > 0
        
    def test_pld_interface_multi_chain(self, temp_files):
        """Test multi-chain execution"""
        tree_file, data_file, temp_dir = temp_files
        
        # Run with multiple chains
        result = PLD_interface(
            fileTREES=tree_file,
            fileDATA=data_file,
            num_step=100,
            ess_lim=5,
            n_chains=2  # Extension parameter
        )
        
        # Should have same result structure
        assert 'sigma1' in result
        assert 'mcmc' in result
        assert result['mcmc']['n_samples'] > 0
        
    def test_pld_interface_phyloland_defaults(self, temp_files):
        """Test phyloland default parameters"""
        tree_file, data_file, temp_dir = temp_files
        
        # Test that defaults match phyloland
        result = PLD_interface(tree_file, data_file, num_step=50, ess_lim=1)
        
        # Should run with phyloland defaults
        assert result is not None
        assert 'mcmc' in result
        
    def test_pld_interface_output_format(self, temp_files):
        """Test output format matches phyloland structure"""
        tree_file, data_file, temp_dir = temp_files
        
        result = PLD_interface(tree_file, data_file, num_step=50, ess_lim=1)
        
        # Test phyloland-compatible structure
        expected_keys = ['sigma1', 'sigma2', 'lambda', 'Lambda', 'likelihood',
                        'trees', 'locations', 'tips', 'space', 'mcmc']
        
        for key in expected_keys:
            assert key in result, f"Missing key: {key}"
            
        # Test parameter arrays have samples
        if result['mcmc']['n_samples'] > 0:
            assert len(result['sigma1']) > 0
            assert len(result['sigma2']) > 0
            assert len(result['lambda']) > 0
            assert len(result['Lambda']) > 0
            
    def test_pld_interface_species_names(self, temp_files):
        """Test species name handling"""
        tree_file, data_file, temp_dir = temp_files
        
        result = PLD_interface(tree_file, data_file, num_step=50, ess_lim=1)
        
        # Should have species information
        assert 'tips' in result
        assert len(result['tips']) == 4  # A, B, C, D from test data
        assert 'A' in result['tips']
        assert 'B' in result['tips']
        assert 'C' in result['tips']
        assert 'D' in result['tips']
        
    def test_pld_interface_convergence_reporting(self, temp_files):
        """Test convergence reporting"""
        tree_file, data_file, temp_dir = temp_files
        
        result = PLD_interface(tree_file, data_file, num_step=200, ess_lim=10)
        
        # Should report convergence status
        assert 'converged' in result['mcmc']
        assert isinstance(result['mcmc']['converged'], bool)
        
    def test_pld_interface_parameter_estimation(self, temp_files):
        """Test parameter estimation produces reasonable values"""
        tree_file, data_file, temp_dir = temp_files
        
        result = PLD_interface(tree_file, data_file, num_step=100, ess_lim=5)
        
        if result['mcmc']['n_samples'] > 0:
            # Parameters should be positive
            assert np.all(result['sigma1'] > 0)
            assert np.all(result['sigma2'] > 0) 
            assert np.all(result['lambda'] > 0)
            assert np.all(result['Lambda'] > 0)
            
            # Should have reasonable ranges
            assert np.median(result['sigma1']) > 0.01
            assert np.median(result['sigma2']) > 0.01
            assert np.median(result['lambda']) > 0.01
            assert np.median(result['Lambda']) > 0.01

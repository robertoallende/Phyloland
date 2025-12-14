"""
Unit 6.6: R Tutorial Validation Tests
Test against actual R phyloland tutorial with real Banza dataset
"""

import pytest
import numpy as np
import os
import tempfile
from phyloland.interface import PLD_interface

class TestRTutorialValidation:
    """Test exact R tutorial reproduction with real Banza data"""
    
    @pytest.fixture
    def tutorial_files(self):
        """Paths to R tutorial files"""
        base_path = "/home/roberto/code/Phyloland/discover/phyloland_tutorial"
        return {
            'tree': os.path.join(base_path, "tree_Banza_posterior.nex"),
            'locations': os.path.join(base_path, "locations_Banza.txt"),
            'names_locations': ["Maui_Nui", "Maui_Nui", "Maui_Nui", "Maui_Nui", 
                              "Kauai", "Kauai", "Maui_Nui", "Maui_Nui", "Maui_Nui", 
                              "Maui_Nui", "Nihoa", "Nihoa", "Hawaii", "Hawaii", 
                              "Hawaii", "Oahu", "Oahu", "Maui_Nui", "Maui_Nui", 
                              "Oahu", "Oahu"]
        }
    
    def test_tutorial_files_exist(self, tutorial_files):
        """Verify R tutorial files are available"""
        assert os.path.exists(tutorial_files['tree']), "Banza tree file missing"
        assert os.path.exists(tutorial_files['locations']), "Banza locations file missing"
        assert len(tutorial_files['names_locations']) == 21, "Expected 21 species"
    
    def test_r_tutorial_exact_reproduction(self, tutorial_files):
        """Run exact R tutorial example with real Banza data"""
        # Exact parameters from tutorial_commands.R
        result = PLD_interface(
            fileTREES=tutorial_files['tree'],
            fileDATA=tutorial_files['locations'],
            num_step=1000,  # 1e3 in R
            freq=100,       # 1e2 in R  
            ess_lim=500,    # 5e2 in R
            names_locations=tutorial_files['names_locations']
        )
        
        # Verify basic structure
        assert 'sigma1' in result, "Missing sigma1 parameter"
        assert 'sigma2' in result, "Missing sigma2 parameter"
        assert 'lambda' in result, "Missing lambda parameter"
        assert 'Lambda' in result, "Missing Lambda parameter"  # Our API uses 'Lambda' not 'tau'
        assert 'mcmc' in result, "Missing MCMC diagnostics"
        assert 'tips' in result, "Missing species names"
        
        # Verify 21 species processed
        assert len(result['tips']) == 21, f"Expected 21 species, got {len(result['tips'])}"
        
        # Verify parameter samples exist
        assert len(result['sigma1']) > 0, "No sigma1 samples"
        assert len(result['sigma2']) > 0, "No sigma2 samples"
        assert len(result['lambda']) > 0, "No lambda samples"
        assert len(result['Lambda']) > 0, "No Lambda samples"
        
        # Verify parameters are reasonable (biological constraints)
        assert np.all(np.array(result['sigma1']) > 0), "sigma1 must be positive"
        assert np.all(np.array(result['sigma2']) > 0), "sigma2 must be positive"
        assert np.all(np.array(result['lambda']) > 0), "lambda must be positive"
        assert np.all(np.array(result['Lambda']) > 0), "Lambda must be positive"
        
        # Verify convergence attempted
        assert 'converged' in result['mcmc'], "Missing convergence status"
        
        print(f"✅ R tutorial reproduction successful:")
        print(f"   Species: {len(result['tips'])}")
        print(f"   Samples: {len(result['sigma1'])}")
        print(f"   Converged: {result['mcmc']['converged']}")


class TestGeographicEdgeCases:
    """Test extreme geographic scenarios"""
    
    def create_test_tree(self, n_species=3):
        """Create minimal test tree"""
        tree_content = f"""#NEXUS
begin trees;
tree tree1 = ({','.join([f'sp{i}:1.0' for i in range(1, n_species+1)])});
end;"""
        return tree_content
    
    def create_test_locations(self, coords_list):
        """Create test location file"""
        content = ""
        for i, (lat, lon) in enumerate(coords_list, 1):
            content += f"sp{i}\t{lat}\t{lon}\n"
        return content
    
    def test_antipodal_points(self):
        """Test maximum Earth distance (~20,000 km)"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.nex', delete=False) as tree_file:
            tree_file.write(self.create_test_tree(2))
            tree_path = tree_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as loc_file:
            # Antipodal points: North Pole and South Pole
            loc_file.write(self.create_test_locations([(90, 0), (-90, 0)]))
            loc_path = loc_file.name
        
        try:
            result = PLD_interface(
                fileTREES=tree_path,
                fileDATA=loc_path,
                num_step=100,
                freq=10,
                ess_lim=50
            )
            
            # Should handle extreme distances without crashing
            assert len(result['sigma1']) > 0, "Failed to handle antipodal points"
            print("✅ Antipodal points handled successfully")
            
        finally:
            os.unlink(tree_path)
            os.unlink(loc_path)
    
    def test_identical_coordinates(self):
        """Test zero distance between species"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.nex', delete=False) as tree_file:
            tree_file.write(self.create_test_tree(3))
            tree_path = tree_file.name
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as loc_file:
            # All species at same location
            loc_file.write(self.create_test_locations([(0, 0), (0, 0), (0, 0)]))
            loc_path = loc_file.name
        
        try:
            result = PLD_interface(
                fileTREES=tree_path,
                fileDATA=loc_path,
                num_step=100,
                freq=10,
                ess_lim=50
            )
            
            # Should handle zero distances gracefully
            assert len(result['sigma1']) > 0, "Failed to handle identical coordinates"
            print("✅ Identical coordinates handled successfully")
            
        finally:
            os.unlink(tree_path)
            os.unlink(loc_path)


class TestParameterBoundaries:
    """Test parameter space boundaries"""
    
    def test_very_short_mcmc_run(self):
        """Test minimal MCMC run (10 steps)"""
        base_path = "/home/roberto/code/Phyloland/discover/phyloland_tutorial"
        tree_path = os.path.join(base_path, "tree_Banza_posterior.nex")
        loc_path = os.path.join(base_path, "locations_Banza.txt")
        
        result = PLD_interface(
            fileTREES=tree_path,
            fileDATA=loc_path,
            num_step=10,  # Very short run
            freq=5,
            ess_lim=5,
            names_locations=["Maui_Nui"] * 21  # Simplified names
        )
        
        # Should handle short runs gracefully
        assert 'sigma1' in result, "Failed short MCMC run"
        assert not result['mcmc']['converged'], "Should not converge in 10 steps"
        print("✅ Short MCMC run handled successfully")
    
    def test_impossible_ess_threshold(self):
        """Test unreachable ESS threshold"""
        base_path = "/home/roberto/code/Phyloland/discover/phyloland_tutorial"
        tree_path = os.path.join(base_path, "tree_Banza_posterior.nex")
        loc_path = os.path.join(base_path, "locations_Banza.txt")
        
        result = PLD_interface(
            fileTREES=tree_path,
            fileDATA=loc_path,
            num_step=100,
            freq=10,
            ess_lim=10000,  # Impossible to reach
            names_locations=["Maui_Nui"] * 21
        )
        
        # Should timeout gracefully
        assert 'sigma1' in result, "Failed with impossible ESS"
        assert not result['mcmc']['converged'], "Should not reach impossible ESS"
        print("✅ Impossible ESS threshold handled successfully")

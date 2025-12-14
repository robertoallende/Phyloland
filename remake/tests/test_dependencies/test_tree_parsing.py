"""Test tree parsing validation: DendroPy vs R ape."""

import pytest
import pandas as pd
import numpy as np
import dendropy
from pathlib import Path


@pytest.fixture
def tree_file(test_data_dir):
    """Path to Banza tree file."""
    return test_data_dir / "banza" / "tree_Banza.nex"


@pytest.fixture
def r_reference(reference_data_dir):
    """Load R reference data for tree parsing."""
    return {
        'properties': pd.read_csv(reference_data_dir / "tree_properties.csv"),
        'tip_names': pd.read_csv(reference_data_dir / "tree_tip_names.csv"),
        'edges': pd.read_csv(reference_data_dir / "tree_edges.csv")
    }


@pytest.fixture
def python_tree(tree_file):
    """Load tree with DendroPy."""
    return dendropy.Tree.get(path=str(tree_file), schema="nexus")


def test_tree_loads_successfully(python_tree):
    """Test that DendroPy can load the Banza tree without errors."""
    assert python_tree is not None
    assert isinstance(python_tree, dendropy.Tree)


def test_basic_tree_properties(python_tree, r_reference):
    """Test basic tree structure matches R ape."""
    props = r_reference['properties'].set_index('property')['value']
    
    # Number of tips
    assert len(python_tree.leaf_nodes()) == props['n_tips']
    
    # Number of internal nodes (use correct DendroPy method)
    internal_nodes = [node for node in python_tree.internal_nodes()]
    assert len(internal_nodes) == props['n_nodes']
    
    # Total number of edges (DendroPy includes root edge, R doesn't)
    python_edges = [e for e in python_tree.edges() if e.length is not None]
    assert len(python_edges) == props['node_count']


def test_tip_names_consistency(python_tree, r_reference):
    """Test tip names match exactly between DendroPy and R ape."""
    # Get Python tip names (sorted for consistency)
    python_tips = sorted([node.taxon.label for node in python_tree.leaf_nodes()])
    
    # Get R tip names (already sorted in reference)
    r_tips = sorted(r_reference['tip_names']['tip_name'].tolist())
    
    assert python_tips == r_tips
    assert len(python_tips) == len(r_tips)


def test_branch_lengths_precision(python_tree, r_reference):
    """Test branch lengths match within tolerance."""
    # Get Python edge lengths
    python_lengths = [edge.length for edge in python_tree.edges() if edge.length is not None]
    python_lengths = sorted(python_lengths)
    
    # Get R edge lengths
    r_lengths = sorted(r_reference['edges']['length'].tolist())
    
    # Compare lengths with high precision tolerance
    np.testing.assert_allclose(python_lengths, r_lengths, rtol=1e-10, atol=1e-10)


def test_total_tree_length(python_tree, r_reference):
    """Test total tree length matches R calculation."""
    props = r_reference['properties'].set_index('property')['value']
    
    # Calculate Python total tree length
    python_total = sum(edge.length for edge in python_tree.edges() if edge.length is not None)
    
    # Compare with R total
    r_total = props['tree_length']
    
    np.testing.assert_allclose(python_total, r_total, rtol=1e-10, atol=1e-10)


def test_tree_structure_integrity(python_tree):
    """Test tree structure is valid and consistent."""
    # Tree should be rooted
    assert python_tree.seed_node is not None
    
    # All leaf nodes should have taxa
    leaf_nodes = python_tree.leaf_nodes()
    assert all(node.taxon is not None for node in leaf_nodes)
    
    # All internal nodes should have children
    internal_nodes = python_tree.internal_nodes()
    assert all(len(node.child_nodes()) >= 2 for node in internal_nodes)
    
    # Tree should be connected
    assert python_tree.is_rooted


def test_edge_consistency(python_tree, r_reference):
    """Test edge structure consistency."""
    # DendroPy includes root edge (length=None), R doesn't
    python_edges_with_length = [e for e in python_tree.edges() if e.length is not None]
    r_edge_count = len(r_reference['edges'])
    
    assert len(python_edges_with_length) == r_edge_count
    
    # All meaningful edges should have valid lengths
    assert all(edge.length is not None for edge in python_edges_with_length)
    assert all(edge.length > 0 for edge in python_edges_with_length)

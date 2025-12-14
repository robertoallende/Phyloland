"""Test geographic distance validation: Python vs R distkm."""

import pytest
import pandas as pd
import numpy as np
from math import radians, sin, cos, acos, pi


def distkm_python(lat1, lat2, lon1, lon2):
    """
    Python implementation of R distkm function.
    Exact translation of C code from Phyloland.
    """
    lat1r = (lat1/180) * pi
    lat2r = (lat2/180) * pi
    lon1r = (lon1/180) * pi
    lon2r = (lon2/180) * pi
    
    # Handle potential numerical issues with acos
    cos_angle = sin(lat1r)*sin(lat2r) + cos(lat1r)*cos(lat2r)*cos(lon2r-lon1r)
    cos_angle = max(-1.0, min(1.0, cos_angle))  # Clamp to [-1, 1]
    
    d = acos(cos_angle) * 6378.137
    return d


@pytest.fixture
def distance_coordinates(reference_data_dir):
    """Load test coordinates."""
    return pd.read_csv(reference_data_dir / "distance_coordinates.csv")


@pytest.fixture
def distance_matrix(reference_data_dir):
    """Load R reference distance matrix."""
    return pd.read_csv(reference_data_dir / "distance_matrix.csv")


def test_distance_function_exists():
    """Test that our Python distance function works."""
    # Basic functionality test
    distance = distkm_python(0, 0, 0, 0)
    assert distance == 0.0
    
    # Non-zero distance test
    distance = distkm_python(0, 1, 0, 0)
    assert distance > 0


def test_hawaiian_island_distances(distance_matrix):
    """Test distances between Hawaiian islands match R distkm."""
    # Filter for Hawaiian island pairs
    hawaiian_names = ["Oahu", "Maui", "Hawaii", "Kauai", "Molokai"]
    hawaiian_pairs = distance_matrix[
        distance_matrix['from_name'].isin(hawaiian_names) & 
        distance_matrix['to_name'].isin(hawaiian_names)
    ]
    
    tolerance_km = 0.001  # 1 meter tolerance
    
    for _, row in hawaiian_pairs.iterrows():
        python_distance = distkm_python(
            row['from_lat'], row['to_lat'], 
            row['from_lon'], row['to_lon']
        )
        r_distance = row['distance_km']
        
        assert abs(python_distance - r_distance) < tolerance_km, \
            f"Distance {row['from_name']} to {row['to_name']}: " \
            f"Python={python_distance:.6f}, R={r_distance:.6f}, " \
            f"diff={abs(python_distance - r_distance):.6f}"


def test_zero_distance_same_points(distance_coordinates):
    """Test that distance from point to itself is zero."""
    for _, coord in distance_coordinates.iterrows():
        distance = distkm_python(coord['lat'], coord['lat'], coord['lon'], coord['lon'])
        assert distance == 0.0, f"Same point distance should be 0 for {coord['name']}"


def test_distance_symmetry(distance_coordinates):
    """Test that distance(A,B) == distance(B,A)."""
    coords = distance_coordinates.head(5)  # Test first 5 points
    
    for i, coord1 in coords.iterrows():
        for j, coord2 in coords.iterrows():
            if i != j:
                dist_ab = distkm_python(coord1['lat'], coord2['lat'], coord1['lon'], coord2['lon'])
                dist_ba = distkm_python(coord2['lat'], coord1['lat'], coord2['lon'], coord1['lon'])
                
                assert abs(dist_ab - dist_ba) < 1e-10, \
                    f"Distance symmetry failed: {coord1['name']} to {coord2['name']}"


def test_edge_case_distances(distance_matrix):
    """Test edge cases: equator, antimeridian, poles."""
    edge_cases = {
        ("Equator1", "Equator2"): "Equator crossing",
        ("Antimeridian1", "Antimeridian2"): "Antimeridian crossing", 
        ("Pole1", "Pole2"): "Polar regions",
        ("Close1", "Close2"): "Very close points"
    }
    
    tolerance_km = 0.001  # 1 meter tolerance
    
    for (from_name, to_name), description in edge_cases.items():
        # Find the reference distance
        ref_row = distance_matrix[
            (distance_matrix['from_name'] == from_name) & 
            (distance_matrix['to_name'] == to_name)
        ]
        
        if not ref_row.empty:
            row = ref_row.iloc[0]
            python_distance = distkm_python(
                row['from_lat'], row['to_lat'],
                row['from_lon'], row['to_lon']
            )
            r_distance = row['distance_km']
            
            assert abs(python_distance - r_distance) < tolerance_km, \
                f"{description}: Python={python_distance:.6f}, R={r_distance:.6f}"


def test_all_reference_distances(distance_matrix):
    """Test all reference distances match within tolerance."""
    tolerance_km = 0.001  # 1 meter tolerance
    failures = []
    
    for _, row in distance_matrix.iterrows():
        python_distance = distkm_python(
            row['from_lat'], row['to_lat'],
            row['from_lon'], row['to_lon']
        )
        r_distance = row['distance_km']
        diff = abs(python_distance - r_distance)
        
        if diff >= tolerance_km:
            failures.append({
                'from': row['from_name'],
                'to': row['to_name'],
                'python': python_distance,
                'r': r_distance,
                'diff': diff
            })
    
    assert len(failures) == 0, f"Failed {len(failures)} distance validations: {failures[:5]}"


def test_distance_precision():
    """Test precision with very close points."""
    # Very close points (about 14 meters apart)
    lat1, lon1 = 45.5000, -122.5000
    lat2, lon2 = 45.5001, -122.5001
    
    distance = distkm_python(lat1, lat2, lon1, lon2)
    
    # Should be small but non-zero
    assert 0 < distance < 1.0, f"Very close points distance: {distance} km"


def test_maximum_distance():
    """Test maximum possible distance (antipodal points)."""
    # Approximately antipodal points
    distance = distkm_python(0, 0, 0, 180)
    
    # Should be close to half Earth's circumference
    expected_max = pi * 6378.137  # Half circumference
    assert abs(distance - expected_max) < 1.0, \
        f"Maximum distance: {distance}, expected ~{expected_max}"


def test_coordinate_validation():
    """Test handling of extreme coordinates."""
    # Test poles
    north_pole_dist = distkm_python(90, 89, 0, 0)
    assert north_pole_dist > 0
    
    # Test equator
    equator_dist = distkm_python(0, 0, 0, 1)
    assert equator_dist > 0
    
    # Test antimeridian
    antimeridian_dist = distkm_python(0, 0, 179, -179)
    assert antimeridian_dist > 0

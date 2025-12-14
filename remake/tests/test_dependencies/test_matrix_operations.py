"""Test NumPy matrix operations equivalence to R matrix operations"""

import numpy as np
import pandas as pd
from pathlib import Path

# Load reference data
TEST_DATA_DIR = Path(__file__).parent.parent.parent.parent / "test_data"
matrix_A = pd.read_csv(TEST_DATA_DIR / "reference" / "matrix_A.csv").values
matrix_B = pd.read_csv(TEST_DATA_DIR / "reference" / "matrix_B.csv").values
r_multiply = pd.read_csv(TEST_DATA_DIR / "reference" / "matrix_multiply.csv").values
r_transpose = pd.read_csv(TEST_DATA_DIR / "reference" / "matrix_transpose.csv").values
r_inverse = pd.read_csv(TEST_DATA_DIR / "reference" / "matrix_inverse.csv").values
r_scalars = pd.read_csv(TEST_DATA_DIR / "reference" / "matrix_scalars.csv")
r_eigenvals = pd.read_csv(TEST_DATA_DIR / "reference" / "matrix_eigenvalues.csv")["eigenvalue"].values

def test_matrix_multiplication():
    """Test NumPy @ operator matches R %*%"""
    py_multiply = matrix_A @ matrix_B
    np.testing.assert_allclose(py_multiply, r_multiply, rtol=1e-12)

def test_matrix_transpose():
    """Test NumPy .T matches R t()"""
    py_transpose = matrix_A.T
    np.testing.assert_allclose(py_transpose, r_transpose, rtol=1e-12)

def test_matrix_inverse():
    """Test np.linalg.inv matches R solve()"""
    py_inverse = np.linalg.inv(matrix_A)
    np.testing.assert_allclose(py_inverse, r_inverse, rtol=1e-9)

def test_matrix_determinant():
    """Test np.linalg.det matches R det()"""
    py_det = np.linalg.det(matrix_A)
    r_det = r_scalars[r_scalars["operation"] == "determinant"]["result"].iloc[0]
    np.testing.assert_allclose(py_det, r_det, rtol=1e-9)

def test_eigenvalue_computation():
    """Test np.linalg.eig matches R eigen() (real parts)"""
    py_eigenvals, _ = np.linalg.eig(matrix_A)
    py_eigenvals_real = np.real(py_eigenvals)
    
    # Sort both arrays for comparison (eigenvalue order may differ)
    py_sorted = np.sort(py_eigenvals_real)
    r_sorted = np.sort(r_eigenvals)
    
    np.testing.assert_allclose(py_sorted, r_sorted, rtol=1e-9)

def test_matrix_properties():
    """Test basic matrix properties are preserved"""
    # Test matrix shapes
    assert matrix_A.shape == (5, 5)
    assert matrix_B.shape == (5, 5)
    
    # Test that A @ inv(A) ≈ I (relaxed tolerance for numerical stability)
    A_inv = np.linalg.inv(matrix_A)
    identity_test = matrix_A @ A_inv
    expected_identity = np.eye(5)
    np.testing.assert_allclose(identity_test, expected_identity, rtol=1e-9, atol=1e-10)

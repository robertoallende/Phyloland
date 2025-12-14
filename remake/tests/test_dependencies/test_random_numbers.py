"""Test NumPy RNG statistical equivalence to R RNG"""

import numpy as np
import pandas as pd
from scipy import stats
import pytest
from pathlib import Path

# Load R reference statistics
TEST_DATA_DIR = Path(__file__).parent.parent.parent.parent / "test_data"
reference_stats = pd.read_csv(TEST_DATA_DIR / "reference" / "rng_statistics.csv")

def skewness(x):
    """Calculate skewness (same formula as R)"""
    n = len(x)
    m = np.mean(x)
    s = np.std(x, ddof=1)  # R uses n-1 denominator
    return np.sum(((x - m) / s)**3) / n

def kurtosis(x):
    """Calculate excess kurtosis (same formula as R)"""
    n = len(x)
    m = np.mean(x)
    s = np.std(x, ddof=1)  # R uses n-1 denominator
    return np.sum(((x - m) / s)**4) / n - 3

def calc_stats(x):
    """Calculate same statistics as R reference"""
    return {
        'n': len(x),
        'mean': np.mean(x),
        'variance': np.var(x, ddof=1),  # R uses n-1 denominator
        'skewness': skewness(x),
        'kurtosis': kurtosis(x),
        'q05': np.percentile(x, 5),
        'q25': np.percentile(x, 25),
        'q50': np.percentile(x, 50),
        'q75': np.percentile(x, 75),
        'q95': np.percentile(x, 95)
    }

@pytest.fixture
def rng_samples():
    """Generate NumPy samples with same seed as R"""
    np.random.seed(12345)
    return {
        'uniform': np.random.uniform(0, 1, 10000),
        'normal': np.random.normal(0, 1, 10000),
        'exponential': np.random.exponential(1, 10000)
    }

def test_uniform_statistical_properties(rng_samples):
    """Test NumPy uniform has same statistical properties as R runif"""
    r_stats = reference_stats[reference_stats['distribution'] == 'uniform'].iloc[0]
    py_stats = calc_stats(rng_samples['uniform'])
    
    # 5% tolerance for different RNG algorithms
    assert abs(py_stats['mean'] - r_stats['mean']) / r_stats['mean'] < 0.05
    assert abs(py_stats['variance'] - r_stats['variance']) / r_stats['variance'] < 0.05

def test_normal_statistical_properties(rng_samples):
    """Test NumPy normal has same statistical properties as R rnorm"""
    r_stats = reference_stats[reference_stats['distribution'] == 'normal'].iloc[0]
    py_stats = calc_stats(rng_samples['normal'])
    
    # 5% tolerance for different RNG algorithms
    assert abs(py_stats['mean'] - r_stats['mean']) < 0.05  # Absolute for mean near 0
    assert abs(py_stats['variance'] - r_stats['variance']) / r_stats['variance'] < 0.05

def test_exponential_statistical_properties(rng_samples):
    """Test NumPy exponential has same statistical properties as R rexp"""
    r_stats = reference_stats[reference_stats['distribution'] == 'exponential'].iloc[0]
    py_stats = calc_stats(rng_samples['exponential'])
    
    # 5% tolerance for different RNG algorithms
    assert abs(py_stats['mean'] - r_stats['mean']) / r_stats['mean'] < 0.05
    assert abs(py_stats['variance'] - r_stats['variance']) / r_stats['variance'] < 0.05

def test_distribution_shapes(rng_samples):
    """Test distribution shapes using Kolmogorov-Smirnov tests"""
    # Test against theoretical distributions (not R samples)
    
    # Uniform should be uniform
    ks_stat, p_value = stats.kstest(rng_samples['uniform'], 'uniform')
    assert p_value > 0.05, f"Uniform KS test failed: p={p_value}"
    
    # Normal should be normal
    ks_stat, p_value = stats.kstest(rng_samples['normal'], 'norm')
    assert p_value > 0.05, f"Normal KS test failed: p={p_value}"
    
    # Exponential should be exponential
    ks_stat, p_value = stats.kstest(rng_samples['exponential'], 'expon')
    assert p_value > 0.05, f"Exponential KS test failed: p={p_value}"

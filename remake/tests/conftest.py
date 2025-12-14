"""Pytest configuration and shared fixtures for Phyloland tests."""

import pytest
import os
from pathlib import Path

# Test data directory (shared between R and Python)
TEST_DATA_DIR = Path(__file__).parent.parent.parent / "test_data"

@pytest.fixture
def test_data_dir():
    """Path to shared test data directory."""
    return TEST_DATA_DIR

@pytest.fixture
def banza_data_dir():
    """Path to Banza dataset directory."""
    return TEST_DATA_DIR / "banza"

@pytest.fixture
def reference_data_dir():
    """Path to R reference outputs directory."""
    return TEST_DATA_DIR / "reference"

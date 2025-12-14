# Testing Strategy for Python Implementation

## Overview

Since Phyloland is an **input → processing → output** algorithm, we can generate diverse test cases, run them through the R implementation to get "ground truth" results, then validate our Python implementation against these references.

## Testing Approach

### 1. Reference Implementation Testing
**Strategy**: Use R package as oracle for correctness validation
- Generate synthetic datasets with varying complexity
- Run through R implementation to get expected outputs
- Compare Python results against R "ground truth"
- Ensure identical results within numerical precision

### 2. Component-Level Testing
**Strategy**: Test individual functions in isolation
- Geographic distance calculations
- Dispersal kernel computations
- Rate matrix construction
- Likelihood calculations

### 3. Integration Testing
**Strategy**: End-to-end workflow validation
- Complete MCMC runs on test datasets
- Parameter recovery from simulated data
- Convergence behavior comparison

## Test Data Generation Strategy

### Synthetic Tree Generation
```python
def generate_test_tree(n_tips, tree_type="balanced"):
    """
    Generate phylogenetic trees with known properties
    - Balanced trees (equal branch lengths)
    - Imbalanced trees (realistic diversification)
    - Star trees (minimal phylogenetic signal)
    - Ladder trees (maximum imbalance)
    """
```

### Geographic Layout Patterns
```python
def generate_locations(n_locations, pattern="random"):
    """
    Create geographic coordinate sets
    - Random: Uniform distribution
    - Clustered: Groups of nearby locations
    - Linear: Island chain-like arrangement
    - Grid: Regular spacing
    - Realistic: Based on actual archipelagos
    """
```

### Parameter Combinations
```python
def generate_parameter_sets():
    """
    Systematic parameter exploration
    - Competition: λ ∈ [0.1, 0.5, 1.0, 2.0, 5.0]
    - Dispersal rate: Λ ∈ [0.1, 1.0, 10.0]
    - Dispersal bias: σ ∈ [low, medium, high bias]
    """
```

## Test Case Categories

### 1. Minimal Cases (Unit Testing)
**Purpose**: Test basic functionality with simple inputs

#### Single Dispersal Event
- **Tree**: 3 tips, 1 internal node
- **Locations**: 2 sites
- **Expected**: Simple likelihood calculation

#### No Competition (λ = 1)
- **Tree**: Small balanced tree
- **Locations**: Multiple sites, some unoccupied
- **Expected**: Neutral dispersal patterns

#### Perfect Competition (λ → 0)
- **Tree**: Any structure
- **Locations**: All occupied
- **Expected**: No secondary colonization

### 2. Intermediate Cases (Integration Testing)
**Purpose**: Test realistic scenarios with moderate complexity

#### Island Chain Scenario
- **Tree**: 10-20 tips
- **Locations**: Linear arrangement (5-10 islands)
- **Parameters**: Moderate competition, distance bias
- **Expected**: Stepping-stone colonization pattern

#### Archipelago Scenario
- **Tree**: 15-30 tips
- **Locations**: Clustered arrangement
- **Parameters**: Variable competition levels
- **Expected**: Within-cluster vs between-cluster patterns

### 3. Complex Cases (System Testing)
**Purpose**: Test full system with realistic complexity

#### Banza-like Dataset
- **Tree**: 20+ tips with realistic branch lengths
- **Locations**: Hawaiian island coordinates
- **Parameters**: Literature-based priors
- **Expected**: Match published results

#### Large-scale Simulation
- **Tree**: 50+ tips
- **Locations**: 20+ sites
- **Parameters**: Full parameter space exploration
- **Expected**: Convergence and parameter recovery

## Test Data Generation Workflow

### Step 1: Generate Test Suite
```bash
# R script to generate reference datasets
Rscript generate_test_data.R --n_cases 100 --output_dir test_data/
```

### Step 2: Run R Reference
```bash
# Process each test case through R implementation
for case in test_data/*.json; do
    Rscript run_phyloland_reference.R --input $case --output ${case%.json}_reference.csv
done
```

### Step 3: Python Validation
```python
# Compare Python results against R reference
def validate_against_reference(test_case, python_result, r_reference):
    assert_parameter_estimates_close(python_result.lambda, r_reference.lambda, rtol=1e-3)
    assert_likelihood_close(python_result.likelihood, r_reference.likelihood, rtol=1e-6)
    assert_mcmc_convergence_similar(python_result.traces, r_reference.traces)
```

## Validation Metrics

### Parameter Estimation Accuracy
- **Relative error**: `|python_estimate - r_estimate| / |r_estimate|`
- **Bias**: Systematic over/under-estimation
- **Precision**: Consistency across multiple runs

### Likelihood Calculation Precision
- **Absolute difference**: For numerical stability testing
- **Relative difference**: For scale-independent comparison
- **Convergence**: Final likelihood values should match

### MCMC Performance
- **Effective Sample Size (ESS)**: Should be similar between implementations
- **Acceptance rates**: Proposal tuning effectiveness
- **Convergence time**: Burn-in period comparison

## Test Implementation Structure

### Test Data Organization
```
test_data/
├── minimal/           # Simple cases for unit testing
│   ├── case_001.json  # Tree + locations + parameters
│   ├── case_001_r.csv # R reference results
│   └── ...
├── intermediate/      # Moderate complexity
│   └── ...
├── complex/          # Full system tests
│   └── ...
└── banza/           # Real data validation
    └── ...
```

### Automated Test Suite
```python
class TestPhylolandImplementation:
    def test_minimal_cases(self):
        """Test basic functionality"""
        
    def test_parameter_recovery(self):
        """Test with known simulation parameters"""
        
    def test_banza_reproduction(self):
        """Reproduce published Banza results"""
        
    def test_edge_cases(self):
        """Test boundary conditions and error handling"""
```

## Continuous Validation

### Regression Testing
- **Baseline**: Establish reference results for standard test cases
- **Monitoring**: Detect when changes break existing functionality
- **Performance**: Track computational efficiency over time

### Cross-Platform Testing
- **Operating systems**: Linux, macOS, Windows
- **Python versions**: 3.8, 3.9, 3.10, 3.11
- **Dependency versions**: NumPy, SciPy version compatibility

## Expected Challenges & Solutions

### Numerical Precision Differences
- **Problem**: Floating-point arithmetic varies between R and Python
- **Solution**: Use relative tolerances, focus on biological significance

### Random Number Generation
- **Problem**: Different RNG algorithms produce different sequences
- **Solution**: Test statistical properties rather than exact sequences

### MCMC Stochasticity
- **Problem**: MCMC results vary between runs
- **Solution**: Test convergence properties and parameter distributions

### Performance Differences
- **Problem**: Python may be slower than R+C implementation
- **Solution**: Focus on correctness first, optimize later with profiling

This testing strategy ensures the Python implementation maintains scientific accuracy while providing comprehensive validation against the established R reference implementation.

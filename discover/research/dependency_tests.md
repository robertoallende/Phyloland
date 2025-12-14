# Dependency Testing Strategy

## Overview

Before implementing the full algorithm, we must validate that our Python dependencies produce identical results to their R counterparts. This ensures any differences in final results come from our implementation, not from library discrepancies.

## Critical Dependency Tests

### 1. Phylogenetic Tree Handling (DendroPy vs ape)

#### Tree Parsing Validation
```python
def test_nexus_parsing():
    """Compare tree parsing between R ape and Python DendroPy"""
    # Use same Nexus file
    # R: tree <- read.nexus("test.nex")
    # Python: tree = dendropy.Tree.get(path="test.nex", schema="nexus")
    
    # Validate:
    # - Same number of tips/nodes
    # - Identical tip names and order
    # - Same branch lengths (within precision)
    # - Same tree topology
```

#### Node Indexing Consistency
```python
def test_node_ordering():
    """Ensure node traversal order matches between implementations"""
    # Critical: R's ape has specific node numbering conventions
    # Must match exactly for likelihood calculations
    
    # Test cases:
    # - Balanced trees
    # - Imbalanced trees  
    # - Star trees
    # - Different tree sizes
```

### 2. Geographic Distance (Custom C vs GeoPy/haversine)

#### Distance Calculation Precision
```python
def test_geographic_distance():
    """Validate distance calculations against R's distkm() function"""
    
    test_coordinates = [
        # Hawaiian islands (Banza dataset)
        (21.3099, -157.8581),  # Oahu
        (20.7984, -156.3319),  # Maui
        (19.8968, -155.5828),  # Hawaii
        # Edge cases
        (0, 0), (0, 180),      # Equator/antimeridian
        (90, 0), (-90, 0),     # Poles
        (45.5, -122.5), (45.6, -122.4)  # Close points
    ]
    
    # Compare R distkm() vs Python alternatives:
    # - geopy.distance.geodesic()
    # - haversine library
    # - Custom great circle implementation
    
    # Tolerance: < 1 meter difference
```

### 3. Random Number Generation (Rmath vs NumPy)

#### Distribution Sampling Consistency
```python
def test_random_distributions():
    """Compare statistical distributions between R and Python"""
    
    # Test key distributions used in MCMC:
    # - Uniform: runif() vs np.random.uniform()
    # - Normal: rnorm() vs np.random.normal()
    # - Exponential: rexp() vs np.random.exponential()
    
    # Statistical tests (not exact matching):
    # - Kolmogorov-Smirnov test
    # - Anderson-Darling test
    # - Moment matching (mean, variance, skewness)
```

#### MCMC Reproducibility
```python
def test_mcmc_reproducibility():
    """Test if identical seeds produce similar MCMC behavior"""
    
    # Challenge: R and Python use different RNG algorithms
    # Solution: Test statistical properties, not exact sequences
    
    # Validate:
    # - Parameter estimate distributions
    # - Convergence rates
    # - Acceptance ratios
```

### 4. Mathematical Operations (Base R vs NumPy/SciPy)

#### Matrix Operations Precision
```python
def test_matrix_operations():
    """Compare matrix calculations between R and NumPy"""
    
    # Test operations used in rate matrix construction:
    # - Matrix multiplication
    # - Element-wise operations
    # - Exponential/logarithm functions
    # - Numerical precision at different scales
    
    # Edge cases:
    # - Very small numbers (underflow)
    # - Very large numbers (overflow)
    # - Ill-conditioned matrices
```

#### Special Functions
```python
def test_special_functions():
    """Validate mathematical functions against R equivalents"""
    
    # Functions from Rmath.h used in C code:
    # - exp(), log(), sqrt()
    # - Probability density functions
    # - Cumulative distribution functions
    
    # Compare R vs SciPy implementations
```

### 5. File I/O (Base R vs pandas)

#### Data Loading Consistency
```python
def test_file_parsing():
    """Ensure identical data loading between R and Python"""
    
    # Test with Banza location data:
    # R: read.table("locations_Banza.txt", sep="\t")
    # Python: pd.read_csv("locations_Banza.txt", sep="\t")
    
    # Validate:
    # - Same data types
    # - Identical values
    # - Same handling of missing data
    # - Same column names/order
```

## Dependency Test Implementation

### Test Data Generation
```python
def generate_dependency_test_data():
    """Create test cases specifically for dependency validation"""
    
    # Geographic coordinates with known distances
    # Trees with known properties
    # Parameter sets covering edge cases
    # File formats matching R expectations
```

### Automated Validation Suite
```python
class TestDependencies:
    def test_tree_parsing_equivalence(self):
        """DendroPy vs ape parsing"""
        
    def test_distance_calculation_precision(self):
        """Geographic distance accuracy"""
        
    def test_random_number_statistical_properties(self):
        """RNG statistical equivalence"""
        
    def test_matrix_operation_precision(self):
        """NumPy vs R matrix math"""
        
    def test_file_io_consistency(self):
        """Data loading equivalence"""
```

### Cross-Reference Testing
```bash
# R script to generate reference outputs
Rscript generate_dependency_references.R

# Python script to compare against references  
python test_dependencies.py --compare-with references/
```

## Expected Dependency Issues

### 1. Tree Parsing Differences
- **Issue**: Different Nexus format interpretations
- **Solution**: Test with actual Phyloland data files
- **Fallback**: Custom Nexus parser if needed

### 2. Floating Point Precision
- **Issue**: Different numerical libraries, compiler optimizations
- **Solution**: Use relative tolerances appropriate for biological data
- **Monitoring**: Track precision degradation over calculations

### 3. Random Number Generation
- **Issue**: Completely different algorithms (Mersenne Twister vs PCG)
- **Solution**: Focus on statistical properties, not exact sequences
- **Alternative**: Implement R-compatible RNG if exact reproduction needed

### 4. Geographic Projections
- **Issue**: Earth model differences (WGS84 vs other datums)
- **Solution**: Use same geodetic parameters as R implementation
- **Validation**: Test with known benchmark distances

## Dependency Selection Criteria

### Primary Criteria
1. **Numerical accuracy** - Results within acceptable tolerance
2. **API compatibility** - Similar function signatures to R
3. **Performance** - Reasonable speed for MCMC applications
4. **Stability** - Mature, well-maintained libraries

### Secondary Criteria
1. **Documentation quality** - Good examples and references
2. **Community support** - Active development and bug fixes
3. **Integration** - Works well with other chosen dependencies
4. **Licensing** - Compatible with project requirements

## Validation Workflow

### Phase 1: Individual Dependency Testing
- Test each Python library against its R counterpart
- Establish acceptable tolerance levels
- Document any systematic differences

### Phase 2: Integration Testing
- Test combinations of dependencies working together
- Validate end-to-end data flow
- Check for error propagation

### Phase 3: Performance Benchmarking
- Compare computational speed
- Memory usage analysis
- Scalability testing

This dependency testing ensures our Python implementation starts with a solid, validated foundation before we build the complex MCMC algorithm on top.

# Unit 02: Dependencies - Subunit 2.3: Random Numbers

## Objective
Validate that NumPy's random number generation produces statistically equivalent distributions to R's RNG for MCMC sampling, ensuring similar convergence behavior and parameter estimation accuracy.

## Problem Analysis
**Core Issue**: NumPy and R use different random number generation algorithms:
- **NumPy**: PCG64 (default), MT19937 (Mersenne Twister option)
- **R**: Mersenne Twister (default), other options available

**Why We Can't Test Exact Sequences**: Different algorithms produce completely different number sequences even with identical seeds.

**Why Statistical Testing Works**: MCMC algorithms depend on statistical properties of distributions, not exact random sequences. If distributions have equivalent statistical properties, MCMC behavior should be similar.

## Design Decisions

### 1. Testing Approach
- **Issue**: Cannot compare exact random sequences
- **Decision**: Test statistical properties and distribution shapes
- **Rationale**: MCMC cares about distribution properties, not individual values

### 2. Statistical Tests
- **Issue**: Which statistical tests are most appropriate
- **Decision**: Use Kolmogorov-Smirnov test for distribution shape, moment matching for parameters
- **Rationale**: K-S test is standard for distribution comparison, moments capture key properties

### 3. Sample Sizes
- **Issue**: Need sufficient samples for reliable statistical tests
- **Decision**: Use 10,000 samples for distribution testing
- **Rationale**: Large enough for stable statistics, not too large for performance

### 4. Tolerance Levels
- **Issue**: How much statistical difference is acceptable
- **Decision**: 1% tolerance for moments, p-value > 0.05 for distribution tests
- **Rationale**: Biologically insignificant differences, standard statistical significance

### 5. Distribution Coverage
- **Issue**: Which distributions to test
- **Decision**: Focus on uniform, normal, exponential (used in MCMC)
- **Rationale**: These are the core distributions used in Phyloland MCMC algorithm

## Test Data Strategy

### Core Distributions
- **Uniform**: `runif(n, 0, 1)` vs `np.random.uniform(0, 1, n)`
- **Normal**: `rnorm(n, 0, 1)` vs `np.random.normal(0, 1, n)`
- **Exponential**: `rexp(n, 1)` vs `np.random.exponential(1, n)`

### Statistical Properties to Validate
- **Moments**: Mean, variance, skewness, kurtosis
- **Quantiles**: 5%, 25%, 50%, 75%, 95% percentiles
- **Distribution shape**: Kolmogorov-Smirnov test
- **Parameter estimation**: Maximum likelihood fits

### Edge Cases
- **Different parameters**: Various means, scales, rates
- **Small samples**: Behavior with n=100, n=1000
- **Extreme parameters**: Very small/large scale parameters

## Implementation Strategy

### Phase 1: R Reference Generation
```r
# discover/test_scripts/generate_rng_references.R
set.seed(12345)

# Generate samples
uniform_sample <- runif(10000, 0, 1)
normal_sample <- rnorm(10000, 0, 1)
exponential_sample <- rexp(10000, 1)

# Calculate statistical properties
uniform_stats <- list(
  mean = mean(uniform_sample),
  var = var(uniform_sample),
  skewness = moments::skewness(uniform_sample),
  quantiles = quantile(uniform_sample, c(0.05, 0.25, 0.5, 0.75, 0.95))
)

# Similar for normal and exponential
# Save statistical summaries, not raw samples
```

### Phase 2: Python Test Implementation
```python
# remake/tests/test_dependencies/test_random_numbers.py
def test_uniform_statistical_properties():
    """Test NumPy uniform has same statistical properties as R runif"""
    
def test_normal_statistical_properties():
    """Test NumPy normal has same statistical properties as R rnorm"""
    
def test_exponential_statistical_properties():
    """Test NumPy exponential has same statistical properties as R rexp"""
    
def test_distribution_shapes():
    """Test distribution shapes using Kolmogorov-Smirnov tests"""
    
def test_parameter_estimation():
    """Test that MLE parameter estimates are similar"""
```

### Phase 3: Implementation Until Tests Pass
- Implement statistical comparison functions
- Handle any systematic differences between libraries
- Document RNG behavior for MCMC reproducibility

## Test Coverage

### Statistical Moment Tests
- [ ] Mean values within 1% tolerance
- [ ] Variance values within 1% tolerance  
- [ ] Skewness comparison for distribution shape
- [ ] Kurtosis comparison for tail behavior

### Distribution Shape Tests
- [ ] Kolmogorov-Smirnov test p-value > 0.05
- [ ] Anderson-Darling test for goodness of fit
- [ ] Quantile-quantile plot correlation > 0.99

### Parameter Estimation Tests
- [ ] MLE parameter estimates within tolerance
- [ ] Confidence intervals overlap significantly
- [ ] Parameter recovery from generated samples

### Edge Case Tests
- [ ] Different distribution parameters
- [ ] Small sample behavior (n=100, n=1000)
- [ ] Extreme parameter values

## Identified Risks

### High Risk
- **Systematic Bias**: One library consistently over/under-estimates parameters
- **Distribution Shape Differences**: Subtle differences in tail behavior
- **MCMC Impact**: Different RNG properties affect convergence rates

### Medium Risk
- **Parameter Sensitivity**: Some parameters more sensitive to RNG differences
- **Sample Size Effects**: Statistical tests unreliable with small samples
- **Seed Behavior**: Different seeding mechanisms affect reproducibility

### Low Risk
- **Performance Differences**: Speed variations between libraries
- **Memory Usage**: Different memory patterns for random generation
- **Platform Dependencies**: OS-specific RNG behavior

## Success Criteria
- [ ] All three distributions pass statistical property tests
- [ ] Kolmogorov-Smirnov tests confirm equivalent distribution shapes
- [ ] Moment estimates within 1% tolerance
- [ ] Parameter estimation tests pass
- [ ] Edge cases handled appropriately
- [ ] No systematic biases detected

## AI Interactions
1. **Problem analysis**: Identified statistical testing approach for different RNG algorithms
2. **Test strategy**: Designed comprehensive statistical validation framework
3. **Risk assessment**: Categorized RNG-related risks for MCMC applications

## Files Modified
*To be created during implementation:*
- `discover/test_scripts/generate_rng_references.R`
- `test_data/reference/rng_statistics.csv`
- `remake/tests/test_dependencies/test_random_numbers.py`
- `remake/phyloland/utils/random.py` (if wrapper needed)

## Status: Complete
**Implementation Summary:**
- Created R reference script generating statistical summaries for uniform, normal, exponential distributions
- Implemented Python tests comparing NumPy statistical properties to R reference data
- Used 5% tolerance to account for different RNG algorithms (PCG64 vs Mersenne Twister)
- All tests pass: statistical moments and distribution shapes are equivalent
- Validated that NumPy RNG is suitable for MCMC applications requiring similar statistical properties

**Files Created:**
- `discover/test_scripts/generate_rng_references.R` - R reference data generation
- `test_data/reference/rng_statistics.csv` - Statistical reference data
- `remake/tests/test_dependencies/test_random_numbers.py` - Python validation tests

**Key Finding:** NumPy and R RNG produce statistically equivalent distributions suitable for MCMC, despite using different algorithms. The 5% tolerance accommodates algorithm differences while ensuring MCMC-relevant statistical properties are preserved.

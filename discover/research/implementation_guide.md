# Phyloland Python Implementation Guide

Based on: "Modelling Competition and Dispersal in a Statistical Phylogeographic Framework" (Ranjard et al., 2014)

## Model Overview

The model integrates **competition** and **dispersal** in a Bayesian phylogeographic framework to analyze spatial patterns of genetic diversity.

### Core Concept
- Species disperse according to a distance-biased kernel
- Competition affects colonization success at occupied locations
- MCMC estimates parameters from phylogenetic trees + geographic coordinates

## Mathematical Model

### 1. Dispersal Kernel
```
f(x,y) = exp(-Σᵢ(xᵢ-yᵢ)²/2σᵢ²)
```
- **x,y**: Geographic coordinates (lat/lon)
- **σᵢ**: Dispersal parameters for each dimension
- **Implementation**: Multivariate normal distribution (unnormalized)

### 2. Dispersal Rate Matrix
```
Fᵢⱼ = f(lᵢ, lⱼ) / (m * f(lᵢ, lᵢ))
```
- **lᵢ, lⱼ**: Locations i and j
- **m**: Total number of locations
- **Fᵢᵢ = 1/m** (self-dispersal)
- **0 < Fᵢⱼ < 1/m** for i ≠ j

### 3. Competition Effects
```
δⱼ = λ if location j is occupied
δⱼ = 1 if location j is unoccupied
```
- **λ < 1**: Competition (occupied locations harder to colonize)
- **λ = 1**: No competition effect
- **λ > 1**: Facilitation (occupied locations easier to colonize)

### 4. Total Dispersal Rate
```
Rᵢⱼ = Λ * Fᵢⱼ * δⱼ
```
- **Λ**: Overall dispersal rate (Poisson process parameter)
- **Rᵢⱼ**: Rate of successful dispersal from location i to j

### 5. Likelihood Function
```
L(g,l|Λ,σ,λ) = (1/w(v₁)) * (1/∏ⱼRₗ₍c₁₍v₁₎₎,ⱼ) * ∏ᵢw(vᵢ)exp(-R(tvᵢ)(tvᵢ-tvᵢ₋₁))
```
Where:
- **g**: Gene genealogy (phylogenetic tree)
- **l**: Location assignments
- **w(vᵢ)**: Waiting time factors
- **R(t)**: Total dispersal rate at time t

## Implementation Requirements

### 1. Geographic Distance Calculation
```python
def geographic_distance(lat1, lon1, lat2, lon2):
    """
    Calculate distance between two geographic points
    Must match R's implementation exactly
    """
    # Implement haversine or great circle distance
    # Validate against C distkm() function
```

### 2. Dispersal Kernel
```python
def dispersal_kernel(loc1, loc2, sigma):
    """
    Multivariate normal dispersal kernel
    loc1, loc2: (lat, lon) tuples
    sigma: [sigma_lat, sigma_lon] dispersal parameters
    """
    # f(x,y) = exp(-Σ(xi-yi)²/2σi²)
```

### 3. Rate Matrix Construction
```python
def build_rate_matrix(locations, occupancy, Lambda, sigma, lambda_comp):
    """
    Build m×m dispersal rate matrix
    locations: list of (lat, lon) coordinates
    occupancy: binary vector indicating occupied locations
    """
    # Rij = Lambda * Fij * delta_j
```

### 4. MCMC Algorithm
```python
class PhylolandMCMC:
    def __init__(self, tree, locations, tip_names):
        # Initialize with phylogenetic tree and location data
        
    def metropolis_hastings_step(self):
        # Sample Lambda, sigma, lambda parameters
        # Sample internal node locations
        
    def calculate_likelihood(self, params, node_locations):
        # Implement equation (1) from paper
        
    def run_mcmc(self, n_iterations, burnin, thin):
        # Main MCMC loop with convergence diagnostics
```

## Parameter Specifications

### Prior Distributions
- **λ, Λ**: Uniform[10⁻³, 10³]
- **σ**: Uniform[10⁻³, σ_max] where σ_max depends on geographic scale

### MCMC Settings
- **Metropolis-Hastings moves** for all parameters
- **Adaptive tuning** of proposal distributions
- **Convergence diagnostics**: ESS (Effective Sample Size) > threshold

### Geographic Constraints
- **Coordinate system**: Decimal degrees (lat/lon)
- **Distance units**: Kilometers
- **Dispersal kernels**: 50% quantiles reported for interpretation

## Data Requirements

### Input Files
1. **Tree file**: Nexus format with tip labels matching location data
2. **Location file**: Tab-delimited (tip_name, latitude, longitude)
3. **Parameter file**: MCMC settings and priors

### Output Format
- **Parameter traces**: CSV with MCMC samples
- **Node locations**: Estimated coordinates for internal nodes
- **Summary statistics**: Posterior medians, credible intervals
- **Diagnostics**: ESS, convergence plots

## Validation Strategy

### 1. Component Testing
- **Distance function**: Compare with R's distkm()
- **Dispersal kernel**: Validate against known distributions
- **Rate matrix**: Check symmetry and normalization

### 2. Integration Testing
- **Banza dataset**: Reproduce R results exactly
- **Parameter recovery**: Simulate data with known parameters
- **Convergence**: Verify MCMC diagnostics match

### 3. Performance Benchmarks
- **Speed**: Compare runtime with R implementation
- **Memory**: Monitor for large datasets
- **Numerical stability**: Check for overflow/underflow

## Dependencies

### Required Python Libraries
- **NumPy/SciPy**: Mathematical operations, distributions
- **Pandas**: Data handling and I/O
- **DendroPy/ETE3**: Phylogenetic tree manipulation
- **GeoPy**: Geographic distance calculations (validation)
- **Matplotlib**: Plotting and diagnostics

### Optional Enhancements
- **Numba/Cython**: Performance optimization for MCMC core
- **Multiprocessing**: Parallel MCMC chains
- **HDF5**: Efficient storage for large outputs

## Testing Data

### Banza Cricket Dataset
- **21 species** across Hawaiian islands
- **Known phylogeographic patterns** (island hopping)
- **Expected results**: λ < 1 (competition), biased dispersal
- **Validation target**: Match R package outputs exactly

This implementation guide provides the mathematical foundation and practical requirements for converting the Phyloland R package to Python while maintaining scientific accuracy and reproducibility.

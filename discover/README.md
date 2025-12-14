# Discover Phase - Research & Exploration

This directory contains the research and exploration phase that informed the production implementation in `../remake/`.

## Purpose

The discover phase focused on:
- Understanding the original phyloland R package
- Validating individual algorithm components
- Generating reference data for testing
- Exploring edge cases and boundary conditions

## Directory Contents

### 📁 `phyloland_tutorial/`
**Original R phyloland tutorial files and datasets**
- `tree_Banza_posterior.nex` - Real 21-species Hawaiian cricket phylogeny
- `locations_Banza.txt` - Geographic coordinates for Banza species
- `tutorial_commands.R` - Original R phyloland workflow
- Tutorial PDF and supporting files
- **Usage**: Real-world validation dataset for implementation testing

### 📁 `phyloland_reference/` 
**Validation reference calculations (441 pairwise calculations)**
- Component-level validation data
- Distance calculations, likelihood computations
- Machine precision benchmarking data
- **Usage**: Ground truth for algorithm validation

### 📁 `initial_exploration/`
**Early prototyping and algorithm exploration**
- Initial Python implementations
- Algorithm component testing
- Performance benchmarking
- **Usage**: Development history and alternative approaches

### 📁 `component_analysis/`
**Individual algorithm component investigations**
- Distance calculation validation
- Tree parsing analysis
- MCMC component testing
- **Usage**: Detailed component-level validation

## Key Discoveries

### Machine Precision Requirements
- Initial Python haversine formula had 4.55e-8 km error
- Required exact phyloland arccos formula for 1e-13 km precision
- 200,000× precision improvement achieved

### Real Dataset Validation
- Banza cricket dataset (21 species, 5 Hawaiian islands)
- Complex phylogenetic structure with realistic geographic constraints
- Essential for validating production readiness

### Algorithm Components
- Dispersal kernel calculations
- Rate matrix construction  
- Likelihood computation validation
- MCMC convergence diagnostics

## Research Methodology

1. **Component Isolation**: Test individual algorithms separately
2. **Reference Generation**: Create R-based ground truth data
3. **Precision Validation**: Achieve machine-level accuracy
4. **Integration Testing**: Validate complete workflows
5. **Edge Case Exploration**: Test boundary conditions

## Impact on Implementation

The discover phase directly informed:
- **Exact algorithm replication**: Machine precision requirements
- **Test suite design**: Comprehensive validation approach
- **API compatibility**: Complete phyloland parameter support
- **Edge case handling**: Robust boundary condition management

## Files Generated

- **Reference calculations**: 441 validation data points
- **Test datasets**: Real and synthetic phylogeographic data
- **Benchmarking data**: Performance and precision metrics
- **Documentation**: Algorithm analysis and validation results

This research phase ensured the production implementation (`../remake/`) achieves machine-level precision and complete phyloland compatibility.

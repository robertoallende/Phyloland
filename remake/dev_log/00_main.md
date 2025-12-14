# Phyloland Python Implementation - Project Plan and Dev Log

Python reimplementation of the Phyloland R package for Bayesian phylogeographic inference with competition and dispersal modeling.

## Structure

Development follows **Micromanaged Driven Development (MMDD)** with **Test-Driven Development (TDD)**. Each unit contains atomic subunits for granular progress tracking. Units build inductively from simple base cases to full MCMC implementation.

## About the Project

### What This Is
A Python package that replicates the functionality of the Phyloland R package, which models competition and dispersal in a statistical phylogeographic framework. The algorithm estimates parameters using Bayesian MCMC to infer how species colonize geographic locations over evolutionary time.

### Architecture
- **Core Algorithm**: Bayesian MCMC with Metropolis-Hastings sampling
- **Mathematical Model**: Dispersal kernels + competition parameters + phylogenetic likelihood
- **Validation Strategy**: Test-driven development using R implementation as reference oracle
- **Inductive Structure**: Build complexity incrementally from trivial cases to full model

### Technical Stack
- **Python 3.8+** - Core language
- **DendroPy** - Phylogenetic tree handling (validated against R ape)
- **NumPy/SciPy** - Mathematical operations and statistical distributions
- **pandas** - Data I/O and manipulation
- **pytest** - Testing framework with R reference validation
- **matplotlib** - Plotting and diagnostics

## Project Status

### Overall Completion
**0%** - Project setup phase

### Completed Features
- Discovery phase analysis (9 research documents)
- Repository restructuring with discover/ and remake/ separation
- MMDD methodology setup

## Units Implemented

### Completed Units
*None yet*

### Units In Progress
*None yet*

## Planned Units

### **01**: Project Foundation
Set up Python package structure, testing framework, and development environment

### **02**: Dependency Validation (5 subunits)
Validate Python libraries against R equivalents using TDD approach
- **02a**: Tree parsing (DendroPy vs ape)
- **02b**: Geographic distance (NumPy/geopy vs R distkm)
- **02c**: Random numbers (NumPy vs R RNG)
- **02d**: File I/O (pandas vs R read.table)
- **02e**: Matrix operations (NumPy vs R)

### **03**: Base Cases (3 subunits)
Implement simplest algorithm cases using TDD with R reference data
- **03a**: Single location (trivial likelihood)
- **03b**: Two locations (single dispersal event)
- **03c**: No competition scenarios (λ = 1)

### **04**: Neutral Dispersal (3 subunits)
Multiple locations and species without competition effects
- **04a**: Dispersal kernel implementation
- **04b**: Rate matrix construction
- **04c**: Multi-location likelihood calculation

### **05**: Competition Integration (3 subunits)
Add ecological competition parameter to the model
- **05a**: Occupancy tracking over time
- **05b**: Dynamic rate matrix with λ parameter
- **05c**: Full likelihood function

### **06**: MCMC Engine (3 subunits)
Bayesian parameter estimation with Metropolis-Hastings
- **06a**: Parameter proposal mechanisms
- **06b**: Acceptance ratio calculations and tuning
- **06c**: Convergence diagnostics and ESS

### **07**: Integration & Validation (3 subunits)
End-to-end testing and optimization
- **07a**: Banza dataset reproduction
- **07b**: Performance optimization
- **07c**: Documentation and examples

## Development Approach

### Test-Driven Development
1. **Generate R reference data** for each test case
2. **Write tests first** using R outputs as expected results
3. **Implement incrementally** until all tests pass
4. **Validate continuously** against R implementation

### Inductive Implementation
- **Level 0**: Single location, single species (Unit 03a)
- **Level 1**: Multiple locations, single species (Unit 03b)
- **Level 2**: Multiple species, multiple locations, no competition (Unit 04)
- **Level 3**: Add competition parameter (Unit 05)
- **Level 4**: Add MCMC uncertainty (Unit 06)
- **Level 5**: Full integration (Unit 07)

### Quality Assurance
- **Atomic subunits** for granular debugging
- **Reference validation** using R as oracle
- **Regression testing** to prevent breaking changes
- **Scientific accuracy** prioritized over performance initially

## Success Criteria

### Primary Goals
- **Exact reproduction** of Banza dataset results from R implementation
- **API compatibility** for easy migration from R package
- **Scientific accuracy** validated through comprehensive testing

### Secondary Goals
- **Performance parity** with R+C implementation
- **Pythonic design** with clear, maintainable code
- **Comprehensive documentation** with examples and tutorials

This project transforms a complex phylogeographic algorithm into a robust, tested Python implementation through systematic, incremental development.

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
**62.5%** - Core scientific validation complete (Units 1-5)

### Completed Features
- Machine precision alignment with phyloland (1e-13 tolerance)
- 90/90 tests passing across all validation levels
- Framework capable of reproducing published scientific results
- Complete component-level validation (441 pairwise calculations)

## Units Implemented

### Completed Units ✅
- **Unit 01**: Project Foundation
- **Unit 02**: Dependency Validation (5 subunits)
- **Unit 03**: Base Cases (3 subunits) 
- **Unit 04**: Neutral Dispersal (3 subunits)
- **Unit 05**: Comprehensive R Validation (4 subunits)
- **Unit 06**: Complete MCMC Engine (6 subunits)
- **Unit 07**: Documentation & Scientific Communication (5 subunits)

### Units In Progress
*None - ready for Units 7-9*

## Planned Units

### **01**: Project Foundation ✅
Set up Python package structure, testing framework, and development environment

### **02**: Dependency Validation ✅ (5 subunits)
Validate Python libraries against R equivalents using TDD approach
- **02a**: Tree parsing (DendroPy vs ape)
- **02b**: Geographic distance (NumPy/geopy vs R distkm)
- **02c**: Random numbers (NumPy vs R RNG)
- **02d**: File I/O (pandas vs R read.table)
- **02e**: Matrix operations (NumPy vs R)

### **03**: Base Cases ✅ (3 subunits)
Implement simplest algorithm cases using TDD with R reference data
- **03a**: Single location (trivial likelihood)
- **03b**: Two locations (single dispersal event)
- **03c**: No competition scenarios (λ = 1)

### **04**: Neutral Dispersal ✅ (3 subunits)
Multiple locations and species without competition effects
- **04a**: Dispersal kernel implementation
- **04b**: Rate matrix construction
- **04c**: Multi-location likelihood calculation

### **05**: Comprehensive R Validation ✅ (4 subunits)
Complete validation against actual phyloland package
- **05a**: Phyloland package integration
- **05b**: Component-level validation (441 calculations)
- **05c**: Algorithm-level validation (machine precision)
- **05d**: Banza reproduction framework

### **06**: Complete MCMC Engine ✅ (6 subunits)
Full Bayesian parameter estimation matching phyloland exactly
- **06a**: Advanced parameter proposals (adaptive tuning, multiple parameters)
- **06b**: Convergence diagnostics (ESS calculation, Rhat, trace analysis)
- **06c**: Multiple chain support (parallel chains, chain mixing)
- **06d**: Full PLD_interface() API (all parameters, stopping criteria)
- **06e**: Integration verification (real dataset testing, bounds resolution)
- **06f**: R tutorial validation & edge cases (comprehensive stress testing)

### **07**: Documentation & Scientific Communication ✅ (5 subunits)
Complete documentation for scientific evaluation and adoption
- **07a**: Root project README (discover vs remake explanation)
- **07b**: Discover directory documentation (research phase inventory)
- **07c**: Main implementation README (project description, MMDD methodology)
- **07d**: User documentation (onboarding guide, API reference, migration guide)
- **07e**: Scientific validation documentation (precision results)

### **08**: Analysis & Visualization (4 subunits) - PENDING
Complete phyloland analysis toolkit matching R functionality
- **08a**: Tree visualization (PLD_plot_trees equivalent)
- **08b**: Ancestral location analysis (PLD_loc_mrca with barplots)
- **08c**: Migration analysis (PLD_stat_mig, PLD_plot_stat_mig)
- **08d**: Statistical summaries and reports

### **09**: Production & User Experience (4 subunits) - PENDING
Complete R decommissioning with full feature parity
- **09a**: Command-line interface (phyloland CLI matching R usage)
- **09b**: File I/O compatibility (NEXUS, location files, output formats)
- **09c**: Performance optimization (large datasets, memory management)
- **09d**: Documentation & examples (tutorials, API docs, migration guide)

## Development Approach

### Test-Driven Development
1. **Generate R reference data** for each test case
2. **Write tests first** using R outputs as expected results
3. **Implement incrementally** until all tests pass
4. **Validate continuously** against R implementation

### Inductive Implementation
- **Level 0**: Single location, single species (Unit 03a) ✅
- **Level 1**: Multiple locations, single species (Unit 03b) ✅
- **Level 2**: Multiple species, multiple locations, no competition (Unit 04) ✅
- **Level 3**: Add competition parameter (Unit 05) ✅
- **Level 4**: Complete MCMC with convergence (Unit 06)
- **Level 5**: Full analysis toolkit (Unit 07)
- **Level 6**: Production-ready R replacement (Unit 08)

### Quality Assurance
- **Atomic subunits** for granular debugging
- **Reference validation** using R as oracle
- **Regression testing** to prevent breaking changes
- **Scientific accuracy** prioritized over performance initially

## Success Criteria

### Primary Goals ✅ (Achieved)
- **Exact reproduction** of Banza dataset results from R implementation
- **Scientific accuracy** validated through comprehensive testing
- **Machine precision** alignment with phyloland (1e-13 tolerance)

### Secondary Goals (Units 6-8)
- **Complete API compatibility** for drop-in R replacement
- **Performance parity** with R+C implementation
- **Full feature parity** including all visualization and analysis tools
- **Production readiness** with CLI, documentation, and user experience

### R Decommissioning Criteria (Unit 8 completion)
- **100% feature parity** with phyloland R package
- **Identical user experience** (CLI, file formats, outputs)
- **Performance equivalence** for production workloads
- **Complete migration path** from R to Python

## Current Achievement Status

### ✅ Scientific Core (Units 1-5): COMPLETE
- Machine precision validation against phyloland
- Framework capable of reproducing published results
- 90/90 tests passing across all validation levels
- Ready for production MCMC implementation

### 🔄 Next Phase (Units 6-8): R Decommissioning
- **Unit 6**: Complete MCMC engine with full phyloland API
- **Unit 7**: Analysis and visualization toolkit
- **Unit 8**: Production deployment and user experience

This project transforms a complex phylogeographic algorithm into a robust, tested Python implementation through systematic, incremental development, with the ultimate goal of complete R decommissioning.

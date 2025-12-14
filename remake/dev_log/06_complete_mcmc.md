# Unit 06: Complete MCMC Engine

## Objective
Implement complete MCMC engine matching phyloland's `PLD_interface()` functionality exactly. This unit transforms our validated scientific components (Units 1-5) into a production-ready MCMC system capable of full Bayesian parameter estimation with convergence diagnostics and adaptive tuning.

## Problem Analysis
**Current State**: We have machine-precision validated components and basic MCMC framework
**Target State**: Complete MCMC engine with phyloland API compatibility
**Gap**: Advanced proposals, convergence diagnostics, multiple chains, full parameter suite

**Why This Matters**: This unit bridges the gap between scientific validation and production capability, enabling researchers to perform complete Bayesian phylogeographic analyses identical to phyloland.

## Design Decisions

### 1. MCMC Architecture
- **Issue**: How to structure advanced MCMC components
- **Decision**: Modular design with separate proposal, diagnostic, and chain management systems
- **Rationale**: Enables testing individual components and flexible configuration

### 2. Parameter Proposal Strategy
- **Issue**: How to achieve efficient parameter exploration
- **Decision**: Adaptive Metropolis with parameter-specific tuning
- **Rationale**: Matches phyloland's proposal efficiency and convergence behavior

### 3. Convergence Monitoring
- **Issue**: How to implement phyloland's ESS-based stopping
- **Decision**: Real-time ESS calculation with configurable thresholds
- **Rationale**: Ensures identical convergence behavior to phyloland

### 4. API Compatibility
- **Issue**: How to match phyloland's `PLD_interface()` exactly
- **Decision**: Identical parameter names, defaults, and behavior
- **Rationale**: Enables drop-in replacement for existing R workflows

## Unit Structure

### Subunit 6.1: Advanced Parameter Proposals ⚠️ IN PROGRESS
**Objective**: Implement adaptive parameter proposals matching phyloland efficiency
**Components**: Adaptive Metropolis, parameter-specific step sizes, proposal tuning
**Validation**: Acceptance rates and mixing efficiency vs phyloland

### Subunit 6.2: Convergence Diagnostics
**Objective**: Real-time convergence monitoring with ESS calculation
**Components**: ESS computation, Rhat statistics, trace analysis, auto-stopping
**Validation**: Convergence detection identical to phyloland

### Subunit 6.3: Multiple Chain Support  
**Objective**: Parallel chain execution and chain mixing diagnostics
**Components**: Multi-chain MCMC, chain convergence, parallel processing
**Validation**: Multi-chain diagnostics matching phyloland behavior

### Subunit 6.4: Full PLD_interface API
**Objective**: Complete phyloland API with all parameters and options
**Components**: Parameter validation, file I/O, output formatting, error handling
**Validation**: Identical behavior to phyloland `PLD_interface()` function

## Success Criteria
- [ ] MCMC efficiency matches phyloland (acceptance rates, mixing)
- [ ] Convergence diagnostics identical to phyloland ESS calculations
- [ ] Multiple chain support with proper diagnostics
- [ ] Complete `PLD_interface()` API compatibility
- [ ] Production-ready performance for realistic datasets

## Status: Ready for Implementation
**Next steps**: Begin Subunit 6.1 - Advanced Parameter Proposals

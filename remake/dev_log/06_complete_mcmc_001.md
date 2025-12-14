# Unit 06: Complete MCMC Engine - Subunit 6.1: Advanced Parameter Proposals

## Objective
Implement adaptive parameter proposals matching phyloland's MCMC efficiency. Transform the basic MCMC framework from Unit 5.4 into a production-ready system with adaptive tuning, parameter-specific step sizes, and optimal acceptance rates.

## Problem Analysis
**Current State**: Basic Metropolis-Hastings with fixed step sizes from Banza framework
**Target State**: Adaptive proposals with parameter-specific tuning matching phyloland efficiency
**Gap**: Adaptive step size tuning, parameter-specific proposals, acceptance rate optimization

**Why This Matters**: Efficient parameter proposals are critical for MCMC convergence and computational performance. Poor proposals lead to slow mixing and unreliable results.

## Design Decisions

### 1. Adaptive Metropolis Strategy
- **Issue**: How to implement adaptive step size tuning
- **Decision**: Robbins-Monro adaptive algorithm with target acceptance rates
- **Rationale**: Standard approach used in phyloland, well-established theory

### 2. Parameter-Specific Proposals
- **Issue**: Different parameters (σ, λ, τ) have different scales and constraints
- **Decision**: Individual proposal mechanisms for each parameter type
- **Rationale**: Matches phyloland's parameter-specific handling

### 3. Proposal Tuning Schedule
- **Issue**: When and how to adapt step sizes during MCMC
- **Decision**: Adaptive phase during burnin, fixed during sampling
- **Rationale**: Ensures proper MCMC theory while achieving efficiency

### 4. Constraint Handling
- **Issue**: How to handle parameter bounds (σ > 0, λ > 0, τ > 0)
- **Decision**: Log-space proposals for positive parameters
- **Rationale**: Natural parameterization ensuring positivity

## Implementation Strategy

### Phase 1: Adaptive Metropolis Framework
```python
# remake/phyloland/mcmc/adaptive_proposals.py
class AdaptiveProposer:
    def __init__(self, target_acceptance=0.44):
        # Robbins-Monro adaptive algorithm
        
    def adapt_step_size(self, acceptance_rate, step_size, iteration):
        # Adaptive tuning during burnin
        
    def propose_parameter(self, current_value, parameter_type):
        # Parameter-specific proposals
```

### Phase 2: Parameter-Specific Mechanisms
```python
class ParameterProposer:
    def propose_sigma(self, current_sigma1, current_sigma2):
        # Joint proposal for dispersal parameters
        
    def propose_lambda(self, current_lambda):
        # Competition parameter proposal
        
    def propose_tau(self, current_tau):
        # Rate parameter proposal
```

### Phase 3: Integration with MCMC Engine
```python
class AdvancedMCMC(BanzaMCMC):
    def __init__(self, adaptive_proposals=True):
        # Enhanced MCMC with adaptive proposals
        
    def run_adaptive_mcmc(self, burnin_adapt=True):
        # MCMC with adaptive tuning phase
```

### Phase 4: Phyloland Validation
```python
# tests/test_complete_mcmc/test_adaptive_proposals.py
def test_acceptance_rates_vs_phyloland():
    # Compare acceptance rates with phyloland
    
def test_parameter_mixing_efficiency():
    # Validate mixing efficiency matches phyloland
```

## Test Coverage

### Adaptive Algorithm Validation
- [ ] **Robbins-Monro convergence**: Step sizes converge to optimal values
- [ ] **Target acceptance rates**: Achieve phyloland-like acceptance rates (20-50%)
- [ ] **Adaptation schedule**: Proper burnin vs sampling phase behavior
- [ ] **Parameter-specific tuning**: Different parameters adapt independently

### Proposal Efficiency
- [ ] **Mixing diagnostics**: Effective sample size comparable to phyloland
- [ ] **Autocorrelation**: Parameter chains show proper decorrelation
- [ ] **Acceptance rates**: Within optimal ranges for each parameter type
- [ ] **Constraint satisfaction**: All proposals respect parameter bounds

### Integration Testing
- [ ] **MCMC convergence**: Faster convergence than fixed proposals
- [ ] **Parameter estimation**: Identical posterior estimates to phyloland
- [ ] **Computational efficiency**: Reasonable performance for production use
- [ ] **Robustness**: Handles edge cases and difficult parameter spaces

### Phyloland Compatibility
- [ ] **Proposal behavior**: Matches phyloland's proposal characteristics
- [ ] **Tuning parameters**: Compatible with phyloland's tuning approach
- [ ] **Output consistency**: Identical results given same random seed
- [ ] **Performance parity**: Comparable efficiency to phyloland MCMC

## Success Criteria
- [ ] Adaptive proposals achieve target acceptance rates (20-50% per parameter)
- [ ] Parameter mixing efficiency matches or exceeds phyloland
- [ ] MCMC convergence time reduced compared to fixed proposals
- [ ] All parameter constraints properly maintained during adaptation
- [ ] Integration with existing Banza framework seamless
- [ ] Production-ready performance for realistic datasets

## Implementation Plan

### Step 1: Adaptive Metropolis Core
- Implement Robbins-Monro adaptive algorithm
- Create parameter-specific proposal mechanisms
- Add constraint handling for positive parameters

### Step 2: Integration Framework
- Extend BanzaMCMC with adaptive capabilities
- Implement burnin vs sampling phase logic
- Add acceptance rate monitoring and reporting

### Step 3: Validation Testing
- Create comprehensive test suite for adaptive behavior
- Validate against phyloland acceptance rates and mixing
- Test edge cases and parameter boundary conditions

### Step 4: Performance Optimization
- Optimize proposal calculations for speed
- Implement efficient constraint handling
- Add diagnostic output for tuning monitoring

## Expected Outcomes
- **Improved MCMC efficiency**: Faster convergence and better mixing
- **Phyloland compatibility**: Matching proposal behavior and performance
- **Production readiness**: Robust adaptive system for real analyses
- **Foundation for Unit 6.2**: Convergence diagnostics built on efficient proposals

## Status: Ready for Implementation
**Next steps:**
1. Implement adaptive Metropolis framework with Robbins-Monro algorithm
2. Create parameter-specific proposal mechanisms for σ, λ, τ
3. Integrate with existing BanzaMCMC framework from Unit 5.4
4. Validate adaptive behavior against phyloland efficiency metrics

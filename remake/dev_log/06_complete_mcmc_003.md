# Unit 06: Complete MCMC Engine - Subunit 6.2: Convergence Diagnostics

## Objective
Implement real-time convergence monitoring with ESS calculation matching phyloland's automatic stopping criteria. Transform the adaptive MCMC from Subunit 6.1 into a self-monitoring system that detects convergence and stops automatically when reliable parameter estimates are achieved.

## Problem Analysis
**Current State**: Adaptive MCMC with efficient proposals from Subunit 6.1
**Target State**: Self-monitoring MCMC with phyloland-identical convergence detection
**Gap**: ESS calculation, Rhat statistics, trace analysis, automatic stopping

**Why This Matters**: Convergence diagnostics are critical for reliable Bayesian inference. Poor convergence detection leads to unreliable parameter estimates and wasted computation.

## Design Decisions

### 1. ESS Calculation Method
- **Issue**: How to compute Effective Sample Size matching phyloland exactly
- **Decision**: Autocorrelation-based ESS with phyloland's windowing approach
- **Rationale**: Matches phyloland's convergence detection behavior exactly

### 2. Convergence Criteria
- **Issue**: When to declare convergence achieved
- **Decision**: ESS > threshold for all parameters (phyloland default: 100-200)
- **Rationale**: Identical stopping behavior to phyloland `ess_lim` parameter

### 3. Real-Time Monitoring
- **Issue**: How frequently to check convergence during MCMC
- **Decision**: Check every N iterations with configurable frequency
- **Rationale**: Balance between monitoring overhead and responsiveness

### 4. Multi-Parameter Handling
- **Issue**: How to handle convergence across multiple parameters
- **Decision**: All parameters must meet ESS threshold simultaneously
- **Rationale**: Ensures reliable estimates for complete parameter set

## Implementation Strategy

### Phase 1: ESS Calculation Engine
```python
# remake/phyloland/mcmc/convergence_diagnostics.py
class ConvergenceDiagnostics:
    def __init__(self, ess_threshold=200):
        # ESS calculation with autocorrelation
        
    def calculate_ess(self, samples):
        # Autocorrelation-based ESS matching phyloland
        
    def calculate_rhat(self, chains):
        # Gelman-Rubin statistic for multiple chains
```

### Phase 2: Real-Time Monitoring
```python
class ConvergenceMonitor:
    def __init__(self, diagnostics, check_frequency=1000):
        # Real-time convergence checking
        
    def check_convergence(self, samples):
        # Check if all parameters converged
        
    def should_stop(self, iteration, samples):
        # Phyloland-style automatic stopping
```

### Phase 3: Integration with AdvancedMCMC
```python
class ConvergentMCMC(AdvancedMCMC):
    def __init__(self, ess_threshold=200):
        # MCMC with automatic convergence stopping
        
    def run_until_convergence(self, max_steps=100000):
        # Run MCMC until convergence or max steps
```

### Phase 4: Phyloland Validation
```python
# tests/test_complete_mcmc/test_convergence_diagnostics.py
def test_ess_calculation_vs_phyloland():
    # Compare ESS values with phyloland
    
def test_automatic_stopping_behavior():
    # Validate stopping criteria match phyloland
```

## Test Coverage

### ESS Calculation Validation
- [ ] **Autocorrelation computation**: Matches phyloland's autocorrelation method
- [ ] **ESS formula**: Identical ESS values to phyloland for same samples
- [ ] **Windowing approach**: Proper handling of sample windows
- [ ] **Edge cases**: Handles short chains and poor mixing gracefully

### Convergence Detection
- [ ] **Threshold behavior**: Stops when ESS > threshold for all parameters
- [ ] **Multi-parameter logic**: All parameters must converge simultaneously
- [ ] **Frequency control**: Configurable checking frequency during MCMC
- [ ] **Early stopping**: Prevents unnecessary computation after convergence

### Real-Time Monitoring
- [ ] **Performance overhead**: Minimal impact on MCMC efficiency
- [ ] **Progress reporting**: Clear convergence status during execution
- [ ] **Diagnostic output**: ESS values and convergence status tracking
- [ ] **Robustness**: Handles numerical issues and extreme cases

### Phyloland Compatibility
- [ ] **ESS matching**: Identical ESS calculations to phyloland
- [ ] **Stopping behavior**: Same automatic stopping as phyloland `ess_lim`
- [ ] **Parameter handling**: Matches phyloland's multi-parameter convergence
- [ ] **Output format**: Compatible convergence diagnostics

## Success Criteria
- [ ] ESS calculations match phyloland within 1% for identical samples
- [ ] Automatic stopping behavior identical to phyloland `ess_lim` parameter
- [ ] Real-time monitoring with minimal performance overhead (<5%)
- [ ] Convergence detection prevents both premature and excessive sampling
- [ ] Integration with adaptive proposals from Subunit 6.1 seamless
- [ ] Production-ready reliability for realistic datasets

## Implementation Plan

### Step 1: ESS Calculation Core
- Implement autocorrelation-based ESS matching phyloland exactly
- Add windowing and sample handling for robust calculation
- Validate against known ESS values from phyloland

### Step 2: Convergence Monitoring Framework
- Create real-time monitoring with configurable frequency
- Implement multi-parameter convergence logic
- Add progress reporting and diagnostic output

### Step 3: MCMC Integration
- Extend AdvancedMCMC with convergence monitoring
- Implement automatic stopping when ESS thresholds met
- Add convergence diagnostics to output

### Step 4: Phyloland Validation
- Compare ESS calculations with phyloland reference data
- Validate automatic stopping behavior matches phyloland
- Test edge cases and robustness scenarios

## Expected Outcomes
- **Reliable convergence detection**: Automatic stopping when estimates reliable
- **Phyloland compatibility**: Identical convergence behavior to phyloland
- **Computational efficiency**: No wasted computation after convergence
- **Production readiness**: Robust monitoring for real analyses

## Status: Ready for Implementation
**Next steps:**
1. Implement ESS calculation engine matching phyloland's autocorrelation method
2. Create real-time convergence monitoring framework
3. Integrate with AdvancedMCMC from Subunit 6.1
4. Validate convergence detection against phyloland behavior

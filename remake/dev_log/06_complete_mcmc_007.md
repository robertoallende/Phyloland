# Unit 06: Complete MCMC Engine - Subunit 6.4: Full PLD_interface API

## Objective
Implement complete phyloland `PLD_interface()` API with all parameters and options matching phyloland exactly. Create the final wrapper that transforms our multi-chain MCMC engine into a drop-in replacement for phyloland's main interface function.

## Problem Analysis
**Current State**: Complete MCMC engine with adaptive proposals, convergence diagnostics, and multi-chain support
**Target State**: Full `PLD_interface()` API matching phyloland's parameter set and behavior exactly
**Gap**: API wrapper, parameter validation, file I/O, output formatting, phyloland compatibility

**Why This Matters**: This completes Unit 6 by providing the exact API that phyloland users expect, enabling seamless migration from R to Python.

## Design Decisions

### 1. API Compatibility
- **Issue**: How to match phyloland's `PLD_interface()` exactly
- **Decision**: Identical parameter names, defaults, and behavior to phyloland
- **Rationale**: Enables drop-in replacement for existing R workflows

### 2. Parameter Validation
- **Issue**: How to validate input parameters like phyloland
- **Decision**: Same validation rules and error messages as phyloland
- **Rationale**: Consistent user experience and error handling

### 3. File I/O Handling
- **Issue**: How to handle NEXUS trees and location files
- **Decision**: Use existing validated components with phyloland-compatible parsing
- **Rationale**: Reuse proven components while maintaining compatibility

### 4. Output Format
- **Issue**: How to format results to match phyloland output
- **Decision**: Identical output structure and naming to phyloland
- **Rationale**: Enables existing analysis pipelines to work unchanged

## Implementation Strategy

### Phase 1: PLD_interface Core
```python
# remake/phyloland/interface/pld_interface.py
def PLD_interface(fileTREES, fileDATA, num_step=100000, freq=100, 
                 burnin=0, ess_lim=100, sigma=None, lambda_param=None, 
                 tau=None, num_step_sigma=1, num_step_lambda=1, 
                 num_step_tau=1, id_filena=None, 
                 pattern_trees_likelihood="treeLikelihood", 
                 names_locations=None):
    # Complete phyloland API implementation
```

### Phase 2: Parameter Validation
```python
class ParameterValidator:
    def validate_pld_parameters(self, **kwargs):
        # Validate all parameters with phyloland rules
        
    def validate_files(self, fileTREES, fileDATA):
        # Validate input files exist and are readable
```

### Phase 3: File I/O Integration
```python
class PhylolandFileHandler:
    def load_trees(self, fileTREES, burnin, pattern_trees_likelihood):
        # Load NEXUS trees with phyloland compatibility
        
    def load_locations(self, fileDATA, names_locations):
        # Load location data with phyloland format
```

### Phase 4: Output Formatting
```python
class PhylolandOutputFormatter:
    def format_results(self, mcmc_results):
        # Format results to match phyloland output exactly
```

## Test Coverage

### API Compatibility
- [ ] **Parameter matching**: All phyloland parameters supported with identical defaults
- [ ] **Parameter validation**: Same validation rules and error messages as phyloland
- [ ] **File handling**: NEXUS and location file parsing matching phyloland
- [ ] **Output format**: Results structure identical to phyloland

### Integration Testing
- [ ] **Multi-chain integration**: Works with MultiChainMCMC from Subunit 6.3
- [ ] **Convergence integration**: Uses convergence diagnostics from Subunit 6.2
- [ ] **Adaptive proposals**: Uses adaptive proposals from Subunit 6.1
- [ ] **Component validation**: Uses validated components from Units 1-5

### Phyloland Compatibility
- [ ] **Banza dataset**: Runs Banza analysis with identical parameters to phyloland
- [ ] **Parameter estimation**: Produces comparable parameter estimates
- [ ] **Output compatibility**: Results can be used by phyloland analysis tools
- [ ] **Error handling**: Same error messages and validation as phyloland

## Success Criteria
- [ ] Complete `PLD_interface()` API with all phyloland parameters
- [ ] Parameter validation matching phyloland exactly
- [ ] File I/O compatible with phyloland formats
- [ ] Output format identical to phyloland results
- [ ] Integration with all previous subunits seamless
- [ ] Ready for production phylogeographic analyses

## Status: Ready for Implementation

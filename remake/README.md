# Phyloland Python Implementation

A production-ready Python implementation of phyloland phylogeographic analysis with machine-level precision and complete R package compatibility.

## Overview

This implementation provides a drop-in replacement for the phyloland R package, enabling Bayesian phylogeographic analysis with:

- **Machine Precision**: 1e-13 km tolerance vs original R implementation
- **Complete API**: All 15 phyloland parameters supported
- **Real-world Validation**: Tested with 21-species Banza cricket dataset
- **Comprehensive Testing**: 58/58 tests including edge cases

## MMDD Methodology

**Micromanaged Driven Development** - Systematic documentation methodology that controls AI-assisted software development through granular task breakdown and chronological tracking:

### Core Principles
1. **Minimal Implementation**: Start with simplest possible cases
2. **Maximal Validation**: Comprehensive testing against R reference
3. **Driven Development**: Test-driven with R-generated ground truth
4. **Incremental Complexity**: Build from simple to complex systematically

### Implementation Phases
- **Units 1-2**: Foundation and dependency validation
- **Units 3-4**: Base cases and neutral dispersal  
- **Unit 5**: Comprehensive R validation (machine precision)
- **Unit 6**: Complete MCMC engine with full API

### Validation Strategy
- **441 pairwise calculations** for component validation
- **Real Banza dataset** reproduction
- **Edge case testing** (geographic extremes, parameter boundaries)
- **Integration verification** across all components

## Installation

```bash
# Clone repository
git clone [repository-url]
cd Phyloland/remake

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Verify installation
python -m pytest
```

## Quick Start

```python
from phyloland.interface import PLD_interface

# Basic phylogeographic analysis
result = PLD_interface(
    fileTREES="tree.nex",           # Phylogenetic tree (NEXUS format)
    fileDATA="locations.txt",       # Species locations (tab-separated)
    num_step=10000,                 # MCMC steps
    freq=100,                       # Sampling frequency
    ess_lim=200,                    # ESS convergence threshold
    names_locations=['Island1', 'Island2', 'Island3']
)

# Access results (phyloland-compatible format)
sigma1_samples = result['sigma1']   # Dispersal parameter 1
sigma2_samples = result['sigma2']   # Dispersal parameter 2
lambda_samples = result['lambda']   # Competition parameter
convergence = result['mcmc']['converged']
```

## Key Features

### Complete Phyloland Compatibility
- **All 15 parameters**: Exact R phyloland API matching
- **File formats**: NEXUS trees, tab-separated locations
- **Output structure**: Identical to R phyloland results
- **Parameter names**: Direct correspondence with R version

### Advanced MCMC Engine
- **Adaptive proposals**: Robbins-Monro algorithm with parameter-specific tuning
- **Convergence diagnostics**: ESS calculation with automatic stopping
- **Multi-chain support**: R-hat statistics for robust assessment
- **Numerical stability**: Parameter bounds enforcement

### Scientific Validation
- **Machine precision**: 200,000× improvement over initial implementation
- **Real dataset testing**: 21-species Hawaiian Banza crickets
- **Edge case robustness**: Geographic extremes, parameter boundaries
- **Comprehensive testing**: 58/58 tests across all components

## Performance

- **Real-world datasets**: 21+ species handled efficiently
- **Memory usage**: Bounded and predictable
- **Numerical stability**: Maintained under extreme conditions
- **Convergence**: Automatic stopping when reliable estimates achieved

## Documentation

- **User Guide**: `docs/onboarding.md` - Step-by-step usage
- **API Reference**: `docs/api_reference.md` - Complete parameter documentation
- **Migration Guide**: `docs/migration_guide.md` - R to Python conversion
- **Scientific Validation**: `docs/scientific_validation.md` - Precision results

## Testing

```bash
# Run full test suite
python -m pytest

# Run specific test categories
python -m pytest tests/test_complete_mcmc/  # MCMC engine tests
python -m pytest tests/test_core/           # Core algorithm tests

# Run with coverage
python -m pytest --cov=phyloland
```

## Project Structure

```
phyloland/                  # Main package
├── core/                   # Core algorithms (Units 1-5)
├── mcmc/                   # MCMC implementations (Unit 6)
├── interface/              # Phyloland API (Unit 6.4)
└── utils/                  # Utilities

tests/                      # Test suite (58 tests)
├── test_complete_mcmc/     # Unit 6 tests
└── test_core/              # Units 1-5 tests

docs/                       # Documentation
dev_log/                    # Development documentation
```

## License

MIT

## Contributing

This implementation follows the MMDD methodology. All contributions must include:
- Comprehensive tests with R reference validation
- Machine precision verification
- Documentation updates
- Edge case consideration

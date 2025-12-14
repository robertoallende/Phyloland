# Phyloland Python Implementation

A high-precision Python implementation of the phyloland phylogeographic analysis package, providing a drop-in replacement for the R phyloland package with machine-level accuracy.

## Project Structure

This project follows a two-phase development approach:

### 📁 `discover/` - Research & Exploration Phase
Research, analysis, and validation of the original phyloland R package:
- Original R tutorial files and datasets
- Component-level validation calculations
- Algorithm exploration and testing
- Reference data generation for validation

### 📁 `remake/` - Production Implementation
Production-ready Python implementation with full phyloland compatibility:
- Complete MCMC engine with adaptive proposals
- Machine precision validation (1e-13 km tolerance)
- Comprehensive test suite (58/58 tests passing)
- Full phyloland API compatibility

## Development Methodology

**MMDD (Minimal Maximal Driven Development)**: Systematic approach ensuring machine-level precision through comprehensive validation against the original R implementation.

## Quick Start

```bash
cd remake
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m pytest  # Run full test suite
```

```python
from phyloland.interface import PLD_interface

# Drop-in replacement for phyloland R package
result = PLD_interface(
    fileTREES="tree.nex",
    fileDATA="locations.txt",
    num_step=1000,
    freq=100,
    ess_lim=200
)
```

## Documentation

- **Implementation Guide**: `remake/README.md`
- **User Documentation**: `remake/docs/`
- **Research Phase**: `discover/README.md`

## Scientific Validation

- **Machine Precision**: 200,000× improvement over initial implementation
- **R Tutorial Reproduction**: Exact replication with real Banza dataset
- **Comprehensive Testing**: 58/58 tests including edge cases
- **API Compatibility**: Complete phyloland parameter support

## Citation

If you use this implementation, please cite both this work and the original phyloland paper. See `remake/CITATION.md` for details.

## License

[License information to be added]

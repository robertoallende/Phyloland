# Unit 01: Foundation

## Objective
Establish the Python package structure, testing framework, and development environment for the Phyloland implementation. Create a clean, installable package with proper dependency management and shared test data structure.

## Implementation

### Repository Structure
Create three-folder structure with shared test data:
```
Phyloland/
├── discover/          # Original R package + research (existing)
├── remake/            # Python implementation
│   ├── dev_log/       # MMDD documentation (existing)
│   ├── phyloland/     # Main Python package
│   ├── tests/         # Python test suite
│   ├── requirements.txt
│   └── setup.py
└── test_data/         # SHARED test data for both R and Python
    ├── banza/         # Real Banza dataset
    ├── minimal/       # Simple test cases
    ├── intermediate/  # Medium complexity
    └── reference/     # R-generated expected outputs
```

### Python Package Structure
```
remake/phyloland/
├── __init__.py        # Package initialization
├── core/              # Core algorithm modules
│   └── __init__.py
├── mcmc/              # MCMC engine
│   └── __init__.py
├── utils/             # Utilities (distance, I/O)
│   └── __init__.py
└── data/              # Sample data files
    └── __init__.py
```

### Testing Framework
```
remake/tests/
├── conftest.py        # pytest configuration
├── test_dependencies/ # Unit 02 dependency validation tests
├── test_core/         # Core algorithm tests
└── test_integration/  # End-to-end tests
```

### Dependencies
- **Core scientific stack**: numpy, scipy, pandas
- **Phylogenetic trees**: dendropy
- **Testing**: pytest, pytest-cov
- **Development install**: `pip install -e .`
- **PEP 8 compliance**: absolute imports only

### Shared Test Data
Copy existing Banza dataset from discover/ to shared test_data/:
- Locations file: `test_data/banza/locations_Banza.txt`
- Tree files: `test_data/banza/tree_Banza.nex`
- Reference outputs: `test_data/reference/` (for validation)

## AI Interactions
1. **Context establishment**: Discussed repository structure and dependency management
2. **Design decisions**: Resolved package naming, import style, and test data sharing
3. **Structure planning**: Defined clean separation between discovery, implementation, and test data

## Files Modified
- `remake/phyloland/__init__.py` - Package initialization
- `remake/phyloland/core/__init__.py` - Core module
- `remake/phyloland/mcmc/__init__.py` - MCMC module  
- `remake/phyloland/utils/__init__.py` - Utilities module
- `remake/phyloland/data/__init__.py` - Data module
- `remake/tests/conftest.py` - pytest configuration
- `remake/requirements.txt` - Python dependencies
- `remake/setup.py` - Package installation configuration
- `test_data/banza/` - Shared Banza dataset
- `test_data/reference/` - Reference output directory

## Status: Complete
**Implementation completed successfully:**
- ✅ Package structure created and importable
- ✅ All dependencies install without errors (virtual environment created)
- ✅ pytest runs successfully with **6 foundation tests passing**
- ✅ Shared test data accessible (Banza dataset copied to test_data/banza/)
- ✅ Clean development environment established

**Validation Tests (6/6 passing):**
- ✅ `test_package_structure()` - All modules importable, version correct
- ✅ `test_module_docstrings()` - All modules properly documented
- ✅ `test_shared_data_access()` - Banza dataset accessible and non-empty
- ✅ `test_reference_data_directory()` - Reference data directory ready
- ✅ `test_test_directory_structure()` - Test organization correct
- ✅ `test_dependencies_importable()` - All 8 dependencies work correctly

**Key achievements:**
- Virtual environment created at `remake/venv/` to handle system package restrictions
- All 8 dependencies installed successfully (numpy, scipy, pandas, dendropy, pytest, etc.)
- Package imports work: `import phyloland` successful
- Test framework ready: pytest 9.0.2 configured with shared fixtures
- Banza dataset available in shared location for both R and Python validation
- **Automated validation** ensures foundation is solid

**Files created:**
- Complete package structure with proper `__init__.py` files
- `setup.py` with development installation configuration
- `requirements.txt` with pinned dependency versions
- `conftest.py` with shared test fixtures
- `tests/test_foundation.py` with 6 validation tests
- Shared `test_data/banza/` with locations and tree files

**Ready for Unit 02: Dependencies** - Foundation is solid and all prerequisites met.

# Unit 03: Base Cases - Subunit 3.1: Single Location

## Objective
Implement the trivial phylogeographic case: single tip tree with single location. This validates the basic likelihood calculation framework and establishes the foundation for more complex scenarios.

## Problem Analysis
**Mathematical Case**: With only one location and one tip, no dispersal events are possible.
- **Input**: 1-tip tree, 1 geographic coordinate
- **Process**: No internal nodes, no dispersal decisions
- **Expected Output**: Likelihood = 1 (observed data is certain)
- **Parameters**: No dispersal parameters to estimate

**Why This Matters**: This trivial case ensures our likelihood calculation framework produces correct results before adding complexity.

## Design Decisions

### 1. R Reference Strategy
- **Issue**: How to generate meaningful reference for trivial case
- **Decision**: Use phyloland package with minimal input, capture all outputs
- **Rationale**: Even trivial cases exercise the full algorithm machinery

### 2. Test Coverage
- **Issue**: What to validate in a trivial case
- **Decision**: Likelihood value, parameter handling, data structure consistency
- **Rationale**: Establishes baseline behavior for complex cases

### 3. Implementation Scope
- **Issue**: How much infrastructure to build for trivial case
- **Decision**: Full likelihood framework, minimal dispersal components
- **Rationale**: Framework must support future complexity additions

## Implementation Strategy

### Phase 1: R Reference Generation
```r
# discover/test_scripts/generate_single_location_reference.R
library(phyloland)

# Create minimal test case
tree_text <- "(tip1:1.0);"
tree <- read.tree(text = tree_text)
locations <- data.frame(
  species = "tip1",
  latitude = 21.0,
  longitude = -157.0
)

# Run phyloland with minimal parameters
result <- phyloland_main(
  tree = tree,
  locations = locations,
  # Minimal MCMC for reference generation
  Nstep = 10,
  # Fixed parameters for reproducibility
  Lambda = 1.0,
  sigma = c(1.0, 1.0),
  lambda = 1.0
)

# Save reference outputs
```

### Phase 2: Python Test Implementation
```python
# remake/tests/test_base_cases/test_single_location.py
def test_single_location_likelihood():
    """Test trivial case produces likelihood = 1"""
    
def test_single_location_parameters():
    """Test parameter handling with no dispersal events"""
    
def test_single_location_data_structures():
    """Test tree and location data processing"""
```

### Phase 3: Core Implementation
```python
# remake/phyloland/core/base_cases.py
class SingleLocationCase:
    def __init__(self, tree, locations):
        # Validate inputs
        # Set up data structures
        
    def calculate_likelihood(self, params):
        # Trivial case: return 1.0
        
    def get_dispersal_events(self):
        # Trivial case: return empty list
```

## Test Coverage

### Core Functionality
- [ ] **Likelihood calculation**: Returns 1.0 for trivial case
- [ ] **Parameter handling**: Accepts but doesn't use dispersal parameters
- [ ] **Tree processing**: Correctly handles single-tip tree
- [ ] **Location processing**: Correctly handles single coordinate

### Data Validation
- [ ] **Input validation**: Rejects invalid tree/location combinations
- [ ] **Output format**: Consistent with multi-location cases
- [ ] **Error handling**: Graceful failure for malformed inputs

### Integration Points
- [ ] **API consistency**: Same interface as complex cases
- [ ] **Data structures**: Compatible with future extensions
- [ ] **Parameter objects**: Proper handling of unused parameters

## Success Criteria
- [ ] Python likelihood matches R reference exactly (= 1.0)
- [ ] All data structures properly initialized
- [ ] Parameter objects handled correctly (even if unused)
- [ ] API established for complex cases
- [ ] Tests pass with 100% coverage

## Status: Complete
**Implementation Summary:**
- Created R reference script generating trivial single location case (likelihood = 1.0)
- Generated minimal test data: single-tip Nexus tree and single coordinate
- Implemented Python tests validating against R reference data
- Created SingleLocationCase class with tree/location loading and likelihood calculation
- All tests pass: likelihood = 1.0, data structures correct, validation working

**Files Created:**
- `discover/test_scripts/generate_single_location_reference.R` - R reference generation
- `test_data/minimal/single_tip.nex` - Minimal single-tip tree
- `test_data/minimal/single_location.txt` - Single coordinate data
- `test_data/reference/single_location_reference.csv` - Reference validation data
- `remake/tests/test_base_cases/test_single_location.py` - Python validation tests
- `remake/phyloland/core/base_cases.py` - Core implementation

**Key Achievement:** Established the **basic likelihood calculation framework** and data loading infrastructure. The trivial case (likelihood = 1.0) validates that our mathematical foundation is correct before adding complexity.

**Mathematical Validation:** Single location case correctly produces likelihood = 1.0 as expected - no dispersal events possible, observed data is certain.

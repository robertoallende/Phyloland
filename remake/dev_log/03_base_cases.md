# Unit 03: Base Cases

## Objective
Implement the simplest phylogeographic scenarios using the inductive algorithm structure. These base cases validate core likelihood calculations and dispersal mechanics before adding complexity in later units.

## Implementation Strategy

### Inductive Approach
Following the algorithm's natural structure from research analysis:
1. **Level 0**: Single location (trivial case)
2. **Level 1**: Two locations (minimal dispersal)  
3. **Level 2**: No competition (pure dispersal patterns)

Each level builds on the previous, establishing mathematical foundations incrementally.

### TDD with R-as-Oracle
1. **Generate R reference data** using phyloland package for each base case
2. **Write Python tests first** comparing against R outputs
3. **Implement Python code** until all tests pass
4. **Validate mathematical correctness** through systematic comparison

## 3 Atomic Subunits

### **3.1: Single Location** 
- **Scenario**: 1 tip tree, 1 geographic location
- **Mathematical case**: No dispersal events possible, likelihood = 1
- **Purpose**: Validates basic likelihood calculation framework
- **R reference**: Trivial phyloland call with single tip/location

### **3.2: Two Locations**
- **Scenario**: 2 tip tree (1 internal node), 2 locations
- **Mathematical case**: 1 dispersal event, simple rate matrix (2×2)
- **Purpose**: Tests core dispersal mechanics and rate calculations
- **R reference**: Minimal phyloland scenario with known dispersal event

### **3.3: No Competition (λ = 1)**
- **Scenario**: Multiple tips/locations, competition parameter λ = 1
- **Mathematical case**: All locations equally accessible
- **Purpose**: Isolates pure dispersal patterns from competition effects
- **R reference**: Multi-location phyloland with lambda fixed at 1

## Mathematical Foundations

### Core Equations (from research)
- **Dispersal kernel**: `f(x,y) = exp(-Σ(xi-yi)²/2σi²)`
- **Rate matrix**: `Rij = Λ * Fij * δj`
- **Competition factor**: `δj = λ` (occupied) or `1` (unoccupied)
- **Likelihood**: Product over dispersal events in phylogeny

### Base Case Simplifications
- **3.1**: No dispersal → R matrix not needed, L = 1
- **3.2**: Single dispersal → 2×2 R matrix, simple calculation
- **3.3**: λ = 1 → δj = 1 always, competition effects removed

## File Organization

```
discover/test_scripts/
├── generate_base_case_references.R    # R reference generation

test_data/reference/
├── single_location_reference.csv      # 3.1 reference data
├── two_locations_reference.csv        # 3.2 reference data  
└── no_competition_reference.csv       # 3.3 reference data

remake/tests/test_base_cases/
├── test_single_location.py            # 3.1 validation tests
├── test_two_locations.py              # 3.2 validation tests
└── test_no_competition.py             # 3.3 validation tests

remake/phyloland/core/
├── base_cases.py                       # Core implementations
├── likelihood.py                       # Likelihood calculations
└── rate_matrix.py                      # Rate matrix construction
```

## Success Criteria
- [ ] All 3 subunits complete with passing tests
- [ ] Python results match R references exactly
- [ ] Mathematical foundations validated for complex cases
- [ ] Core algorithm components implemented and tested
- [ ] Inductive structure established for Units 4-7

## AI Interactions
1. **Research analysis**: Identified inductive algorithm structure from papers
2. **Unit planning**: Designed base cases following mathematical complexity
3. **TDD strategy**: Established R-as-oracle validation approach

## Status: Complete
**Implementation Summary:**
All 3 atomic subunits completed with passing validation tests:

- **3.1: Single Location** ✅ - Trivial case (likelihood = 1.0), basic framework established
- **3.2: Two Locations** ✅ - Core dispersal mechanics (2×2 rate matrix, geographic distance, dispersal kernel)
- **3.3: No Competition** ✅ - Multi-location framework (5×5 rate matrix, λ=1 constraint, Hawaiian islands)

**Inductive Foundation Established:** Successfully validated phylogeographic inference from trivial cases to realistic multi-location scenarios. All Python calculations match R implementation exactly within numerical precision.

**Files Created:**
- 3 R reference generation scripts in `discover/test_scripts/`
- 6 minimal test data files (trees, locations) in `test_data/minimal/`
- 7 reference validation files in `test_data/reference/`
- 3 comprehensive Python test suites in `remake/tests/test_base_cases/`
- Complete base case implementations in `remake/phyloland/core/base_cases.py`

**Mathematical Validation:**
- Geographic distance calculation matches R distkm exactly
- Dispersal kernel f(x,y) = exp(-Σ(xi-yi)²/2σi²) validated
- Rate matrix construction Rij = Λ * Fij * δj with proper normalization
- Multi-location framework ready for competition and MCMC integration

**Key Achievement:** Established the **complete mathematical and software foundation** for phylogeographic inference through systematic inductive validation. Ready for Units 4-7 implementation.

# Unit 02: Dependencies

## Objective
Validate that Python dependencies behave identically to their R counterparts using Test-Driven Development. This unit serves as a "dependency firewall" ensuring any differences in final results come from our algorithm implementation, not from library discrepancies.

## Implementation

### Strategy
Use R implementation as oracle for correctness validation:
1. **Generate R reference data** using scripts in `discover/test_scripts/`
2. **Write Python tests first** comparing against R references
3. **Implement Python wrappers** until all tests pass
4. **Validate continuously** with atomic subunit approach

### 5 Atomic Subunits

#### **02a: Tree Parsing** (DendroPy vs ape)
- **Critical Risk**: Different Nexus parsing breaks entire algorithm
- **Validation**: Same tip names, node count, branch lengths, topology
- **Test Data**: Banza tree file from shared test_data/

#### **02b: Geographic Distance** (NumPy/geopy vs R distkm)
- **Critical Risk**: Distance errors propagate through dispersal calculations  
- **Validation**: Results within 1 meter tolerance
- **Test Data**: Hawaiian island coordinates

#### **02c: Random Numbers** (NumPy vs R RNG)
- **Critical Risk**: Different RNG affects MCMC convergence patterns
- **Validation**: Statistical properties (K-S tests), not exact sequences
- **Test Data**: Distribution samples (uniform, normal, exponential)

#### **02d: File I/O** (pandas vs R read.table)
- **Critical Risk**: Data loading differences corrupt input processing
- **Validation**: Identical data types, values, column handling
- **Test Data**: Banza locations file

#### **02e: Matrix Operations** (NumPy vs R)
- **Critical Risk**: Precision errors accumulate in rate matrix calculations
- **Validation**: Numerical precision within acceptable tolerance
- **Test Data**: Matrix operations used in dispersal rate calculations

### TDD Workflow per Subunit
1. **Create R reference script** in `discover/test_scripts/`
2. **Generate reference outputs** to `test_data/reference/`
3. **Write failing Python tests** in `remake/tests/test_dependencies/`
4. **Implement Python code** until tests pass
5. **Document any systematic differences**

### File Organization
```
discover/test_scripts/          # R reference generation (created as needed)
├── generate_tree_references.R
├── generate_distance_references.R  
├── generate_rng_references.R
├── generate_io_references.R
└── generate_matrix_references.R

test_data/reference/            # Shared reference outputs
├── tree_parsing_reference.csv
├── distance_reference.csv
├── rng_reference.csv
├── io_reference.csv
└── matrix_reference.csv

remake/tests/test_dependencies/ # Python validation tests
├── test_tree_parsing.py
├── test_geographic_distance.py
├── test_random_numbers.py
├── test_file_io.py
└── test_matrix_operations.py
```

## AI Interactions
1. **Context establishment**: Discussed dependency validation strategy and TDD approach
2. **Structure planning**: Defined atomic subunits and file organization
3. **Risk assessment**: Identified critical failure points for each dependency

## Files Modified
*Files will be created during subunit implementation following TDD approach*

## Status: In Progress
**Next steps:**
1. Create subunit 02a: Tree Parsing validation
2. Generate R reference script for tree parsing
3. Write failing Python tests
4. Implement until tests pass
5. Repeat for remaining 4 subunits

**Success criteria:**
- [ ] All 5 subunits complete with passing tests
- [ ] Python libraries validated against R equivalents
- [ ] Any systematic differences documented and justified
- [ ] Dependency firewall established for algorithm implementation

**Completion target**: All subunits passing validation tests, providing confidence that Python stack behaves equivalently to R implementation.

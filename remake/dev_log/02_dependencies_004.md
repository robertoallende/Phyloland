# Unit 02: Dependencies - Subunit 2.4: File I/O

## Objective
Validate that pandas reads CSV/text files identically to R's read.table/read.csv, ensuring consistent data loading, column types, and value parsing for phylogeographic data processing.

## Problem Analysis
**Core Issue**: File I/O differences can corrupt the entire analysis pipeline:
- **Column type mismatches**: Strings vs factors vs numeric
- **Missing value handling**: Different NA representations
- **Decimal precision**: Floating point parsing differences
- **Header parsing**: Column name interpretation

**Why Critical**: Location data and tree metadata must be parsed identically to maintain coordinate precision and species matching.

## Design Decisions

### 1. Test Data Strategy
- **Issue**: Need representative phylogeographic data files
- **Decision**: Use existing Banza dataset files from test_data/
- **Rationale**: Real data reveals actual parsing edge cases

### 2. Validation Approach
- **Issue**: How to compare data frames between R and Python
- **Decision**: Export R data frame to CSV, compare with pandas output
- **Rationale**: Avoids cross-language data structure comparison complexity

### 3. Precision Tolerance
- **Issue**: Floating point representation differences
- **Decision**: 1e-10 tolerance for coordinates, exact match for strings/integers
- **Rationale**: Geographic coordinates need high precision, categorical data must be exact

### 4. Column Type Validation
- **Issue**: R factors vs Python strings, different numeric types
- **Decision**: Focus on value equivalence, document type mapping
- **Rationale**: Algorithm cares about values, not specific type representations

## Test Coverage

### Core File Types
- [ ] **CSV files**: Comma-separated location data
- [ ] **Tab-delimited**: Alternative delimiter handling
- [ ] **Headers**: Column name parsing and preservation
- [ ] **Missing values**: NA, NULL, empty string handling

### Data Type Validation
- [ ] **Numeric precision**: Latitude/longitude coordinates
- [ ] **String handling**: Species names, location labels
- [ ] **Integer preservation**: Sample counts, indices
- [ ] **Boolean values**: Presence/absence data

### Edge Cases
- [ ] **Special characters**: Unicode in species names
- [ ] **Whitespace**: Leading/trailing spaces in values
- [ ] **Quote handling**: Embedded commas in quoted fields
- [ ] **Empty files**: Zero-row data handling

## Implementation Strategy

### Phase 1: R Reference Generation
```r
# discover/test_scripts/generate_io_references.R
# Read Banza location data with R
locations <- read.csv("../../test_data/banza/locations.csv", stringsAsFactors=FALSE)

# Export detailed structure information
io_reference <- data.frame(
  column = names(locations),
  type = sapply(locations, class),
  sample_value = sapply(locations, function(x) as.character(x[1])),
  row_count = nrow(locations),
  col_count = ncol(locations)
)

# Save both data and metadata
write.csv(locations, "../../test_data/reference/io_data_reference.csv", row.names=FALSE)
write.csv(io_reference, "../../test_data/reference/io_structure_reference.csv", row.names=FALSE)
```

### Phase 2: Python Test Implementation
```python
# remake/tests/test_dependencies/test_file_io.py
def test_csv_data_equivalence():
    """Test pandas reads same data values as R read.csv"""
    
def test_column_structure():
    """Test column names and count match R parsing"""
    
def test_numeric_precision():
    """Test coordinate precision within tolerance"""
    
def test_missing_value_handling():
    """Test NA/NULL handling matches R behavior"""
```

### Phase 3: Implementation Until Tests Pass
- Handle any systematic differences in parsing
- Document pandas vs R read.csv behavior
- Ensure phylogeographic data loads correctly

## Success Criteria
- [ ] Data values match R reference within tolerance
- [ ] Column structure (names, count) identical
- [ ] Numeric precision preserved for coordinates
- [ ] Missing value handling equivalent
- [ ] Edge cases handled appropriately
- [ ] No data corruption during file loading

## Status: Complete
**Implementation Summary:**
- Created R reference script reading Banza location data with read.table
- Generated reference CSV with data values and structure metadata
- Implemented Python tests validating pandas reads identical data to R
- All tests pass: data values, column structure, numeric precision, data types match
- Validated pandas file I/O is equivalent to R for phylogeographic data loading

**Files Created:**
- `discover/test_scripts/generate_io_references.R` - R reference data generation
- `test_data/reference/io_data_reference.csv` - Data values reference
- `test_data/reference/io_structure_reference.csv` - Structure metadata reference  
- `remake/tests/test_dependencies/test_file_io.py` - Python validation tests

**Key Finding:** Pandas and R read.table produce identical results for tab-delimited phylogeographic data. High-precision coordinates (1e-10 tolerance) are preserved correctly.

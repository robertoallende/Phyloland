# Unit 02: Dependencies - Subunit 2.1: Tree Parsing

## Objective
Validate that DendroPy parses Nexus files identically to R's ape package, ensuring consistent tree structure, node relationships, and branch lengths for accurate likelihood calculations.

## Problem Analysis
**Core Issue**: DendroPy and R ape might parse the same Nexus file differently, causing:
- Different node numbering/ordering systems
- Inconsistent tip name sequences  
- Different branch length interpretations
- Altered tree topology representation

**Why Critical**: Entire likelihood calculation depends on correct tree traversal and node relationships. Any parsing differences will cascade through the algorithm.

## Design Decisions

### 1. Node Numbering Convention
- **Issue**: R ape uses specific numbering (tips 1-n, internals n+1 to n+m)
- **Decision**: Create mapping functions rather than forcing DendroPy to match ape numbering
- **Rationale**: Less fragile, maintains library independence

### 2. Branch Length Precision
- **Issue**: Floating-point precision differences between libraries
- **Decision**: Tolerance level of 1e-10 for branch lengths
- **Rationale**: High precision needed for accurate dispersal calculations

### 3. Tip Name Ordering
- **Issue**: Libraries might return tip names in different orders
- **Decision**: Always sort tip names for consistent comparison
- **Rationale**: Eliminates ordering dependencies, ensures reproducible results

### 4. Tree Format Coverage
- **Issue**: Nexus format has many variations
- **Decision**: Start with Banza tree, add edge cases if validation fails
- **Rationale**: Incremental approach, focus on working case first

### 5. Error Handling Strategy
- **Issue**: DendroPy might fail to parse what ape can parse
- **Decision**: Fail fast with clear error messages
- **Rationale**: Better to catch incompatibilities early than debug later

## Implementation Strategy

### Phase 1: R Reference Generation
```r
# discover/test_scripts/generate_tree_references.R
library(ape)
tree <- read.nexus("../../test_data/banza/tree_Banza.nex")

reference <- list(
  n_tips = length(tree$tip.label),
  n_nodes = tree$Nnode,
  tip_names = sort(tree$tip.label),  # Sorted for consistency
  edge_matrix = tree$edge,
  edge_lengths = tree$edge.length,
  node_count = nrow(tree$edge),
  tree_length = sum(tree$edge.length)
)

write.csv(reference, "../../test_data/reference/tree_parsing_reference.csv")
```

### Phase 2: Python Test Implementation
```python
# remake/tests/test_dependencies/test_tree_parsing.py
def test_basic_tree_structure():
    """Validate basic tree properties match R ape"""
    python_tree = dendropy.Tree.get(path="tree_Banza.nex", schema="nexus")
    r_reference = pd.read_csv("tree_parsing_reference.csv")
    
    assert len(python_tree.leaf_nodes()) == r_reference['n_tips']
    assert python_tree.internal_node_count() == r_reference['n_nodes']

def test_tip_names_consistency():
    """Validate tip names match exactly"""
    python_tips = sorted([node.taxon.label for node in python_tree.leaf_nodes()])
    r_tips = sorted(r_reference['tip_names'])
    assert python_tips == r_tips

def test_branch_lengths_precision():
    """Validate branch lengths within tolerance"""
    python_lengths = [edge.length for edge in python_tree.edges()]
    r_lengths = r_reference['edge_lengths']
    np.testing.assert_allclose(python_lengths, r_lengths, rtol=1e-10)
```

### Phase 3: Implementation Until Tests Pass
- Create DendroPy wrapper functions if needed
- Handle any API differences between libraries
- Ensure consistent tree representation

## Test Coverage

### Basic Structure Tests
- [ ] Node counts (tips and internal nodes)
- [ ] Tip name consistency and ordering
- [ ] Tree topology verification

### Detailed Comparison Tests  
- [ ] Edge matrix comparison
- [ ] Branch length validation (1e-10 precision)
- [ ] Total tree length calculation

### Edge Case Tests
- [ ] Trees with polytomies (if present)
- [ ] Trees with missing branch lengths
- [ ] Trees with special characters in tip names

## Identified Risks

### High Risk
- **API Incompatibility**: DendroPy and ape have fundamentally different tree representations
- **Nexus Format Variations**: Different handling of comments, formatting, special characters
- **Precision Loss**: Floating-point differences accumulate in complex calculations

### Medium Risk
- **Memory Representation**: Different internal tree structures affect traversal order
- **Node Indexing**: Inconsistent numbering systems break likelihood calculations
- **Performance**: DendroPy significantly slower than ape for large trees

### Low Risk
- **Tip Name Encoding**: Unicode/ASCII differences in species names
- **Branch Length Units**: Different interpretations of time/distance units

## Success Criteria
- [ ] DendroPy loads Banza tree without errors
- [ ] All structural properties match R ape within tolerance
- [ ] Tip names and ordering consistent (sorted comparison)
- [ ] Branch lengths within 1e-10 precision
- [ ] Tree traversal produces equivalent node sequences
- [ ] All edge case tests pass

## AI Interactions
1. **Problem analysis**: Identified critical tree parsing validation requirements
2. **Design decisions**: Made 5 key architectural choices with clear rationales
3. **Risk assessment**: Categorized potential issues by severity and likelihood
4. **Test strategy**: Defined comprehensive validation approach with specific tolerances

## Files Modified
*To be created during implementation:*
- `discover/test_scripts/generate_tree_references.R`
- `test_data/reference/tree_parsing_reference.csv`
- `remake/tests/test_dependencies/test_tree_parsing.py`
- `remake/phyloland/utils/tree_parsing.py` (if wrapper needed)

## Status: Complete
**Implementation completed successfully:**
- ✅ R reference generation script created and working
- ✅ Reference data generated (4 properties, 21 tips, 40 edges)
- ✅ Python tests implemented with 7 comprehensive test cases
- ✅ All tests passing (7/7) with proper API fixes

**Key findings:**
- **DendroPy API differences**: Used `internal_nodes()` instead of `internal_node_count()`
- **Root edge handling**: DendroPy includes root edge (length=None), R doesn't - filtered appropriately
- **Precision validation**: Branch lengths match within 1e-10 tolerance
- **Tip name consistency**: Perfect match between libraries when sorted
- **Tree structure**: Both libraries produce equivalent tree representations

**Validation results:**
- ✅ Tree loads successfully without errors
- ✅ Basic properties match (21 tips, 20 internal nodes, 40 edges)
- ✅ Tip names identical between DendroPy and R ape
- ✅ Branch lengths match within 1e-10 precision
- ✅ Total tree length matches R calculation
- ✅ Tree structure integrity validated
- ✅ Edge consistency confirmed (handling root edge difference)

**Files created:**
- `discover/test_scripts/generate_tree_references.R` - R reference generation
- `test_data/reference/tree_*.csv` - Reference data files
- `remake/tests/test_dependencies/test_tree_parsing.py` - Python validation tests

**Tree parsing dependency validated** - DendroPy behaves equivalently to R ape for Banza dataset.

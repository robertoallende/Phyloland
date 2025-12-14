# Unit 04: Neutral Dispersal

## Objective
Implement realistic phylogeographic inference for multiple locations and species without competition effects (λ = 1). This unit handles full dataset complexity while maintaining mathematical simplicity, bridging the validated foundation from Unit 3 to ecological realism in Unit 5.

## Implementation Strategy

### Complexity Scaling
Building on Unit 3's validated foundation:
- **Unit 3**: Simple cases (1, 2, 5 locations) - mathematical validation
- **Unit 4**: Realistic complexity (21 locations, 21 species) - computational validation
- **Unit 5**: Add competition effects - ecological validation

### TDD with Full Dataset
1. **Generate R reference data** using complete Banza dataset with λ = 1
2. **Write Python tests first** comparing against R outputs for realistic scenarios
3. **Implement scalable algorithms** until all tests pass
4. **Optimize performance** for computational efficiency

## 3 Atomic Subunits

### **4.1: Dispersal Kernel Implementation**
- **Objective**: Robust dispersal kernel calculation for realistic datasets
- **Challenge**: Handle 21×21 pairwise calculations, parameter sensitivity, edge cases
- **Focus**: Numerical stability, computational efficiency, validation against R
- **Output**: Optimized dispersal kernel computation for full Banza dataset

### **4.2: Rate Matrix Construction**
- **Objective**: Efficient n×n rate matrix construction for large phylogeographic datasets
- **Challenge**: 21×21 matrix construction, memory management, matrix properties validation
- **Focus**: Scalable algorithms, proper normalization, computational performance
- **Output**: Complete rate matrix construction matching R phyloland exactly

### **4.3: Multi-location Likelihood Calculation**
- **Objective**: End-to-end likelihood computation for realistic phylogenetic trees
- **Challenge**: Complex tree traversal, multiple dispersal events, numerical precision
- **Focus**: Complete algorithm integration, likelihood accuracy, performance optimization
- **Output**: Full phylogeographic likelihood calculation validated against R

## Mathematical Foundations

### Core Equations (Neutral Dispersal)
- **Dispersal kernel**: `f(x,y) = exp(-Σ(xi-yi)²/2σi²)` (optimized for n×n calculations)
- **Rate matrix**: `Rij = Λ * Fij` (no competition: δj = 1 always)
- **Likelihood**: Complete phylogenetic likelihood without competition terms
- **Parameter space**: σ₁, σ₂ (dispersal parameters), Λ (overall rate)

### Computational Challenges
- **Matrix scaling**: 21×21 = 441 pairwise calculations
- **Tree complexity**: 21 tips, 20 internal nodes, multiple dispersal events
- **Numerical precision**: Maintain accuracy across realistic parameter ranges
- **Performance**: Efficient computation for MCMC applications

## Test Data Strategy

### Full Banza Dataset
- **21 species**: Complete Hawaiian cricket phylogeny
- **21 locations**: All Hawaiian islands with precise coordinates
- **Realistic tree**: Complex topology with known evolutionary relationships
- **Known parameters**: Use established σ, Λ values from literature

### Validation Approach
- **Component testing**: Each subunit validated independently
- **Integration testing**: End-to-end likelihood calculation
- **Performance benchmarking**: Computational efficiency vs R
- **Numerical accuracy**: Precision validation across parameter space

## File Organization

```
discover/test_scripts/
├── generate_neutral_dispersal_references.R    # Full dataset R references

test_data/banza/
├── tree_Banza.nex                            # Complete 21-tip tree
├── locations_Banza.txt                       # 21 Hawaiian coordinates
└── (existing files)

test_data/reference/
├── neutral_dispersal_kernels.csv             # 21×21 kernel matrix
├── neutral_dispersal_rates.csv               # 21×21 rate matrix  
└── neutral_dispersal_likelihood.csv          # Complete likelihood

remake/tests/test_neutral_dispersal/
├── test_dispersal_kernels.py                 # 4.1 validation tests
├── test_rate_matrix.py                       # 4.2 validation tests
└── test_likelihood_calculation.py            # 4.3 validation tests

remake/phyloland/core/
├── dispersal.py                               # Optimized kernel calculations
├── rate_matrix.py                             # Scalable matrix construction
└── likelihood.py                              # Complete likelihood computation
```

## Success Criteria
- [ ] All 3 subunits complete with passing tests
- [ ] Python results match R references for full Banza dataset
- [ ] Computational performance suitable for MCMC applications
- [ ] Numerical accuracy maintained across realistic parameter ranges
- [ ] Scalable algorithms ready for competition integration (Unit 5)

## Performance Targets
- **Kernel calculation**: < 1ms for 21×21 matrix
- **Rate matrix construction**: < 10ms for complete matrix
- **Likelihood calculation**: < 100ms for full tree evaluation
- **Memory usage**: Efficient for repeated MCMC evaluations

## AI Interactions
1. **Unit planning**: Designed realistic complexity scaling from Unit 3 foundation
2. **Algorithm strategy**: Identified computational challenges and optimization needs
3. **Test strategy**: Established full dataset validation approach

## Status: Ready for Implementation
**Next steps:**
1. Create subunit 4.1: Dispersal Kernel Implementation
2. Generate R reference data using complete Banza dataset
3. Implement optimized kernel calculations
4. Validate performance and accuracy
5. Proceed through subunits 4.2 and 4.3

**Strategic goal**: Establish computationally efficient phylogeographic inference for realistic datasets, maintaining mathematical accuracy while preparing for ecological complexity in Unit 5.

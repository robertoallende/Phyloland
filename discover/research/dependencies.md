# R Dependencies Analysis & Python Alternatives

## R Package Dependencies

### Explicit Dependencies (from DESCRIPTION)

#### `ape` (Analysis of Phylogenetics and Evolution)
**Purpose**: Core phylogenetic tree manipulation
- **Functions used**: `read.nexus()`, tree structure handling, node operations
- **Critical for**: Loading phylogenetic trees, tree traversal, tip/node indexing
- **Why essential**: Provides standardized phylogenetic data structures and I/O

### Implicit Dependencies (Base R)

#### Graphics System
**Purpose**: Plotting and visualization
- **Functions used**: `plot()`, `hist()`, `par()`, `x11()`, `pdf()`, `dev.off()`, `abline()`
- **Critical for**: MCMC diagnostics, parameter distributions, tree visualization
- **Why needed**: User feedback and result interpretation

#### File I/O System  
**Purpose**: Data input/output operations
- **Functions used**: `read.table()`, `read.csv()`, `write.csv()`, `readLines()`
- **Critical for**: Loading location data, saving MCMC results, configuration files
- **Why needed**: Data exchange with external tools

#### Statistical Functions
**Purpose**: Random number generation and distributions
- **Functions used**: `runif()`, `rnorm()`, `sample()`, statistical summaries
- **Critical for**: MCMC sampling, parameter initialization, convergence diagnostics
- **Why needed**: Bayesian inference engine

### C Library Dependencies

#### `R.h` & `Rmath.h`
**Purpose**: R's C API and mathematical functions
- **Functions used**: `Rprintf()`, `GetRNGstate()`, `PutRNGstate()`, distribution functions
- **Critical for**: Integration with R, random number generation, mathematical operations
- **Why essential**: Performance-critical MCMC computations

#### Standard C Libraries
**Purpose**: Basic C functionality
- **Libraries**: `stdio.h`, `stdlib.h`, `math.h`
- **Functions used**: Memory allocation, mathematical functions, I/O operations
- **Critical for**: Core algorithmic implementation

## Python Alternatives Mapping

| R Dependency | Purpose | Python Alternatives | **Recommended** | Notes |
|--------------|---------|-------------------|-----------------|-------|
| **ape** | Phylogenetic trees | DendroPy, ETE3, Bio.Phylo, toytree | **DendroPy** | Most comprehensive, handles Nexus well |
| **Base Graphics** | Plotting/visualization | matplotlib, seaborn, plotly | **matplotlib** | Most mature, R-like interface available |
| **File I/O** | Data input/output | pandas, csv, pathlib | **pandas** | Excellent for tabular data, handles multiple formats |
| **Statistical Functions** | Random numbers, distributions | NumPy, SciPy.stats | **NumPy + SciPy** | NumPy for basic, SciPy for advanced distributions |
| **Rmath.h** | Mathematical functions | NumPy, SciPy, math | **NumPy** | Vectorized operations, similar function coverage |
| **R.h** | R integration | ctypes, Cython, pybind11 | **NumPy + Numba** | Pure Python approach, JIT compilation |

## Detailed Python Alternatives

### Phylogenetic Tree Handling

#### **DendroPy** (Recommended)
- **Pros**: Comprehensive phylogenetic library, excellent Nexus support, tree manipulation
- **Cons**: Can be slower than alternatives, learning curve
- **Key features**: Tree I/O, node traversal, branch length handling

#### ETE3
- **Pros**: Fast, good visualization, active development
- **Cons**: Different API paradigm, less standardized formats
- **Key features**: Tree visualization, fast operations

#### Bio.Phylo (Biopython)
- **Pros**: Part of Biopython ecosystem, stable
- **Cons**: Limited functionality compared to DendroPy
- **Key features**: Basic tree operations, multiple format support

### Visualization

#### **matplotlib** (Recommended)
- **Pros**: R-like plotting interface (pyplot), extensive customization, publication quality
- **Cons**: Verbose syntax, steeper learning curve
- **Key features**: Histograms, scatter plots, statistical plots

#### seaborn
- **Pros**: Statistical plotting, beautiful defaults, pandas integration
- **Cons**: Less flexible than matplotlib, focused on statistical plots
- **Key features**: Distribution plots, correlation matrices

### Data Handling

#### **pandas** (Recommended)
- **Pros**: Excellent CSV/TSV handling, data manipulation, R-like data frames
- **Cons**: Memory overhead for simple operations
- **Key features**: read_csv(), data filtering, groupby operations

#### NumPy
- **Pros**: Fast, memory efficient, fundamental arrays
- **Cons**: Less convenient for mixed data types
- **Key features**: Array operations, basic I/O

### Mathematical Operations

#### **NumPy** (Recommended for basic math)
- **Pros**: Vectorized operations, broadcasting, extensive function library
- **Cons**: Limited statistical distributions
- **Key features**: Array math, linear algebra, random numbers

#### **SciPy** (Recommended for advanced stats)
- **Pros**: Comprehensive statistical functions, optimization, special functions
- **Cons**: Larger dependency, some functions slower than NumPy
- **Key features**: Statistical distributions, optimization, interpolation

### Performance Optimization

#### **Numba** (Recommended)
- **Pros**: JIT compilation, minimal code changes, excellent NumPy integration
- **Cons**: Limited Python feature support, compilation overhead
- **Key features**: @jit decorator, automatic parallelization

#### Cython
- **Pros**: C-like performance, gradual optimization
- **Cons**: Requires compilation step, more complex deployment
- **Key features**: Static typing, C integration

## Migration Strategy

### Phase 1: Core Dependencies
1. **DendroPy** for phylogenetic tree handling
2. **NumPy/SciPy** for mathematical operations
3. **pandas** for data I/O

### Phase 2: Visualization & Diagnostics
1. **matplotlib** for plotting
2. **seaborn** for statistical plots (optional)

### Phase 3: Performance Optimization
1. **Numba** for MCMC acceleration
2. **multiprocessing** for parallel chains (optional)

### Phase 4: Advanced Features
1. **HDF5/PyTables** for large data storage
2. **Jupyter** for interactive analysis
3. **pytest** for comprehensive testing

## Compatibility Considerations

### Random Number Generation
- **R**: Uses specific RNG algorithms (Mersenne Twister)
- **Python**: NumPy uses different default RNG
- **Solution**: Implement R-compatible RNG or document differences

### Floating Point Precision
- **R**: Uses specific numerical libraries
- **Python**: NumPy may have different precision behavior
- **Solution**: Validate critical calculations against R implementation

### File Format Compatibility
- **R**: Specific Nexus parsing behavior in ape
- **Python**: DendroPy may parse differently
- **Solution**: Test with actual Phyloland data files

This dependency analysis provides the foundation for selecting appropriate Python libraries while maintaining compatibility with the original R implementation.

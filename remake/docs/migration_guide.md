# Migration Guide: R Phyloland → Python Phyloland

Complete guide for converting R phyloland workflows to Python phyloland.

## Quick Conversion

### R Code
```r
library(phyloland)

result <- PLD_interface(
  fileTREES="tree.nex",
  fileDATA="locations.txt", 
  num_step=1e5,
  freq=1e2,
  ess_lim=5e2
)
```

### Python Equivalent
```python
from phyloland.interface import PLD_interface

result = PLD_interface(
    fileTREES="tree.nex",
    fileDATA="locations.txt",
    num_step=100000,  # 1e5
    freq=100,         # 1e2  
    ess_lim=500       # 5e2
)
```

## Parameter Mapping

### Direct Equivalents
| R Parameter | Python Parameter | Notes |
|-------------|------------------|-------|
| `fileTREES` | `fileTREES` | Identical |
| `fileDATA` | `fileDATA` | Identical |
| `num_step` | `num_step` | Identical |
| `freq` | `freq` | Identical |
| `burnin` | `burnin` | Identical |
| `ess_lim` | `ess_lim` | Identical |
| `sigma` | `sigma` | Identical |
| `lambda` | `lambda_param` | Note parameter name |
| `tau` | `tau` | Identical |
| `num_step_sigma` | `num_step_sigma` | Identical |
| `num_step_lambda` | `num_step_lambda` | Identical |
| `num_step_tau` | `num_step_tau` | Identical |
| `names_locations` | `names_locations` | Identical |

### Python Extensions
| Python Parameter | Description |
|------------------|-------------|
| `n_chains` | Multi-chain MCMC (not in R version) |

## Result Structure Comparison

### R Results
```r
# Access results in R
sigma1_samples <- result$sigma1
sigma2_samples <- result$sigma2  
lambda_samples <- result$lambda
tau_samples <- result$tau
species_names <- result$tips
```

### Python Results  
```python
# Access results in Python
sigma1_samples = result['sigma1']
sigma2_samples = result['sigma2']
lambda_samples = result['lambda'] 
tau_samples = result['Lambda']      # Note: 'Lambda' not 'tau'
species_names = result['tips']
```

### Key Difference: tau vs Lambda
- **R**: Uses `tau` for migration rate parameter
- **Python**: Uses `Lambda` for migration rate parameter  
- **Values**: Numerically equivalent, just different naming

## File Format Compatibility

### Tree Files (NEXUS)
✅ **Fully Compatible** - Same NEXUS files work in both versions

### Location Files  
✅ **Fully Compatible** - Same tab-separated format

### Example Location File
```
species1	21.3099	-157.8581
species2	19.7362	-155.6069
species3	22.0644	-159.5456
```

## Real Example: Banza Tutorial

### Original R Code
```r
library(phyloland)

names_locations = c("Maui_Nui", "Maui_Nui", "Maui_Nui", "Maui_Nui", 
                   "Kauai", "Kauai", "Maui_Nui", "Maui_Nui", 
                   "Maui_Nui", "Maui_Nui", "Nihoa", "Nihoa",
                   "Hawaii", "Hawaii", "Hawaii", "Oahu", "Oahu",
                   "Maui_Nui", "Maui_Nui", "Oahu", "Oahu")

Banza <- PLD_interface(
  fileTREES="tree_Banza_posterior.nex", 
  fileDATA="locations_Banza.txt",
  num_step=1e3, 
  freq=1e2, 
  ess_lim=5e2,
  names_locations=names_locations
)
```

### Python Conversion
```python
from phyloland.interface import PLD_interface

names_locations = ["Maui_Nui", "Maui_Nui", "Maui_Nui", "Maui_Nui",
                  "Kauai", "Kauai", "Maui_Nui", "Maui_Nui", 
                  "Maui_Nui", "Maui_Nui", "Nihoa", "Nihoa",
                  "Hawaii", "Hawaii", "Hawaii", "Oahu", "Oahu",
                  "Maui_Nui", "Maui_Nui", "Oahu", "Oahu"]

Banza = PLD_interface(
    fileTREES="tree_Banza_posterior.nex",
    fileDATA="locations_Banza.txt", 
    num_step=1000,    # 1e3
    freq=100,         # 1e2
    ess_lim=500,      # 5e2
    names_locations=names_locations
)
```

## Result Analysis Comparison

### R Analysis
```r
# Parameter summaries in R
summary(Banza$sigma1)
summary(Banza$sigma2) 
summary(Banza$lambda)
summary(Banza$tau)

# Convergence check
Banza$mcmc$converged
```

### Python Analysis
```python
import numpy as np

# Parameter summaries in Python
print(f"σ₁: {np.median(Banza['sigma1']):.3f}")
print(f"σ₂: {np.median(Banza['sigma2']):.3f}")
print(f"λ: {np.median(Banza['lambda']):.3f}")
print(f"Λ: {np.median(Banza['Lambda']):.3f}")  # Note: Lambda

# Convergence check
print(f"Converged: {Banza['mcmc']['converged']}")
```

## Advanced Features

### Multi-Chain Analysis (Python Extension)
```python
# Not available in R phyloland
result = PLD_interface(
    fileTREES="tree.nex",
    fileDATA="locations.txt",
    n_chains=4,           # Run 4 independent chains
    ess_lim=500          # Higher convergence threshold
)

# Multi-chain convergence diagnostics
print(f"Multi-chain converged: {result['mcmc']['converged']}")
```

## Common Migration Issues

### 1. Scientific Notation
**R**: `1e5`, `1e2`, `5e2`  
**Python**: `100000`, `100`, `500` (or keep scientific notation)

### 2. Parameter Access
**R**: `result$parameter`  
**Python**: `result['parameter']`

### 3. tau vs Lambda
**R**: `result$tau`  
**Python**: `result['Lambda']` (note capitalization)

### 4. Vector vs Array
**R**: Vectors  
**Python**: NumPy arrays (mostly compatible)

## Performance Comparison

### Speed
- **Python**: Generally comparable to R
- **Large datasets**: Python may be faster due to NumPy optimizations
- **Memory**: Similar usage patterns

### Precision
- **Python**: Machine precision (1e-13 km tolerance)
- **R**: Reference implementation
- **Results**: Numerically equivalent within machine precision

## Workflow Integration

### R Workflow
```r
# Typical R phyloland workflow
library(phyloland)
result <- PLD_interface(...)
plot(result$sigma1)
write.csv(result$mcmc, "results.csv")
```

### Python Workflow  
```python
# Equivalent Python workflow
from phyloland.interface import PLD_interface
import matplotlib.pyplot as plt
import pandas as pd

result = PLD_interface(...)
plt.hist(result['sigma1'])
pd.DataFrame(result).to_csv("results.csv")
```

## Validation

### Numerical Equivalence
Both implementations should produce numerically equivalent results:

```python
# Python results should match R results within machine precision
# Differences typically < 1e-10 due to floating point arithmetic
```

### File Compatibility
- Same input files work in both versions
- Output formats can be made compatible with post-processing

## Troubleshooting

### Common Issues

#### "Different results from R"
- Check parameter names (tau vs Lambda)
- Verify same random seed if needed
- Ensure identical input files

#### "Import errors"
- Verify Python environment setup
- Check package installation
- Use virtual environment

#### "File format issues"
- Ensure tab-separated (not space-separated) location files
- Check NEXUS tree format validity
- Verify species name matching

### Getting Help
1. Check parameter mapping table above
2. Verify file formats are identical
3. Compare simple examples first
4. Review error messages carefully

## Best Practices

### Migration Strategy
1. **Start simple**: Convert basic examples first
2. **Validate results**: Compare outputs with R version
3. **Test thoroughly**: Use same datasets in both versions
4. **Document differences**: Note any workflow changes needed

### Code Organization
```python
# Recommended Python structure
from phyloland.interface import PLD_interface
import numpy as np
import matplotlib.pyplot as plt

def analyze_phylogeography(tree_file, location_file):
    """Phylogeographic analysis function"""
    result = PLD_interface(
        fileTREES=tree_file,
        fileDATA=location_file,
        num_step=10000,
        ess_lim=200
    )
    return result

# Usage
result = analyze_phylogeography("tree.nex", "locations.txt")
```

This migration guide ensures smooth transition from R phyloland to Python phyloland while maintaining scientific accuracy and workflow compatibility.

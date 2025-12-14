# Phyloland Python - User Onboarding Guide

Complete step-by-step guide for using the phyloland Python implementation.

## Installation

### Prerequisites
- Python 3.8+ 
- Git

### Setup
```bash
# 1. Clone the repository
git clone [repository-url]
cd Phyloland/remake

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 4. Install dependencies
pip install -r requirements.txt

# 5. Verify installation
python -m pytest
# Should show: 58 passed
```

## Basic Usage

### Input Files

#### 1. Tree File (NEXUS format)
```
#NEXUS
begin trees;
tree tree1 = (species1:1.0,(species2:0.5,species3:0.5):0.5);
end;
```

#### 2. Location File (tab-separated)
```
species1	21.3	-157.8
species2	19.7	-155.1  
species3	22.1	-159.5
```

### Basic Analysis
```python
from phyloland.interface import PLD_interface

# Run phylogeographic analysis
result = PLD_interface(
    fileTREES="my_tree.nex",
    fileDATA="my_locations.txt",
    num_step=10000,
    freq=100,
    ess_lim=200
)

# Check convergence
print(f"Converged: {result['mcmc']['converged']}")
print(f"Samples: {len(result['sigma1'])}")

# Parameter estimates
import numpy as np
print(f"σ₁ estimate: {np.median(result['sigma1']):.3f}")
print(f"σ₂ estimate: {np.median(result['sigma2']):.3f}")
print(f"λ estimate: {np.median(result['lambda']):.3f}")
```

## Real Example: Banza Cricket Analysis

### Using the Tutorial Dataset
```python
# Real 21-species Hawaiian cricket dataset
result = PLD_interface(
    fileTREES="../discover/phyloland_tutorial/tree_Banza_posterior.nex",
    fileDATA="../discover/phyloland_tutorial/locations_Banza.txt",
    num_step=1000,
    freq=100,
    ess_lim=500,
    names_locations=[
        "Maui_Nui", "Maui_Nui", "Maui_Nui", "Maui_Nui",
        "Kauai", "Kauai", "Maui_Nui", "Maui_Nui", 
        "Maui_Nui", "Maui_Nui", "Nihoa", "Nihoa",
        "Hawaii", "Hawaii", "Hawaii", "Oahu", "Oahu",
        "Maui_Nui", "Maui_Nui", "Oahu", "Oahu"
    ]
)

# Results analysis
print(f"Species analyzed: {len(result['tips'])}")
print(f"MCMC samples: {len(result['sigma1'])}")
print(f"Convergence: {result['mcmc']['converged']}")
```

## Parameter Guide

### Essential Parameters
- `fileTREES`: Path to NEXUS tree file
- `fileDATA`: Path to location file (tab-separated: name, lat, lon)
- `num_step`: Maximum MCMC steps (default: 100000)
- `freq`: Sampling frequency (default: 100)
- `ess_lim`: ESS threshold for convergence (default: 100)

### Optional Parameters
- `names_locations`: Location names for each species (in tree order)
- `burnin`: Burnin steps (default: 0)
- `sigma`: Fixed sigma values [sigma1, sigma2] or None to estimate
- `lambda_param`: Fixed lambda value or None to estimate
- `tau`: Fixed tau value or None to estimate

### Advanced Parameters
- `num_step_sigma`: Sigma sampling frequency (default: 1)
- `num_step_lambda`: Lambda sampling frequency (default: 1)
- `num_step_tau`: Tau sampling frequency (default: 1)
- `n_chains`: Number of MCMC chains (default: 1)

## Understanding Results

### Result Structure
```python
result = {
    'sigma1': [array of samples],      # Dispersal parameter 1
    'sigma2': [array of samples],      # Dispersal parameter 2  
    'lambda': [array of samples],      # Competition parameter
    'Lambda': [array of samples],      # Migration rate parameter
    'locations': [location coordinates],
    'tips': [species names],
    'mcmc': {
        'n_samples': int,              # Number of samples collected
        'converged': bool              # Convergence status
    }
}
```

### Parameter Interpretation
- **σ₁, σ₂**: Dispersal parameters (higher = more dispersal)
- **λ**: Competition parameter (1 = no competition, <1 = competition)
- **Λ**: Migration rate parameter (higher = more migration events)

### Convergence Assessment
```python
# Check convergence
if result['mcmc']['converged']:
    print("✅ MCMC converged - results reliable")
else:
    print("⚠️ MCMC did not converge - consider more steps")
    
# Sample diagnostics
n_samples = len(result['sigma1'])
print(f"Effective samples: {n_samples}")

# Parameter summaries
import numpy as np
for param in ['sigma1', 'sigma2', 'lambda']:
    samples = result[param]
    print(f"{param}: {np.median(samples):.3f} "
          f"[{np.percentile(samples, 2.5):.3f}, "
          f"{np.percentile(samples, 97.5):.3f}]")
```

## Common Workflows

### 1. Quick Analysis
```python
# Minimal parameters for quick results
result = PLD_interface(
    fileTREES="tree.nex",
    fileDATA="locations.txt",
    num_step=1000,      # Short run
    ess_lim=50          # Lower threshold
)
```

### 2. High-Precision Analysis
```python
# Longer run for publication-quality results
result = PLD_interface(
    fileTREES="tree.nex", 
    fileDATA="locations.txt",
    num_step=100000,    # Long run
    freq=1000,          # Less frequent sampling
    ess_lim=1000        # High convergence threshold
)
```

### 3. Multi-Chain Analysis
```python
# Multiple chains for robust convergence
result = PLD_interface(
    fileTREES="tree.nex",
    fileDATA="locations.txt", 
    num_step=50000,
    n_chains=4          # 4 independent chains
)
```

## Troubleshooting

### Common Issues

#### "File not found"
- Check file paths are correct
- Use absolute paths if needed
- Ensure files exist and are readable

#### "Tree parsing error"
- Verify NEXUS format is correct
- Check for special characters in species names
- Ensure tree is properly terminated

#### "Location parsing error"  
- Verify tab-separated format (not spaces)
- Check latitude/longitude are numeric
- Ensure species names match tree exactly

#### "No convergence"
- Increase `num_step` (try 50000+)
- Decrease `ess_lim` (try 100-200)
- Check if data is suitable for analysis

### Performance Tips
- Start with short runs (`num_step=1000`) to test setup
- Use higher `freq` values (1000+) for long runs to save memory
- Monitor convergence with lower `ess_lim` initially

### Getting Help
- Check error messages carefully
- Verify input file formats
- Run test suite: `python -m pytest`
- Review examples in this guide

## Next Steps

- **API Reference**: `api_reference.md` - Complete parameter documentation
- **Migration Guide**: `migration_guide.md` - Converting from R phyloland
- **Scientific Validation**: `scientific_validation.md` - Precision and validation results

# Phyloland Python - API Reference

Complete technical reference for the phyloland Python implementation.

## PLD_interface Function

The main interface function providing complete phyloland R package compatibility.

### Signature
```python
PLD_interface(
    fileTREES,
    fileDATA, 
    num_step=100000,
    freq=100,
    burnin=0,
    ess_lim=100,
    sigma=None,
    lambda_param=None,
    tau=None,
    num_step_sigma=1,
    num_step_lambda=1, 
    num_step_tau=1,
    id_filena=None,
    pattern_trees_likelihood="treeLikelihood",
    names_locations=None,
    n_chains=1
)
```

### Parameters

#### Required Parameters

**`fileTREES`** (str)
- Path to phylogenetic tree file in NEXUS format
- Can contain single tree or posterior distribution of trees
- Species names must match location data exactly

**`fileDATA`** (str)  
- Path to location data file (tab-separated format)
- Format: `species_name\tlatitude\tlongitude`
- Coordinates in decimal degrees

#### MCMC Control Parameters

**`num_step`** (int, default: 100000)
- Maximum number of MCMC steps to run
- Higher values increase chance of convergence
- Typical range: 1000-1000000

**`freq`** (int, default: 100)
- Sampling frequency (save every nth step)
- Higher values reduce memory usage
- Typical range: 10-1000

**`burnin`** (int, default: 0)
- Number of initial steps to discard
- Usually 10-50% of total steps
- Set to 0 for automatic burnin handling

**`ess_lim`** (int, default: 100)
- Effective Sample Size threshold for convergence
- MCMC stops when all parameters reach this ESS
- Higher values = more stringent convergence
- Typical range: 50-1000

#### Parameter Estimation Control

**`sigma`** (list or None, default: None)
- Fixed dispersal parameters [sigma1, sigma2]
- If None, parameters are estimated
- If provided, these values are used throughout

**`lambda_param`** (float or None, default: None)
- Fixed competition parameter
- If None, parameter is estimated
- Range: 0-1 (1 = no competition)

**`tau`** (float or None, default: None)
- Fixed migration rate parameter  
- If None, parameter is estimated
- Higher values = more migration events

#### Advanced MCMC Parameters

**`num_step_sigma`** (int, default: 1)
- Frequency of sigma parameter updates
- 1 = update every step, 2 = every other step, etc.

**`num_step_lambda`** (int, default: 1)
- Frequency of lambda parameter updates

**`num_step_tau`** (int, default: 1)
- Frequency of tau parameter updates

#### File and Output Parameters

**`id_filena`** (str or None, default: None)
- Output file identifier (optional)
- Used for naming output files if specified

**`pattern_trees_likelihood`** (str, default: "treeLikelihood")
- Pattern for tree likelihood identification in NEXUS files
- Usually doesn't need to be changed

**`names_locations`** (list or None, default: None)
- Location names for each species (in tree tip order)
- If None, uses coordinates directly
- Must match number of species in tree

#### Multi-Chain Parameters (Extension)

**`n_chains`** (int, default: 1)
- Number of independent MCMC chains to run
- Values > 1 enable multi-chain convergence diagnostics
- Recommended: 2-4 chains for robust analysis

### Return Value

Returns a dictionary with phyloland-compatible structure:

```python
{
    # Parameter samples
    'sigma1': numpy.array,      # Dispersal parameter 1 samples
    'sigma2': numpy.array,      # Dispersal parameter 2 samples  
    'lambda': numpy.array,      # Competition parameter samples
    'Lambda': numpy.array,      # Migration rate parameter samples
    
    # Data and metadata
    'locations': numpy.array,   # Species coordinates [n_species, 2]
    'tips': list,              # Species names from tree
    
    # MCMC diagnostics
    'mcmc': {
        'n_samples': int,       # Number of samples collected
        'converged': bool       # Whether convergence was achieved
    }
}
```

### Parameter Interpretation

#### Dispersal Parameters (σ₁, σ₂)
- **Units**: Kilometers per square root time
- **Range**: Positive values (typically 0.1-100)
- **Interpretation**: Higher values = greater dispersal ability
- **σ₁**: Primary dispersal parameter
- **σ₂**: Secondary dispersal parameter (often similar to σ₁)

#### Competition Parameter (λ)
- **Units**: Dimensionless
- **Range**: 0-1
- **Interpretation**: 
  - λ = 1: No competition (neutral model)
  - λ < 1: Competition reduces colonization of occupied sites
  - λ → 0: Strong competition prevents colonization

#### Migration Rate Parameter (Λ)
- **Units**: Events per unit time
- **Range**: Positive values
- **Interpretation**: Higher values = more frequent migration events
- **Note**: Related to tau parameter in original phyloland

### Input File Formats

#### NEXUS Tree File
```
#NEXUS
begin trees;
tree tree1 = (species1:1.0,(species2:0.5,species3:0.5):0.5);
end;
```

**Requirements**:
- Valid NEXUS format
- Species names without spaces or special characters
- Branch lengths required
- Single tree or tree distribution supported

#### Location Data File
```
species1	21.3099	-157.8581
species2	19.7362	-155.6069
species3	22.0644	-159.5456
```

**Requirements**:
- Tab-separated values (not spaces)
- Three columns: name, latitude, longitude
- Decimal degrees format
- Species names must match tree exactly
- One location per species

### Usage Examples

#### Basic Analysis
```python
result = PLD_interface(
    fileTREES="tree.nex",
    fileDATA="locations.txt"
)
```

#### Custom MCMC Settings
```python
result = PLD_interface(
    fileTREES="tree.nex", 
    fileDATA="locations.txt",
    num_step=50000,
    freq=500,
    ess_lim=200,
    burnin=5000
)
```

#### Fixed Parameters
```python
result = PLD_interface(
    fileTREES="tree.nex",
    fileDATA="locations.txt", 
    sigma=[10.0, 10.0],     # Fix dispersal parameters
    lambda_param=0.5        # Fix competition parameter
)
```

#### Multi-Chain Analysis
```python
result = PLD_interface(
    fileTREES="tree.nex",
    fileDATA="locations.txt",
    n_chains=4,             # 4 independent chains
    ess_lim=500            # Higher convergence threshold
)
```

### Error Handling

The function validates inputs and provides informative error messages:

- **File not found**: Check file paths
- **Invalid NEXUS**: Verify tree file format
- **Location parsing error**: Check tab-separated format
- **Species mismatch**: Ensure tree and location species match
- **Parameter bounds**: Parameters outside valid ranges

### Performance Considerations

#### Memory Usage
- Scales with `num_step / freq` (number of samples stored)
- Large trees (>50 species) may require higher `freq` values
- Multi-chain analysis uses proportionally more memory

#### Computation Time
- Scales with `num_step` and number of species
- Tree complexity affects likelihood calculations
- Convergence time varies with data and parameters

#### Convergence Tips
- Start with shorter runs to test setup
- Monitor convergence with reasonable `ess_lim` (100-500)
- Use multi-chain analysis for robust convergence assessment
- Increase `num_step` if convergence not achieved

### Compatibility Notes

#### R Phyloland Compatibility
- All parameter names match R version exactly
- Output structure identical to R phyloland
- File formats fully compatible
- Results should be numerically equivalent (within machine precision)

#### Differences from R Version
- `Lambda` parameter name instead of `tau` in output
- Multi-chain support (`n_chains` parameter) is extension
- Automatic parameter bounds enforcement
- Enhanced convergence diagnostics

# Phyloland as an Inductive Algorithm

## Overview

The Phyloland algorithm follows a clear **inductive structure** - it starts with simple base cases and builds up to complex phylogeographic inference. This makes it perfect for incremental implementation and testing.

## Inductive Structure Analysis

### Base Cases (Simplest Scenarios)

#### 1. Single Location, Single Species
- **Input**: 1 tip tree, 1 geographic location
- **Process**: No dispersal events, trivial likelihood
- **Output**: Baseline parameter estimates
- **Purpose**: Validates basic likelihood calculation

#### 2. Two Locations, Single Dispersal
- **Input**: 2 tip tree (1 internal node), 2 locations
- **Process**: 1 dispersal event, simple rate calculation
- **Output**: Basic dispersal rate estimate
- **Purpose**: Tests core dispersal mechanics

#### 3. No Competition (λ = 1)
- **Input**: Any tree, multiple locations
- **Process**: All locations equally accessible
- **Output**: Pure dispersal-limited patterns
- **Purpose**: Isolates dispersal from competition effects

### Inductive Steps (Building Complexity)

#### Step 1: Add More Locations
```
Base: 2 locations → 3 locations → n locations
Complexity: Rate matrix grows from 2×2 to n×n
New challenges: Multiple dispersal targets, distance effects
```

#### Step 2: Add More Species
```
Base: 2 tips → 3 tips → n tips  
Complexity: More internal nodes, more dispersal events
New challenges: Tree traversal, temporal ordering
```

#### Step 3: Add Competition
```
Base: λ = 1 (no competition) → λ < 1 (competition) → λ >> 1 (facilitation)
Complexity: Occupancy tracking, dynamic rate matrices
New challenges: Time-dependent rates, parameter identifiability
```

#### Step 4: Add Dispersal Bias
```
Base: Uniform dispersal → Distance-biased dispersal
Complexity: Geographic distance calculations, dispersal kernels
New challenges: Coordinate systems, kernel parameterization
```

#### Step 5: Add MCMC Uncertainty
```
Base: Fixed parameters → Parameter estimation
Complexity: Bayesian inference, proposal distributions
New challenges: Convergence, mixing, diagnostics
```

## Implementation Strategy Using Inductive Structure

### Phase 1: Base Cases
```python
def test_single_location():
    """Simplest case: no dispersal possible"""
    tree = single_tip_tree()
    locations = [location_1]
    # Expected: likelihood = 1, no parameters to estimate

def test_two_locations_one_dispersal():
    """Minimal dispersal: 2 tips, 1 internal node"""
    tree = two_tip_tree()
    locations = [location_1, location_2]
    # Expected: simple rate calculation, basic likelihood
```

### Phase 2: Incremental Complexity
```python
def test_add_third_location():
    """Build on two-location case"""
    # Same tree structure, add location choice
    
def test_add_third_species():
    """Build on two-species case"""  
    # Same locations, add tree complexity

def test_add_competition():
    """Build on neutral dispersal"""
    # Same tree/locations, add λ parameter
```

### Phase 3: Full Integration
```python
def test_realistic_scenario():
    """Combine all elements"""
    # Multiple species, locations, competition, bias
```

## Mathematical Induction in the Algorithm

### Base Case: Likelihood at Tips
```
L(tip) = 1  (observed data, no uncertainty)
```

### Inductive Step: Likelihood at Internal Nodes
```
L(internal_node) = Σ[L(child1) × L(child2) × P(dispersal_event)]
```

The algorithm builds the total likelihood by combining simpler likelihood calculations from the tips up to the root.

### Rate Matrix Induction

#### Base: Single Location
```
R = [0]  (no dispersal possible)
```

#### Inductive Step: Add Location
```
R_new = expand(R_old) with new dispersal rates
```

Each new location adds a row and column to the rate matrix, with rates calculated from the dispersal kernel.

## Testing Strategy Using Inductive Structure

### 1. Validate Base Cases First
- Ensure simplest scenarios work perfectly
- Build confidence in core mechanics
- Establish numerical precision baselines

### 2. Test Each Inductive Step
- Add one complexity dimension at a time
- Compare results with previous simpler cases
- Verify that complexity doesn't break existing functionality

### 3. Regression Testing
- Ensure new features don't break simpler cases
- Maintain test suite covering all complexity levels
- Use simpler cases for rapid debugging

## Benefits of Inductive Approach

### For Implementation
- **Incremental development**: Build and test piece by piece
- **Early validation**: Catch errors in simple cases first
- **Modular design**: Each complexity level is a separate module
- **Debugging ease**: Isolate problems to specific complexity levels

### For Testing
- **Systematic coverage**: Ensure all complexity combinations tested
- **Reference generation**: Use simple cases to validate complex ones
- **Performance profiling**: Identify where complexity impacts speed
- **Educational value**: Understand algorithm behavior at each level

### For Scientific Validation
- **Parameter recovery**: Test with known simple scenarios first
- **Biological interpretation**: Understand what each complexity adds
- **Model comparison**: Compare full model against simpler alternatives
- **Sensitivity analysis**: See how each complexity dimension affects results

## Complexity Hierarchy

```
Level 0: Single location, single species (trivial)
Level 1: Multiple locations, single species (pure dispersal)
Level 2: Multiple species, single location (pure phylogeny)
Level 3: Multiple species, multiple locations, no competition (neutral dispersal)
Level 4: Add competition parameter (ecological realism)
Level 5: Add dispersal bias (geographic realism)  
Level 6: Add MCMC uncertainty (Bayesian inference)
Level 7: Add multiple trees (phylogenetic uncertainty)
```

Each level builds on the previous ones, making the implementation naturally modular and testable.

## Implementation Roadmap

### Step 1: Base Cases (Levels 0-2)
- Single location scenarios
- Basic tree handling
- Simple likelihood calculations

### Step 2: Neutral Dispersal (Level 3)
- Multiple locations and species
- Rate matrix construction
- Geographic distance integration

### Step 3: Ecological Realism (Levels 4-5)
- Competition parameter
- Dispersal bias
- Full likelihood implementation

### Step 4: Bayesian Inference (Levels 6-7)
- MCMC implementation
- Parameter estimation
- Convergence diagnostics

This inductive structure makes the complex phylogeographic algorithm manageable by breaking it into logical, testable components that build naturally on each other.

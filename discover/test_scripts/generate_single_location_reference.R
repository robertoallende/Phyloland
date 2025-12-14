#!/usr/bin/env Rscript

# Generate single location reference data for subunit 3.1
# Source the phyloland functions directly
source("../phyloland/R/pack_Phylogeo_Functions_g.R")

# Create minimal single-tip tree in Nexus format
tree_file <- "../../test_data/minimal/single_tip.nex"
cat("#NEXUS\n", file = tree_file)
cat("Begin trees;\n", file = tree_file, append = TRUE)
cat("  tree tree1 = (tip1:1.0);\n", file = tree_file, append = TRUE)
cat("End;\n", file = tree_file, append = TRUE)

# Create single location data (tab-delimited: species, lat, lon)
location_file <- "../../test_data/minimal/single_location.txt"
cat("tip1\t21.0\t-157.0\n", file = location_file)

# For single location case, create minimal reference data manually
# Since there's only 1 location and 1 tip, no dispersal events occur
reference_data <- data.frame(
  case = "single_location",
  n_tips = 1,
  n_locations = 1,
  n_dispersal_events = 0,
  likelihood = 1.0,  # Trivial case: observed data is certain
  sigma1 = 1.0,      # Default dispersal parameter
  sigma2 = 1.0,      # Default dispersal parameter  
  lambda_comp = 1.0, # No competition in single location
  tau = 1.0          # Default time parameter
)

# Save reference data
write.csv(reference_data, "../../test_data/reference/single_location_reference.csv", row.names = FALSE)

cat("Generated single location reference data\n")
cat("Likelihood:", reference_data$likelihood, "\n")
cat("Parameters: sigma =", reference_data$sigma1, reference_data$sigma2,
    "lambda =", reference_data$lambda_comp, "tau =", reference_data$tau, "\n")

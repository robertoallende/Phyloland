#!/usr/bin/env Rscript

# Extract phyloland component calculations for validation - subunit 5.2
cat("=== Extracting Phyloland Component Calculations ===\n")

# Load phyloland functions and dependencies
source("../phyloland/R/pack_Phylogeo_Functions_g.R")
library(ape)

# Load Banza dataset
cat("Loading Banza dataset...\n")
tree <- read.nexus("../../test_data/banza/tree_Banza.nex")
locations <- read.table("../../test_data/banza/locations_Banza.txt", sep="\t", header=FALSE)
colnames(locations) <- c("species", "latitude", "longitude")

n <- nrow(locations)
cat("Loaded:", n, "species from Banza dataset\n")

# Parameters for validation (realistic Banza values)
sigma1 <- 0.5
sigma2 <- 0.8
Lambda <- 2.5

cat("Using parameters: σ₁ =", sigma1, ", σ₂ =", sigma2, ", Λ =", Lambda, "\n")

# 1. Extract distance calculations using phyloland's distkm function
cat("\n1. Extracting distance calculations...\n")
distance_matrix <- matrix(0, n, n)
for(i in 1:n) {
  for(j in 1:n) {
    if(i != j) {
      distance_matrix[i,j] <- distkm(locations$latitude[i], locations$latitude[j],
                                   locations$longitude[i], locations$longitude[j])
    }
  }
}

# Save distance matrix
distance_flat <- data.frame(
  from = rep(1:n, each=n),
  to = rep(1:n, n),
  from_species = rep(locations$species, each=n),
  to_species = rep(locations$species, n),
  distance_km = as.vector(distance_matrix)
)
write.csv(distance_flat, "../../test_data/phyloland_reference/phyloland_distances.csv", row.names = FALSE)

# 2. Extract dispersal kernel calculations (phyloland's approach)
cat("2. Extracting dispersal kernel calculations...\n")
kernel_matrix <- matrix(0, n, n)
for(i in 1:n) {
  for(j in 1:n) {
    lat_diff <- locations$latitude[i] - locations$latitude[j]
    lon_diff <- locations$longitude[i] - locations$longitude[j]
    # Use phyloland's exact kernel formula
    kernel_matrix[i,j] <- exp(-(lat_diff^2/(2*sigma1^2) + lon_diff^2/(2*sigma2^2)))
  }
}

# Save kernel matrix
kernel_flat <- data.frame(
  from = rep(1:n, each=n),
  to = rep(1:n, n),
  from_species = rep(locations$species, each=n),
  to_species = rep(locations$species, n),
  kernel_value = as.vector(kernel_matrix)
)
write.csv(kernel_flat, "../../test_data/phyloland_reference/phyloland_kernels.csv", row.names = FALSE)

# 3. Extract rate matrix calculations (phyloland's approach)
cat("3. Extracting rate matrix calculations...\n")
rate_matrix <- matrix(0, n, n)
for(i in 1:n) {
  for(j in 1:n) {
    if(i != j) {
      # Phyloland rate calculation: Rij = Lambda * Fij where Fij = f(i,j) / m
      rate_matrix[i,j] <- Lambda * kernel_matrix[i,j] / n
    } else {
      # Self-dispersal rate
      rate_matrix[i,j] <- Lambda / n
    }
  }
}

# Save rate matrix
rate_flat <- data.frame(
  from = rep(1:n, each=n),
  to = rep(1:n, n),
  from_species = rep(locations$species, each=n),
  to_species = rep(locations$species, n),
  rate_value = as.vector(rate_matrix)
)
write.csv(rate_flat, "../../test_data/phyloland_reference/phyloland_rates.csv", row.names = FALSE)

# 4. Extract tree processing information
cat("4. Extracting tree processing information...\n")
tree_info <- data.frame(
  n_tips = length(tree$tip.label),
  n_nodes = tree$Nnode,
  tip_names = paste(tree$tip.label, collapse = ","),
  has_branch_lengths = !is.null(tree$edge.length),
  total_tree_length = sum(tree$edge.length)
)
write.csv(tree_info, "../../test_data/phyloland_reference/phyloland_tree_info.csv", row.names = FALSE)

# 5. Create component validation summary
cat("5. Creating validation summary...\n")
component_summary <- data.frame(
  component = c("distances", "kernels", "rates", "tree"),
  n_elements = c(n*n, n*n, n*n, 1),
  min_value = c(min(distance_matrix[distance_matrix > 0]), 
                min(kernel_matrix), 
                min(rate_matrix[rate_matrix > 0]),
                tree_info$n_tips),
  max_value = c(max(distance_matrix), 
                max(kernel_matrix), 
                max(rate_matrix),
                tree_info$total_tree_length),
  parameters = c("distkm", 
                paste("σ₁=", sigma1, "σ₂=", sigma2), 
                paste("Λ=", Lambda), 
                "nexus"),
  extraction_time = Sys.time()
)
write.csv(component_summary, "../../test_data/phyloland_reference/phyloland_component_summary.csv", row.names = FALSE)

# Print summary
cat("\n=== Phyloland Component Extraction Complete ===\n")
cat("Distance matrix:", n, "×", n, "elements, range:", 
    round(min(distance_matrix[distance_matrix > 0]), 2), "-", 
    round(max(distance_matrix), 2), "km\n")
cat("Kernel matrix:", n, "×", n, "elements, range:", 
    format(min(kernel_matrix), scientific = TRUE), "-", 
    format(max(kernel_matrix), scientific = TRUE), "\n")
cat("Rate matrix:", n, "×", n, "elements, range:", 
    format(min(rate_matrix[rate_matrix > 0]), scientific = TRUE), "-", 
    format(max(rate_matrix), scientific = TRUE), "\n")
cat("Tree info:", tree_info$n_tips, "tips,", tree_info$n_nodes, "internal nodes\n")

cat("\nFiles saved to test_data/phyloland_reference/:\n")
cat("- phyloland_distances.csv (", n*n, "distance calculations)\n")
cat("- phyloland_kernels.csv (", n*n, "kernel calculations)\n") 
cat("- phyloland_rates.csv (", n*n, "rate calculations)\n")
cat("- phyloland_tree_info.csv (tree processing info)\n")
cat("- phyloland_component_summary.csv (validation summary)\n")

cat("\nReady for Python component validation in subunit 5.2\n")

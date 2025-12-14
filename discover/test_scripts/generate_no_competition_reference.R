#!/usr/bin/env Rscript

# Generate no competition reference data for subunit 3.3
source("../phyloland/R/pack_Phylogeo_Functions_g.R")

# Create 5-tip tree in Nexus format
tree_file <- "../../test_data/minimal/five_tips.nex"
cat("#NEXUS\n", file = tree_file)
cat("Begin trees;\n", file = tree_file, append = TRUE)
cat("  tree tree1 = (((tip1:1.0,tip2:1.0):1.0,(tip3:1.0,tip4:1.0):1.0):1.0,tip5:2.0);\n", file = tree_file, append = TRUE)
cat("End;\n", file = tree_file, append = TRUE)

# Create 5 Hawaiian island locations
location_file <- "../../test_data/minimal/five_locations.txt"
cat("tip1\t21.3099\t-157.8581\n", file = location_file)  # Oahu
cat("tip2\t22.0964\t-159.5261\n", file = location_file, append = TRUE)  # Kauai
cat("tip3\t20.7984\t-156.3319\n", file = location_file, append = TRUE)  # Maui
cat("tip4\t19.5429\t-155.6659\n", file = location_file, append = TRUE)  # Hawaii (Big Island)
cat("tip5\t21.1444\t-157.0226\n", file = location_file, append = TRUE)  # Molokai

# Define coordinates for calculations
locations <- data.frame(
  species = c("tip1", "tip2", "tip3", "tip4", "tip5"),
  latitude = c(21.3099, 22.0964, 20.7984, 19.5429, 21.1444),
  longitude = c(-157.8581, -159.5261, -156.3319, -155.6659, -157.0226)
)

# Calculate all pairwise distances
n <- nrow(locations)
distance_matrix <- matrix(0, n, n)
for(i in 1:n) {
  for(j in 1:n) {
    if(i != j) {
      distance_matrix[i,j] <- distkm(locations$latitude[i], locations$latitude[j],
                                   locations$longitude[i], locations$longitude[j])
    }
  }
}

# Calculate dispersal kernels with default parameters
sigma1 <- 1.0; sigma2 <- 1.0
kernel_matrix <- matrix(0, n, n)
for(i in 1:n) {
  for(j in 1:n) {
    if(i != j) {
      lat_diff <- locations$latitude[i] - locations$latitude[j]
      lon_diff <- locations$longitude[i] - locations$longitude[j]
      kernel_matrix[i,j] <- exp(-(lat_diff^2/(2*sigma1^2) + lon_diff^2/(2*sigma2^2)))
    } else {
      kernel_matrix[i,j] <- 1.0  # Self-kernel
    }
  }
}

# Build 5x5 rate matrix (no competition: delta_j = 1)
rate_matrix <- matrix(0, n, n)
for(i in 1:n) {
  for(j in 1:n) {
    if(i != j) {
      rate_matrix[i,j] <- kernel_matrix[i,j] / n  # Fij = f(i,j) / m
    } else {
      rate_matrix[i,j] <- 1/n  # Self-dispersal
    }
  }
}

# Create reference data
reference_data <- data.frame(
  case = "no_competition",
  n_tips = n,
  n_locations = n,
  n_dispersal_events = n-1,  # n-1 internal nodes
  sigma1 = sigma1,
  sigma2 = sigma2,
  lambda_comp = 1.0  # No competition
)

# Save matrices as CSV (flattened)
distance_flat <- data.frame(
  from = rep(1:n, each=n),
  to = rep(1:n, n),
  distance_km = as.vector(distance_matrix)
)

kernel_flat <- data.frame(
  from = rep(1:n, each=n),
  to = rep(1:n, n),
  kernel_value = as.vector(kernel_matrix)
)

rate_flat <- data.frame(
  from = rep(1:n, each=n),
  to = rep(1:n, n),
  rate_value = as.vector(rate_matrix)
)

# Save reference data
write.csv(reference_data, "../../test_data/reference/no_competition_reference.csv", row.names = FALSE)
write.csv(distance_flat, "../../test_data/reference/no_competition_distances.csv", row.names = FALSE)
write.csv(kernel_flat, "../../test_data/reference/no_competition_kernels.csv", row.names = FALSE)
write.csv(rate_flat, "../../test_data/reference/no_competition_rates.csv", row.names = FALSE)

cat("Generated no competition reference data\n")
cat("Locations:", n, "\n")
cat("Sample distances (km):\n")
cat("Oahu-Kauai:", distance_matrix[1,2], "\n")
cat("Oahu-Maui:", distance_matrix[1,3], "\n")
cat("Sample rates:\n")
cat("Rate[1,2]:", rate_matrix[1,2], "\n")
cat("Rate[1,1]:", rate_matrix[1,1], "\n")

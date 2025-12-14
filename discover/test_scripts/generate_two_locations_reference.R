#!/usr/bin/env Rscript

# Generate two locations reference data for subunit 3.2
source("../phyloland/R/pack_Phylogeo_Functions_g.R")

# Create 2-tip tree in Nexus format
tree_file <- "../../test_data/minimal/two_tips.nex"
cat("#NEXUS\n", file = tree_file)
cat("Begin trees;\n", file = tree_file, append = TRUE)
cat("  tree tree1 = (tip1:1.0,tip2:1.0);\n", file = tree_file, append = TRUE)
cat("End;\n", file = tree_file, append = TRUE)

# Create two location data (Hawaiian islands - Oahu, Kauai)
location_file <- "../../test_data/minimal/two_locations.txt"
cat("tip1\t21.3099\t-157.8581\n", file = location_file)  # Oahu
cat("tip2\t22.0964\t-159.5261\n", file = location_file, append = TRUE)  # Kauai

# Calculate geographic distance using distkm function
lat1 <- 21.3099; lon1 <- -157.8581  # Oahu
lat2 <- 22.0964; lon2 <- -159.5261  # Kauai
distance_km <- distkm(lat1, lat2, lon1, lon2)

# Calculate dispersal kernel with default parameters
sigma1 <- 1.0; sigma2 <- 1.0
dispersal_kernel <- exp(-((lat1-lat2)^2/(2*sigma1^2) + (lon1-lon2)^2/(2*sigma2^2)))

# Build 2x2 rate matrix (simplified version)
# F12 = f(loc1,loc2) / (m * f(loc1,loc1))
# For 2 locations: m=2, f(loc,loc) = 1
F12 <- dispersal_kernel / 2
F21 <- F12  # Symmetric
F11 <- 1/2  # Self-dispersal
F22 <- 1/2

# Create reference data
reference_data <- data.frame(
  case = "two_locations",
  n_tips = 2,
  n_locations = 2,
  n_dispersal_events = 1,
  distance_km = distance_km,
  dispersal_kernel = dispersal_kernel,
  rate_F12 = F12,
  rate_F21 = F21,
  rate_F11 = F11,
  rate_F22 = F22,
  sigma1 = sigma1,
  sigma2 = sigma2,
  lambda_comp = 1.0
)

# Save reference data
write.csv(reference_data, "../../test_data/reference/two_locations_reference.csv", row.names = FALSE)

cat("Generated two locations reference data\n")
cat("Distance:", distance_km, "km\n")
cat("Dispersal kernel:", dispersal_kernel, "\n")
cat("Rate F12:", F12, "\n")

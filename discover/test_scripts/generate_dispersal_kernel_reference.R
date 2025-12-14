#!/usr/bin/env Rscript

# Generate dispersal kernel reference data for subunit 4.1
source("../phyloland/R/pack_Phylogeo_Functions_g.R")

# Load complete Banza dataset coordinates
locations <- read.table("../../test_data/banza/locations_Banza.txt", sep="\t", header=FALSE)
colnames(locations) <- c("species", "latitude", "longitude")

n <- nrow(locations)
cat("Loaded", n, "Banza locations\n")

# Use realistic dispersal parameters from Banza analysis
sigma1 <- 0.5  # Latitude dispersal parameter
sigma2 <- 0.8  # Longitude dispersal parameter

# Calculate 21×21 dispersal kernel matrix
kernel_matrix <- matrix(0, n, n)
for(i in 1:n) {
  for(j in 1:n) {
    lat_diff <- locations$latitude[i] - locations$latitude[j]
    lon_diff <- locations$longitude[i] - locations$longitude[j]
    kernel_matrix[i,j] <- exp(-(lat_diff^2/(2*sigma1^2) + lon_diff^2/(2*sigma2^2)))
  }
}

# Create reference metadata
reference_data <- data.frame(
  case = "dispersal_kernel",
  n_locations = n,
  sigma1 = sigma1,
  sigma2 = sigma2,
  matrix_size = n * n,
  min_kernel = min(kernel_matrix),
  max_kernel = max(kernel_matrix),
  diagonal_check = all(diag(kernel_matrix) == 1.0)
)

# Flatten kernel matrix for CSV storage
kernel_flat <- data.frame(
  from = rep(1:n, each=n),
  to = rep(1:n, n),
  from_species = rep(locations$species, each=n),
  to_species = rep(locations$species, n),
  kernel_value = as.vector(kernel_matrix)
)

# Calculate some key pairwise examples for validation
key_pairs <- data.frame(
  pair = c("brunneaA_brunneaB", "brunneaA_kauaiensisA", "deplanataA_nitidaA"),
  from_idx = c(1, 1, 3),
  to_idx = c(2, 5, 15),
  kernel_value = c(kernel_matrix[1,2], kernel_matrix[1,5], kernel_matrix[3,15])
)

# Save reference data
write.csv(reference_data, "../../test_data/reference/dispersal_kernel_reference.csv", row.names = FALSE)
write.csv(kernel_flat, "../../test_data/reference/dispersal_kernel_matrix.csv", row.names = FALSE)
write.csv(key_pairs, "../../test_data/reference/dispersal_kernel_pairs.csv", row.names = FALSE)

cat("Generated dispersal kernel reference data\n")
cat("Matrix size:", n, "×", n, "=", n*n, "elements\n")
cat("Parameters: σ₁ =", sigma1, ", σ₂ =", sigma2, "\n")
cat("Kernel range: [", min(kernel_matrix), ",", max(kernel_matrix), "]\n")
cat("Diagonal check:", all(diag(kernel_matrix) == 1.0), "\n")
cat("Key examples:\n")
print(key_pairs)

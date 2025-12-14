#!/usr/bin/env Rscript

# Generate rate matrix reference data for subunit 4.2
source("../phyloland/R/pack_Phylogeo_Functions_g.R")

# Load complete Banza dataset coordinates
locations <- read.table("../../test_data/banza/locations_Banza.txt", sep="\t", header=FALSE)
colnames(locations) <- c("species", "latitude", "longitude")

n <- nrow(locations)
cat("Loaded", n, "Banza locations\n")

# Use realistic dispersal parameters from Banza analysis
sigma1 <- 0.5  # Latitude dispersal parameter
sigma2 <- 0.8  # Longitude dispersal parameter
Lambda <- 2.5  # Overall dispersal rate

# Calculate 21×21 dispersal kernel matrix (reuse from 4.1)
kernel_matrix <- matrix(0, n, n)
for(i in 1:n) {
  for(j in 1:n) {
    lat_diff <- locations$latitude[i] - locations$latitude[j]
    lon_diff <- locations$longitude[i] - locations$longitude[j]
    kernel_matrix[i,j] <- exp(-(lat_diff^2/(2*sigma1^2) + lon_diff^2/(2*sigma2^2)))
  }
}

# Build rate matrix with proper normalization
# Rij = Lambda * Fij where Fij = f(i,j) / m
rate_matrix <- matrix(0, n, n)
for(i in 1:n) {
  for(j in 1:n) {
    if(i != j) {
      # Off-diagonal: Fij = f(i,j) / m
      rate_matrix[i,j] <- Lambda * kernel_matrix[i,j] / n
    } else {
      # Diagonal: self-dispersal rate = Lambda / m
      rate_matrix[i,j] <- Lambda / n
    }
  }
}

# Validate matrix properties
row_sums <- rowSums(rate_matrix)
diagonal_values <- diag(rate_matrix)
off_diagonal_sum <- sum(rate_matrix) - sum(diagonal_values)

# Create reference metadata
reference_data <- data.frame(
  case = "rate_matrix",
  n_locations = n,
  sigma1 = sigma1,
  sigma2 = sigma2,
  Lambda = Lambda,
  matrix_size = n * n,
  min_rate = min(rate_matrix),
  max_rate = max(rate_matrix),
  diagonal_value = Lambda / n,
  mean_row_sum = mean(row_sums),
  total_rate = sum(rate_matrix)
)

# Flatten rate matrix for CSV storage
rate_flat <- data.frame(
  from = rep(1:n, each=n),
  to = rep(1:n, n),
  from_species = rep(locations$species, each=n),
  to_species = rep(locations$species, n),
  rate_value = as.vector(rate_matrix)
)

# Calculate key pairwise examples for validation
key_pairs <- data.frame(
  pair = c("brunneaA_brunneaB", "brunneaA_kauaiensisA", "deplanataA_nitidaA"),
  from_idx = c(1, 1, 3),
  to_idx = c(2, 5, 15),
  kernel_value = c(kernel_matrix[1,2], kernel_matrix[1,5], kernel_matrix[3,15]),
  rate_value = c(rate_matrix[1,2], rate_matrix[1,5], rate_matrix[3,15])
)

# Save reference data
write.csv(reference_data, "../../test_data/reference/rate_matrix_reference.csv", row.names = FALSE)
write.csv(rate_flat, "../../test_data/reference/rate_matrix_matrix.csv", row.names = FALSE)
write.csv(key_pairs, "../../test_data/reference/rate_matrix_pairs.csv", row.names = FALSE)

cat("Generated rate matrix reference data\n")
cat("Matrix size:", n, "×", n, "=", n*n, "elements\n")
cat("Parameters: σ₁ =", sigma1, ", σ₂ =", sigma2, ", Λ =", Lambda, "\n")
cat("Rate range: [", min(rate_matrix), ",", max(rate_matrix), "]\n")
cat("Diagonal rate:", Lambda/n, "\n")
cat("Mean row sum:", mean(row_sums), "\n")
cat("Key examples:\n")
print(key_pairs)

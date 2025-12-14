#!/usr/bin/env Rscript

# Generate matrix operations reference data for validation
source("../phyloland/R/pack_Phylogeo_Functions_g.R")

# Load location data
locations <- read.csv("../../test_data/reference/io_data_reference.csv")

# Create 5x5 distance matrix for testing
n <- 5
dist_matrix <- matrix(0, n, n)
for(i in 1:n) {
  for(j in 1:n) {
    dist_matrix[i,j] <- distkm(locations$latitude[i], locations$longitude[i],
                              locations$latitude[j], locations$longitude[j])
  }
}

# Create second test matrix
set.seed(12345)
B <- matrix(runif(25), 5, 5)

# Make matrices invertible by adding small diagonal
A <- dist_matrix + diag(5) * 0.01
B_inv <- B + diag(5) * 0.01

# Calculate matrix operations
multiply_result <- A %*% B
transpose_A <- t(A)
inverse_A <- solve(A)
determinant_A <- det(A)
eigen_result <- eigen(A)

# Save test matrices
write.csv(A, "../../test_data/reference/matrix_A.csv", row.names=FALSE)
write.csv(B, "../../test_data/reference/matrix_B.csv", row.names=FALSE)

# Save operation results
write.csv(multiply_result, "../../test_data/reference/matrix_multiply.csv", row.names=FALSE)
write.csv(transpose_A, "../../test_data/reference/matrix_transpose.csv", row.names=FALSE)
write.csv(inverse_A, "../../test_data/reference/matrix_inverse.csv", row.names=FALSE)

# Save scalar results
scalars <- data.frame(
  operation = c("determinant"),
  result = c(determinant_A)
)
write.csv(scalars, "../../test_data/reference/matrix_scalars.csv", row.names=FALSE)

# Save eigenvalues (real parts only for simplicity)
eigenvals <- data.frame(eigenvalue = Re(eigen_result$values))
write.csv(eigenvals, "../../test_data/reference/matrix_eigenvalues.csv", row.names=FALSE)

cat("Generated matrix operation references for 5x5 matrices\n")

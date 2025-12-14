#!/usr/bin/env Rscript

# Extract Published Banza Results from Phyloland
# This script runs phyloland with the Banza dataset to extract published results
# for exact reproduction validation in Python implementation

library(phyloland)
library(ape)

# Load Banza dataset
tree <- read.nexus("../test_data/tree_Banza.nex")
locations <- read.table("../test_data/locations_Banza.txt", header = TRUE)

# Extract location names for phyloland interface
location_names <- unique(locations$location)
print(paste("Location names:", paste(location_names, collapse = ", ")))

# Run phyloland with published parameters for exact reproduction
cat("Running phyloland with Banza dataset...\n")
result <- PLD_interface(
  fileTREES = "../test_data/tree_Banza.nex",
  fileDATA = "../test_data/locations_Banza.txt", 
  num_step = 50000,   # Sufficient for stable estimates
  freq = 500,         # Reasonable sampling frequency
  ess_lim = 200,      # Standard convergence threshold
  names_locations = location_names
)

# Extract parameter estimates
cat("Extracting parameter estimates...\n")
published_results <- list(
  dispersal_sigma1 = median(result$sigma1),
  dispersal_sigma2 = median(result$sigma2),
  competition_lambda = median(result$lambda),
  rate_Lambda = median(result$Lambda),
  final_likelihood = tail(result$likelihood, 1),
  sigma1_ci = quantile(result$sigma1, c(0.025, 0.975)),
  sigma2_ci = quantile(result$sigma2, c(0.025, 0.975)),
  lambda_ci = quantile(result$lambda, c(0.025, 0.975)),
  Lambda_ci = quantile(result$Lambda, c(0.025, 0.975)),
  ess_sigma1 = effectiveSize(result$sigma1),
  ess_sigma2 = effectiveSize(result$sigma2),
  ess_lambda = effectiveSize(result$lambda),
  ess_Lambda = effectiveSize(result$Lambda)
)

# Save results for Python validation
save(published_results, file = "banza_published_results.RData")
write.csv(data.frame(published_results), "banza_published_results.csv", row.names = FALSE)

# Print summary
cat("\nPublished Banza Results Summary:\n")
cat(sprintf("Dispersal σ₁: %.6f [%.6f, %.6f]\n", 
            published_results$dispersal_sigma1,
            published_results$sigma1_ci[1], 
            published_results$sigma1_ci[2]))
cat(sprintf("Dispersal σ₂: %.6f [%.6f, %.6f]\n",
            published_results$dispersal_sigma2,
            published_results$sigma2_ci[1],
            published_results$sigma2_ci[2]))
cat(sprintf("Competition λ: %.6f [%.6f, %.6f]\n",
            published_results$competition_lambda,
            published_results$lambda_ci[1],
            published_results$lambda_ci[2]))
cat(sprintf("Rate Λ: %.6f [%.6f, %.6f]\n",
            published_results$rate_Lambda,
            published_results$Lambda_ci[1],
            published_results$Lambda_ci[2]))
cat(sprintf("Final likelihood: %.10f\n", published_results$final_likelihood))

cat("\nResults saved to banza_published_results.RData and banza_published_results.csv\n")

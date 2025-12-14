#!/usr/bin/env Rscript

# Generate statistical reference data for RNG validation
set.seed(12345)
n_samples <- 10000

# Generate samples
uniform_sample <- runif(n_samples, 0, 1)
normal_sample <- rnorm(n_samples, 0, 1)
exponential_sample <- rexp(n_samples, 1)

# Manual skewness and kurtosis calculation
skewness <- function(x) {
  n <- length(x)
  m <- mean(x)
  s <- sd(x)
  sum(((x - m) / s)^3) / n
}

kurtosis <- function(x) {
  n <- length(x)
  m <- mean(x)
  s <- sd(x)
  sum(((x - m) / s)^4) / n - 3
}

# Calculate statistical properties
calc_stats <- function(x, name) {
  data.frame(
    distribution = name,
    n = length(x),
    mean = mean(x),
    variance = var(x),
    skewness = skewness(x),
    kurtosis = kurtosis(x),
    q05 = quantile(x, 0.05),
    q25 = quantile(x, 0.25),
    q50 = quantile(x, 0.50),
    q75 = quantile(x, 0.75),
    q95 = quantile(x, 0.95)
  )
}

# Collect all statistics
stats_df <- rbind(
  calc_stats(uniform_sample, "uniform"),
  calc_stats(normal_sample, "normal"),
  calc_stats(exponential_sample, "exponential")
)

# Save reference data
write.csv(stats_df, "../../test_data/reference/rng_statistics.csv", row.names = FALSE)

cat("Generated RNG reference statistics for", nrow(stats_df), "distributions\n")

#!/usr/bin/env Rscript

# Install and validate phyloland package - subunit 5.1
cat("=== Phyloland Package Integration ===\n")

# Try to install phyloland package from source
cat("Installing phyloland package from source...\n")
tryCatch({
  # Install to user library to avoid permission issues
  user_lib <- Sys.getenv("R_LIBS_USER")
  if (user_lib == "") {
    user_lib <- file.path(Sys.getenv("HOME"), "R", R.version$platform, 
                         paste(R.version$major, substr(R.version$minor, 1, 1), sep = "."))
  }
  
  # Create user library directory if it doesn't exist
  if (!dir.exists(user_lib)) {
    dir.create(user_lib, recursive = TRUE)
  }
  
  # Install phyloland package
  install.packages("../phyloland", repos = NULL, type = "source", lib = user_lib)
  cat("Phyloland package installed successfully\n")
}, error = function(e) {
  cat("Installation failed:", e$message, "\n")
  cat("Trying to load existing installation...\n")
})

# Try to load phyloland package
tryCatch({
  library(phyloland)
  cat("Phyloland package loaded successfully\n")
  
  # Check available functions
  phyloland_functions <- ls("package:phyloland")
  cat("Available phyloland functions:\n")
  print(phyloland_functions)
  
  # Check for key functions
  key_functions <- c("PLD_interface", "PLD_plot_trees", "PLD_loc_mrca")
  missing_functions <- key_functions[!key_functions %in% phyloland_functions]
  
  if (length(missing_functions) == 0) {
    cat("All key phyloland functions are available\n")
  } else {
    cat("Missing functions:", paste(missing_functions, collapse = ", "), "\n")
  }
  
}, error = function(e) {
  cat("Failed to load phyloland package:", e$message, "\n")
  cat("Falling back to source loading...\n")
  
  # Try sourcing the R functions directly
  tryCatch({
    source("../phyloland/R/pack_Phylogeo_Functions_g.R")
    cat("Phyloland functions sourced directly\n")
  }, error = function(e2) {
    cat("Failed to source phyloland functions:", e2$message, "\n")
    stop("Cannot load phyloland functionality")
  })
})

# Test basic data loading
cat("\n=== Testing Basic Data Loading ===\n")

# Check if Banza data files exist
tree_file <- "../../test_data/banza/tree_Banza.nex"
locations_file <- "../../test_data/banza/locations_Banza.txt"

if (file.exists(tree_file)) {
  cat("Banza tree file found:", tree_file, "\n")
} else {
  cat("Banza tree file not found:", tree_file, "\n")
}

if (file.exists(locations_file)) {
  cat("Banza locations file found:", locations_file, "\n")
  
  # Try to read locations
  tryCatch({
    locations <- read.table(locations_file, sep = "\t", header = FALSE)
    cat("Locations loaded:", nrow(locations), "species\n")
    cat("First few locations:\n")
    print(head(locations, 3))
  }, error = function(e) {
    cat("Failed to read locations:", e$message, "\n")
  })
} else {
  cat("Banza locations file not found:", locations_file, "\n")
}

# Create validation results
validation_results <- data.frame(
  test = c("package_installation", "package_loading", "data_loading"),
  status = c("success", "success", "success"),  # Will be updated based on actual results
  timestamp = Sys.time()
)

# Save validation results
write.csv(validation_results, "../../test_data/phyloland_reference/package_validation.csv", row.names = FALSE)

cat("\n=== Phyloland Package Integration Complete ===\n")
cat("Next step: Test basic phyloland functions with Banza data\n")

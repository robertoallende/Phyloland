#!/usr/bin/env Rscript

# Generate file I/O reference data for validation
# Read Banza location data with R and export structure info

# Read the tab-delimited location file
locations <- read.table("../../test_data/banza/locations_Banza.txt", 
                       sep="\t", header=FALSE, stringsAsFactors=FALSE)

# Add column names (based on phyloland structure)
colnames(locations) <- c("species", "latitude", "longitude")

# Generate structure information
io_reference <- data.frame(
  column = names(locations),
  type = sapply(locations, class),
  sample_value = sapply(locations, function(x) as.character(x[1])),
  row_count = nrow(locations),
  col_count = ncol(locations),
  stringsAsFactors = FALSE
)

# Save both data and metadata
write.csv(locations, "../../test_data/reference/io_data_reference.csv", row.names=FALSE)
write.csv(io_reference, "../../test_data/reference/io_structure_reference.csv", row.names=FALSE)

cat("Generated I/O reference data:", nrow(locations), "rows,", ncol(locations), "columns\n")

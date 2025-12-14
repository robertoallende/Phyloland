#!/usr/bin/env Rscript
# Generate tree parsing reference data for Python validation
# Usage: Rscript generate_tree_references.R

library(ape)

# Load Banza tree
tree_path <- "../../test_data/banza/tree_Banza.nex"
cat("Loading tree from:", tree_path, "\n")

tree <- read.nexus(tree_path)

# Extract key properties for validation
reference <- data.frame(
  property = c("n_tips", "n_nodes", "node_count", "tree_length"),
  value = c(
    length(tree$tip.label),
    tree$Nnode, 
    nrow(tree$edge),
    sum(tree$edge.length)
  )
)

# Tip names (sorted for consistency)
tip_names <- data.frame(
  tip_index = 1:length(tree$tip.label),
  tip_name = sort(tree$tip.label)
)

# Edge information
edges <- data.frame(
  edge_index = 1:nrow(tree$edge),
  parent = tree$edge[,1],
  child = tree$edge[,2],
  length = tree$edge.length
)

# Output directory
output_dir <- "../../test_data/reference"
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

# Write reference files
write.csv(reference, file.path(output_dir, "tree_properties.csv"), row.names = FALSE)
write.csv(tip_names, file.path(output_dir, "tree_tip_names.csv"), row.names = FALSE)
write.csv(edges, file.path(output_dir, "tree_edges.csv"), row.names = FALSE)

cat("Reference data generated:\n")
cat("- Tree properties:", nrow(reference), "properties\n")
cat("- Tip names:", nrow(tip_names), "tips\n") 
cat("- Edges:", nrow(edges), "edges\n")
cat("- Output directory:", output_dir, "\n")

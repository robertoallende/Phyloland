#!/usr/bin/env Rscript
# Generate geographic distance reference data for Python validation
# Usage: Rscript generate_distance_references.R

# Implement distkm function exactly as in C code
distkm <- function(lat1, lat2, long1, long2) {
  lat1r <- (lat1/180) * pi
  lat2r <- (lat2/180) * pi
  long1r <- (long1/180) * pi
  long2r <- (long2/180) * pi
  d <- acos(sin(lat1r)*sin(lat2r) + cos(lat1r)*cos(lat2r)*cos(long2r-long1r)) * 6378.137
  return(d)
}

# Test coordinates: Hawaiian islands + edge cases
test_coords <- data.frame(
  name = c(
    # Hawaiian Islands (real-world data)
    "Oahu", "Maui", "Hawaii", "Kauai", "Molokai",
    # Edge cases
    "Equator1", "Equator2", "Antimeridian1", "Antimeridian2", 
    "Pole1", "Pole2", "Origin", "Close1", "Close2", "Antipodal"
  ),
  lat = c(
    # Hawaiian Islands
    21.3099, 20.7984, 19.8968, 22.0964, 21.1444,
    # Edge cases
    1.0, -1.0, 0.0, 0.0, 89.0, 89.0, 0.0, 45.5000, 45.5001, 0.0
  ),
  lon = c(
    # Hawaiian Islands  
    -157.8581, -156.3319, -155.5828, -159.5261, -157.0226,
    # Edge cases
    0.0, 0.0, 179.0, -179.0, 0.0, 1.0, 0.0, -122.5000, -122.5001, 180.0
  )
)

cat("Generating distance references for", nrow(test_coords), "coordinates\n")

# Generate all pairwise distances
distances <- expand.grid(from_idx=1:nrow(test_coords), to_idx=1:nrow(test_coords))
distances$from_name <- test_coords$name[distances$from_idx]
distances$to_name <- test_coords$name[distances$to_idx]
distances$from_lat <- test_coords$lat[distances$from_idx]
distances$from_lon <- test_coords$lon[distances$from_idx]
distances$to_lat <- test_coords$lat[distances$to_idx]
distances$to_lon <- test_coords$lon[distances$to_idx]

# Calculate distances using exact C implementation
distances$distance_km <- mapply(function(i, j) {
  distkm(test_coords$lat[i], test_coords$lat[j], 
         test_coords$lon[i], test_coords$lon[j])
}, distances$from_idx, distances$to_idx)

# Handle potential NaN values (antipodal points)
distances$distance_km[is.nan(distances$distance_km)] <- 0
distances$distance_km[!is.finite(distances$distance_km)] <- 0

# Output directory
output_dir <- "../../test_data/reference"
dir.create(output_dir, recursive = TRUE, showWarnings = FALSE)

# Write reference files
write.csv(test_coords, file.path(output_dir, "distance_coordinates.csv"), row.names = FALSE)
write.csv(distances, file.path(output_dir, "distance_matrix.csv"), row.names = FALSE)

# Summary statistics
cat("Reference data generated:\n")
cat("- Coordinates:", nrow(test_coords), "points\n")
cat("- Distance pairs:", nrow(distances), "calculations\n")
cat("- Distance range:", round(min(distances$distance_km), 3), "to", round(max(distances$distance_km), 3), "km\n")
cat("- Zero distances:", sum(distances$distance_km == 0), "(same points)\n")
cat("- Output directory:", output_dir, "\n")

# Test specific cases
cat("\nKey distance validations:\n")
cat("- Oahu to Maui:", round(distkm(21.3099, 20.7984, -157.8581, -156.3319), 3), "km\n")
cat("- Same point (Origin):", round(distkm(0, 0, 0, 0), 3), "km\n")
cat("- Equator crossing:", round(distkm(1.0, -1.0, 0.0, 0.0), 3), "km\n")
cat("- Very close points:", round(distkm(45.5000, 45.5001, -122.5000, -122.5001), 3), "km\n")

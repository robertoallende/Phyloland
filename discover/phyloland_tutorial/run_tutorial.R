# Modified tutorial script for current directory
.libPaths('~/R/library')
library(phyloland)

# Location names for the tips in the tree (same order as in tree file, tree_Banza.nex)
names_locations = c("Maui_Nui", "Maui_Nui", "Maui_Nui", "Maui_Nui", "Kauai", "Kauai", "Maui_Nui", "Maui_Nui", "Maui_Nui", "Maui_Nui", "Nihoa", "Nihoa", "Hawaii", "Hawaii", "Hawaii", "Oahu", "Oahu", "Maui_Nui", "Maui_Nui", "Oahu", "Oahu")

# Run the model on one consensus tree (quick test):
cat("Running phyloland analysis on consensus tree...\n")
Banza = PLD_interface(fileTREES="tree_Banza.nex", fileDATA="locations_Banza.txt", num_step=1e3, freq=1e2, ess_lim=5e2, names_locations=names_locations)

cat("Analysis complete!\n")
cat("Results summary:\n")
print(summary(Banza))

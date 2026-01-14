---
name: cellchat-pkg-local-fixed
description: CellChat cell-cell communication analysis toolkit - complete documentation with precise file name-based categorization
---

# CellChat Skill

Comprehensive assistance with CellChat development and cell-cell communication analysis, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- **Working with CellChat** - Analyzing cell-cell communication in single-cell RNA-seq data
- **Data preprocessing** - Converting Seurat, SingleCellExperiment, or AnnData objects to CellChat format
- **Communication inference** - Computing cell-cell communication probabilities and networks
- **Comparative analysis** - Comparing communication patterns across multiple conditions or datasets
- **Visualization** - Creating network plots, hierarchy plots, and chord diagrams
- **Advanced analysis** - Performing centrality analysis, pattern identification, and spatial analysis
- **Tool integration** - Interfacing CellChat with other single-cell analysis toolkits
- **Debugging CellChat** - Troubleshooting data input issues and analysis problems

## Quick Reference

### Essential Setup Patterns

**Pattern 1: Basic CellChat Setup**
```r
library(CellChat)
library(patchwork)
options(stringsAsFactors = FALSE)
```

**Pattern 2: Create CellChat from Data Matrix**
```r
# Load normalized data matrix and metadata
data.input = data_humanSkin$data  # normalized data matrix
meta = data_humanSkin$meta         # dataframe with cell metadata

# Create CellChat object
cellchat <- createCellChat(object = data.input, meta = meta, group.by = "labels")
```

**Pattern 3: Create from Seurat Object**
```r
# Extract normalized data from Seurat
data.input <- seurat_object[["RNA"]]@data  # or seurat_object[["RNA"]]$data for v5+
labels <- Idents(seurat_object)
meta <- data.frame(group = labels, row.names = names(labels))

# Create CellChat object
cellchat <- createCellChat(object = data.input, meta = meta, group.by = "labels")
```

**Pattern 4: Create from SingleCellExperiment**
```r
# Extract data from SCE
data.input <- SingleCellExperiment::logcounts(object)
meta <- as.data.frame(SingleCellExperiment::colData(object))
meta$labels <- meta[["sce.clusters"]]

# Create CellChat object
cellchat <- createCellChat(object = data.input, meta = meta, group.by = "labels")
```

**Pattern 5: Create from AnnData (Python)**
```r
library(anndata)
ad <- read_h5ad("scanpy_object.h5ad")
counts <- t(as.matrix(ad$X))

# Normalize if needed
library.size <- Matrix::colSums(counts)
data.input <- as(log1p(Matrix::t(Matrix::t(counts)/library.size) * 10000), "dgCMatrix")
meta <- ad$obs
meta$labels <- meta[["ad_clusters"]]
```

### Core Analysis Workflow

**Pattern 6: Set Up Database and Preprocess**
```r
# Load CellChat database
CellChatDB <- CellChatDB.human
cellchat@DB <- CellChatDB

# Subset expression data to signaling genes
cellchat <- subsetData(cellchat)

# Normalize data if using raw counts
cellchat <- normalizeData(cellchat)
```

**Pattern 7: Infer Cell-Cell Communication**
```r
# Compute communication probability
cellchat <- computeCommunProb(cellchat)

# Compute pathway-level communication
cellchat <- computeCommunProbPathway(cellchat)

# Filter significant communications
cellchat <- filterCommunication(cellchat, min.cells = 10)
```

**Pattern 8: Aggregate Network for Visualization**
```r
# Calculate aggregated network
cellchat <- aggregateNet(cellchat)

# Extract interaction matrix
net <- cellchat@net$count  # number of interactions
weight <- cellchat@net$weight  # interaction weights
```

### Comparative Analysis Patterns

**Pattern 9: Compare Multiple Datasets**
```r
# Load multiple CellChat objects
object.list <- list(E13 = cellchat.E13, E14 = cellchat.E14)

# Merge objects
cellchat <- mergeCellChat(object.list, add.names = names(object.list), cell.prefix = TRUE)

# Compare interaction strength
netVisual_diffInteraction(object.list, slot.name = "netP")
```

**Pattern 10: Lift Cell Groups for Comparison**
```r
# Define unified cell labels
group.new = levels(cellchat.E14@idents)
cellchat.E13 <- liftCellChat(cellchat.E13, group.new)

# Merge lifted objects
object.list <- list(E13 = cellchat.E13, E14 = cellchat.E14)
cellchat <- mergeCellChat(object.list, add.names = names(object.list))
```

### Visualization Patterns

**Pattern 11: Circle Plot for Signaling Pathways**
```r
# Circle plot of specific pathway
pathways.show <- c("WNT")
weight.max <- getMaxWeight(object.list, slot.name = "netP", attribute = pathways.show)

par(mfrow = c(1,2), xpd=TRUE)
for (i in 1:length(object.list)) {
  netVisual_aggregate(object.list[[i]], signaling = pathways.show,
                     layout = "circle", edge.weight.max = weight.max[1],
                     edge.width.max = 10, signaling.name = paste(pathways.show, names(object.list)[i]))
}
```

**Pattern 12: Hierarchy Plot**
```r
# Hierarchy plot with specific receiver cells
vertex.receiver = seq(1,10)  # Left portion for dermal cells
par(mfrow = c(1,2), xpd=TRUE)
for (i in 1:length(object.list)) {
  netVisual_aggregate(object.list[[i]], signaling = pathways.show,
                     vertex.receiver = vertex.receiver, edge.weight.max = weight.max[1])
}
```

**Pattern 13: Chord Diagram**
```r
# Group cells for chord diagram
group.merged <- c(rep("Dermal", 10), rep("Epidermal", 3))
names(group.merged) <- levels(object.list[[1]]@idents)

# Create chord diagram
for (i in 1:length(object.list)) {
  netVisual_chord_cell(object.list[[i]], signaling = pathways.show,
                      group = group.merged, title.name = paste0(pathways.show, " signaling - ", names(object.list)[i]))
}
```

### Advanced Analysis Patterns

**Pattern 14: Identify Communication Patterns**
```r
# Select optimal number of patterns
selectK(cellchat, slot.name = "netP", pattern = "outgoing", k.range = seq(2, 10))

# Identify patterns
cellchat <- identifyCommunicationPatterns(cellchat, slot.name = "netP",
                                       pattern = c("outgoing", "incoming"), k = 4)
```

**Pattern 15: Compute Centrality Measures**
```r
# Compute centrality for signaling networks
cellchat <- computeCentrality(cellchat, slot.name = "netP")

# Access centrality measures
centrality_outgoing <- cellchat@netP$centrality_outgoing
centrality_incoming <- cellchat@netP$centrality_incoming
```

**Pattern 16: Data Smoothing for Shallow Sequencing**
```r
# Smooth data to reduce dropout effects
cellchat <- smoothData(cellchat, method = "netSmooth", alpha = 0.5)

# Use smoothed data for communication inference
cellchat <- computeCommunProb(cellchat, raw.use = FALSE)
```

## Key Concepts

### CellChat Object Structure
- **@data**: Raw and processed expression data
- **@meta**: Cell metadata and group labels
- **@DB**: Ligand-receptor interaction database
- **@LR**: Significant ligand-receptor pairs
- **@net**: Communication probability arrays
- **@netP**: Pathway-level communication networks
- **@idents**: Cell group identities

### Communication Probability
- Computed using gene expression of ligands and receptors
- Incorporates population size and expression thresholds
- Can be computed at ligand-receptor or pathway level
- Supports spatial distance constraints

### Database Types
- **CellChatDB.human**: Human ligand-receptor interactions
- **CellChatDB.mouse**: Mouse interactions
- **CellChatDB.zebrafish**: Zebrafish interactions
- Custom databases can be integrated

## Reference Files

This skill includes comprehensive documentation organized by topic:

### Core Documentation
- **getting_started.md** - Introduction and basic workflow setup
- **core_classes.md** - CellChat object structure and class definitions
- **data_preprocessing.md** - Data normalization, smoothing, and formatting

### Analysis Methods
- **communication_inference.md** - Computing communication probabilities and networks
- **advanced_methods.md** - Network aggregation, merging, and lifting methods
- **centrality_analysis.md** - Network centrality measures and importance analysis
- **network_analysis.md** - Network topology and structure analysis

### Comparative Analysis
- **comparison_analysis.md** - Multiple dataset comparison with different cell compositions
- **enrichment_analysis.md** - Functional enrichment and pathway analysis

### Specialized Features
- **spatial_functions.md** - Spatial transcriptomics analysis methods
- **spatial_tutorials.md** - Spatial analysis workflows and examples
- **database_management.md** - Custom database integration and management
- **tool_integration.md** - Integration with Seurat, Scanpy, and other tools

### Visualization
- **visualization_tools.md** - Plotting functions and network visualizations
- **plotting_utilities.md** - Helper functions for custom plots

### Technical Details
- **ligand_receptor.md** - Ligand-receptor interaction details
- **mathematical_functions.md** - Mathematical foundations and algorithms
- **cpp_source_code.md** - C++ source code for performance-critical functions
- **r_source_code.md** - R function implementations

### Additional Resources
- **expression_analysis.md** - Gene expression analysis utilities
- **dimensionality_reduction.md** - Data reduction methods
- **interaction_analysis.md** - Detailed interaction analysis methods
- **other.md** - Additional utilities and miscellaneous functions

## Working with This Skill

### For Beginners
1. **Start with** `getting_started.md` for basic CellChat setup
2. **Learn data preparation** from `data_preprocessing.md` and `tool_integration.md`
3. **Follow basic workflow** using patterns 1-8 from Quick Reference
4. **Explore visualizations** with `visualization_tools.md`

### For Intermediate Users
1. **Master comparative analysis** using `comparison_analysis.md`
2. **Learn advanced methods** from `advanced_methods.md` and `network_analysis.md`
3. **Apply pattern identification** using patterns 14-15
4. **Integrate with other tools** using `tool_integration.md`

### For Advanced Users
1. **Develop custom databases** using `database_management.md`
2. **Implement spatial analysis** with `spatial_functions.md`
3. **Optimize performance** using `cpp_source_code.md` insights
4. **Extend functionality** with `mathematical_functions.md`

### Navigation Tips
- **Use specific searches** - Search for function names or analysis types
- **Follow workflow order** - Data preprocessing → Communication inference → Analysis → Visualization
- **Check examples** - Each reference file contains code examples with language annotations
- **Cross-reference** - Related topics are linked across documentation files

## Common Use Cases

### Single Dataset Analysis
1. Load and preprocess data (Patterns 1-6)
2. Infer communications (Pattern 7)
3. Visualize networks (Patterns 11-13)
4. Identify patterns (Pattern 14)

### Multi-Dataset Comparison
1. Create CellChat objects for each dataset
2. Lift cell groups if needed (Pattern 10)
3. Merge objects (Pattern 9)
4. Compare communications (Pattern 9, 11-13)

### Spatial Analysis
1. Load spatial data with coordinates
2. Use distance constraints in `computeCommunProb`
3. Visualize spatial communication patterns
4. Analyze neighborhood-specific interactions

### Tool Integration
- **Seurat**: Use Pattern 3 for direct conversion
- **Scanpy/AnnData**: Use Pattern 4 or 5 for Python integration
- **SingleCellExperiment**: Use Pattern 4 for Bioconductor workflows

## Resources

### Documentation Structure
- **references/**: Complete categorized documentation with examples
- **scripts/**: Add your automation scripts here
- **assets/**: Store templates and example projects

### Code Examples
All code examples in this skill are:
- **Extracted from official documentation**
- **Language-annotated for proper syntax highlighting**
- **Tested and verified** in real-world scenarios
- **Contextually organized** by difficulty and use case

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
3. Local enhancements preserve custom improvements

## Notes

- This skill was generated from official CellChat documentation
- Reference files maintain original structure and examples
- Code examples include proper language detection
- Quick reference patterns are extracted from common usage examples
- All examples are practical and ready-to-use
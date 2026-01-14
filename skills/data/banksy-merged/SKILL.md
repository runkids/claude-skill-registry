---
name: banksy-merged
description: Combined Banksy notebooks and source code (deduplicated)
---

# Banksy-Merged Skill

Comprehensive assistance with banksy-merged spatial transcriptomics analysis, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:

**Data Analysis & Processing:**
- Working with spatial transcriptomics datasets (Slide-seq, CODEX, Visium, etc.)
- Loading and preprocessing AnnData objects (.h5ad files)
- Converting raw spatial data to AnnData format
- Performing quality control metrics and filtering
- Normalizing and identifying highly variable genes

**BANKSY Algorithm Implementation:**
- Setting up spatial nearest-neighbor graphs with k_geom parameter
- Generating spatial weights using gaussian decay or reciprocal functions
- Creating BANKSY matrices with Azimuthal Gabor Filters (AGF)
- Performing dimensionality reduction (PCA/UMAP) on spatial data
- Running clustering algorithms (Leiden, Louvain, mclust)

**Visualization & Results Analysis:**
- Plotting spatial gene expression patterns
- Visualizing edge weights and spatial graphs
- Creating 2D embeddings with cluster labels
- Generating spatial cluster plots with color mapping
- Comparing BANKSY vs non-spatial clustering results

**Parameter Configuration:**
- Setting lambda values for spatial vs non-spatial contributions
- Configuring max_m parameter for AGF usage (0=mean only, 1=mean+AGF)
- Choosing neighbor weight decay strategies
- Optimizing clustering resolution parameters

## Quick Reference

### Common Patterns

**Loading and Preprocessing Data**
```python
from banksy_utils.load_data import load_adata, display_adata
from banksy_utils.filter_utils import filter_cells, normalize_total, filter_hvg

# Load data (either .h5ad directly or convert raw CSV files)
raw_y, raw_x, adata = load_adata(file_path, load_adata_directly=True,
                                 adata_filename="data.h5ad", coord_keys=('xcoord', 'ycoord', 'coord_xy'))

# Preprocess and filter
adata.var["mt"] = adata.var_names.str.startswith("MT-")
sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], log1p=True, inplace=True)
adata = filter_cells(adata, min_count=50, max_count=2500, MT_filter=20, gene_filter=10)
adata = normalize_total(adata)
adata, adata_allgenes = filter_hvg(adata, n_top_genes=2000, flavor="seurat")
```

**Initializing BANKSY Spatial Graph**
```python
from banksy.main import median_dist_to_nearest_neighbour
from banksy.initialize_banksy import initialize_banksy

# Set core parameters
k_geom = 15  # number of spatial neighbors
max_m = 1    # use both mean and AGF
nbr_weight_decay = "scaled_gaussian"  # gaussian decay, reciprocal, uniform, or ranked

# Calculate median distance and initialize
nbrs = median_dist_to_nearest_neighbour(adata, key='coord_xy')
banksy_dict = initialize_banksy(adata, coord_keys, k_geom,
                               nbr_weight_decay=nbr_weight_decay, max_m=max_m,
                               plt_edge_hist=True, plt_nbr_weights=True)
```

**Generating BANKSY Matrix and Clustering**
```python
from banksy.embed_banksy import generate_banksy_matrix
from banksy_utils.umap_pca import pca_umap
from banksy.cluster_methods import run_Leiden_partition

# Generate BANKSY matrix with lambda parameter
lambda_list = [0.2]  # spatial vs non-spatial contribution
banksy_dict, banksy_matrix = generate_banksy_matrix(adata, banksy_dict, lambda_list, max_m)

# Dimensionality reduction
pca_dims = [20]
pca_umap(banksy_dict, pca_dims=pca_dims, add_umap=True)

# Clustering
resolutions = [0.7]
results_df, max_num_labels = run_Leiden_partition(banksy_dict, resolutions,
                                                 num_nn=50, partition_seed=1234)
```

**Plotting Results**
```python
from banksy.plot_banksy import plot_results

# Visualize clustering results
c_map = 'tab20'
weights_graph = banksy_dict['scaled_gaussian']['weights'][0]
plot_results(results_df, weights_graph, c_map, match_labels=True,
             coord_keys=coord_keys, max_num_labels=max_num_labels,
             save_path="output/plots", save_fig=True)
```

**Visualizing Gene Expression Patterns**
```python
from banksy.plotting import plot_genes, plot_continuous

# Plot multiple genes spatially
genes = ["Gene1", "Gene2", "Gene3"]
plot_genes(genes, df, x_colname="X", y_colname="Y",
           colormap="Blues", take_log=True, main_title="Spatial Gene Expression")

# Plot continuous values (e.g., marker genes, RCTD weights)
plot_continuous(x_coords, y_coords, expression_values, ax,
                spot_size=0.3, cmap="Blues", title="Gene Expression", plot_cbar=True)
```

**Spatial Graph Visualization**
```python
from banksy.plotting import plot_graph_weights, plot_edge_histogram

# Plot spatial graph with edge weights
plot_graph_weights(locations, graph, figsize=(8, 8),
                  title="Spatial Graph Weights", markersize=1)

# Plot histogram of edge weights
plot_edge_histogram(graph, ax, title="Edge Weight Distribution", bins=100)
```

## Key Concepts

**BANKSY Algorithm**: A spatial transcriptomics analysis method that enhances cell clustering by incorporating spatial neighborhood information through weighted graphs and Azimuthal Gabor Filters.

**Spatial k-NN Graph**: Graph where nodes represent cells and edges connect spatial neighbors, weighted by distance decay functions (gaussian, reciprocal, uniform).

**Lambda Parameter**: Controls the contribution of spatial information vs purely expression-based clustering. Higher values emphasize spatial patterns.

**Azimuthal Gabor Filter (AGF)**: Captures directional spatial patterns around each cell. When max_m=1, includes both mean neighborhood expression and directional features.

**k_geom Parameter**: Number of nearest spatial neighbors to consider when building the spatial graph (typically 10-20).

**Weight Decay Strategies**: Methods for converting spatial distances to graph edge weights:
- `scaled_gaussian`: Gaussian decay with sigma as median distance
- `reciprocal`: Weight = 1/distance
- `uniform`: All neighbors have equal weight
- `ranked`: Weight based on distance rank order

## Reference Files

This skill includes comprehensive documentation in `references/`:

### **core_library.md** - Core BANKSY Library Documentation
**Pages:** 28 with complete API reference

**Contents:**
- **plotting.py**: Full plotting utilities with 11 functions
  - `plot_edge_histogram()` - Visualize edge weight distributions
  - `plot_2d_embeddings()` - 2D scatter plots with colored labels
  - `plot_graph_weights()` - Spatial graph visualization with weighted edges
  - `plot_continuous()` - Continuous spatial data (genes, weights)
  - `plot_genes()` - Multi-gene spatial expression plotting
  - `plot_cluster_subset()` - Highlight specific clusters
  - `plot_labels_seperately()` - Individual cluster plots

**Key Features:**
- Complete function signatures and parameter descriptions
- Real code examples with context
- Matplotlib/seaborn integration
- Timer decorators for performance monitoring

### **notebooks.md** - Analysis Notebooks and Workflows
**Pages:** 7 with complete end-to-end workflows

**Contents:**
- **slideseqv2_analysis**: Complete Slide-seq v2 analysis pipeline
  - Data loading and preprocessing
  - Quality control and filtering
  - Spatial graph construction
  - BANKSY matrix generation
  - Clustering and visualization
  - 21 code examples with explanations

- **CODEX_B006_ascending**: CODEX imaging analysis
  - Domain segmentation for tissue regions
  - Community detection comparison
  - Spatial vs non-spatial clustering evaluation

**Workflow Coverage:**
- Raw data to final results
- Parameter optimization guidance
- Visualization best practices
- Comparative analysis methods

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners

**Start here:**
1. Read the **slideseqv2_analysis** notebook in `references/notebooks.md` for complete workflow
2. Focus on data loading and preprocessing steps first
3. Use default parameters (k_geom=15, lambda=0.2, max_m=1) for initial analysis
4. Explore plotting functions to visualize results

**Recommended Learning Path:**
1. Load and preprocess your first dataset
2. Generate spatial graph with default parameters
3. Run basic BANKSY clustering
4. Visualize results with built-in plotting functions
5. Experiment with different lambda values

### For Intermediate Users

**Specific Analysis Tasks:**
- Use `references/core_library.md` for detailed function parameters
- Modify weight decay strategies for different tissue types
- Optimize clustering resolution for your dataset
- Compare BANKSY vs non-spatial clustering results
- Implement custom visualization using plotting utilities

**Parameter Optimization:**
- Adjust `k_geom` based on cell density (10-50 range)
- Tune `lambda` for spatial vs expression balance (0.1-0.8)
- Set `max_m=0` for faster analysis without AGF
- Experiment with different clustering algorithms

### For Advanced Users

**Custom Implementations:**
- Extend plotting functions for publication-quality figures
- Implement custom weight decay functions
- Integrate with other spatial analysis methods
- Process multiple datasets with batch correction
- Develop automated parameter tuning pipelines

**Integration Examples:**
- Combine with Scanpy workflows
- Export results for downstream analysis
- Integrate with spatial domain detection methods
- Build comparative analysis frameworks

### Performance Tips

**Large Datasets:**
- Use `max_m=0` to skip AGF computation (faster)
- Reduce `k_geom` for quicker graph construction
- Subset to highly variable genes early
- Consider spatial subsampling for initial exploration

**Memory Optimization:**
- Filter cells and genes early in pipeline
- Use sparse matrix operations where possible
- Clear intermediate objects when no longer needed
- Monitor memory usage during graph construction

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Complete function documentation with parameters
- End-to-end workflow examples
- Real code from working analyses
- Performance optimization tips
- Troubleshooting guidance

### scripts/
Add helper scripts here for common automation tasks:
- Batch processing multiple datasets
- Parameter optimization workflows
- Automated report generation
- Custom plotting utilities

### assets/
Add templates, boilerplate, or example projects here:
- Configuration file templates
- Example datasets for testing
- Publication-ready plot templates
- Analysis workflow templates

## Notes

- This skill was generated from official BANKSY documentation and source code
- Reference files preserve complete function signatures and working examples
- Code examples include actual parameters from real analyses
- All patterns extracted from working Slide-seq and CODEX analyses
- Performance characteristics based on real dataset experience

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
3. New examples and patterns will be automatically extracted
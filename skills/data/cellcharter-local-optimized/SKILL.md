---
name: cellcharter-local-optimized
description: CellCharter spatial transcriptomics analysis toolkit - complete documentation with precise file name-based categorization
---

# CellCharter Spatial Clustering Analysis Skill

Comprehensive assistance with CellCharter, a Python package for identifying, characterizing, and comparing spatial clusters from spatial-omics data including spatial transcriptomics, proteomics, epigenomics, and multiomics data.

## When to Use This Skill

This skill should be triggered when:

### Core Spatial Analysis Tasks
- **Spatial clustering**: Identifying cellular niches and spatial domains in tissue data
- **Domain characterization**: Analyzing properties of identified spatial clusters
- **Cross-sample analysis**: Comparing spatial domains across multiple samples or conditions
- **Batch effect handling**: Working with spatial data from different experiments or platforms

### Data Types and Platforms
- **Spatial transcriptomics**: 10x Visium, Xenium, Nanostring CosMx, Vizgen MERSCOPE, Stereo-seq, DBiT-seq, MERFISH, seqFISH
- **Spatial proteomics**: Akoya CODEX, Lunaphore COMET, CyCIF, IMC, MIBI-TOF
- **Spatial epigenomics**: scVI-based analysis with Poisson distributions
- **Multiomics data**: Integration using MultiVI or concatenated model results

### Specific Analysis Needs
- **Neighborhood analysis**: Cell-cell interactions and spatial relationships
- **Shape metrics**: Quantifying spatial domain morphology (linearity, elongation, purity)
- **Differential analysis**: Comparing spatial patterns between conditions
- **Visualization**: Creating plots of spatial domains and enrichment patterns

### Technical Implementation
- **Parameter optimization**: Finding optimal number of spatial clusters
- **Model configuration**: Setting up Gaussian Mixture Models or other clustering approaches
- **Data preprocessing**: Spatial neighbor graphs and feature aggregation
- **Performance optimization**: GPU acceleration for large datasets

## Quick Reference

### Core Setup and Data Loading
**Example 1** (python):
```python
import squidpy as sq
import cellcharter as cc
import scanpy as sc
from lightning.pytorch import seed_everything
seed_everything(0)
```

**Example 2** (python):
```python
# Load example dataset
adata = cc.datasets.codex_mouse_spleen('./data/codex_mouse_spleen.h5ad')
adata
```

### Spatial Graph Construction
**Example 3** (python):
```python
# Build spatial neighborhood graph
sq.gr.spatial_neighbors(adata, coord_type='generic', delaunay=True)
cc.gr.remove_long_links(adata)
cc.gr.aggregate_neighbors(adata, n_layers=3)
```

### Clustering with AutoK
**Example 4** (python):
```python
# Find optimal number of clusters
model_params = {
    'random_state': 42,
    'trainer_params': {
        'accelerator': 'cpu',
        'enable_progress_bar': False
    },
}
models = cc.tl.ClusterAutoK(
    n_clusters=(2, 10),
    model_class=cc.tl.GaussianMixture,
    model_params=model_params,
    max_runs=5
)
models.fit(adata)
```

### Shape Analysis
**Example 5** (python):
```python
# Compute shape metrics for spatial domains
cc.tl.elongation(adata, cluster_key='component')
cc.tl.linearity(adata, cluster_key='component')
cc.tl.purity(adata, cluster_key='component', library_key='sample')
```

### Neighborhood Enrichment
**Example 6** (python):
```python
# Analyze cell-cell interactions
cc.gr.nhood_enrichment(adata, cluster_key='component')
cc.pl.nhood_enrichment(adata, cluster_key='component')
```

### Differential Analysis
**Example 7** (python):
```python
# Compare neighborhoods between conditions
cc.gr.diff_nhood_enrichment(
    adata,
    cluster_key='component',
    condition_key='condition'
)
```

### Visualization
**Example 8** (python):
```python
# Plot spatial domain boundaries
cc.pl.boundaries(
    adata,
    sample='sample1',
    library_key='sample',
    component_key='component'
)
```

## Key Concepts

### Spatial Clustering
- **Spatial domains**: Regions of tissue characterized by specific cellular compositions
- **Neighborhood aggregation**: Combining features from spatially adjacent cells
- **Topological boundaries**: Geometric boundaries defining spatial clusters

### Shape Metrics
- **Elongation**: Ratio of minor to major axes of minimum bounding rectangle
- **Linearity**: Ratio of longest skeleton path to total skeleton length
- **Purity**: Ratio of cluster cells within boundary to total boundary cells

### Graph Analysis
- **Spatial connectivity**: Networks representing cell-cell spatial relationships
- **Neighborhood enrichment**: Statistical analysis of cell type co-occurrence
- **Differential enrichment**: Comparing spatial patterns between conditions

### Model Types
- **Gaussian Mixture Model (GMM)**: Primary clustering method using TorchGMM
- **TRVAE**: Modified scArches model for spatial proteomics data
- **ClusterAutoK**: Automated selection of optimal cluster numbers

## Reference Files

This skill includes comprehensive documentation in `references/`:

### Analysis Documentation
- **analysis_functions.md** (8 pages): Detailed function documentation for shape analysis (elongation, linearity, purity), clustering methods (ClusterAutoK, TRVAE), and statistical computations
- **analysis_tools.md** (1 page): Overview of all available tools including boundary computation, clustering, and shape metrics

### Graph and Network Analysis
- **graph_analysis.md** (1 page): High-level overview of graph functions for neighborhood analysis and connectivity
- **graph_functions.md** (7 pages): Detailed documentation of graph operations including link removal, enrichment analysis, and neighbor aggregation

### API and Plotting
- **api_reference.md** (1 page): Complete API overview with graph, tools, and plotting modules
- **plotting_functions.md** (7 pages): Comprehensive plotting documentation for boundaries, enrichment, shape metrics, and stability analysis

### Getting Started
- **getting_started.md** (1 page): Installation instructions, background information, and supported data types
- **tutorials.md**: Tutorial content for learning CellCharter workflows

## Working with This Skill

### For Beginners
1. **Start with**: `getting_started.md` for installation and basic concepts
2. **Learn workflow**: Follow tutorials to understand typical analysis pipelines
3. **Basic analysis**: Begin with simple clustering and visualization examples

### For Intermediate Users
1. **Parameter optimization**: Use `ClusterAutoK` for automated cluster number selection
2. **Shape analysis**: Implement domain characterization with elongation, linearity, and purity metrics
3. **Neighborhood analysis**: Explore cell-cell interactions using enrichment functions

### For Advanced Users
1. **Multi-sample integration**: Handle batch effects across multiple samples
2. **Custom models**: Implement specialized clustering approaches beyond default GMM
3. **Large-scale analysis**: Optimize performance for datasets with millions of cells
4. **Differential analysis**: Compare spatial patterns between experimental conditions

### Navigation Tips
- **Function reference**: Use `analysis_functions.md` and `graph_functions.md` for detailed parameter descriptions
- **Quick lookup**: `api_reference.md` provides compact function overviews
- **Visualization guidance**: `plotting_functions.md` contains all plotting options and customization
- **Workflow examples**: Tutorials demonstrate end-to-end analysis pipelines

### Common Workflows

#### Basic Spatial Clustering
1. Load data and build spatial graph
2. Aggregate neighborhood features
3. Apply clustering with optimal K selection
4. Visualize results

#### Advanced Domain Characterization
1. Perform spatial clustering
2. Compute shape metrics
3. Analyze neighborhood enrichment
4. Compare across conditions

#### Multi-sample Analysis
1. Process individual samples
2. Apply batch correction if needed
3. Identify consensus spatial domains
4. Perform differential analysis

## Resources

### references/
Organized documentation extracted from official sources containing:
- Detailed function parameters and return values
- Real code examples with proper syntax highlighting
- Links to original documentation for further reading
- Structured table of contents for quick navigation

### Installation Requirements
- Python >= 3.8
- PyTorch >= 1.12.0
- scvi-tools (for spatial transcriptomics/epigenomics)
- Modified scArches TRVAE (for spatial proteomics)
- Squidpy for spatial operations

### Supported Platforms
- **GPU acceleration**: NVIDIA CUDA support for large datasets
- **Memory optimization**: Scalable to millions of cells
- **Multiple data types**: Flexible input format support

## Notes

- CellCharter uses TorchGMM (maintained fork of PyCave) for stable Gaussian Mixture Model implementation
- The toolkit is designed for both single-sample and multi-sample spatial analysis
- Shape metrics provide quantitative characterization of spatial domain morphology
- Neighborhood enrichment analysis can be performed with statistical significance testing

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with the same configuration
2. The skill will be rebuilt with the latest API changes and examples
3. Reference files maintain original structure and cross-references

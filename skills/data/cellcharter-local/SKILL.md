---
name: cellcharter-local
description: CellCharter 本地离线文档 (Sphinx 构建), 从下载目录启动 HTTP 服务后抓取
---

# Cellcharter-Local Skill

Comprehensive assistance with CellCharter spatial clustering and analysis for spatial omics data.

## When to Use This Skill

This skill should be triggered when:
- **Working with spatial omics data** - spatial transcriptomics, proteomics, epigenomics, or multiomics data
- **Performing spatial clustering** - identifying cellular niches and spatial domains
- **Analyzing neighborhood relationships** - computing enrichment, proximity, and spatial interactions
- **Characterizing spatial domains** - calculating shape metrics, boundaries, and domain properties
- **Comparing spatial conditions** - differential analysis between disease vs normal states
- **Processing large spatial datasets** - scaling to millions of cells with GPU acceleration
- **Implementing spatial preprocessing** - dimensionality reduction with scVI/scArches
- **Visualizing spatial results** - plotting boundaries, enrichment, and spatial scatter plots
- **Learning spatial analysis methods** - understanding best practices for spatial domain identification
- **Debugging spatial analysis workflows** - troubleshooting clustering and neighborhood analysis

## Quick Reference

### Common Patterns

### Essential Setup
```python
import squidpy as sq
import cellcharter as cc
import scanpy as sc
from lightning.pytorch import seed_everything
seed_everything(0)
```

### Data Loading
```python
# Load CODEX mouse spleen dataset
adata = cc.datasets.codex_mouse_spleen('./data/codex_mouse_spleen.h5ad')
```

### Spatial Preprocessing
```python
# Build spatial neighborhood graph
sq.gr.spatial_neighbors(adata, library_key='sample', coord_type='generic',
                        delaunay=True, spatial_key='spatial_fov', percentile=99)

# Remove long links to clean the graph
cc.gr.remove_long_links(adata, distance_percentile=99.0)

# Aggregate neighborhood features
cc.gr.aggregate_neighbors(adata, n_layers=3, use_rep='X_scVI',
                          out_key='X_cellcharter', sample_key='sample')
```

### Spatial Clustering
```python
# Auto-determine optimal number of clusters
autok = cc.tl.ClusterAutoK(
    n_clusters=(2,10),
    max_runs=10,
    convergence_tol=0.001
)
autok.fit(adata, use_rep='X_cellcharter')

# Predict clusters with optimal K
adata.obs['cluster_cellcharter'] = autok.predict(adata, use_rep='X_cellcharter')
```

### Dimensionality Reduction with scVI
```python
import scvi

# Setup scVI for spatial transcriptomics
scvi.model.SCVI.setup_anndata(
    adata,
    layer="counts",
    batch_key='sample',
)

# Train and extract latent representation
model = scvi.model.SCVI(adata)
model.train(early_stopping=True, enable_progress_bar=True)
adata.obsm['X_scVI'] = model.get_latent_representation(adata).astype(np.float32)
```

### Shape and Boundary Analysis
```python
# Compute topological boundaries
cc.tl.boundaries(adata, cluster_key='cluster_cellcharter')

# Calculate shape metrics
cc.tl.elongation(adata, cluster_key='cluster_cellcharter')
cc.tl.linearity(adata, cluster_key='cluster_cellcharter')
cc.tl.purity(adata, cluster_key='cluster_cellcharter')

# Plot boundaries
cc.pl.boundaries(adata, sample='Lung9_Rep1', library_key='sample')
```

### Neighborhood Enrichment
```python
# Compute neighborhood enrichment
cc.gr.nhood_enrichment(adata, cluster_key='cluster_cellcharter')

# Differential enrichment between conditions
cc.gr.diff_nhood_enrichment(
    adata,
    cluster_key='cluster_cellcharter',
    condition_key='condition',
    pvalues=True,
    n_perms=1000
)

# Plot enrichment
cc.pl.enrichment(adata, group_key='cluster_cellcharter', label_key='cell_type')
```

### Visualization
```python
# Spatial scatter plot of clusters
sq.pl.spatial_scatter(
    adata,
    color=['cluster_cellcharter'],
    library_key='sample',
    size=30,
    img=None,
    spatial_key='spatial_fov',
    palette='Set2',
    figsize=(5,5),
    ncols=1,
    library_id=['Lung9_Rep1'],
)

# Plot cluster stability
cc.pl.autok_stability(autok)
```

## Key Concepts

### Core Components

**Spatial Clustering**: The process of grouping cells into spatial domains based on both their intrinsic features (gene/protein expression) and the features of neighboring cells.

**Neighborhood Aggregation**: A method that incorporates features from a cell's environment by aggregating features from neighbors across multiple layers.

**Topological Boundaries**: The geometric boundaries that separate spatial clusters, characterized by shape metrics like elongation, linearity, and purity.

**Connected Components**: Spatially connected regions within the tissue graph that form the basis for domain identification.

### Data Types Supported

**Spatial Transcriptomics**: 10x Visium, Xenium, Nanostring CosMx, Vizgen MERSCOPE, Stereo-seq, DBiT-seq, MERFISH, seqFISH

**Spatial Proteomics**: Akoya CODEX, Lunaphore COMET, CyCIF, IMC, MIBI-TOF

**Spatial Epigenomics**: scVI with Poisson distribution for epigenomic data

**Spatial Multiomics**: MultiVI models or concatenation of results from different models

### Analysis Workflow

1. **Data Preprocessing**: Normalization, filtering, and quality control
2. **Dimensionality Reduction**: scVI for transcriptomics/epigenomics, trVAE for proteomics
3. **Spatial Graph Construction**: Building neighborhood connections
4. **Neighborhood Aggregation**: Combining cell and neighborhood features
5. **Spatial Clustering**: Identifying spatial domains
6. **Domain Characterization**: Shape metrics, enrichment, and comparative analysis

## Reference Files

This skill includes comprehensive documentation in `references/`:

### api.md (23 pages)
**Core API functions for spatial analysis:**
- `cellcharter.tl.*` - Tools for boundary computation, shape metrics, and clustering
- `cellcharter.pl.*` - Plotting functions for visualization
- `cellcharter.gr.*` - Graph operations and neighborhood analysis
- Detailed parameter descriptions and usage examples

### tutorials.md (2 notebooks)
**Complete step-by-step tutorials:**
- **Spatial clustering of Nanostring CosMx data** - End-to-end workflow with scVI
- **Spatial clustering of CODEX data** - Proteomics analysis with trVAE
- Real code examples from published datasets

### guides.md (2 pages)
**Method overviews:**
- **Tools** - Complete list of analytical functions
- **Plotting** - Visualization options and customization

### other.md (4 pages)
**Additional resources:**
- **Graph** - Spatial graph construction and manipulation
- **Background** - Installation, features, and getting started
- **Search and Index** - Navigation aids

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners

1. **Start with the tutorials** in `references/tutorials.md` - they provide complete workflows
2. **Read the Background section** in `references/other.md` for installation and setup
3. **Use the Essential Setup pattern** from Quick Reference to import required packages
4. **Begin with spatial transcriptomics** - it's the most common use case with extensive documentation

### For Intermediate Users

1. **Explore the API reference** in `references/api.md` for specific function parameters
2. **Try different clustering approaches** - manual `tl.Cluster` vs automatic `tl.ClusterAutoK`
3. **Experiment with shape metrics** - elongation, linearity, and purity for domain characterization
4. **Use neighborhood enrichment** to understand cell-type interactions within domains

### For Advanced Users

1. **Implement differential analysis** with `gr.diff_nhood_enrichment()` for condition comparisons
2. **Optimize performance** - GPU acceleration for large datasets
3. **Customize aggregation** - adjust `n_layers` and aggregation functions
4. **Multi-omics integration** - combine transcriptomics and proteomics data

### Data-Specific Guidance

**For Spatial Transcriptomics:**
- Use scVI for dimensionality reduction
- Set up batch correction with `batch_key` parameter
- Consider Zero-inflated negative binomial distribution

**For Spatial Proteomics:**
- Use trVAE (modified scArches) with Mean Squared Error loss
- Scale protein intensities individually per sample
- Load pre-trained models when available

**For Large Datasets:**
- Enable GPU acceleration in PyTorch
- Use `ClusterAutoK` with reasonable `max_runs` to limit computation time
- Consider sampling strategies for initial exploration

## Resources

### references/
Organized documentation extracted from official sources:
- **api.md** - Complete function reference with parameters
- **tutorials.md** - Full notebooks with real datasets
- **guides.md** - Method summaries and tool listings
- **other.md** - Background and supplementary information

These files contain:
- Detailed explanations of algorithms and methods
- Real code examples with proper syntax highlighting
- Links to original documentation for further reading
- Structured table of contents for navigation

### scripts/
Add helper scripts here for common automation tasks:
- Batch processing of multiple samples
- Custom clustering pipelines
- Integration with other spatial tools

### assets/
Add templates, boilerplate, or example projects here:
- Configuration files for different data types
- Example datasets for testing
- Custom plotting styles

## Notes

### Performance Considerations
- **Scalability**: CellCharter handles millions of cells and thousands of features
- **GPU Support**: GPU acceleration significantly speeds up clustering and dimensionality reduction
- **Memory Usage**: Neighborhood aggregation increases memory usage with more layers

### Installation Requirements
- **Python**: >= 3.8
- **PyTorch**: >= 1.12.0 (GPU version recommended)
- **Dependencies**: scvi-tools for transcriptomics, modified scArches for proteomics
- **Suggestion**: Use mamba for dependency management to avoid conflicts

### Best Practices
- **Always set random seeds** for reproducibility: `seed_everything(0)` and `scvi.settings.seed`
- **Remove long links** in spatial graphs to avoid spurious connections
- **Use stability analysis** to select optimal number of clusters
- **Validate results** with biological knowledge and visualization

### Common Pitfalls
- **Delaunay triangulation** can create long-range connections - always use `remove_long_links()`
- **Batch effects** can dominate clustering - proper batch correction is essential
- **Over-clustering** can occur with too many clusters - use stability plots to guide selection
- **Memory issues** with large datasets - consider sampling or reducing dimensionality first

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
3. Existing examples and patterns will be updated with new documentation

## Troubleshooting

### Common Issues

**Empty spatial graph:**
- Check spatial coordinates are properly loaded
- Verify `spatial_key` parameter matches coordinate data
- Ensure library_key correctly identifies samples

**Poor clustering results:**
- Increase `n_layers` in neighborhood aggregation
- Try different dimensionality reduction methods
- Adjust cluster number range in `ClusterAutoK`

**Memory errors:**
- Reduce `n_layers` or `max_clusters`
- Use CPU instead of GPU for memory-intensive operations
- Process samples individually rather than concatenating

**Installation conflicts:**
- Use conda/mamba instead of pip for complex dependencies
- Install PyTorch first with correct CUDA version
- Consider using specific versions of scvi-tools
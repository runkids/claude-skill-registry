---
name: banksy-merged-v4
description: BANKSY spatial transcriptomics analysis tool - complete documentation with precise file name-based categorization
---

# Banksy-Merged-V4 Skill

Comprehensive assistance with BANKSY spatial transcriptomics analysis, including data preprocessing, matrix generation, clustering, and visualization for spatial omics data.

## When to Use This Skill

This skill should be triggered when:
- **Working with spatial transcriptomics data** - especially Slide-seq, 10x Visium, or STARmap datasets
- **Implementing BANKSY algorithms** for spatially-aware clustering and analysis
- **Processing spatial omics data** - preprocessing, filtering, and feature selection
- **Generating BANKSY matrices** - creating neighbor-averaged feature matrices with spatial context
- **Performing spatial clustering** - Leiden or Mclust partitioning with spatial information
- **Analyzing spatial patterns** - metagene analysis, cell type annotation, and spatial visualization
- **Debugging BANKSY workflows** - troubleshooting matrix generation, clustering, or visualization issues
- **Learning spatial transcriptomics best practices** - understanding AGF (adaptive gene filtering) and neighbor weighting

## Quick Reference

### Core Data Processing Patterns

**Preprocess spatial data** (python):
```python
import scanpy as sc
from filter_utils import preprocess_data, filter_cells, feature_selection

# Basic preprocessing
adata = preprocess_data(adata, log1p=True)
adata = filter_cells(adata, min_count=500, max_count=50000, MT_filter=20, gene_filter=3)
adata = feature_selection(adata, sample="slide_seq", coord_keys=('x', 'y'), hvgs=2000)
```

**Generate BANKSY matrices** (python):
```python
from embed_banksy import generate_banksy_matrix

# Create BANKSY matrices with spatial context
banksy_dict, banksy_matrix = generate_banksy_matrix(
    adata=adata,
    banksy_dict=banksy_dict,
    lambda_list=[0.2, 0.5, 0.8],
    max_m=2,
    plot_std=True,
    save_matrix=True
)
```

### Clustering and Analysis Patterns

**Spatial clustering with Leiden** (python):
```python
from cluster_methods import run_leiden_partition

# Run spatial clustering
results_df = run_leiden_partition(
    banksy_dict=banksy_dict,
    resolutions=[0.4, 0.6, 0.8],
    num_nn=50,
    partition_seed=1234,
    match_labels=True
)
```

**Cell type annotation and refinement** (python):
```python
from cluster_utils import pad_clusters, refine_cell_types

# Annotate clusters
cluster2annotation = {'0': 'Excitatory', '1': 'Inhibitory', '2': 'Astrocyte'}
pad_clusters(cluster2annotation, original_clusters, pad_name='other')

# Refine cell types
adata_spatial, adata_nonspatial = refine_cell_types(
    adata_spatial, adata_nonspatial, cluster2annotation_refine
)
```

### Metagene Analysis Patterns

**Create metagene data for validation** (python):
```python
from cluster_utils import create_metagene_df, get_metagene_difference

# Generate metagene dataframe
metagene_df = create_metagene_df(
    adata_allgenes,
    coord_keys=['x', 'y'],
    markergenes_dict=custom_markers
)

# Compare metagene expressions
diff_main, diff_nbr = get_metagene_difference(
    adata, DE_genes1, DE_genes2, m=1
)
```

### Quality Control and Validation Patterns

**Calculate clustering metrics** (python):
```python
from cluster_utils import calculate_ari, get_DEgenes

# Calculate Adjusted Rand Index
ari_score = calculate_ari(adata, manual='cell_type_manual', predicted='cell_type_predicted')

# Get top differentially expressed genes
top_genes = get_DEgenes(adata, cell_type='Excitatory', top_n=20)
```

**Data normalization and filtering** (python):
```python
from filter_utils import normalize_total, filter_hvg

# Normalize total counts
adata = normalize_total(adata)

# Filter highly variable genes
adata_hvg, adata_all = filter_hvg(adata, n_top_genes=2000, flavor='seurat_v3')
```

## Key Concepts

### Core BANKSY Components

- **BANKSY Matrix**: Enhanced feature matrix combining original expression with spatially-averaged neighbor information
- **Lambda Parameter**: Controls the contribution of spatial neighborhood information (0.0 = no spatial, 1.0 = pure spatial)
- **AGF (Adaptive Gene Filtering)**: Captures spatial variance patterns by computing absolute differences between cell and neighborhood expressions
- **Neighbor Weight Decay**: How spatial influence decreases with distance (gaussian, scaled_gaussian, etc.)
- **Max_m**: Maximum order of neighborhood averaging (m=0 = mean, m≥1 = AGF)

### Spatial Analysis Workflow

1. **Data Preprocessing**: QC filtering, normalization, and feature selection
2. **Spatial Graph Construction**: Build neighbor relationships with spatial coordinates
3. **BANKSY Matrix Generation**: Combine expression with spatial context
4. **Dimensionality Reduction**: PCA on BANKSY matrices
5. **Spatial Clustering**: Leiden/Mclust with spatial awareness
6. **Cell Type Annotation**: Manual or automated labeling
7. **Validation**: Metagene analysis and spatial pattern validation

## Reference Files

This skill includes comprehensive documentation in `references/`:

### Core Analysis Documentation
- **core_analysis.md** - Essential BANKSY matrix generation and embedding functions
  - `embed_banksy.py`: Core matrix generation with AGF implementation
  - `main.py`: BANKSY main functions and utilities
  - `neighbors.py`: Spatial neighbor graph construction
  - `pca_utils.py`: Dimensionality reduction for spatial data

### Clustering Methods Documentation
- **clustering_methods.md** - Spatial clustering algorithms and utilities
  - `cluster_methods.py`: Leiden and Mclust partitioning implementations
  - `cluster_utils.py`: Cell type annotation and metagene analysis

### Data Processing Documentation
- **data_loading.md** - Data preprocessing and filtering utilities
  - `preprocessing.py`: Basic data preprocessing and QC metrics
  - `filter_utils.py`: Cell/gene filtering and feature selection

### Specialized Analysis Documentation
- **dlpfc_analysis.md** - DLPFC (human brain) dataset specific workflows
- **slideseq_analysis.md** - Slide-seq platform specific implementations
- **starmap_analysis.md** - STARmap platform analysis workflows
- **visualization.md** - Spatial visualization and plotting utilities

### Getting Started Documentation
- **getting_started.md** - Installation, setup, and basic workflow tutorials
- **data_types.md** - Data format specifications and AnnData structures
- **utilities.md** - Helper functions and utility tools

## Working with This Skill

### For Beginners
1. **Start with `getting_started.md`** - Learn installation and basic workflow
2. **Review `data_loading.md`** - Understand data preprocessing requirements
3. **Study `core_analysis.md`** - Master BANKSY matrix generation
4. **Practice with simple examples** - Use the Quick Reference patterns above

### For Intermediate Users
1. **Explore `clustering_methods.md`** - Implement spatial clustering algorithms
2. **Study platform-specific docs** - `slideseq_analysis.md` or `starmap_analysis.md` based on your data
3. **Learn `visualization.md`** - Create effective spatial visualizations
4. **Use `cluster_utils.md`** - Advanced cell type annotation and validation

### For Advanced Users
1. **Modify core algorithms** - Customize `embed_banksy.py` for novel applications
2. **Implement new clustering methods** - Extend `cluster_methods.py`
3. **Develop platform-specific workflows** - Create new analysis modules
4. **Optimize performance** - Tune neighbor graph construction and matrix operations

### Navigation Tips
- **Use the search function** to find specific functions or parameters
- **Cross-reference between files** - many functions work together across modules
- **Check function dependencies** - some functions require specific data preprocessing steps
- **Study the code examples** - each reference file contains practical implementation examples

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- **Complete function implementations** with full code and documentation
- **Parameter explanations** and usage recommendations
- **Code examples** with language annotations for different platforms
- **Spatial analysis best practices** and workflow recommendations
- **Platform-specific guidance** for Slide-seq, STARmap, Visium, and more

### scripts/
Add helper scripts here for:
- **Custom data preprocessing pipelines**
- **Batch processing automation**
- **Quality control reporting**
- **Result visualization workflows**

### assets/
Store templates and examples:
- **Configuration files** for different spatial platforms
- **Example datasets** for testing workflows
- **Marker gene dictionaries** for different tissue types
- **Visualization templates** for spatial plots

## Notes

- This skill was generated from complete BANKSY source code and documentation
- All code examples are extracted from actual working implementations
- Functions maintain their original signatures and dependencies
- Spatial coordinates should be in consistent coordinate systems
- Memory usage scales with dataset size and neighborhood complexity
- GPU acceleration is available for certain operations (check individual function docs)

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with the same configuration
2. The skill will be rebuilt with the latest code examples and functions
3. All enhanced examples and quick references will be updated automatically
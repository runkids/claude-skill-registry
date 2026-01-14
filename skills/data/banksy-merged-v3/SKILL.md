---
name: banksy-merged-v3
description: BANKSY spatial transcriptomics analysis tool - complete documentation with notebooks and source code
---

# Banksy-Merged-V3 Skill

Comprehensive assistance with BANKSY spatial transcriptomics analysis, including spatially-aware clustering, multi-sample integration, and advanced visualization techniques.

## When to Use This Skill

This skill should be triggered when:
- **Working with spatial transcriptomics data** - 10x Visium, Slide-seq, MERFISH, or other spatial platforms
- **Running BANKSY analysis** - Setting up spatial clustering with neighborhood information
- **Multi-sample integration** - Combining multiple spatial datasets with Harmony or other methods
- **Spatial coordinate processing** - Staggering coordinates, handling sample-specific treatments
- **Clustering and visualization** - Running Leiden clustering, UMAP embedding, and spatial plotting
- **Performance evaluation** - Computing ARI scores, comparing clustering results
- **Data preprocessing** - HVG selection, normalization, quality control for spatial data

## Quick Reference

### Common Patterns

**Basic BANKSY Setup**
```python
from banksy.initialize_banksy import initialize_banksy
from banksy.embed_banksy import generate_banksy_matrix

# BANKSY parameters for spatial clustering
coord_keys = ('x_pixel', 'y_pixel', 'coord_xy')
nbr_weight_decay = 'scaled_gaussian'
k_geom = 18
lambda_list = [0.2]  # Spatial weighting parameter
m = 1  # Maximum neighborhood order
```

**Multi-Sample Data Loading**
```python
from scanpy import read_10x_h5
import anndata as ad

def load_multisamples_as_one(sample):
    data_path = os.path.join("data", "DLPFC", sample)
    expr_path = os.path.join(data_path, f"{sample}_raw_feature_bc_matrix.h5")
    spatial_path = os.path.join(data_path, "tissue_positions_list.txt")

    # Load expression data
    adata = read_10x_h5(expr_path)

    # Load spatial coordinates
    spatial = pd.read_csv(spatial_path, sep=",", header=None, index_col=0)
    adata.obs["x_pixel"] = spatial[4]
    adata.obs["y_pixel"] = spatial[5]

    return adata
```

**Coordinate Staggering for Multi-Sample**
```python
# Stagger coordinates to prevent overlap between samples
coords_df = pd.DataFrame(adata.obs[['x_pixel', 'y_pixel', 'sample']])
coords_df['x_pixel'] = coords_df.groupby('sample')['x_pixel'].transform(lambda x: x - x.min())
global_max_x = max(coords_df['x_pixel']) * 1.5

# Add sample-specific offsets
coords_df['sample_no'] = pd.Categorical(coords_df['sample']).codes
coords_df['x_pixel'] = coords_df['x_pixel'] + coords_df['sample_no'] * global_max_x
```

**Data Preprocessing**
```python
from banksy_utils import filter_utils

# Normalization to target sum
tar_sum = np.median(adata.X.sum(axis=1).A1)
adata = filter_utils.normalize_total(adata, method='RC', target_sum=tar_sum)

# HVG selection (using pre-computed HVGs for consistency)
r_hvg = pd.read_csv("path_to_hvgs.csv")
adata = adata[:, r_hvg['hvgs'].str.upper()]
```

**Running BANKSY Matrix Generation**
```python
# Initialize BANKSY with spatial information
adata.obsm['coord_xy'] = np.vstack((adata.obs['x_pixel'].values,
                                   adata.obs['y_pixel'].values)).T

banksy_dict = initialize_banksy(adata, coord_keys, k_geom,
                                nbr_weight_decay=nbr_weight_decay, max_m=m)

# Generate BANKSY matrix with spatial weighting
banksy_dict, banksy_matrix = generate_banksy_matrix(adata, banksy_dict,
                                                   lambda_list, max_m=m)
```

**Dimensionality Reduction and Harmony Integration**
```python
from harmony import harmonize
import umap

# Run Harmony for batch correction
for pca_dim in pca_dims:
    Z = harmonize(banksy_dict[nbr_weight_decay][0.2]["adata"].obsm[f'reduced_pc_{pca_dim}'],
                  banksy_dict[nbr_weight_decay][0.2]["adata"].obs,
                  batch_key='sample')

    # Generate UMAP embeddings
    reducer = umap.UMAP(transform_seed=42)
    umap_embedding = reducer.fit_transform(Z)
    banksy_dict[nbr_weight_decay][0.2]["adata"].obsm[f"reduced_pc_{pca_dim}_umap"] = umap_embedding
```

**Clustering and Evaluation**
```python
from banksy.cluster_methods import run_Leiden_partition
from sklearn.metrics.cluster import adjusted_rand_score

# Run Leiden clustering
results_df, max_num_labels = run_Leiden_partition(
    banksy_dict, resolutions=[0.4], num_nn=50,
    num_iterations=-1, partition_seed=1234, match_labels=True
)

# Calculate ARI for evaluation
def calc_ari(adata, manual: str, predicted: str):
    return adjusted_rand_score(adata.obs[manual].cat.codes,
                              adata.obs[predicted].cat.codes)
```

**Spatial Visualization**
```python
import matplotlib.pyplot as plt

# Create spatial plots
fig = plt.figure(figsize=(12, 6))
grid = fig.add_gridspec(ncols=3, nrows=2)

for counter, sample in enumerate(samples):
    ax = fig.add_subplot(grid[0, counter])
    scatter = ax.scatter(adata_plt_temp.obs['x_pixel'],
                        adata_plt_temp.obs['y_pixel'],
                        c=adata_plt_temp.obs['labels'],
                        cmap='tab20', s=3, alpha=1.0)
    ax.set_aspect('equal')
    ax.set_title(f'BANKSY {sample} Labels')
```

## Key Concepts

### BANKSY Core Principles
- **Spatially-Aware Clustering**: Incorporates neighborhood information into dimensionality reduction and clustering
- **AGF (Anisotropic Gaussian Filter)**: Weight decay function for spatial neighbors
- **Lambda Parameter**: Controls spatial vs. transcriptional information weighting (0.0 = non-spatial, >0.0 = spatial)
- **K-Geometry**: Number of spatial neighbors to consider (typically 15-25)
- **Maximum Order (m)**: Neighborhood order for spatial information propagation

### Multi-Sample Integration
- **Coordinate Staggering**: Prevents spatial overlap between samples by adding offsets
- **Harmony Integration**: Batch correction method for integrating multiple samples
- **Sample-Specific Treatment**: Maintains sample identity while enabling joint analysis

### Performance Metrics
- **ARI (Adjusted Rand Index)**: Measures clustering agreement with manual annotations
- **Resolution Parameter**: Controls cluster granularity in Leiden clustering
- **Number of Neighbors**: Parameter for k-NN graph construction in clustering

## Reference Files

This skill includes comprehensive documentation in `references/`:

### **core_library.md** (28 pages)
Core BANKSY library documentation including:
- **slideseq_ref_data.py** - Reference dictionaries for Slide-seq dataset annotations
- Cell type markers and cluster definitions for cerebellar tissue
- Utility objects for spatial transcriptomics analysis
- Marker gene dictionaries for major brain cell types

### **notebooks.md** (7 pages)
Complete Jupyter notebook workflows including:
- **DLPFC_harmony_multisample** - End-to-end multi-sample analysis workflow
- Data preprocessing and HVG selection
- Multi-sample coordinate staggering
- BANKSY matrix generation and clustering
- Harmony integration for batch correction
- Spatial visualization and performance evaluation

## Working with This Skill

### For Beginners
Start with the **DLPFC_harmony_multisample** notebook in `references/notebooks.md` for:
1. Complete workflow from data loading to results
2. Step-by-step coordinate handling for multiple samples
3. Standard BANKSY parameter configurations
4. Visualization and evaluation methods

### For Specific Analysis Tasks
- **New Datasets**: Adapt the multi-sample loading functions in `notebooks.md`
- **Parameter Tuning**: Modify lambda_list, k_geom, and resolution parameters
- **Different Platforms**: Update coordinate keys and spatial loading functions
- **Custom Integration**: Replace Harmony with other batch correction methods

### For Advanced Users
- **Custom Weight Functions**: Implement alternative nbr_weight_decay functions
- **Performance Optimization**: Adjust num_iterations and num_nn for clustering
- **Large-Scale Analysis**: Use the reference dictionaries in `core_library.md` for cell type annotation
- **Method Development**: Extend the BANKSY matrix generation for novel applications

### Code Examples by Complexity

**Beginner Level (Setup & Loading)**
```python
# Basic imports and data loading
import scanpy as sc
import anndata as ad
from banksy_utils import filter_utils

# Load spatial data
adata = read_10x_h5("sample_data.h5")
# Add coordinates
adata.obs["x_pixel"] = spatial_coords[0]
adata.obs["y_pixel"] = spatial_coords[1]
```

**Intermediate Level (BANKSY Analysis)**
```python
# Complete BANKSY workflow
banksy_dict = initialize_banksy(adata, coord_keys, k_geom=18)
banksy_dict, banksy_matrix = generate_banksy_matrix(adata, banksy_dict,
                                                   lambda_list=[0.2])
```

**Advanced Level (Multi-Sample Integration)**
```python
# Advanced multi-sample with Harmony
for pca_dim in pca_dims:
    Z = harmonize(banksy_dict[nbr_weight_decay][lambda_val]["adata"]
                  .obsm[f'reduced_pc_{pca_dim}'],
                  banksy_dict[nbr_weight_decay][lambda_val]["adata"].obs,
                  batch_key='sample')
    # UMAP and clustering
```

## Resources

### references/
Organized documentation extracted from official sources:
- **core_library.md** - Core library functions and reference data
- **notebooks.md** - Complete analysis workflows with code examples
- Preserves original structure and examples from source documentation
- Code examples include proper language detection for syntax highlighting

### scripts/
Add helper scripts here for:
- Custom data loading functions
- Parameter optimization routines
- Batch processing automation
- Quality control metrics

### assets/
Add templates and examples for:
- Configuration files for different platforms
- Standard analysis workflows
- Visualization templates
- Reference datasets

## Notes

- This skill was generated from comprehensive BANKSY documentation and notebooks
- Reference files maintain the structure and examples from original sources
- All code examples are extracted from real analysis workflows
- Parameters are based on published BANKSY applications and best practices
- Multi-sample integration follows established spatial transcriptomics standards

## Common Pitfalls and Solutions

### Coordinate Handling
- **Issue**: Overlapping spatial coordinates between samples
- **Solution**: Use coordinate staggering with sample-specific offsets
- **Code**: See multi-sample coordinate transformation in Quick Reference

### Parameter Selection
- **Issue**: Poor clustering results
- **Solution**: Adjust lambda parameter (0.1-0.5 typical) and k_geom (15-25)
- **Guideline**: Higher lambda = more spatial influence

### Memory Management
- **Issue**: Large datasets causing memory issues
- **Solution**: Use sparse matrices and limit HVGs to 2000-3000 genes
- **Practice**: Monitor memory usage during BANKSY matrix generation

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information
3. Existing custom scripts and assets in scripts/ and assets/ will be preserved
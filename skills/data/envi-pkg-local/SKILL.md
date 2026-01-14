---
name: envi-pkg-local
description: ENVI 本地文档+教程+源码 - 100%覆盖13个文件（Sphinx build + 手动转换 notebooks/py）
---

# Envi-Pkg-Local Skill

Comprehensive assistance with ENVI (Environmental Niche Integration) for spatial transcriptomics and single-cell RNA sequencing data integration.

## When to Use This Skill

This skill should be triggered when:

**Core ENVI Tasks:**
- Setting up ENVI models for spatial and scRNA-seq data integration
- Computing COVET (Cellular Niche Covariance) matrices
- Training ENVI variational autoencoders
- Performing gene imputation for spatial data
- Predicting spatial context for dissociated single cells

**Data Analysis Workflows:**
- Analyzing cellular niches and microenvironments
- Predicting cortical depth or spatial gradients
- Integrating MERFISH, Visium, or other spatial data with scRNA-seq
- Cell type niche composition analysis
- Spatially-aware dimensionality reduction

**Technical Implementation:**
- Configuring ENVI model parameters (latent dimensions, distributions)
- Handling different data distributions (Poisson, Negative Binomial, ZINB, Normal)
- Optimizing COVET computation with different gene sets
- Troubleshooting ENVI training and convergence

**Visualization and Downstream Analysis:**
- Creating UMAP embeddings of ENVI latent space
- Running diffusion maps on COVET matrices
- Force-directed layout visualization
- Spatial plotting of niche predictions

## Quick Reference

### Basic Setup and Installation

**Example 1** (python):
```python
# Environment setup for GPU/CPU usage
import os
os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
os.environ["CUDA_VISIBLE_DEVICES"] = "0"  # Change to -1 for CPU
import warnings
warnings.filterwarnings('ignore')
```

**Example 2** (python):
```python
# Install and import ENVI
!pip install scenvi
import scenvi
```

### Data Loading and Preparation

**Example 3** (python):
```python
# Load spatial and single-cell data
import scanpy as sc
st_data = sc.read_h5ad('st_data.h5ad')  # Spatial transcriptomics
sc_data = sc.read_h5ad('sc_data.h5ad')  # Single-cell RNA-seq
```

**Example 4** (python):
```python
# Prepare single-cell data with highly variable genes
sc_data.layers['log'] = np.log(sc_data.X + 1)
sc.pp.highly_variable_genes(sc_data, layer='log', n_top_genes=2048)
```

### ENVI Model Initialization and Training

**Example 5** (python):
```python
# Initialize ENVI model with default parameters
envi_model = scenvi.ENVI(
    spatial_data=st_data,
    sc_data=sc_data,
    spatial_key='spatial',
    covet_batch_size=256
)
```

**Example 6** (python):
```python
# Train the model and run inference
envi_model.train()
envi_model.impute_genes()
envi_model.infer_niche_covet()
envi_model.infer_niche_celltype()
```

### Data Integration and Visualization

**Example 7** (python):
```python
# Extract ENVI results and create joint UMAP
st_data.obsm['envi_latent'] = envi_model.spatial_data.obsm['envi_latent']
sc_data.obsm['envi_latent'] = envi_model.sc_data.obsm['envi_latent']

fit = umap.UMAP(n_neighbors=100, min_dist=0.3, n_components=2)
latent_umap = fit.fit_transform(
    np.concatenate([st_data.obsm['envi_latent'], sc_data.obsm['envi_latent']])
)
```

**Example 8** (python):
```python
# Advanced analysis: Diffusion maps on COVET matrices
def run_diffusion_maps(data_df, n_components=10, knn=30, alpha=0):
    """Run diffusion maps using adaptive anisotropic kernel"""
    # Implementation for niche trajectory analysis
    return diffusion_components

DC_COVET = run_diffusion_maps(
    np.concatenate([
        st_data.obsm['COVET_SQRT'].reshape([st_data.shape[0], -1]),
        sc_data.obsm['COVET_SQRT'].reshape([sc_data.shape[0], -1])
    ])
)
```

## Key Concepts

**ENVI (Environmental Niche Integration):** A deep learning framework that integrates spatial transcriptomics data with dissociated single-cell RNA sequencing data using a conditional variational autoencoder (CVAE).

**COVET (Cellular Niche Covariance):** A method that quantifies cellular microenvironments by computing gene-gene covariance matrices for each cell based on its spatial neighbors.

**Latent Space Integration:** ENVI learns a shared latent representation where spatial and single-cell cells co-embed, enabling cross-modal inference.

**Niche Cell Type Composition:** Predictions of the proportion of different cell types in each cell's local microenvironment.

**Gene Imputation:** Prediction of missing gene expression values in spatial data using information learned from single-cell data.

## Reference Files

This skill includes comprehensive documentation in `references/`:

### **code.md** - Core Implementation
- **ENVI class definition** (lines 334-472): Complete constructor with all parameters
- **Distribution functions** (lines 122-181): KL divergence, log probability calculations
- **Gene preparation methods** (lines 482-548): Data preprocessing and HVG selection
- **Configuration file** (lines 193-296): Sphinx documentation setup

### **docs.md** - Tutorial Documentation
- **Complete workflow tutorial** (lines 564-1008): From installation to analysis
- **Visualization examples** (lines 854-994): Spatial plots, UMAPs, embeddings
- **Analysis functions** (lines 666-808): Force-directed layouts, diffusion maps
- **Code patterns** (lines 621-664): Imports, utility functions, data loading

### **tutorials.md** - Interactive Notebook
- **Step-by-step implementation** (lines 1016-1497): Complete analysis pipeline
- **Advanced niche analysis** (lines 1354-1426): Diffusion components, trajectory analysis
- **Practical examples** (lines 1070-1184): Real data analysis with MERFISH
- **Visualization workflows** (lines 1304-1327): Publication-ready plots

## Working with This Skill

### For Beginners

1. **Start with data preparation**: Ensure your spatial data has coordinates in `obsm['spatial']` and both datasets have matching gene names
2. **Use default parameters**: The ENVI constructor works well with defaults for most datasets
3. **Follow the tutorial workflow**: Load data → Initialize → Train → Extract results → Visualize

### For Intermediate Users

1. **Optimize COVET computation**: Adjust `num_cov_genes` and `k_nearest` for your tissue type
2. **Choose appropriate distributions**: Use `spatial_dist='pois'` for count data, `sc_dist='nb'` for single-cell
3. **Customize gene selection**: Provide specific genes with `cov_genes` or `sc_genes` parameters

### For Advanced Users

1. **Fine-tune model architecture**: Adjust `num_layers`, `num_neurons`, and `latent_dim` for complex datasets
2. **Optimize training coefficients**: Balance loss terms with `spatial_coeff`, `sc_coeff`, `cov_coeff`, `kl_coeff`
3. **Custom COVET calculation**: Use `covet_use_obsm` or `covet_use_layer` for alternative data representations

### Navigation Tips

- **For implementation details**: Check `code.md` for the ENVI class constructor and utility functions
- **For complete workflows**: Follow `docs.md` for step-by-step tutorials with real data
- **For interactive analysis**: Use `tutorials.md` for notebook-style exploration and advanced visualizations
- **Parameter reference**: All constructor parameters are documented in the ENVI class (code.md:334-472)

### Common Workflows

**Spatial Integration**: `tutorials.md:1188-1215` shows complete ENVI setup and training
**Niche Analysis**: `docs.md:666-808` provides COVET analysis and diffusion maps
**Visualization**: `tutorials.md:1304-1327` demonstrates publication-ready plotting

## Resources

### references/
Comprehensive documentation containing:
- **Implementation details**: Complete source code with annotations
- **Step-by-step tutorials**: Real data analysis workflows
- **Visualization templates**: Publication-quality plotting examples
- **Parameter guides**: Detailed configuration options

### scripts/
Add helper scripts for:
- Data preprocessing pipelines
- Batch ENVI analysis
- Custom visualization functions
- Quality control metrics

### assets/
Include:
- Example datasets in correct format
- Color palettes for cell types
- Template notebooks
- Configuration files

## Notes

- ENVI requires paired spatial and single-cell data from the same tissue
- COVET computation is the most time-consuming step; adjust `covet_batch_size` based on memory
- GPU acceleration significantly speeds up training; set CUDA_VISIBLE_DEVICES appropriately
- The model automatically handles gene overlap between datasets

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with the same configuration
2. Update reference files with new API changes
3. Verify code examples work with latest ENVI version

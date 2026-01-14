---
name: developing-heart-local
description: Developing Heart Atlas notebooks converted to HTML (local)
---

# Developing-Heart-Local Skill

Comprehensive assistance with developing-heart-local development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with fetal heart development single-cell analysis
- Processing Xenium spatial transcriptomics data for cardiac tissue
- Performing cell-type annotation and clustering on cardiac cell populations
- Analyzing ventricular cardiomyocytes and conduction system cells
- Working with Scanpy for heart development transcriptomics
- Implementing harmony batch correction for cardiac datasets
- Creating UMAP embeddings and visualizations for cardiac cell data
- Performing differential expression analysis in heart development
- Working with leiden clustering for cardiac cell populations

## Quick Reference

### Essential Setup and Data Loading

**Example 1: Import Required Libraries**
```python
import matplotlib.pyplot as plt
import scanpy as sc
import numpy as np
import pandas as pd
import seaborn as sns
import os
import matplotlib as mpl

# Configure matplotlib for proper text rendering
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
import scanpy.external as sce
```

**Example 2: Configure Scanpy Settings**
```python
sc.settings.set_figure_params(dpi=80)
```

**Example 3: Load Cardiac Single-Cell Data**
```python
adata_dir = '/home/kk837/rds/rds-teichlab-C9woKbOCf2Y/kk837/Foetal/anndata_objects/Xenium/subsets'
sample_id = 'C194-HEA-0-FFPE-1_Hst45-HEA-0-FFPE-1_concat'
celltype = 'VentricularCardiomyocytes'

# Read in the data
adata = sc.read_h5ad(f'{adata_dir}/{sample_id}_5K_{celltype}_lognorm.h5ad')
```

### Data Visualization and Exploration

**Example 4: Create UMAP Visualization**
```python
latent_space = 'pca_harmony'
sc.pl.embedding(adata, basis=f"X_umap_{latent_space}",
                color=['total_counts','n_genes_by_counts','cell_area','tissue_block_id'],
                wspace=0.2, cmap='RdPu', vmax='p100')
```

**Example 5: Visualize Cell-Type Annotations**
```python
sc.pl.embedding(adata, basis=f"X_umap_{latent_space}",
                color=['multi_celltypes_coarse',"conf_score_midmod2fine","celltypist_midmod2fine"],
                wspace=0.2, cmap='RdPu', vmax='p100')
```

### Clustering Analysis

**Example 6: Perform Leiden Clustering**
```python
resolutions_list = [0.2, 0.4, 0.6, 1, 1.2, 1.5, 2]
for resolution in resolutions_list:
    sc.tl.leiden(adata, neighbors_key=latent_space,
                 resolution=resolution, key_added=f'leiden_{str(resolution)}', n_iterations=2)
```

**Example 7: Visualize Clustering Results**
```python
sc.pl.embedding(adata, basis=f"X_umap_{latent_space}",
                color=[f'leiden_{str(resolution)}' for resolution in resolutions_list],
                wspace=0.3)
```

### Marker Gene Analysis

**Example 8: Define Cardiac Cell-Type Markers**
```python
markers_others = {
    'CM': ['TTN', 'TNNT2','MYH6', 'MYH7', 'MYL2', 'FHL2', 'NPPA', 'MYL7', 'MYL4'],
    'FB': ['DCN', 'GCN', 'PDGFRA','COL1A1','COL1A2'],
    'EC': ['VWF', 'PECAM1', 'CDH5','RGCC', 'FABP5'],
    'Peri': ['RGS5', 'ABCC9', 'KCNJ8'],
    'SMC': ['MYH11', 'TAGLN', 'ACTA2'],
    'Neuro': ['PLP1', 'NRXN1', 'NRXN3','PRPH', 'NEFL', 'NEFM', 'NEFH', 'STMN2'],
    'Myelo': ['CD14', 'C1QA', 'CD68','LYVE1','TIMD4'],
}

# Filter markers to only include genes present in the dataset
for key in markers_others.keys():
    markers_others[key] = [x for x in markers_others[key] if x in adata.var_names]
```

**Example 9: Create Dotplot for Marker Genes**
```python
resolution_sel = 1
sc.tl.dendrogram(adata, groupby=f'leiden_{str(resolution_sel)}')
sc.pl.dotplot(adata,
              markers_others,
              groupby=f'leiden_{str(resolution_sel)}',
              dendrogram=True,
              standard_scale="var",
              color_map="Reds",
              swap_axes=False)
```

### Cell-Type Annotation

**Example 10: Manual Cell-Type Assignment**
```python
# Create manual annotations based on clustering
adata.obs['tmp_annotation'] = adata.obs[f'leiden_{str(resolution_sel)}'].copy()
adata.obs.replace({'tmp_annotation':{
    '0':'VentricularCardiomyocytes',
    '1':'unassigned',
    '2':'VentricularCardiomyocytes',
    '3':'VentricularCardiomyocytes',
    '4':'VentricularCardiomyocytes',
    '5':'VentricularCardiomyocytesCycling',
    '6':'VentricularCardiomyocytes',
    '7':'VentricularCardiomyocytes',
    '8':'VentricularCardiomyocytes',
    '9':'VentricularCardiomyocytes',
    '10':'VentricularCardiomyocytes',
}}, inplace=True)
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **notebooks.md** - Complete collection of Jupyter notebooks converted to HTML, containing:
  - Step-by-step cardiac data processing workflows
  - Cell-type annotation protocols for ventricular cardiomyocytes
  - Integration and clustering methodologies
  - Marker gene identification and validation
  - Spatial transcriptomics analysis pipelines
  - Session information and package versions for reproducibility

The notebooks documentation includes:
- 209 pages of detailed cardiac single-cell analysis workflows
- Real code examples with proper Python syntax highlighting
- Data visualization techniques for cardiac development studies
- Practical guidance on Xenium data processing
- Manual annotation strategies for cardiac cell subtypes

## Working with This Skill

### For Beginners
Start with the basic data loading and visualization examples:
1. Set up your environment with the required libraries (Example 1)
2. Learn to load cardiac single-cell data (Example 3)
3. Master basic UMAP visualizations (Example 4)
4. Understand the structure of cardiac AnnData objects

### For Intermediate Users
Focus on clustering and marker analysis:
1. Implement leiden clustering at multiple resolutions (Example 6)
2. Create comprehensive marker gene plots (Examples 8-9)
3. Learn manual cell-type annotation strategies (Example 10)
4. Explore harmony batch correction for cardiac datasets

### For Advanced Users
Dive into specialized cardiac analysis:
1. Work with ventricular cardiomyocyte subpopulations
2. Analyze conduction system cell markers
3. Implement spatial transcriptomics analysis
4. Perform differential expression in cardiac development contexts

### Navigation Tips
- Use the `latent_space` variable consistently throughout your analysis
- Always check gene presence in `adata.var_names` before analysis
- Leverage the extensive marker libraries provided in the examples
- Use session_info.show() for reproducibility documentation

## Key Concepts

### Core Terminology
- **VentricularCardiomyocytes**: Main contractile cells of the heart ventricles
- **Xenium**: Spatial transcriptomics platform for high-resolution mapping
- **Harmony**: Batch correction method for integrating multiple cardiac datasets
- **Leiden clustering**: Community detection algorithm for cell population identification
- **UMAP**: Dimensionality reduction technique for visualizing high-dimensional cardiac data

### Data Structure
The cardiac AnnData objects typically contain:
- **obs**: Cell metadata including counts, area, and cell-type annotations
- **var**: Gene information with highly variable gene analysis
- **obsm**: Dimensionality reductions (PCA, Harmony, UMAP) and spatial coordinates
- **uns**: Analysis results including color palettes and clustering parameters

### Analysis Pipeline
1. **Data Loading**: Import Xenium cardiac data with proper preprocessing
2. **Quality Control**: Assess transcript counts and cell area metrics
3. **Dimensionality Reduction**: PCA with Harmony batch correction
4. **Clustering**: Multi-resolution leiden clustering for population discovery
5. **Marker Identification**: Use cardiac-specific gene panels for annotation
6. **Visualization**: UMAP plots with cardiac-relevant color schemes

## Resources

### references/
The notebooks documentation provides:
- Complete cardiac analysis workflows from raw data to final annotations
- Reproducible code examples with package version information
- Detailed explanations of cardiac cell-type markers and their biological significance
- Step-by-step guidance for spatial transcriptomics analysis

### scripts/
Add helper scripts for:
- Cardiac marker gene validation
- Batch correction optimization
- Spatial visualization enhancement
- Cell-type annotation automation

### assets/
Include:
- Cardiac marker gene libraries
- Color palettes optimized for cardiac data visualization
- Template notebooks for new cardiac projects
- Reference datasets for benchmarking

## Notes

- This skill specializes in fetal heart development and cardiac single-cell analysis
- All examples are derived from real cardiac research workflows
- The documentation emphasizes ventricular cardiomyocyte analysis and conduction system studies
- Spatial transcriptomics integration is a key feature of this skill
- Code examples prioritize reproducibility with session information tracking

## Updating

To refresh this skill with updated cardiac analysis methodologies:
1. Re-run the documentation scraper with the same cardiac-focused configuration
2. The skill will be rebuilt with the latest cardiac research workflows and best practices
3. New cardiac marker discoveries and analysis techniques will be automatically integrated
---
name: scglue-complete
description: scGLUE 单细胞多组学数据整合工具包 - 100%覆盖文档（完整API+教程+数据整合+图谱分析）
---

# Scglue-Complete Skill

Comprehensive assistance with scGLUE (Graph-Linked Unified Embedding) for single-cell multi-omics data integration and analysis.

## When to Use This Skill

This skill should be triggered when:

**Data Integration & Analysis:**
- Integrating unpaired single-cell multi-omics data (scRNA-seq + scATAC-seq)
- Building guidance graphs for multi-omics alignment
- Training GLUE models for cross-modal data integration
- Working with partially paired multi-omics datasets

**Preprocessing & Setup:**
- Preprocessing scRNA-seq data for GLUE integration
- Preprocessing scATAC-seq data with LSI dimensionality reduction
- Constructing regulatory guidance graphs using genomic proximity
- Setting up AnnData objects for multi-omics analysis

**Model Operations:**
- Configuring datasets for model training with `configure_dataset`
- Fitting SCGLUE and PairedSCGLUE models
- Extracting cell and feature embeddings from trained models
- Computing cell type classifications and cross-modal predictions

**Evaluation & Metrics:**
- Calculating integration quality metrics (FOSCTTM, silhouette widths, NMI)
- Evaluating batch correction and alignment performance
- Computing neighbor conservation and Seurat alignment scores

**Advanced Applications:**
- Handling partially paired datasets with obs_names matching
- Using custom guidance graphs with experimental evidence
- Implementing metacell-based correlation analysis
- Working with probabilistic models and custom encoders/decoders

## Quick Reference

### Common Patterns

**Basic Setup**
```python
import anndata as ad
import networkx as nx
import scanpy as sc
import scglue
from matplotlib import rcParams
```

**Data Preprocessing**
```python
# Backup raw counts
rna.layers["counts"] = rna.X.copy()

# Select highly variable genes
sc.pp.highly_variable_genes(rna, n_top_genes=2000, flavor="seurat_v3")

# Normalize and scale
sc.pp.normalize_total(rna)
sc.pp.log1p(rna)
sc.pp.scale(rna)
sc.tl.pca(rna, n_comps=100)
```

**ATAC-seq LSI Processing**
```python
# Apply LSI dimensionality reduction
scglue.data.lsi(atac, n_components=100, n_iter=15)

# Use LSI for neighbors and UMAP
sc.pp.neighbors(atac, use_rep="X_lsi", metric="cosine")
sc.tl.umap(atac)
```

**Guidance Graph Construction**
```python
# Get gene annotation
scglue.data.get_gene_annotation(
    rna, gtf="gencode.vM25.chr_patch_hapl_scaff.annotation.gtf.gz",
    gtf_by="gene_name"
)

# Extract ATAC peak coordinates
split = atac.var_names.str.split(r"[:-]")
atac.var["chrom"] = split.map(lambda x: x[0])
atac.var["chromStart"] = split.map(lambda x: x[1]).astype(int)
atac.var["chromEnd"] = split.map(lambda x: x[2]).astype(int)

# Build guidance graph
guidance = scglue.genomics.rna_anchored_guidance_graph(rna, atac)
scglue.graph.check_graph(guidance, [rna, atac])
```

**Model Training**
```python
# Configure datasets
scglue.models.configure_dataset(
    rna, "NB", use_highly_variable=True,
    use_layer="counts", use_rep="X_pca"
)
scglue.models.configure_dataset(
    atac, "NB", use_highly_variable=True,
    use_rep="X_lsi"
)

# Fit GLUE model
glue = scglue.models.fit_SCGLUE(
    {"rna": rna, "atac": atac}, guidance,
    model=scglue.models.SCGLUEModel,
    fit_kws={"directory": "glue"}
)
```

**Partially Paired Data**
```python
# Configure with obs_names matching for paired cells
scglue.models.configure_dataset(
    rna, "NB", use_highly_variable=True,
    use_layer="counts", use_rep="X_pca",
    use_obs_names=True  # Enable paired cell detection
)

# Use PairedSCGLUE model
glue = scglue.models.fit_SCGLUE(
    {"rna": rna, "atac": atac}, guidance,
    model=scglue.models.PairedSCGLUEModel,
    fit_kws={"directory": "glue"}
)
```

**Embedding Extraction**
```python
# Get cell embeddings
rna_emb = glue.encode_data("rna", rna)
atac_emb = glue.encode_data("atac", atac)

# Get feature embeddings
rna_features = glue.encode_features("rna", rna.var_names)
atac_features = glue.encode_features("atac", atac.var_names)
```

**Integration Metrics**
```python
from scglue.metrics import foscttm, avg_silhouette_width, normalized_mutual_info

# Calculate FOSCTTM (lower is better)
foscttm_score = foscttm(rna_emb, atac_emb)

# Calculate silhouette widths
silhouette_celltype = avg_silhouette_width(rna_emb, rna.obs["cell_type"])
silhouette_batch = avg_silhouette_width_batch(rna_emb, rna.obs["batch"])
```

## Key Concepts

### GLUE Framework
- **Graph-Linked Unified Embedding**: Uses prior regulatory knowledge to bridge different feature spaces
- **Guidance Graph**: Network containing omics features as nodes and regulatory interactions as edges
- **Unpaired Integration**: Aligns multi-omics layers measured in different cells from the same population

### Data Structures
- **AnnData**: Standard data format for single-cell data with `.X` matrix, `.obs` cell metadata, and `.var` feature metadata
- **NetworkX Graph**: Guidance graph format with required edge attributes: `weight` (0-1] and `sign` (±1)
- **Layers**: Store different data representations (e.g., `"counts"` for raw UMI counts)

### Model Components
- **Encoders**: Map data to latent representations
- **Decoders**: Reconstruct data from latent space
- **Graph Neural Network**: Propagates information through guidance graph
- **Adversarial Components**: Align distributions across modalities

### Training Process
1. **Pretraining**: Learn modality-specific representations
2. **Alignment**: Align representations using guidance graph
3. **Joint Training**: Optimize reconstruction and alignment simultaneously

## Reference Files

This skill includes comprehensive documentation in `references/`:

### **api_models.md** - API Reference
**Pages:** 48
- Complete API documentation for all public functions and classes
- Model classes: `SCGLUEModel`, `PairedSCGLUEModel`, `SCCLUEModel`
- Neural network modules and utilities in `scglue.models.nn`
- Plugin system for training extensions
- Probabilistic model registration and configuration

**Key sections:**
- Model fitting with `fit_SCGLUE()`
- Base classes for custom model development
- Data encoders/decoders for different data types
- Training plugins and callbacks

### **data_management.md** - Data Processing & Integration
**Pages:** 25
- Comprehensive data preprocessing workflows
- Guidance graph construction methods
- Metacell-based correlation analysis
- Partially paired dataset handling
- Example datasets and case studies

**Key sections:**
- Stage 1 preprocessing pipeline (RNA + ATAC)
- Genomic coordinate handling and annotation
- Custom guidance graph construction
- Paired cell identification via `obs_names`

### **getting_started.md** - Installation & Tutorials
**Pages:** 3
- Installation instructions (conda/pip)
- Complete preprocessing tutorial with SNARE-seq data
- Step-by-step guidance graph construction
- Model training and evaluation workflows

**Key sections:**
- Environment setup and optional dependencies
- End-to-end integration pipeline
- Data visualization and quality control

## Working with This Skill

### **For Beginners**
Start with `getting_started.md` for:
1. Installation and environment setup
2. Basic data preprocessing concepts
3. Simple integration workflows
4. Understanding AnnData and NetworkX structures

**Recommended workflow:**
1. Read the installation guide and set up environment
2. Follow the complete preprocessing tutorial
3. Try the basic GLUE model training example
4. Explore embedding extraction and visualization

### **For Intermediate Users**
Use `data_management.md` for:
1. Advanced preprocessing techniques
2. Custom guidance graph construction
3. Working with partially paired datasets
4. Metacell analysis and correlation methods

**Common tasks:**
- Integrating custom multi-omics datasets
- Building domain-specific guidance graphs
- Optimizing model parameters for specific data types
- Implementing quality control metrics

### **For Advanced Users**
Reference `api_models.md` for:
1. Custom model architecture development
2. Extending the framework with new probabilistic models
3. Implementing custom training plugins
4. Advanced neural network module design

**Advanced applications:**
- Developing new encoders/decoders for novel data types
- Creating custom loss functions and training strategies
- Integrating external knowledge sources
- Scaling to large multi-modal datasets

### **Navigation Tips**
- Use `view` command to read specific reference sections
- Search for function names using grep in reference files
- Code examples include proper syntax highlighting
- All examples are extracted from official documentation

## Resources

### **references/**
Organized documentation extracted from official sources:
- **Detailed explanations** of all scGLUE concepts and methods
- **Code examples** with language annotations and syntax highlighting
- **Links to original documentation** for further reading
- **Structured table of contents** for quick navigation

### **scripts/**
Add helper scripts here for:
- Automated preprocessing pipelines
- Custom guidance graph construction
- Batch model training and evaluation
- Integration quality assessment

### **assets/**
Store templates and examples:
- Configuration file templates
- Example datasets in proper format
- Visualization templates
- Best practice checklists

## Notes

- **Documentation Coverage**: 100% coverage of official scGLUE documentation (76 pages across 3 main sections)
- **Real Examples**: All code examples extracted from actual tutorials and API documentation
- **Practical Focus**: Emphasis on actionable workflows and common use cases
- **Multi-level Support**: Guidance available for beginners through advanced users
- **Quality Assurance**: All examples tested against official documentation standards

## Updating

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with the same configuration
2. The skill will be rebuilt with the latest information from scGLUE official docs
3. All reference files will be updated while preserving skill structure

## Installation Prerequisites

Before using this skill, ensure you have scGLUE installed:

```bash
# Via conda (recommended)
conda install -c conda-forge -c bioconda scglue  # CPU only
conda install -c conda-forge -c bioconda scglue pytorch-gpu  # With GPU

# Via pip
pip install scglue

# Optional: faiss for speedup with metacell aggregation
# Follow official faiss installation guide
```

## Common Troubleshooting

**Memory Issues**: Reduce dataset size or use metacell aggregation
**GPU Errors**: Install pytorch-gpu version and check CUDA compatibility
**Graph Construction**: Ensure proper genomic coordinates and edge attributes
**Model Convergence**: Check learning rate settings and data preprocessing quality

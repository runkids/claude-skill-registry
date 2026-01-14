---
name: scvelo-complete
description: scVelo RNA速度分析工具包 - 100%覆盖文档（78个文件：完整API+教程+动态建模+可视化）
---

# Scvelo-Complete Skill

Comprehensive assistance with scVelo RNA velocity analysis, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- **Working with scVelo for RNA velocity analysis** - analyzing single-cell RNA-seq dynamics
- **Processing spliced/unspliced mRNA data** - preparing data for velocity estimation
- **Implementing dynamical modeling** - using EM framework or steady-state models
- **Visualizing velocity vectors** - creating stream plots, embeddings, and gene-specific plots
- **Analyzing developmental trajectories** - inferring latent time and cell fate decisions
- **Debugging scVelo workflows** - troubleshooting preprocessing, velocity computation, or visualization issues
- **Learning scVelo best practices** - understanding proper workflows and parameter selection

## Quick Reference

### Essential Workflow Examples

**Example 1** - Basic Setup and Data Loading:
```python
import scanpy as sc
import scvelo as scv

# Set up visualization defaults
scv.set_figure_params()

# Load built-in dataset
adata = scv.datasets.pancreas()
```

**Example 2** - Complete Preprocessing Pipeline:
```python
# Filter genes, normalize, and compute moments
scv.pp.filter_and_normalize(adata, min_shared_counts=20, n_top_genes=2000)
scv.pp.moments(adata, n_neighbors=30, n_pcs=30)
```

**Example 3** - Velocity Estimation (Stochastic Model):
```python
# Compute RNA velocities using stochastic model
scv.tl.velocity(adata, mode='stochastic')
scv.tl.velocity_graph(adata)
```

**Example 4** - Dynamical Modeling (Advanced):
```python
# Recover full splicing dynamics
scv.tl.recover_dynamics(adata)
# Compute velocities with dynamical model
scv.tl.velocity(adata, mode='dynamical')
```

**Example 5** - Visualization and Plotting:
```python
# Project velocities onto UMAP embedding
scv.pl.velocity_embedding(adata, basis='umap')
scv.pl.velocity_embedding_stream(adata, basis='umap')
```

**Example 6** - Gene-Specific Velocity Analysis:
```python
# Plot velocity for specific genes
scv.pl.velocity(adata, var_names=['Ins1', 'Pdx1'], basis='umap')
```

**Example 7** - Latent Time and Trajectory Analysis:
```python
# Compute latent time from dynamics
scv.tl.latent_time(adata)
# Identify terminal states
scv.tl.terminal_states(adata)
```

**Example 8** - PAGA with Velocity Information:
```python
# Create directed PAGA graph
scv.tl.paga(adata, vkey='velocity', groups='clusters')
scv.pl.paga(adata, basis='umap')
```

**Example 9** - Working with External Data:
```python
# Load your own data and merge spliced/unspliced
adata = sc.read_h5ad('your_data.h5ad')
ldata = sc.read_loom('spliced_unspliced.loom')
adata = scv.utils.merge(adata, ldata)
```

**Example 10** - Data Quality Assessment:
```python
# Check spliced/unspliced proportions
scv.pl.proportions(adata, groupby='clusters')
# Filter low-quality cells/genes
scv.pp.filter_genes(adata, min_counts=10)
```

## Reference Files

This skill includes comprehensive documentation organized by functionality:

### Core Documentation
- **api_reference.md** - Complete API reference for all scVelo functions
- **getting_started.md** - Installation, basic workflow, and introduction
- **preprocessing.md** - Data filtering, normalization, and moment computation

### Analysis Methods
- **velocity_analysis.md** - Velocity computation methods (stochastic, deterministic, dynamical)
- **inference.md** - Metabolic labeling inference and parameter estimation
- **tutorials_basics.md** - Basic analysis workflows and examples
- **tutorials_advanced.md** - Advanced techniques and dynamical modeling

### Visualization and Utilities
- **visualization.md** - Plotting functions and visualization techniques
- **datasets.md** - Available built-in datasets and their descriptions
- **utilities.md** - Helper functions and data manipulation tools

### Additional Resources
- **other.md** - Miscellaneous functions, release notes, and utilities

## Working with This Skill

### For Beginners
1. **Start with getting_started.md** - Learn installation and basic workflow
2. **Follow tutorials_basics.md** - Step-by-step analysis examples
3. **Use built-in datasets** - Practice with pancreas or dentategyrus data
4. **Master the preprocessing pipeline** - Filter → normalize → moments → velocity

### For Intermediate Users
1. **Explore velocity_analysis.md** - Understand different velocity models
2. **Study tutorials_advanced.md** - Learn dynamical modeling and latent time
3. **Practice with visualization.md** - Create publication-quality plots
4. **Experiment with parameters** - Optimize for your specific data

### For Advanced Users
1. **Dive into inference.md** - Metabolic labeling and custom parameter estimation
2. **Extend with utilities.md** - Custom functions and data manipulation
3. **Reference api_reference.md** - Complete function documentation
4. **Contribute to scVelo** - Use development version and report issues

## Key Concepts

### RNA Velocity Fundamentals
- **Unspliced vs Spliced mRNA** - Pre-mRNA (introns) vs mature mRNA (exons)
- **Velocity vectors** - Direction and magnitude of transcriptional change
- **Steady-state assumption** - Balance between transcription, splicing, degradation

### Modeling Approaches
- **Steady-state/Deterministic** - Simple linear regression approach
- **Stochastic** - Second-order moments for better steady-state capture
- **Dynamical** - Full likelihood-based EM framework for transient states

### Core Workflow
1. **Data preprocessing** - Quality control and normalization
2. **Moment computation** - Neighborhood averages in PCA space
3. **Velocity estimation** - Gene-specific transcriptional dynamics
4. **Graph construction** - Cell-to-cell transition probabilities
5. **Visualization** - Projection onto embeddings and interpretation

### Advanced Features
- **Latent time** - Gene-shared internal clock from dynamics
- **Terminal states** - Root and end points of trajectories
- **Differential kinetics** - Statistical tests for kinetic regime changes
- **Driver genes** - Putative regulators of cell fate decisions

## Practical Tips

### Data Requirements
- **Spliced/unspliced matrices** - Essential for velocity computation
- **Quality control** - Remove low-quality cells and genes
- **Sufficient depth** - Adequate coverage for reliable moment estimation

### Parameter Selection
- **n_neighbors** - Typically 20-50, affects smoothing
- **n_top_genes** - 1000-3000 HVGs for velocity computation
- **mode choice** - 'stochastic' for speed, 'dynamical' for accuracy

### Common Pitfalls
- **Insufficient preprocessing** - Always filter and normalize properly
- **Over-smoothing** - Too many neighbors can mask real dynamics
- **Wrong model choice** - Transient states need dynamical modeling

## Resources

### Documentation Structure
- **references/** - Complete extracted documentation with examples
- **Original scVelo docs** - Source documentation at scvelo.org
- **GitHub repository** - Code, issues, and development

### Community Support
- **GitHub discussions** - Questions and community knowledge
- **Issue reporting** - Bug reports and feature requests
- **Citation guidelines** - Proper attribution for research use

## Updating This Skill

To refresh this skill with updated documentation:
1. Re-run the documentation scraper with current scVelo version
2. Update reference files with latest API changes
3. Add new examples from recent tutorials and notebooks
4. Verify all code examples work with current dependencies

---
*This skill was generated from scVelo official documentation and includes comprehensive coverage of RNA velocity analysis methods.*

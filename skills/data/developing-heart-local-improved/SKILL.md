---
name: developing-heart-local-improved
description: Developing Heart Atlas - comprehensive cardiac development analysis with spatial multi-omics integration
---

# Developing-Heart-Local-Improved Skill

Comprehensive assistance with developing-heart-local-improved development, generated from official documentation.

## When to Use This Skill

This skill should be triggered when:
- Working with developing-heart-local-improved
- Asking about developing-heart-local-improved features or APIs
- Implementing developing-heart-local-improved solutions
- Debugging developing-heart-local-improved code
- Learning developing-heart-local-improved best practices

## Quick Reference

### Common Patterns

**Pattern 1:** In [13]: ?sc.pl.embedding Signature: sc.pl.embedding( adata: anndata._core.anndata.AnnData, basis: str, *, color: Union[str, Sequence[str], NoneType] = None, gene_symbols: Union[str, NoneType] = None, use_raw: Union[bool, NoneType] = None, sort_order: bool = True, edges: bool = False, edges_width: float = 0.1, edges_color: Union[str, Sequence[float], Sequence[str]] = 'grey', neighbors_key: Union[str, NoneType] = None, arrows: bool = False, arrows_kwds: Union[Mapping[str, Any], NoneType] = None, groups: Union[str, NoneType] = None, components: Union[str, Sequence[str]] = None, dimensions: Union[Tuple[int, int], Sequence[Tuple[int, int]], NoneType] = None, layer: Union[str, NoneType] = None, projection: Literal['2d', '3d'] = '2d', scale_factor: Union[float, NoneType] = None, color_map: Union[matplotlib.colors.Colormap, str, NoneType] = None, cmap: Union[matplotlib.colors.Colormap, str, NoneType] = None, palette: Union[str, Sequence[str], cycler.Cycler, NoneType] = None, na_color: Union[str, Tuple[float, ...]] = 'lightgray', na_in_legend: bool = True, size: Union[float, Sequence[float], NoneType] = None, frameon: Union[bool, NoneType] = None, legend_fontsize: Union[int, float, Literal['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'], NoneType] = None, legend_fontweight: Union[int, Literal['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']] = 'bold', legend_loc: str = 'right margin', legend_fontoutline: Union[int, NoneType] = None, colorbar_loc: Union[str, NoneType] = 'right', vmax: Union[str, float, Callable[[Sequence[float]], float], Sequence[Union[str, float, Callable[[Sequence[float]], float]]], NoneType] = None, vmin: Union[str, float, Callable[[Sequence[float]], float], Sequence[Union[str, float, Callable[[Sequence[float]], float]]], NoneType] = None, vcenter: Union[str, float, Callable[[Sequence[float]], float], Sequence[Union[str, float, Callable[[Sequence[float]], float]]], NoneType] = None, norm: Union[matplotlib.colors.Normalize, Sequence[matplotlib.colors.Normalize], NoneType] = None, add_outline: Union[bool, NoneType] = False, outline_width: Tuple[float, float] = (0.3, 0.05), outline_color: Tuple[str, str] = ('black', 'white'), ncols: int = 4, hspace: float = 0.25, wspace: Union[float, NoneType] = None, title: Union[str, Sequence[str], NoneType] = None, show: Union[bool, NoneType] = None, save: Union[bool, str, NoneType] = None, ax: Union[matplotlib.axes._axes.Axes, NoneType] = None, return_fig: Union[bool, NoneType] = None, **kwargs, ) -> Union[matplotlib.figure.Figure, matplotlib.axes._axes.Axes, NoneType] Docstring: Scatter plot for user specified embedding basis (e.g. umap, pca, etc) Parameters ---------- basis : str Name of the `obsm` basis to use. adata : AnnData Annotated data matrix. color : typing.Union[str, typing.Sequence[str], NoneType], optional (default: None) Keys for annotations of observations/cells or variables/genes, e.g., `'ann1'` or `['ann1', 'ann2']`. gene_symbols : typing.Union[str, NoneType], optional (default: None) Column name in `.var` DataFrame that stores gene symbols. By default `var_names` refer to the index column of the `.var` DataFrame. Setting this option allows alternative names to be used. use_raw : typing.Union[bool, NoneType], optional (default: None) Use `.raw` attribute of `adata` for coloring with gene expression. If `None`, defaults to `True` if `layer` isn't provided and `adata.raw` is present. layer : typing.Union[str, NoneType], optional (default: None) Name of the AnnData object layer that wants to be plotted. By default adata.raw.X is plotted. If `use_raw=False` is set, then `adata.X` is plotted. If `layer` is set to a valid layer name, then the layer is plotted. `layer` takes precedence over `use_raw`. edges : bool, optional (default: False) Show edges. edges_width : float, optional (default: 0.1) Width of edges. edges_color : typing.Union[str, typing.Sequence[float], typing.Sequence[str]], optional (default: 'grey') Color of edges. See :func:`~networkx.drawing.nx_pylab.draw_networkx_edges`. neighbors_key : typing.Union[str, NoneType], optional (default: None) Where to look for neighbors connectivities. If not specified, this looks .obsp['connectivities'] for connectivities (default storage place for pp.neighbors). If specified, this looks .obsp[.uns[neighbors_key]['connectivities_key']] for connectivities. arrows : bool, optional (default: False) Show arrows (deprecated in favour of `scvelo.pl.velocity_embedding`). arrows_kwds : typing.Union[typing.Mapping[str, typing.Any], NoneType], optional (default: None) Passed to :meth:`~matplotlib.axes.Axes.quiver` sort_order : bool, optional (default: True) For continuous annotations used as color parameter, plot data points with higher values on top of others. groups : typing.Union[str, NoneType], optional (default: None) Restrict to a few categories in categorical observation annotation. The default is not to restrict to any groups. dimensions : typing.Union[typing.Tuple[int, int], typing.Sequence[typing.Tuple[int, int]], NoneType], optional (default: None) 0-indexed dimensions of the embedding to plot as integers. E.g. [(0, 1), (1, 2)]. Unlike `components`, this argument is used in the same way as `colors`, e.g. is used to specify a single plot at a time. Will eventually replace the components argument. components : typing.Union[str, typing.Sequence[str]], optional (default: None) For instance, `['1,2', '2,3']`. To plot all available components use `components='all'`. projection : typing.Literal['2d', '3d'], optional (default: '2d') Projection of plot (default: `'2d'`). legend_loc : str, optional (default: 'right margin') Location of legend, either `'on data'`, `'right margin'` or a valid keyword for the `loc` parameter of :class:`~matplotlib.legend.Legend`. legend_fontsize : typing.Union[int, float, typing.Literal['xx-small', 'x-small', 'small', 'medium', 'large', 'x-large', 'xx-large'], NoneType], optional (default: None) Numeric size in pt or string describing the size. See :meth:`~matplotlib.text.Text.set_fontsize`. legend_fontweight : typing.Union[int, typing.Literal['light', 'normal', 'medium', 'semibold', 'bold', 'heavy', 'black']], optional (default: 'bold') Legend font weight. A numeric value in range 0-1000 or a string. Defaults to `'bold'` if `legend_loc == 'on data'`, otherwise to `'normal'`. See :meth:`~matplotlib.text.Text.set_fontweight`. legend_fontoutline : typing.Union[int, NoneType], optional (default: None) Line width of the legend font outline in pt. Draws a white outline using the path effect :class:`~matplotlib.patheffects.withStroke`. colorbar_loc : typing.Union[str, NoneType], optional (default: 'right') Where to place the colorbar for continous variables. If `None`, no colorbar is added. size : typing.Union[float, typing.Sequence[float], NoneType], optional (default: None) Point size. If `None`, is automatically computed as 120000 / n_cells. Can be a sequence containing the size for each cell. The order should be the same as in adata.obs. color_map : typing.Union[matplotlib.colors.Colormap, str, NoneType], optional (default: None) Color map to use for continous variables. Can be a name or a :class:`~matplotlib.colors.Colormap` instance (e.g. `"magma`", `"viridis"` or `mpl.cm.cividis`), see :func:`~matplotlib.cm.get_cmap`. If `None`, the value of `mpl.rcParams["image.cmap"]` is used. The default `color_map` can be set using :func:`~scanpy.set_figure_params`. palette : typing.Union[str, typing.Sequence[str], cycler.Cycler, NoneType], optional (default: None) Colors to use for plotting categorical annotation groups. The palette can be a valid :class:`~matplotlib.colors.ListedColormap` name (`'Set2'`, `'tab20'`, …), a :class:`~cycler.Cycler` object, a dict mapping categories to colors, or a sequence of colors. Colors must be valid to matplotlib. (see :func:`~matplotlib.colors.is_color_like`). If `None`, `mpl.rcParams["axes.prop_cycle"]` is used unless the categorical variable already has colors stored in `adata.uns["{var}_colors"]`. If provided, values of `adata.uns["{var}_colors"]` will be set. na_color : typing.Union[str, typing.Tuple[float, ...]], optional (default: 'lightgray') Color to use for null or masked values. Can be anything matplotlib accepts as a color. Used for all points if `color=None`. na_in_legend : bool, optional (default: True) If there are missing values, whether they get an entry in the legend. Currently only implemented for categorical legends. frameon : typing.Union[bool, NoneType], optional (default: None) Draw a frame around the scatter plot. Defaults to value set in :func:`~scanpy.set_figure_params`, defaults to `True`. title : typing.Union[str, typing.Sequence[str], NoneType], optional (default: None) Provide title for panels either as string or list of strings, e.g. `['title1', 'title2', ...]`. vmin : typing.Union[str, float, typing.Callable[[typing.Sequence[float]], float], typing.Sequence[typing.Union[str, float, typing.Callable[[typing.Sequence[float]], float]]], NoneType], optional (default: None) The value representing the lower limit of the color scale. Values smaller than vmin are plotted with the same color as vmin. vmin can be a number, a string, a function or `None`. If vmin is a string and has the format `pN`, this is interpreted as a vmin=percentile(N). For example vmin='p1.5' is interpreted as the 1.5 percentile. If vmin is function, then vmin is interpreted as the return value of the function over the list of values to plot. For example to set vmin tp the mean of the values to plot, `def my_vmin(values): return np.mean(values)` and then set `vmin=my_vmin`. If vmin is None (default) an automatic minimum value is used as defined by matplotlib `scatter` function. When making multiple plots, vmin can be a list of values, one for each plot. For example `vmin=[0.1, 'p1', None, my_vmin]` vmax : typing.Union[str, float, typing.Callable[[typing.Sequence[float]], float], typing.Sequence[typing.Union[str, float, typing.Callable[[typing.Sequence[float]], float]]], NoneType], optional (default: None) The value representing the upper limit of the color scale. The format is the same as for `vmin`. vcenter : typing.Union[str, float, typing.Callable[[typing.Sequence[float]], float], typing.Sequence[typing.Union[str, float, typing.Callable[[typing.Sequence[float]], float]]], NoneType], optional (default: None) The value representing the center of the color scale. Useful for diverging colormaps. The format is the same as for `vmin`. Example: sc.pl.umap(adata, color='TREM2', vcenter='p50', cmap='RdBu_r') add_outline : typing.Union[bool, NoneType], optional (default: False) If set to True, this will add a thin border around groups of dots. In some situations this can enhance the aesthetics of the resulting image outline_color : typing.Tuple[str, str], optional (default: ('black', 'white')) Tuple with two valid color names used to adjust the add_outline. The first color is the border color (default: black), while the second color is a gap color between the border color and the scatter dot (default: white). outline_width : typing.Tuple[float, float], optional (default: (0.3, 0.05)) Tuple with two width numbers used to adjust the outline. The first value is the width of the border color as a fraction of the scatter dot size (default: 0.3). The second value is width of the gap color (default: 0.05). ncols : int, optional (default: 4) Number of panels per row. wspace : typing.Union[float, NoneType], optional (default: None) Adjust the width of the space between multiple panels. hspace : float, optional (default: 0.25) Adjust the height of the space between multiple panels. return_fig : typing.Union[bool, NoneType], optional (default: None) Return the matplotlib figure. kwargs : _empty Arguments to pass to :func:`matplotlib.pyplot.scatter`, for instance: the maximum and minimum values (e.g. `vmin=-2, vmax=5`). show : typing.Union[bool, NoneType], optional (default: None) Show the plot, do not return axis. save : typing.Union[bool, str, NoneType], optional (default: None) If `True` or a `str`, save the figure. A string is appended to the default filename. Infer the filetype if ending on {`'.pdf'`, `'.png'`, `'.svg'`}. ax : typing.Union[matplotlib.axes._axes.Axes, NoneType], optional (default: None) A matplotlib axes object. Only works if plotting a single component. Returns ------- If `show==False` a :class:`~matplotlib.axes.Axes` or a list of it. File: /nfs/team205/kk18/miniconda3/envs/vitro/lib/python3.8/site-packages/scanpy/plotting/_tools/scatterplots.py Type: function

```
?sc.pl.embedding
```

### Example Code Patterns

**Example 1** (python):
```python
import scanpy as sc
import pandas as pd
import numpy as np
import anndata

from scipy.io import mmwrite, mmread
from scipy.sparse import csr_matrix
```

**Example 2** (python):
```python
import scvi
import anndata
import scipy
import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt

scvi.settings.seed = 420
```

**Example 3** (python):
```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import gaussian_kde

import scanpy as sc
```

**Example 4** (python):
```python
import session_info
session_info.show()
```

**Example 5** (python):
```python
import numpy as np
import pandas as pd
import scanpy as sc
import matplotlib.pyplot as plt
import scrublet as scr
import session_info
```

## Reference Files

This skill includes comprehensive documentation in `references/`:

- **atac_analysis.md** - Atac Analysis documentation
- **atac_preprocessing.md** - Atac Preprocessing documentation
- **cardiomyocytes.md** - Cardiomyocytes documentation
- **cell_annotation.md** - Cell Annotation documentation
- **cell_communication.md** - Cell Communication documentation
- **niche_analysis.md** - Niche Analysis documentation
- **other.md** - Other documentation
- **rna_integration.md** - Rna Integration documentation
- **rna_qc.md** - Rna Qc documentation
- **supplementary.md** - Supplementary documentation
- **trisomy21.md** - Trisomy21 documentation
- **visium_analysis.md** - Visium Analysis documentation
- **visiumhd_analysis.md** - Visiumhd Analysis documentation
- **xenium_analysis.md** - Xenium Analysis documentation

Use `view` to read specific reference files when detailed information is needed.

## Working with This Skill

### For Beginners
Start with the getting_started or tutorials reference files for foundational concepts.

### For Specific Features
Use the appropriate category reference file (api, guides, etc.) for detailed information.

### For Code Examples
The quick reference section above contains common patterns extracted from the official docs.

## Resources

### references/
Organized documentation extracted from official sources. These files contain:
- Detailed explanations
- Code examples with language annotations
- Links to original documentation
- Table of contents for quick navigation

### scripts/
Add helper scripts here for common automation tasks.

### assets/
Add templates, boilerplate, or example projects here.

## Notes

- This skill was automatically generated from official documentation
- Reference files preserve the structure and examples from source docs
- Code examples include language detection for better syntax highlighting
- Quick reference patterns are extracted from common usage examples in the docs

## Updating

To refresh this skill with updated documentation:
1. Re-run the scraper with the same configuration
2. The skill will be rebuilt with the latest information

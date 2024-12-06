import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scanpy as sc
import scipy.sparse as ss
from plotnine import *
from sklearn import preprocessing
from sklearn.neighbors import NearestNeighbors
import networkx as nx
from scipy.stats import norm
from typing import Optional, Union
import anndata
import matplotlib as mpl
import gseapy as gp
import seaborn as sns


def lr_module_umap(adata, return_fig=False):
    plot_data = adata.uns['lr_module_info']['lr_umap_df'].copy()
    plot_data['label'] = adata.uns['lr_module_info']['lr_module_df']['module']
    plot_data.columns = ['UMAP_1', 'UMAP_2', 'Module']

    # plot
    p = (ggplot(plot_data, aes(x='UMAP_1', y='UMAP_2', fill='Module'))
         + geom_point(stroke=0, size=3)
         + scale_fill_hue()
         + theme_classic())
    print(p)
    if return_fig:
        return p


def svi_kneed_plot(interaction_df, return_fig=False):
    plot_data = interaction_df.loc[:, ['gft_score', 'svi_rank', 'cutoff_gft_score']]
    plt.figure()
    sns.scatterplot(x="svi_rank", y="gft_score",
                    hue="cutoff_gft_score",
                    data=plot_data,
                    palette='Set2')
    plt.xlabel("Rank of spatial variable L-Rs")
    plt.ylabel("GFT score")
    plt.grid(False)
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    plt.show()
    if return_fig:
        return ax


def cell_type_heatmap(ct_df, return_fig=False, cmap='magma'):
    plot_df = ct_df.transpose().stack().reset_index()
    plot_df.columns = ['Receiver', 'Sender', 'Value']
    p = ggplot(plot_df,
               aes(x='Receiver', y='Sender', fill='Value')) + \
        geom_tile() + \
        scale_fill_cmap(cmap) + \
        labs(title='Cell type communications', x='Receiver', y='Sender') + \
        theme(axis_text_x=element_text(angle=90, hjust=1))
    print(p)
    if return_fig:
        return p


def obtain_rd_single(adata, interaction, step=1):
    add_columns = [interaction + f"-{step}-ligand", interaction + f"-{step}-receptor",
                   interaction + f"-{step}-interaction", interaction + f"-{step}-new_ligand",
                   interaction + f"-{step}-new_receptor"]
    if step == 1:
        adata.obs[interaction + f"-{step}-ligand"] = adata.uns['interaction_info'][str(step - 1)][0].loc[:,
                                                     interaction].values
        adata.obs[interaction + f"-{step}-receptor"] = adata.uns['interaction_info'][str(step - 1)][1].loc[:,
                                                       interaction].values
    else:
        adata.obs[interaction + f"-{step}-ligand"] = adata.uns['interaction_info'][str(step - 1)][1].loc[:,
                                                     interaction].values
        adata.obs[interaction + f"-{step}-receptor"] = adata.uns['interaction_info'][str(step - 1)][2].loc[:,
                                                       interaction].values
    adata.obs[interaction + f"-{step}-interaction"] = adata.uns['interaction_info'][str(step)][0].loc[:,
                                                      interaction].values
    adata.obs[interaction + f"-{step}-new_ligand"] = adata.uns['interaction_info'][str(step)][1].loc[:,
                                                     interaction].values
    adata.obs[interaction + f"-{step}-new_receptor"] = adata.uns['interaction_info'][str(step)][2].loc[:,
                                                       interaction].values

    return add_columns


def obtain_rd_system(adata, interaction, step=1):
    ligands = adata.uns['lr_info']['ligand_unit'][interaction]
    receptors = adata.uns['lr_info']['receptor_unit'][interaction]
    add_columns = [i + f"-{step}-ligand" for i in ligands] + \
                  [i + f"-{step}-receptor" for i in receptors] + \
                  [interaction + f"-{step}-interaction"] + \
                  [i + f"-{step}-new_ligand" for i in ligands] + \
                  [i + f"-{step}-new_receptor" for i in receptors]

    if step == 1:
        for ligand in ligands:
            adata.obs[ligand + f"-{step}-ligand"] = adata.uns['interaction_info'][str(step - 1)][0].loc[:,
                                                    ligand].values
        for receptor in receptors:
            adata.obs[receptor + f"-{step}-receptor"] = adata.uns['interaction_info'][str(step - 1)][1].loc[:,
                                                        receptor].values
    else:
        for ligand in ligands:
            adata.obs[ligand + f"-{step}-ligand"] = adata.uns['interaction_info'][str(step - 1)][1].loc[:,
                                                    ligand].values
        for receptor in receptors:
            adata.obs[receptor + f"-{step}-receptor"] = adata.uns['interaction_info'][str(step - 1)][2].loc[:,
                                                        receptor].values

    adata.obs[interaction + f"-{step}-interaction"] = adata.uns['interaction_info'][str(step)][0].loc[:,
                                                      interaction].values
    for ligand in ligands:
        adata.obs[ligand + f"-{step}-new_ligand"] = adata.uns['interaction_info'][str(step)][1].loc[:,
                                                    ligand].values
    for receptor in receptors:
        adata.obs[receptor + f"-{step}-new_receptor"] = adata.uns['interaction_info'][str(step)][2].loc[:,
                                                        receptor].values

    return add_columns


def plot_module_go(adata,
                   module,
                   organism='Human',
                   top_terms=20,
                   figsize=(20, 8),
                   gene_sets='GO_Biological_Process_2021',
                   return_fig=False):
    if isinstance(module, int):
        module = str(module)
    if 'module' not in module:
        module = 'module_' + module

    # add ligands and receptors
    lr_list = []
    lr_module_df = adata.uns['lr_module_info']['lr_module_df']
    lr_module_df = lr_module_df.loc[lr_module_df['module'] == module.split('module_')[-1], :]
    for lr in lr_module_df.index:
        lr_list.append(adata.uns['lr_info'].loc[lr, 'ligand'])
        lr_list.append(adata.uns['lr_info'].loc[lr, 'receptor'])
    lr_list = np.unique(lr_list).tolist()

    # enrichment analysis
    enr = gp.enrichr(gene_list=lr_list,
                     gene_sets=gene_sets,
                     organism=organism,
                     outdir=f'./tmp/GO_module-{module}',
                     no_plot=False,
                     cutoff=0.05  # test dataset, use lower value from range(0,1)
                     )

    from gseapy.plot import barplot, dotplot
    ax = barplot(enr.results[enr.results.Gene_set == 'GO_Biological_Process_2021'],
                 column='P-value',
                 top_term=top_terms,
                 title=f'{gene_sets}: module {module}',
                 figsize=figsize,

                 )
    plt.yticks(fontsize=18)
    plt.yticks(fontsize=18)
    plt.tight_layout()
    plt.show()
    if return_fig:
        return ax


# def plot_pathway(adata,
#                  module,
#                  add_lr=True,
#                  organism='Human',
#                  top_terms=20,
#                  gene_sets='GO_Biological_Process_2021',
#                  return_fig=False):
#     if isinstance(module, int):
#         module = str(module)
#     if 'module' not in module:
#         module = 'module_' + module
#     # extract genes
#     module_genes = adata.uns['lr_module_info']['gene_module_df']
#     module_genes = module_genes.index[module_genes['module'] == module]
#     module_genes = module_genes.tolist()
#
#     # add ligands and receptors
#     lr_list = []
#     lr_module_df = adata.uns['lr_module_info']['lr_module_df']
#     lr_module_df = lr_module_df.loc[lr_module_df['module'] == module.split('module_')[-1], :]
#     for lr in lr_module_df.index:
#         lr_list.append(adata.uns['lr_info'].loc[lr, 'ligand'])
#         lr_list.append(adata.uns['lr_info'].loc[lr, 'receptor'])
#     lr_list = np.unique(lr_list).tolist()
#     if add_lr:
#         module_genes = module_genes + lr_list
#         module_genes = np.unique(module_genes).tolist()
#
#     # enrichment analysis
#     enr = gp.enrichr(gene_list=module_genes,
#                      gene_sets=gene_sets,
#                      organism=organism,
#                      outdir=f'./tmp/GO_module-{module}',
#                      no_plot=False,
#                      cutoff=0.05  # test dataset, use lower value from range(0,1)
#                      )
#
#     from gseapy.plot import barplot, dotplot
#     barplot(enr.results[enr.results.Gene_set == 'GO_Biological_Process_2021'],
#             column='P-value',
#             top_term=top_terms,
#             title=f'{gene_sets}: module {module}',
#             figsize=(15, 10),
#             )
#     plt.yticks(fontsize=18)
#     plt.yticks(fontsize=18)
#     plt.tight_layout()
#     ax = plt.gca()
#     plt.show()
#     if return_fig:
#         return ax


def plot_interaction(adata,
                     interaction,
                     source='original',
                     return_figure=True,
                     **kwargs):
    # Obtain ligands
    if isinstance(interaction, pd.core.indexes.base.Index):
        interaction = interaction[0]
    ax_list = []
    ligands = adata.uns['lr_info']['ligand_unit'][interaction]
    receptors = adata.uns['lr_info']['receptor_unit'][interaction]

    # Add vectors
    if ss.issparse(adata.X):
        adata.obs.loc[:, [f'Ligand {ligand}' for ligand in ligands]] = \
            adata[:, ligands].X.A
        adata.obs.loc[:, [f'Receptor {receptor}' for receptor in receptors]] = \
            adata[:, receptors].X.A
    else:
        adata.obs.loc[:, [f'Ligand {ligand}' for ligand in ligands]] = \
            adata[:, ligands].X
        adata.obs.loc[:, [f'Receptor {receptor}' for receptor in receptors]] = \
            adata[:, receptors].X
    adata.obs.loc[:, [f'Ligand {ligand} with diffusion' for ligand in ligands]] = \
        adata.obsm['ligand_unit_diffusion_expression'].loc[:, ligands].values

    if source == 'original':
        ax_list = sc.pl.spatial(adata,
                                color=[f'Ligand {ligand}' for ligand in ligands] +
                                      [f'Receptor {receptor}' for receptor in receptors],
                                return_fig=True,
                                **kwargs)
    elif source == 'diffusion':
        ax_list = sc.pl.spatial(adata,
                                color=[f'Ligand {ligand} with diffusion' for ligand in ligands] +
                                      [f'Receptor {receptor}' for receptor in receptors],
                                return_fig=True, **kwargs)
    elif source == 'mixed':
        ax_list = sc.pl.spatial(adata,
                                color=[f'Ligand {ligand}' for ligand in ligands] +
                                      [f'Ligand {ligand} with diffusion' for ligand in ligands] +
                                      [f'Receptor {receptor}' for receptor in receptors],
                                return_fig=True, **kwargs)

    # Remove vectors
    adata.obs.drop([f'Ligand {ligand}' for ligand in ligands] +
                   [f'Ligand {ligand} with diffusion' for ligand in ligands] +
                   [f'Receptor {receptor}' for receptor in receptors],
                   axis=1)
    if return_figure:
        return ax_list


def pie_annotation(adata,
                   module,
                   fig_size=(9, 6)):
    if isinstance(module, int):
        module = str(module)
    color_map = {'ECM-Receptor': plt.cm.tab20c(9), 'Cell-Cell Contact': plt.cm.tab20c(5),
                 'Secreted Signaling': plt.cm.tab20c(13)}

    data = adata.uns['lr_info']['lr_score_df']
    data = data.loc[data['lr_module'] == module, :]
    total_counts = data.shape[0]
    unique_name, counts = np.unique(data['annotation'], return_counts=True)
    colors = [color_map[i] for i in unique_name]

    plt.figure(figsize=fig_size)
    plt.pie(counts,
            labels=unique_name,
            colors=colors,
            autopct=lambda pct: f"{pct:.1f}% ({int(pct / 100 * sum(counts))})")
    plt.title(f"interaction annotations in module {module}")
    plt.show()


def pie_pathway(adata,
                module,
                fig_size=(9, 6)):
    if isinstance(module, int):
        module = str(module)

    data = adata.uns['lr_info']['lr_score_df']
    data = data.loc[data['lr_module'] == module, :]
    unique_name, counts = np.unique(data['pathway_name'], return_counts=True)
    plt.figure(figsize=fig_size)
    plt.title(f"pathway names in module {module}")
    plt.pie(counts,
            labels=unique_name,
            autopct=lambda pct: f"{pct:.1f}% ({int(pct / 100 * sum(counts))})",
            textprops={'fontsize': 10})
    plt.show()


def lr_freq_signal(adata,
                   interaction,
                   dpi=100,
                   colors=None,
                   fontsize=10,
                   **kwargs):
    if colors is None:
        colors = ['#CA1C1C', '#345591']
    annotation = adata.uns['lr_info']['lr_meta'].at[interaction, 'annotation']
    if annotation == 'Cell-Cell Contact':
        ligands_freq_signal = adata.uns['GFT_info']['ligands_freq_mtx'].loc[interaction, :].values
    else:
        ligands_freq_signal = adata.uns['GFT_info']['ligands_diffusion_freq_mtx'].loc[interaction, :].values
    receptor_freq_signal = adata.uns['GFT_info']['receptors_freq_mtx'].loc[interaction, :].values

    # plot
    y_max = max(ligands_freq_signal.max(), receptor_freq_signal.max())
    y_min = min(ligands_freq_signal.min(), receptor_freq_signal.min())
    y_range = max(abs(y_max), abs(y_min)) * 1.05
    plt.figure(dpi=dpi, **kwargs)
    plt.subplot(211)
    plt.bar(list(range(len(ligands_freq_signal))), ligands_freq_signal, color=colors[0])
    ax = plt.gca()
    plt.xticks([])
    plt.grid(False)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    ax.spines['right'].set_color("none")
    ax.spines['top'].set_color("none")
    ax.spines['bottom'].set_color("none")
    plt.ylim(-y_range, y_range)
    plt.title(f"Ligand signals of {interaction}", fontsize=fontsize)
    plt.subplot(212)
    plt.bar(list(range(len(ligands_freq_signal))), receptor_freq_signal, color=colors[1])
    ax = plt.gca()
    plt.grid(False)
    plt.xticks(fontsize=fontsize)
    plt.yticks(fontsize=fontsize)
    ax.spines['right'].set_color("none")
    ax.spines['top'].set_color("none")
    plt.ylim(-y_range, y_range)
    plt.title(f"Receptor signals of {interaction}", fontsize=fontsize)
    plt.show()


def svg_freq_signal(adata,
                    gene,
                    domain='freq_domain_svg',
                    figsize=(6, 2),
                    dpi=100,
                    colors=None,
                    return_fig=False, **kwargs):
    # Show the frequency signal
    if colors is None:
        colors = ['#CA1C1C', '#345591']
    freq_signal = adata[:, gene].varm[domain]
    freq_signal = np.ravel(freq_signal)
    plt.figure(figsize=figsize, dpi=dpi)
    low = list(range(adata.uns['identify_SVG_data']['fms_low'].shape[1]))
    plt.bar(low, freq_signal[low], color=colors[0])
    high = list(range(len(low), freq_signal.size))
    plt.bar(high, freq_signal[high], color=colors[1])
    ax = plt.gca()
    ax.set_ylabel("signal")
    ax.spines['right'].set_color("none")
    ax.spines['top'].set_color("none")
    y_max = max(freq_signal)
    plt.ylim(0, y_max * 1.1)
    plt.xlim(0, freq_signal.size)
    plt.title("Gene: " + gene)
    plt.show()
    if return_fig:
        return ax


def umap_lr_module(adata,
                   size=3,
                   alpha=1,
                   return_fig=True,
                   save_path=None):
    plot_df = adata.uns['lr_module_info']['lr_umap_df']
    plot_df['module'] = adata.uns['lr_module_info']['lr_module_df']
    categories = [eval(i) for i in np.unique(plot_df.module)]
    categories = np.sort(np.array(categories))
    categories = categories.astype(str)
    plot_df.ftu = pd.Categorical(plot_df.module,
                                 categories=categories)
    base_plot = (ggplot(plot_df,
                        aes('UMAP_1', 'UMAP_2',
                            fill='module'))
                 + geom_point(size=size, alpha=alpha, stroke=0.1)
                 + scale_fill_hue(s=0.9, l=0.65, h=0.0417, color_space='husl')
                 + theme_classic())
    print(base_plot)
    if save_path is not None:
        base_plot.save(f"{save_path}")
    if return_fig:
        return base_plot


def tm_freq_signal(adata, tm,
                   domain='freq_domain_svg', figsize=(6, 2),
                   dpi=100, color='#CA1C1C',
                   y_range=[0, 0.08],
                   return_fig=False, **kwargs):
    # Show the frequency signal
    freq_signal = signal = adata.uns['freq_signal_tm'].loc[tm, :].values
    plt.figure(figsize=figsize, dpi=dpi)
    low = list(range(len(freq_signal)))
    plt.bar(low, freq_signal, color=color)
    plt.grid(False)
    ax = plt.gca()
    ax.set_ylabel("siganl")
    ax.spines['right'].set_color("none")
    ax.spines['top'].set_color("none")
    plt.ylim(y_range[0], y_range[1])
    plt.xlim(0, freq_signal.size)
    plt.title(tm)
    plt.show()
    if return_fig:
        return ax


def subTm_freq_signal(adata, subTM,
                      domain='freq_domain_svg', figsize=(6, 2),
                      dpi=100, color='#CA1C1C',
                      y_range=[0, 0.08],
                      return_fig=False, **kwargs):
    # Show the frequency signal
    freq_signal = signal = adata.uns['freq_signal_subTM'].loc[subTM, :].values
    plt.figure(figsize=figsize, dpi=dpi)
    low = list(range(len(freq_signal)))
    plt.bar(low, freq_signal, color=color)
    ax = plt.gca()
    plt.grid(False)
    ax.set_ylabel("siganl")
    ax.spines['right'].set_color("none")
    ax.spines['top'].set_color("none")
    plt.ylim(y_range[0], y_range[1])
    plt.xlim(0, freq_signal.size)
    plt.title(subTM)
    plt.show()
    if return_fig:
        return ax


def gene_signal_umap(adata, svg_list, colors=['#C81E1E', '#BEBEBE'],
                     return_fig=False, n_neighbors=15,
                     random_state=0, **kwargs):
    low_length = adata.uns['identify_SVG_data']['frequencies_low'].shape[0]
    freq_domain = adata.varm['freq_domain_svg'][:, :low_length].copy()
    # weight_list = 1 /(1 + adata.uns['identify_SVG_data']['frequencies_low'])
    # freq_domain = np.multiply(freq_domain, weight_list)
    freq_domain = preprocessing.normalize(freq_domain, norm='l1')
    freq_domain = pd.DataFrame(freq_domain)
    freq_domain.index = adata.var_names
    umap_adata = sc.AnnData(freq_domain)
    sc.pp.neighbors(umap_adata, n_neighbors=n_neighbors, use_rep='X')
    sc.tl.umap(umap_adata, random_state=0)
    adata.varm['freq_umap_svg'] = umap_adata.obsm['X_umap']
    print("""The umap coordinates of genes when identify SVGs could be found in 
          adata.varm['freq_umap_svg']""")
    # svg_list
    umap_adata.obs['SpaGFT'] = 'Non-SVGs'
    umap_adata.obs.loc[svg_list, 'SpaGFT'] = 'SVGs'
    umap_adata.obs['SpaGFT'] = pd.Categorical(umap_adata.obs['SpaGFT'],
                                              categories=['SVGs', 'Non-SVGs'],
                                              ordered=True)
    umap_adata.uns['SpaGFT_colors'] = colors
    t = sc.pl.umap(umap_adata, color="SpaGFT", return_fig=return_fig,
                   **kwargs)
    if return_fig:
        return t


# def scatter_gene_distri(adata, 
#                         gene, 
#                         size=3, 
#                         shape='h',
#                         cmap='magma',
#                         spatial_info=['array_row', 'array_col'],
#                         coord_ratio=1,
#                         return_plot=False):
#     if ss.issparse(adata.X):
#         plot_df = pd.DataFrame(adata.X.todense(), index=adata.obs_names,
#                            columns=adata.var_names)
#     else:
#         plot_df = pd.DataFrame(adata.X, index=adata.obs_names,
#                            columns=adata.var_names)
#     if spatial_info in adata.obsm_keys():
#         plot_df['x'] = adata.obsm[spatial_info][:, 0]
#         plot_df['y'] = adata.obsm[spatial_info][:, 1]
#     elif set(spatial_info) <= set(adata.obs.columns):
#         plot_coor = adata.obs
#         plot_df = plot_df[gene]
#         plot_df = pd.DataFrame(plot_df)
#         plot_df['x'] = plot_coor.loc[:, spatial_info[0]].values
#         plot_df['y'] = plot_coor.loc[:, spatial_info[1]].values
#     plot_df['radius'] = size
#     plot_df = plot_df.sort_values(by=gene, ascending=True)
#     for i in [gene]:
#         base_plot = (ggplot() + geom_point(plot_df, aes(x='x', y='y', fill=i), 
#                                            shape=shape, stroke=0.1, size=size) +
#                       xlim(min(plot_df.x)-1, max(plot_df.x)+1) + 
#                       ylim(min(plot_df.y)-1, max(plot_df.y)+1) + 
#                       scale_fill_cmap(cmap_name=cmap) + 
#                       coord_equal(ratio=coord_ratio) +
#                       theme_classic() +
#                       theme(legend_position=('right'),
#                             legend_background=element_blank(),
#                             legend_key_width=4,
#                             legend_key_height=50)
#                       )
#         print(base_plot)
#     if return_plot:
#         return base_plot

def umap_svg_cluster(adata,
                     svg_list=None,
                     size=3,
                     shape='o',
                     cmap='magma',
                     spatial_info=['array_row', 'array_col'],
                     coord_ratio=1,
                     return_plot=True):
    if svg_list == None:
        tmp_df = adata.var.copy()
        svg_list = tmp_df[tmp_df.cutoff_gft_score][tmp_df.qvalue < 0.05].index
    plot_df = adata.uns['gft_umap_tm']
    plot_df = pd.DataFrame(plot_df)
    plot_df.index = adata.var_names
    plot_df.columns = ['UMAP_1', 'UMAP_2']

    plot_df.loc[svg_list, 'gene'] = 'SVG'
    plot_df['gene'] = pd.Categorical(plot_df['gene'],
                                     categories=['SVG', 'Non-SVG'],
                                     ordered=True)
    plot_df['radius'] = size
    # plot
    base_plot = (ggplot(plot_df, aes(x='UMAP_1', y='UMAP_2', fill='gene')) +
                 geom_point(size=size, color='white', stroke=0.25) +
                 scale_fill_manual(values=colors) +
                 theme_classic() +
                 coord_equal(ratio=coord_ratio))
    print(base_plot)
    if return_plot:
        return base_plot


def scatter_tm_expression(adata, tm, size=3, shape='o', cmap='magma',
                          spatial_info=['array_row', 'array_col'],
                          coord_ratio=0.7, return_plot=False):
    if '-' in tm:
        tm = 'tm-' + tm.split('-')[0] + "_subTm-" + tm.split('-')[1]
        plot_df = adata.obsm['subTm_pseudo_expression']
    else:
        tm = 'tm_' + tm
        plot_df = adata.obsm['tm_pseudo_expression']
    plot_df = pd.DataFrame(plot_df)
    if spatial_info in adata.obsm_keys():
        plot_df = plot_df[tm]
        plot_df['x'] = adata.obsm[spatial_info][:, 0]
        plot_df['y'] = adata.obsm[spatial_info][:, 1]
    elif set(spatial_info) <= set(adata.obs.columns):
        plot_coor = adata.obs
        plot_df = plot_df[tm]
        plot_df = pd.DataFrame(plot_df)
        plot_df['x'] = plot_coor.loc[:, spatial_info[0]].values
        plot_df['y'] = plot_coor.loc[:, spatial_info[1]].values
    plot_df['radius'] = size
    plot_df = plot_df.sort_values(by=tm, ascending=True)
    base_plot = (ggplot() + geom_point(plot_df, aes(x='x', y='y', fill=tm),
                                       shape=shape, stroke=0.1, size=size) +
                 xlim(min(plot_df.x) - 1, max(plot_df.x) + 1) +
                 ylim(min(plot_df.y) - 1, max(plot_df.y) + 1) +
                 scale_fill_cmap(cmap_name=cmap) +
                 coord_equal(ratio=coord_ratio) +
                 theme_classic() +
                 theme(legend_position=('right'),
                       legend_background=element_blank(),
                       legend_key_width=4,
                       legend_key_height=50)
                 )
    print(base_plot)
    if return_plot:
        return base_plot


def scatter_tm_binary(adata, tm, size=3, shape='h',
                      spatial_info=['array_row', 'array_col'],
                      colors=['#CA1C1C', '#CCCCCC'],
                      coord_ratio=0.7, return_plot=False):
    if '-' in tm:
        tm = 'tm-' + tm.split('-')[0] + "_subTm-" + tm.split('-')[1]
        plot_df = adata.obsm['subTm_binary']
    else:
        tm = 'tm_' + tm
        plot_df = adata.obsm['tm_binary']
    plot_df = pd.DataFrame(plot_df)
    if spatial_info in adata.obsm_keys():
        plot_df['x'] = adata.obsm[spatial_info][:, 0]
        plot_df['y'] = adata.obsm[spatial_info][:, 1]
    elif set(spatial_info) <= set(adata.obs.columns):
        plot_coor = adata.obs
        plot_df = plot_df[tm]
        plot_df = pd.DataFrame(plot_df)
        plot_df['x'] = plot_coor.loc[:, spatial_info[0]].values
        plot_df['y'] = plot_coor.loc[:, spatial_info[1]].values
    plot_df['radius'] = size
    plot_df[tm] = plot_df[tm].values.astype(int)
    plot_df[tm] = plot_df[tm].values.astype(str)
    plot_df[tm] = pd.Categorical(plot_df[tm],
                                 categories=['1', '0'],
                                 ordered=True)
    base_plot = (ggplot() + geom_point(plot_df, aes(x='x', y='y', fill=tm),
                                       shape=shape, stroke=0.1, size=size) +
                 xlim(min(plot_df.x) - 1, max(plot_df.x) + 1) +
                 ylim(min(plot_df.y) - 1, max(plot_df.y) + 1) +
                 scale_fill_manual(values=colors) +
                 coord_equal(ratio=coord_ratio) +
                 theme_classic() +
                 theme(legend_position=('right'),
                       legend_background=element_blank(),
                       legend_key_width=4,
                       legend_key_height=50)
                 )
    print(base_plot)
    if return_plot:
        return base_plot


def umap_svg(adata, svg_list=None, colors=['#CA1C1C', '#CCCCCC'], size=2,
             coord_ratio=0.7, return_plot=False):
    if 'gft_umap_svg' not in adata.varm_keys():
        raise KeyError("Please run SpaGFT.calculate_frequcncy_domain firstly")
    plot_df = adata.varm['gft_umap_svg']
    plot_df = pd.DataFrame(plot_df)
    plot_df.index = adata.var_names
    plot_df.columns = ['UMAP_1', 'UMAP_2']
    plot_df['gene'] = 'Non-SVG'
    if svg_list == None:
        tmp_df = adata.var.copy()
        svg_list = tmp_df[tmp_df.cutoff_gft_score][tmp_df.qvalue < 0.05].index
    plot_df.loc[svg_list, 'gene'] = 'SVG'
    plot_df['gene'] = pd.Categorical(plot_df['gene'],
                                     categories=['SVG', 'Non-SVG'],
                                     ordered=True)
    plot_df['radius'] = size
    # plot
    base_plot = (ggplot(plot_df, aes(x='UMAP_1', y='UMAP_2', fill='gene')) +
                 geom_point(size=size, color='white', stroke=0.25) +
                 scale_fill_manual(values=colors) +
                 theme_classic() +
                 coord_equal(ratio=coord_ratio))
    print(base_plot)
    if return_plot:
        return base_plot


def visualize_fms(adata, rank=1, low=True, size=3, cmap='magma',
                  spatial_info=['array_row', 'array_col'], shape='h',
                  coord_ratio=0.7, return_plot=False):
    if low:
        plot_df = pd.DataFrame(adata.uns['fms_low'])
        plot_df.index = adata.obs.index
        plot_df.columns = ['low_FM_' + str(i + 1) for i in range(plot_df.shape[1])]
        if spatial_info in adata.obsm_keys():
            plot_df['x'] = adata.obsm[spatial_info][:, 0]
            plot_df['y'] = adata.obsm[spatial_info][:, 1]
        elif set(spatial_info) <= set(adata.obs.columns):
            plot_coor = adata.obs
            plot_df = plot_df['low_FM_' + str(rank)]
            plot_df = pd.DataFrame(plot_df)
            plot_df['x'] = plot_coor.loc[:, spatial_info[0]].values
            plot_df['y'] = plot_coor.loc[:, spatial_info[1]].values
        plot_df['radius'] = size
        base_plot = (ggplot() + geom_point(plot_df, aes(x='x', y='y',
                                                        fill='low_FM_' + str(rank)),
                                           shape=shape, stroke=0.1, size=size) +
                     xlim(min(plot_df.x) - 1, max(plot_df.x) + 1) +
                     ylim(min(plot_df.y) - 1, max(plot_df.y) + 1) +
                     scale_fill_cmap(cmap_name=cmap) +
                     coord_equal(ratio=coord_ratio) +
                     theme_classic() +
                     theme(legend_position=('right'),
                           legend_background=element_blank(),
                           legend_key_width=4,
                           legend_key_height=50)
                     )
        print(base_plot)

    else:
        plot_df = pd.DataFrame(adata.uns['fms_high'])
        plot_df.index = adata.obs.index
        plot_df.columns = ['high_FM_' + str(i + 1) for i in \
                           range(adata.uns['fms_high'].shape[1])]
        if spatial_info in adata.obsm_keys():
            plot_df['x'] = adata.obsm[spatial_info][:, 0]
            plot_df['y'] = adata.obsm[spatial_info][:, 1]
        elif set(spatial_info) <= set(adata.obs.columns):
            plot_coor = adata.obs
            plot_df = plot_df['high_FM_' + str(plot_df.shape[1] - rank + 1)]
            plot_df = pd.DataFrame(plot_df)
            plot_df['x'] = plot_coor.loc[:, spatial_info[0]].values
            plot_df['y'] = plot_coor.loc[:, spatial_info[1]].values
        plot_df['radius'] = size
        base_plot = (ggplot() + geom_point(plot_df,
                                           aes(x='x', y='y',
                                               fill='high_FM_' + str(adata.uns['fms_high'].shape[1] - rank + 1)),
                                           shape=shape, stroke=0.1, size=size) +
                     xlim(min(plot_df.x) - 1, max(plot_df.x) + 1) +
                     ylim(min(plot_df.y) - 1, max(plot_df.y) + 1) +
                     scale_fill_cmap(cmap_name=cmap) +
                     coord_equal(ratio=coord_ratio) +
                     theme_classic() +
                     theme(legend_position=('right'),
                           legend_background=element_blank(),
                           legend_key_width=4,
                           legend_key_height=50)
                     )
        print(base_plot)

    if return_plot:
        return base_plot


def scatter_gene_distri(adata,
                        gene,
                        size=3,
                        shape='h',
                        cmap='magma',
                        spatial_info=['array_row', 'array_col'],
                        coord_ratio=1,
                        return_plot=False):
    if gene in adata.obs.columns:
        if isinstance(gene, str):
            plot_df = pd.DataFrame(adata.obs.loc[:, gene].values,
                                   index=adata.obs_names,
                                   columns=[gene])
        else:
            plot_df = pd.DataFrame(adata.obs.loc[:, gene],
                                   index=adata.obs_names,
                                   columns=gene)
        if spatial_info in adata.obsm_keys():
            plot_df['x'] = adata.obsm[spatial_info][:, 0]
            plot_df['y'] = adata.obsm[spatial_info][:, 1]
        elif set(spatial_info) <= set(adata.obs.columns):
            plot_coor = adata.obs
            plot_df['x'] = plot_coor.loc[:, spatial_info[0]].values
            plot_df['y'] = plot_coor.loc[:, spatial_info[1]].values

        if isinstance(gene, str):
            base_plot = (ggplot() + geom_point(plot_df, aes(x='x', y='y', fill=gene),
                                               shape=shape, stroke=0.1, size=size) +
                         xlim(min(plot_df.x) - 1, max(plot_df.x) + 1) +
                         ylim(min(plot_df.y) - 1, max(plot_df.y) + 1) +
                         scale_fill_cmap(cmap_name=cmap) +
                         coord_equal(ratio=coord_ratio) +
                         theme_classic() +
                         theme(legend_position=('right'),
                               legend_background=element_blank(),
                               legend_key_width=4,
                               legend_key_height=50)
                         )
            print(base_plot)
        else:
            for i in gene:
                base_plot = (ggplot() + geom_point(plot_df, aes(x='x', y='y', fill=gene),
                                                   shape=shape, stroke=0.1, size=size) +
                             xlim(min(plot_df.x) - 1, max(plot_df.x) + 1) +
                             ylim(min(plot_df.y) - 1, max(plot_df.y) + 1) +
                             scale_fill_cmap(cmap_name=cmap) +
                             coord_equal(ratio=coord_ratio) +
                             theme_classic() +
                             theme(legend_position=('right'),
                                   legend_background=element_blank(),
                                   legend_key_width=4,
                                   legend_key_height=50)
                             )
                print(base_plot)

        return
    if ss.issparse(adata.X):
        plot_df = pd.DataFrame(adata.X.todense(), index=adata.obs_names,
                               columns=adata.var_names)
    else:
        plot_df = pd.DataFrame(adata.X, index=adata.obs_names,
                               columns=adata.var_names)
    if spatial_info in adata.obsm_keys():
        plot_df['x'] = adata.obsm[spatial_info][:, 0]
        plot_df['y'] = adata.obsm[spatial_info][:, 1]
    elif set(spatial_info) <= set(adata.obs.columns):
        plot_coor = adata.obs
        plot_df = plot_df[gene]
        plot_df = pd.DataFrame(plot_df)
        plot_df['x'] = plot_coor.loc[:, spatial_info[0]].values
        plot_df['y'] = plot_coor.loc[:, spatial_info[1]].values
    plot_df['radius'] = size
    plot_df = plot_df.sort_values(by=gene, ascending=True)
    if isinstance(gene, str):
        base_plot = (ggplot() + geom_point(plot_df, aes(x='x', y='y', fill=gene),
                                           shape=shape, stroke=0.1, size=size) +
                     xlim(min(plot_df.x) - 1, max(plot_df.x) + 1) +
                     ylim(min(plot_df.y) - 1, max(plot_df.y) + 1) +
                     scale_fill_cmap(cmap_name=cmap) +
                     coord_equal(ratio=coord_ratio) +
                     theme_classic() +
                     theme(legend_position=('right'),
                           legend_background=element_blank(),
                           legend_key_width=4,
                           legend_key_height=50)
                     )
        print(base_plot)
    else:
        for i in gene:
            base_plot = (ggplot() + geom_point(plot_df, aes(x='x', y='y', fill=gene),
                                               shape=shape, stroke=0.1, size=size) +
                         xlim(min(plot_df.x) - 1, max(plot_df.x) + 1) +
                         ylim(min(plot_df.y) - 1, max(plot_df.y) + 1) +
                         scale_fill_cmap(cmap_name=cmap) +
                         coord_equal(ratio=coord_ratio) +
                         theme_classic() +
                         theme(legend_position=('right'),
                               legend_background=element_blank(),
                               legend_key_width=4,
                               legend_key_height=50)
                         )
            print(base_plot)
    if return_plot:
        return base_plot


def plot_molecule_scatter(adata,
                          molecule_name,
                          figsize=(3, 3),
                          size=None,
                          vmin=0,
                          vmax=1,
                          dpi=300,
                          cmap='viridis',
                          add_title=True,
                          show=True):
    from mpl_toolkits.axes_grid1 import make_axes_locatable
    time.sleep(2)
    coords = adata.obsm['spatial']
    fig, ax = plt.subplots(figsize=figsize, dpi=dpi)
    expression = adata[:, molecule_name].X.flatten()
    if size is not None:
        scatter = ax.scatter(coords[:, 0],
                             coords[:, 1],
                             c=expression,
                             s=size,
                             cmap=cmap,
                             vmin=vmin,
                             marker='o',
                             vmax=vmax)
    else:
        scatter = ax.scatter(coords[:, 0],
                             coords[:, 1],
                             c=expression,
                             marker='o',
                             cmap=cmap,
                             vmin=vmin,
                             vmax=vmax
                             )
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="3%", pad=0.05)
    cbar = plt.colorbar(scatter, cax=cax)
    if add_title:
        ax.set_title(molecule_name)
    ax.axis('on')
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_aspect('equal')
    plt.tight_layout()
    if show:
        plt.show()
    return fig


def dynamic_plot(adata,
                 lr_pair,
                 cmap='Oranges',
                 color='interaction',
                 save_path=None,
                 fps=5,
                 **kwargs):
    import imageio
    import os
    from pathlib import Path

    if color == 'ligand':
        plot_df = adata.obsm['ligand_process']
    elif color == 'receptor':
        plot_df = adata.obsm['receptor_process']
    else:
        plot_df = adata.obsm['interaction_process']
    selected_logs = []
    for i in plot_df.columns:
        if lr_pair in i:
            selected_logs.append(i)
    img_list = []
    plot_adata = sc.AnnData(plot_df)
    plot_adata.obsm['spatial'] = adata.obsm['spatial'].copy()
    vmax = plot_df[selected_logs].max().max()
    for i in selected_logs:
        fig = sc.pl.spatial(plot_adata, color=i, vmax=vmax, spot_size=5, cmap=cmap, return_fig=True, show=False,
                            **kwargs)
        fig.tight_layout()
        fig.show()
        img = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        img_list.append(img)
    # save gif
    save_name = lr_pair + '_' + color + "_dynamic.gif"
    if save_path is not None:
        save_name = os.path.join(save_path, save_name)
    imageio.mimsave(save_name, img_list, fps=fps)


def interaction_sum_over_time(adata):
    plot_df = adata.uns['lr_interaction_sum'].copy()
    for lr in plot_df.index:
        values = plot_df.loc[lr, :].values.tolist()
        fig, ax = plt.subplots(figsize=(10, 5))
        plt.plot(range(len(values)), values)
        plt.xlabel('Time')
        plt.ylabel('Interaction Sum')
        plt.title(lr)
        # remove top line and right line
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        # save
        plt.savefig(lr + '_interaction_sum.png')
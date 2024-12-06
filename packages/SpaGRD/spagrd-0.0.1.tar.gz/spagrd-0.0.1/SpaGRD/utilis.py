import numpy as np
import pandas as pd
import scanpy as sc
from scipy.spatial.distance import pdist, squareform
import itertools
import scipy.sparse as ss
from sklearn import preprocessing
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.neighbors import kneighbors_graph
import networkx as nx


def get_laplacian_mtx(adata,
                      num_neighbors=6,
                      sigma=1,
                      spatial_key='spatial',
                      normalization=False):
    if spatial_key in adata.obsm_keys():
        loc = adata.obsm[spatial_key]
    elif set(spatial_key) <= set(adata.obs_keys()):
        loc = adata.obs[spatial_key]
    else:
        raise KeyError("%s is not available in adata.obsm_keys" % \
                       spatial_key + " or adata.obs_keys")
    loc = pd.DataFrame(loc,
                       index=adata.obs_names)
    loc = sc.AnnData(loc)
    sc.pp.neighbors(loc,
                    n_neighbors=num_neighbors)
    adj_mtx = loc.obsp['distances'].A
    adj_mtx = adj_mtx / adj_mtx.max()
    # transform adj_mtx using gauss kernel function
    adj_mtx = np.exp(-adj_mtx / (2 * sigma ** 2))
    adj_mtx[adj_mtx == 1] = 0

    deg_mtx = adj_mtx.sum(axis=1)
    deg_mtx = create_degree_mtx(deg_mtx)
    if not normalization:
        lap_mtx = deg_mtx - adj_mtx
    else:
        deg_mtx = np.array(adj_mtx.sum(axis=1)) ** (-0.5)
        deg_mtx = create_degree_mtx(deg_mtx)
        lap_mtx = ss.identity(deg_mtx.shape[0]) - deg_mtx @ adj_mtx @ deg_mtx

    return lap_mtx


def find_hvgs(adata, norm_method=None, num_genes=2000):
    # Normalization
    if norm_method == "CPM":
        sc.pp.normalize_total(adata, target_sum=1e5)
        # log-transform
        sc.pp.log1p(adata)
    else:
        pass
    # Find high variable genes using sc.pp.highly_variable_genes() with default 
    # parameters
    sc.pp.highly_variable_genes(adata, n_top_genes=num_genes)
    HVG_list = adata.var.index[adata.var.highly_variable]
    HVG_list = list(HVG_list)

    return HVG_list


def create_adjacent_mtx(coor_df, spatial_names=['array_row', 'array_col'],
                        num_neighbors=4):
    # Transform coordinate dataframe to coordinate array
    coor_array = coor_df.loc[:, spatial_names].values
    coor_array.astype(np.float32)
    edge_list = []
    num_neighbors += 1
    for i in range(coor_array.shape[0]):
        point = coor_array[i, :]
        distances = np.sum(np.asarray((point - coor_array) ** 2), axis=1)
        distances = pd.DataFrame(distances,
                                 index=range(coor_array.shape[0]),
                                 columns=["distance"])
        distances = distances.sort_values(by='distance', ascending=True)
        neighbors = distances[1:num_neighbors].index.tolist()
        edge_list.extend((i, j) for j in neighbors)
        edge_list.extend((j, i) for j in neighbors)
    # Remove duplicates
    edge_list = set(edge_list)
    edge_list = list(edge_list)
    row_index = []
    col_index = []
    row_index.extend(j[0] for j in edge_list)
    col_index.extend(j[1] for j in edge_list)

    sparse_mtx = ss.coo_matrix((np.ones_like(row_index), (row_index, col_index)),
                               shape=(coor_array.shape[0], coor_array.shape[0]))

    return sparse_mtx


def cal_mean_expression(adata, gene_list):
    tmp_adata = adata[:, gene_list].copy()
    if 'log1p' not in adata.uns_keys():
        tmp_adata = sc.pp.log1p(tmp_adata)
    mean_vector = tmp_adata.X.mean(axis=1)
    mean_vector = np.array(mean_vector).ravel()

    return mean_vector


def kneed_select_values(value_list, S=3, increasing=True):
    from kneed import KneeLocator
    x_list = list(range(1, 1 + len(value_list)))
    y_list = value_list.copy()
    if increasing:
        magic = KneeLocator(x=x_list,
                            y=y_list,
                            S=S)
    else:
        y_list = y_list[::-1].copy()
        magic = KneeLocator(x=x_list,
                            y=y_list,
                            direction='decreasing',
                            S=S,
                            curve='convex')
    return magic.elbow

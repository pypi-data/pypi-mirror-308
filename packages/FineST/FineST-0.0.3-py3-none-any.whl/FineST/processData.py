import pandas as pd
import scanpy as sc
import numpy as np
from anndata import AnnData
import time
from scipy.sparse import csr_matrix
from .utils import *
from .inference import *
import pickle

######################################
# 2024.11.12 add for pathway analysis
######################################
def clean_save_adata(adata, filename):
    adata_save = adata.copy()

    # List of keys to remove
    keys_to_remove = ['single_cell', 'mean', 'num_pairs',
                      # 'ligand', 'receptor',  'geneInter'                      
                      'global_I', 'global_stat', 'global_res', 'local_z', 
                      # 'local_stat', 'local_z_p', 
                      'selected_spots']

    for key in keys_to_remove:
        if key in adata_save.uns:
            del adata_save.uns[key]

    # Update problematic elements in adata_save.uns and save them as pickle files
    for key, value in adata_save.uns.items():
        # Save the original value as a pickle file
        with open(f"{key}.pkl", "wb") as f:
            pickle.dump(value, f)

        # Update the value in adata with the filename of the pickle file
        adata_save.uns[key] = f"{key}.pkl"

    # Save adata
    adata_save.write_h5ad(filename)

    return adata_save


def Load_clean_save_adata(adata):
    keys = ["local_z_p", "local_stat", "geneInter", "ligand", "receptor"]
    for key in keys:
        with open(adata.uns[key], "rb") as f:
            adata.uns[key] = pickle.load(f)
    return adata




######################################
# 2024.11.11 add for all spot: Visium
######################################
def get_allspot_coors(input_coord_all):
    
    tensor_1 = input_coord_all[0][0]
    tensor_2 = input_coord_all[0][1]

    input_coord_all_concat = torch.stack((tensor_1, tensor_2))
    spatial_loc = input_coord_all_concat.T.numpy()

    # Find unique rows and their counts
    unique_rows, counts = np.unique(spatial_loc, axis=0, return_counts=True)
    # Check if there are any duplicate rows
    duplicate_rows = (counts > 1).any()
    print("Are there any duplicate rows? :", duplicate_rows)
    return spatial_loc


def adata_LR(adata, file_path):
    LRgene = pd.read_csv(file_path)
    adata_matrix = pd.DataFrame(adata.X.A, index=adata.obs_names, columns=adata.var_names)
    available_genes = [gene for gene in LRgene['LR gene'].tolist() if gene in adata_matrix.columns]
    adataLR_matrix = adata_matrix[available_genes]
    adata._n_vars = adataLR_matrix.shape[1]
    adata.X = adataLR_matrix.values
    adata.var = adata.var.loc[available_genes]
    adata.var_names = adataLR_matrix.columns
    return adata


def adata_preprocess(adata, min_cells=10, target_sum=None, n_top_genes=None): 
    adata.var_names_make_unique()

    adata.var["mt"] = adata.var_names.str.startswith("MT-")
    sc.pp.calculate_qc_metrics(adata, qc_vars=["mt"], inplace=True)
    sc.pp.filter_genes(adata, min_cells=min_cells)
    
    if n_top_genes is not None:
        sc.pp.normalize_total(adata, target_sum=target_sum)
    else:
        sc.pp.normalize_total(adata)
        
    sc.pp.log1p(adata)
    
    if n_top_genes is not None:
        sc.pp.highly_variable_genes(adata, flavor="seurat", n_top_genes=n_top_genes)
        
    return adata


def adata2matrix(adata, gene_hv):
    # Access the matrix and convert it to a dense matrix
    matrix = pd.DataFrame(adata.X)
    matrix.columns = gene_hv
    spotID = np.array(pd.DataFrame(adata.obs['in_tissue']).index)
    matrix.insert(0, '', spotID)   
    matrix = matrix.set_index(matrix.columns[0])
    print(matrix.shape)
    return matrix



###############################################
# 2024.11.02 update 
###############################################
def get_image_coord(file_paths, dataset_class="Visium"):
    data = []
    file_paths.sort() 
    for file_path in file_paths:
        parts = file_path.split('_')
        if dataset_class == "Visium":
            part_3 = int(parts[-2])
            part_4 = int(parts[-1].split('.')[0])
        elif dataset_class == "VisiumHD":
            part_3 = parts[-2]
            part_4 = parts[-1].split('.pth')[0]
        else:
            print("Invalid dataset_class. Please use 'Visium' or 'VisiumHD'")
            return
        data.append([part_3, part_4])
    df = pd.DataFrame(data, columns=['pixel_y', 'pixel_x'])
    return df[['pixel_x', 'pixel_y']]
    

def get_image_coord_all(file_paths, dataset_class="Visium"):
    file_paths.sort()
    data = []
    for file_path in file_paths:
        parts = file_path.split('_')
        if dataset_class == 'Visium':
            data.append([parts[-2], parts[-1].split('.pth')[0]])
    return data


def image_coord_merge(df, position, dataset):
    # Define merge_dfs function within the new function
    def merge_dfs(df, position):
        merged_df = pd.merge(df, position, on=['pixel_x', 'pixel_y'], how='left')
        cols = merged_df.columns.tolist()
        cols.remove('pixel_x')
        cols.remove('pixel_y')
        merged_df = merged_df[cols + ['pixel_x', 'pixel_y']]
        col_x = merged_df.columns[-4]
        col_y = merged_df.columns[-3]
        return merged_df.rename(columns={col_x: 'x', col_y: 'y'})

    # Define merge_dfs_HD function within the new function
    def merge_dfs_HD(df, position):
        position['pxl_col_in_fullres'] = pd.to_numeric(position['pxl_col_in_fullres'], errors='coerce').round(6)
        position['pxl_row_in_fullres'] = pd.to_numeric(position['pxl_row_in_fullres'], errors='coerce').round(6)
        position = position.rename(columns={'pxl_col_in_fullres': 'pixel_x', 'pxl_row_in_fullres': 'pixel_y'})

        df['pixel_x'] = df['pixel_x'].astype('float64').round(6)
        df['pixel_y'] = df['pixel_y'].astype('float64').round(6)

        in_df = position['pixel_x'].isin(df['pixel_x']) & position['pixel_y'].isin(df['pixel_y'])
        merged_df = position[in_df].reset_index(drop=True)
        merged_df = merged_df.rename(columns={'array_row': 'x', 'array_col': 'y'})
        return merged_df

    # Use dataset to decide which function to call
    if dataset == 'Visium':
        return merge_dfs(df, position)
    elif dataset == 'Visium HD':
        return merge_dfs_HD(df, position)
    else:
        raise ValueError(f"Unknown dataset: {dataset}")


def sort_matrix(matrix, position_image, spotID_order, gene_hv):
    # Reset the index of the matrix and rename the first column
    position_image_first_col = position_image.columns[0]
    matrix = matrix.reset_index().rename(columns={matrix.index.name: position_image_first_col})
    
    # Merge position_image and matrix based on the first column
    sorted_matrix = pd.merge(position_image[[position_image_first_col]], matrix, on=position_image_first_col, how="left")
    matrix_order = np.array(sorted_matrix.set_index(position_image_first_col))
    
    # Convert matrix_order to DataFrame and set the index and column names
    matrix_order_df = pd.DataFrame(matrix_order)
    matrix_order_df.index = spotID_order
    matrix_order_df.columns = gene_hv
    
    return matrix_order, matrix_order_df


def update_adata_coord(adata, matrix_order, position_image):
    adata.X = csr_matrix(matrix_order, dtype=np.float32)
    adata.obsm['spatial'] = np.array(position_image.loc[:, ['pixel_y', 'pixel_x']])
    adata.obs['array_row'] = np.array(position_image.loc[:, 'y'])
    adata.obs['array_col'] = np.array(position_image.loc[:, 'x'])
    return adata


def update_st_coord(position_image):
    position_order = pd.DataFrame({
        "pixel_y": position_image.loc[:, 'pixel_y'],
        "pixel_x": position_image.loc[:, 'pixel_x'],
        "array_row": position_image.loc[:, 'y'],
        "array_col": position_image.loc[:, 'x']
    })
    return position_order


def update_adata_coord_HD(matrix_order, spotID_order, gene_hv, position_image):

    sparse_matrix = csr_matrix(matrix_order, dtype=np.float32)

    #################################################
    # construct new adata (reduce 97 coords)
    #################################################
    adata_redu = sc.AnnData(X=sparse_matrix, 
                            obs=pd.DataFrame(index=spotID_order), 
                            var=pd.DataFrame(index=gene_hv))

    adata_redu.X = csr_matrix(matrix_order, dtype=np.float32)
    adata_redu.obsm['spatial'] = np.array(position_image.loc[:, ['pixel_y', 'pixel_x']])
    adata_redu.obs['array_row'] = np.array(position_image.loc[:, 'y'])
    adata_redu.obs['array_col'] = np.array(position_image.loc[:, 'x'])
    return adata_redu


# def prepare_impute_adata(adata, adata_spot, C2, gene_hv):
#     # adata_know: adata (original) 1331 × 596
#     # adata_spot: all subspot 21296 × 596
#     adata_know = adata.copy()
#     adata_know.obs["x"]=adata.obsm['spatial'][:,0]
#     adata_know.obs["y"]=adata.obsm['spatial'][:,1]

#     x_sudo, y_sudo = adata_spot.obs["x"].values, adata_spot.obs["y"].values
#     x_know, y_know = adata_know.obs["x"].values, adata_know.obs["y"].values
#     print("X_sudo & x_know:", x_sudo.shape, x_know.shape)    # X_sudo & x_know: (17424,) (adata.shape[0],)

#     adata_spot.obsm['spatial'] = np.stack([adata_spot.obs["x"], adata_spot.obs["y"]]).T

#     xlist = C2[:, 0].tolist()
#     ylist = C2[:, 1].tolist()
#     sudo = pd.DataFrame({"x": xlist, "y": ylist})  

#     sudo_adata = anndata.AnnData(np.zeros((sudo.shape[0], len(gene_hv))))
#     sudo_adata.obs = sudo
#     sudo_adata.var = adata_know.var
    
#     return adata_know, sudo_adata, adata_spot


# def impute_adata(adata_spot, adata_know, sudo_adata, gene_hv, k=None, w=0.5):

#     start_time = time.time()

#     nearest_points = find_nearest_point(adata_spot.obsm['spatial'], adata_know.obsm['spatial'])    
#     nbs, nbs_indices = find_nearest_neighbors(nearest_points, adata_know.obsm['spatial'], k=k)
#     distances = calculate_euclidean_distances(adata_spot.obsm['spatial'], nbs)

#     # Iterate over each point in sudo_adata
#     for i in range(sudo_adata.shape[0]):
#         dis_tmp = (distances[i] + 0.1) / np.min(distances[i] + 0.1)
#         weight_exponent = 1
#         weights = ((1 / (dis_tmp ** weight_exponent)) / ((1 / (dis_tmp ** weight_exponent)).sum()))
#         sudo_adata.X[i, :] = np.dot(weights, adata_know.X[nbs_indices[i]].todense())
        
#     print("--- %s seconds ---" % (time.time() - start_time))

#     weight_impt_data = w*adata_spot.X + (1-w)*sudo_adata.X
#     data_impt = torch.tensor(weight_impt_data)

#     adata_impt = sc.AnnData(X = pd.DataFrame(weight_impt_data))
#     adata_impt.var_names = gene_hv
#     adata_impt.obs = adata_spot.obs

#     return sudo_adata, adata_impt, data_impt


def impute_adata(adata, adata_spot, C2, gene_hv, k=None, w=0.5):
    ## Prepare impute_adata
    # adata_know: adata (original) 1331 × 596
    # adata_spot: all subspot 21296 × 596

    adata_know = adata.copy()
    adata_know.obs[["x", "y"]] = adata.obsm['spatial']
    adata_spot.obsm['spatial'] = adata_spot.obs[["x", "y"]].values

    sudo = pd.DataFrame(C2, columns=["x", "y"])
    sudo_adata = anndata.AnnData(np.zeros((sudo.shape[0], len(gene_hv))), obs=sudo, var=adata.var)

    ## Impute_adata
    start_time = time.time()

    nearest_points = find_nearest_point(adata_spot.obsm['spatial'], adata_know.obsm['spatial'])
    nbs, nbs_indices = find_nearest_neighbors(nearest_points, adata_know.obsm['spatial'], k=k)
    distances = calculate_euclidean_distances(adata_spot.obsm['spatial'], nbs)

    # Iterate over each point in sudo_adata
    for i in range(sudo_adata.shape[0]):
        dis_tmp = (distances[i] + 0.1) / np.min(distances[i] + 0.1)
        weight_exponent = 1
        weights = ((1 / (dis_tmp ** weight_exponent)) / ((1 / (dis_tmp ** weight_exponent)).sum()))
        sudo_adata.X[i, :] = np.dot(weights, adata_know.X[nbs_indices[i]].todense())

    print("--- %s seconds ---" % (time.time() - start_time))

    # sudo_adata: Imputed data using k neighbours of within spots
    # adata_spot: Inferred super-resolved gene expression data with 16x solution
    # adata_impt: Add inference data `adata_spot` and imputed data ``, with weight `w` and `1-w`
    weight_impt_data = w*adata_spot.X + (1-w)*sudo_adata.X
    data_impt = torch.tensor(weight_impt_data)

    adata_impt = sc.AnnData(X = pd.DataFrame(weight_impt_data))
    adata_impt.var_names = gene_hv
    adata_impt.obs = adata_spot.obs

    return sudo_adata, adata_impt, data_impt
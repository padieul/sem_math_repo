from pathlib import Path 
import pandas as pd
import matplotlib 
import matplotlib.pyplot as plt
import ast
import os


def get_data_small():

    elem_set_th_df = Path("..") / "data_intermediate_multiclass_type_tokens_BOTH" / "formula_data_elementary-set-theory.csv"
    algebra_precalc_df = Path("..") / "data_intermediate_multiclass_type_tokens_BOTH" / "formula_data_algebra-precalculus.csv"
    a_geometry_df = Path("..") / "data_intermediate_multiclass_type_tokens_BOTH" / "formula_data_analytic-geometry.csv"
    elem_func_df = Path("..") / "data_intermediate_multiclass_type_tokens_BOTH" / "formula_data_elementary-functions.csv"
    elem_num_th_df = Path("..") / "data_intermediate_multiclass_type_tokens_BOTH" / "formula_data_elementary-number-theory.csv" 
    euc_geom_df = Path("..") / "data_intermediate_multiclass_type_tokens_BOTH" / "formula_data_euclidean-geometry.csv" 
    trig_df = Path("..") / "data_intermediate_multiclass_type_tokens_BOTH" / "formula_data_trigonometry.csv"

    elem_set_th_df = pd.read_csv(elem_set_th_df)
    algebra_precalc_df = pd.read_csv(algebra_precalc_df)
    a_geometry_df = pd.read_csv(a_geometry_df)
    elem_func_df = pd.read_csv(elem_func_df)
    elem_num_th_df = pd.read_csv(elem_num_th_df)
    euc_geom_df = pd.read_csv(euc_geom_df)
    trig_df = pd.read_csv(trig_df)

    all_dfs = [elem_set_th_df, algebra_precalc_df, a_geometry_df, elem_func_df, elem_num_th_df, euc_geom_df, trig_df]

    return all_dfs



def get_data_large():
    subdir_str = "data_intermediate_multiclass_type_tokens_FORMULA"
    
    elem_set_th_df = Path("..") / subdir_str / "formula_data_formulas_elementary-set-theory.csv"
    algebra_precalc_df = Path("..") / subdir_str / "formula_data_formulas_algebra-precalculus.csv"
    a_geometry_df = Path("..") / subdir_str / "formula_data_formulas_analytic-geometry.csv"
    elem_func_df = Path("..") / subdir_str / "formula_data_formulas_elementary-functions.csv"
    elem_num_th_df = Path("..") / subdir_str / "formula_data_formulas_elementary-number-theory.csv" 
    euc_geom_df = Path("..") / subdir_str / "formula_data_formulas_euclidean-geometry.csv" 
    trig_df = Path("..") / subdir_str / "formula_data_formulas_trigonometry.csv"

    elem_set_th_df = pd.read_csv(elem_set_th_df)
    algebra_precalc_df = pd.read_csv(algebra_precalc_df)
    a_geometry_df = pd.read_csv(a_geometry_df)
    elem_func_df = pd.read_csv(elem_func_df)
    elem_num_th_df = pd.read_csv(elem_num_th_df)
    euc_geom_df = pd.read_csv(euc_geom_df)
    trig_df = pd.read_csv(trig_df)

    all_dfs = [elem_set_th_df, algebra_precalc_df, a_geometry_df, elem_func_df, elem_num_th_df, euc_geom_df, trig_df]

    return all_dfs



def merge_dfs_list(df_list, intended_size_per_c):
    if intended_size_per_c == -1:
        sel_dfs = df_list
    elif intended_size_per_c > 0:
        sel_dfs = [df_list[i].sample(n=intended_size_per_c) for i in range(len(df_list))]
    else:
        print("False value")
    merged_df = pd.concat(sel_dfs, axis=0)
    return merged_df

def get_labels_frequencies(df):
    labels_ids_dict = {}
    labels_count = 0
    labels_frequencies_dict = {}

    def cell_to_label_lists(cell_val):
        nonlocal labels_count
        labels_list = ast.literal_eval(cell_val)
        for elem in labels_list:
            if elem in labels_ids_dict.keys():
                labels_frequencies_dict[elem] += 1
            else:
                labels_frequencies_dict[elem] = 1
                labels_ids_dict[elem] = labels_count
                labels_count += 1

        return labels_list

    df["labels"] = df["tags"].map(cell_to_label_lists)
    return labels_frequencies_dict, labels_ids_dict


def get_top_frequencies(labels_frequencies_dict, num_top_values = 10):
    selected_labels = []
    for k in sorted(labels_frequencies_dict, key=lambda k: labels_frequencies_dict[k], reverse=True)[:num_top_values]:
        selected_labels.append((k,labels_frequencies_dict[k]))
    return selected_labels



def plot_label_frequencies(selected_labels_freq):

    labels = [l for (l,f) in selected_labels_freq] 
    freq = [f for (l,f) in selected_labels_freq]

    fig = plt.figure()
    plt.xticks(rotation=90)
    ax = fig.add_axes([0,0,1,1])

    for label in ax.get_xticklabels():
        label.set_rotation(45)
        label.set_ha('right')
    ax.set_ylabel('number of formulas')
    ax.set_yscale("log")
    ax.bar(labels,freq)
    plt.show()

def plot_input_lengths(df):
    
    counts = df['tokens_len'].value_counts()

    # Create bar chart
    fig, ax = plt.subplots()
    ax.bar(counts.index, counts.values, color="green")
    ax.set_yscale("log")
    ax.set_xlabel('Tokens list lengths')
    ax.set_ylabel('Frequency')
    #ax.set_title("Distribution of Tokens Lengths")
    plt.show()

def preprocess_data(corpus,
                    irrelevant_features=["mtype",]):
    # drop irrelevant columns
    new_df = corpus.copy()
    new_df.drop(irrelevant_features, inplace=True, axis=1)

    # filter strings
    def process_cell(cell_str):
        stripped_f_str = cell_str[1:-1].replace("\\\\", "\\")
        f_list = stripped_f_str.split(",")
        f_list = [token.replace("'", "").replace(" ", "") for token in f_list]
        f_list = ["{" if token == "\\{" else token for token in f_list]
        f_list = ["}" if token == "\\}" else token for token in f_list]
        return f_list

    
    #new_df["type_tokens"] = corpus["type_tokens"].map(process_cell)
    #corpus["type_tokens_len"] = corpus["type_tokens"].apply(lambda x: len(x))
    new_df["tokens"] = corpus["tokens"].map(process_cell)
    new_df["tokens_len"] = new_df["tokens"].apply(lambda x: len(x))
    return new_df



def labels_to_multi_hot(df, selected_labels, labels_ids_dict):

    def cell_to_label_lists(cell_val):
        new_labels_ls = []
        for elem in cell_val:
            if elem in selected_labels:
                new_labels_ls.append(labels_ids_dict[elem])
        if new_labels_ls == []:
            new_labels_ls.append(10000) # 10000 is the "other" label id
        return new_labels_ls

    def label_to_label_str(cell_val):
        new_list = [ids_to_label_str_dict[elem] for elem in cell_val]
        return new_list

    def label_ids_to_one_hot(cell_val):
        new_list = [0 for i in range (40)]
        for label_id in cell_val:
            new_list[ids_to_pos_index_dict[label_id]] = 1
        return new_list

    df["labels"] = df["labels"].map(cell_to_label_lists)
    ids_to_label_str_dict = {}
    ids_to_pos_index_dict = {}
    count = 0
    for label in selected_labels:
        ids_to_label_str_dict[labels_ids_dict[label]] = label
        ids_to_pos_index_dict[labels_ids_dict[label]] = count 
        count += 1

    df["labels_str"] = df["labels"].map(label_to_label_str)
    df["labels"] = df["labels"].map(label_ids_to_one_hot)
    
    return df, ids_to_pos_index_dict


def types_to_one_hot(df):

    def mtype_to_vec(cell_val):
        
        if cell_val == "SET":
            return [1,0,0]
        elif cell_val == "SCAL":
            return [0,1,0]
        elif cell_val == "FUNC":
            return [0,0,1]
        else:
            return [0,0,0]


    df["mtype_one_hot"] = df["mtype"].map(mtype_to_vec)
    return df
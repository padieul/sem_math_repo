from mse_db import MSE_DBS # provides an interface for interaction with a local MongoDB instance
import funcs               # provides data processing functions

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

from sem_math import FormulaType, SemMathTokenizer
from mse_db import MSE_DBS 
from pathlib import Path

from wrapt_timeout_decorator import * # use with care on win systems


import pandas as pd

from tqdm import tqdm


# Chapter 1 and 2
# -----------------------------------------------------------------------------------------

def get_sel_ds_size(sel_coll_names, data):
    sel_data_size = 0
    for coll in sel_coll_names:
        coll_size = data.apply_once(coll, funcs.count_all_post_threads_once)
        posts_len, posts_av = data.apply_once(coll, funcs.count_av_all_posts_once)  
        print("\"{}\": {} post-threads, number of posts: {} , average: {:.2f}".format(coll,coll_size, posts_len, posts_av))
        sel_data_size += coll_size
    return sel_data_size


def get_sel_formulas_counts(sel_coll_names, data):
    sel_formulas_total = 0
    formula_counts_list = []
    for coll in sel_coll_names:
        num_formulas = data.apply_once(coll, funcs.count_all_formulas_once)
        av_formulas = data.apply_once(coll, funcs.formulas_av_once)  
        formula_counts_list.append(num_formulas)
        print("\"{}\": {} formulas , average: {:.2f} ".format(coll,num_formulas, av_formulas))
        sel_formulas_total += num_formulas
    return sel_formulas_total




# Chapter 3
# -----------------------------------------------------------------------------------------
def reformat_coll_names_to_labels(sel_coll_names):
    
    sel_coll_labels = [elem.replace("-", "-\n") for elem in sel_coll_names]
    return sel_coll_labels


def plot_types(labels, val_lists, types, title_str):

    fig = plt.figure(figsize=(10,5))
    ax = fig.add_subplot(111)
    width = 0.5 

    sums = [0 for i in range(len(val_lists[0]))]
    for i in range(len(val_lists)):
        if not i == 0:
            sums = [ v1 + v2 for v1, v2 in zip(sums, val_lists[i-1])]
        ax.bar(labels, val_lists[i], width, label=types[i], bottom=sums)
   
    y_formatter = ScalarFormatter(useOffset=False)
    y_formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(y_formatter)
    ax.set_ylabel('Number of formulas')
    ax.set_title(title_str)
    ax.legend()
    plt.show()


def get_extracted_types_count(m_type_labels, sel_coll_names, data):
    vals_list = []
    for t_label in m_type_labels:
        t_all_counts_list = []
        for coll in sel_coll_names:
            type_count_dict = data.apply_once(coll, funcs.count_m_type_occurences_once, {"m_type": t_label})
            type_count_total = type_count_dict["TypeBothCount"] + \
                            type_count_dict["TypeContextCount"] + \
                            type_count_dict["TypeContextR2Count"] + \
                            type_count_dict["TypeFormulaCount"]
            t_all_counts_list.append(type_count_total)
        vals_list.append(t_all_counts_list)
    return vals_list


def get_determining_f_data(data, type_str, sel_coll_names, categories):
    vals_list = [[] for cat in categories]
    for coll in sel_coll_names:
        coll = coll.replace("\n", "")
        type_count_dict = data.apply_once(coll, funcs.count_m_type_occurences_once, {"m_type": type_str})
        vals_list[0].append(type_count_dict["TypeFormulaCount"])
        vals_list[1].append(type_count_dict["TypeContextCount"])
        vals_list[2].append(type_count_dict["TypeContextR2Count"])
        vals_list[3].append(type_count_dict["TypeBothCount"])
    return vals_list


def plot_subplot(fig, subplot_counter, val_lists, title_str, types, labels):
    ax = fig.add_subplot(subplot_counter)
    width = 0.5 

    sums = [0 for i in range(len(val_lists[0]))]
    for i in range(len(val_lists)):
        if not i == 0:
            sums = [ v1 + v2 for v1, v2 in zip(sums, val_lists[i-1])]
        ax.bar(labels, val_lists[i], width, label=types[i], bottom=sums)
   
    y_formatter = ScalarFormatter(useOffset=False)
    y_formatter.set_scientific(False)
    ax.yaxis.set_major_formatter(y_formatter)
    ax.set_ylabel('Number of formulas')
    ax.set_title(title_str)
    ax.legend()


def plot_determining_factors(data, m_type_labels, sel_coll_names, categories, figure_size):

    type_num = len(m_type_labels)
    subplot_counter = 100 * type_num + 10

    fig = plt.figure(figsize=figure_size)
    for m_type_str in m_type_labels:
        subplot_counter += 1
        title_str = "Determining factors in choosing " +  m_type_str + " as the formula type"
        vals_list = get_determining_f_data(data, m_type_str, sel_coll_names, categories)
        plot_subplot(fig, subplot_counter, vals_list, title_str, categories, sel_coll_names)

    plt.subplots_adjust()
    plt.show()


def get_determining_f_counts_both(data, m_type_labels, sel_coll_names):

    vals_list = []
    for t_label in m_type_labels:
        t_all_counts_list = []
        for coll in sel_coll_names:
            type_count_dict = data.apply_once(coll, funcs.count_m_type_occurences_once, {"m_type": t_label})
            type_count_total = type_count_dict["TypeBothCount"] 
            t_all_counts_list.append(type_count_total)
        vals_list.append(t_all_counts_list)
    return vals_list


def get_determining_f_data_both(data, m_type_labels, sel_coll_names):

    vals_list = []
    for t_label in m_type_labels:
        t_all_counts_list = []
        for coll in sel_coll_names:
            type_count_dict = data.apply_once(coll, funcs.count_m_type_occurences_once, {"m_type": t_label})
            type_count_total = type_count_dict["TypeBothCount"] 
            t_all_counts_list.append(type_count_total)
        vals_list.append(t_all_counts_list)
    return vals_list

def print_examples_both(data, sel_coll_names, count_per_coll):
    
    for coll in sel_coll_names:
        coll_exs = data.apply_once(coll, funcs.get_m_types_both_once, {"limit_count": count_per_coll})
        for ex in coll_exs:
            print("TYPE: {}, EXPR: {}, DESCRIPTIVE MENTION: {}".format(ex["m_type"], ex["lx_str"], ex["f_descriptor"]))


# Chapter 4
# -----------------------------------------------------------------------------------------

def get_tokens(form_str):
    r_val = None
    parsed_structure = FormulaType(form_str).determine_formula_type()
    if parsed_structure == None:
        r_val = "COULD NOT PARSE"
    try:
        sem_tok_no_subtypes = SemMathTokenizer(parsed_structure, True)
        r_val = sem_tok_no_subtypes.get_tokens()
        #r_val = TokenizeTransformer().transform(parsed_structure)
    except:
        r_val = "COULD NOT TRANSFORM"

    return r_val

def get_type_tokens(form_str):
    r_val = None
    parsed_structure = FormulaType(form_str).determine_formula_type()
    if parsed_structure == None:
        r_val = "COULD NOT PARSE"
    try:
        sem_tok_with_subtypes = SemMathTokenizer(parsed_structure, False)
        r_val = sem_tok_with_subtypes.get_tokens()
        #r_val = TokenizeTransformer().transform(parsed_structure)
    except:
        r_val = "COULD NOT TRANSFORM"

    return r_val

def retrieve_examples_both(datab, sel_coll_names, count_per_coll):
    
    count = 1
    for coll in sel_coll_names:
        print(coll + ": " + str(len(sel_coll_names)-count)+ " collections left")
        coll_exs = datab.apply_once(coll, funcs.retrieve_m_types_both_once, {"limit_count": count_per_coll})
        ####
        #data = [[ex["f_id"], ex["m_type"], ex["lx_str"], ex["f_descriptor"], get_tokens(ex["lx_str"]), ex["tags"]] for ex in coll_exs]
        data = []
        for ex in coll_exs:
            if "tags" in ex.keys():
                data.append([ex["f_id"], ex["m_type"], ex["lx_str"], ex["f_descriptor"], get_tokens(ex["lx_str"]), get_type_tokens(ex["lx_str"]), ex["tags"]])
        ###
        columns_str = ["fid", "mtype", "exprstr", "mention", "tokens", "type_tokens", "tags"]
        #get_tokens(ex["lx_str"]), ex["tags"])
        df = pd.DataFrame(data, columns=columns_str)
        df.to_csv("print_outs/formula_data_" + str(coll) + ".csv", index=False, header=True)
        count += 1
        #for ex in coll_exs:
            #print("ID: {}, TYPE: {}, EXPR: {}, DESCRIPTIVE MENTION: {}, TOKENS: {}, TAGS: {}".format(ex["f_id"], ex["m_type"], ex["lx_str"], ex["f_descriptor"], get_tokens(ex["lx_str"]), ex["tags"]))

def retrieve_examples_unk(datab, sel_coll_names, count_per_coll):
    
    count = 1
    for coll in sel_coll_names:
        print(coll + ": " + str(len(sel_coll_names)-count)+ " collections left")
        coll_exs = datab.apply_once(coll, funcs.retrieve_m_types_unk_long, {"limit_count": count_per_coll})
        ####
        #data = [[ex["f_id"], ex["m_type"], ex["lx_str"], ex["f_descriptor"], get_tokens(ex["lx_str"]), ex["tags"]] for ex in coll_exs]
        data = []
        for ex in coll_exs:
            if "tags" in ex.keys():
                data.append([ex["f_id"], ex["m_type"], ex["lx_str"], ex["f_descriptor"], ex["tags"]])
        ###
        columns_str = ["fid", "mtype", "exprstr", "mention", "tags"]
        #get_tokens(ex["lx_str"]), ex["tags"])
        df = pd.DataFrame(data, columns=columns_str)
        df.to_csv("print_outs/formula_data_unk_" + str(coll) + ".csv", index=False, header=True)
        count += 1
        #for ex in coll_exs:
            #print("ID: {}, TYPE: {}, EXPR: {}, DESCRIPTIVE MENTION: {}, TOKENS: {}, TAGS: {}".format(ex["f_id"], ex["m_type"], ex["lx_str"], ex["f_descriptor"], get_tokens(ex["lx_str"]), ex["tags"]))


def retrieve_examples_and_write_to_file(datab, sel_coll_names,l_th_10_size, sh_th_10_size):
    """
    @timeout(2)
    def execute(ex):
        return [ex["f_id"], ex["m_type"], ex["lx_str"], ex["f_descriptor"], get_tokens(ex["lx_str"]), get_type_tokens(ex["lx_str"]), ex["tags"]]
    """

    count = 0
    for coll in sel_coll_names:
        print(coll + ": " + str(len(sel_coll_names)-count)+ " collections left")
        coll_exs = datab.apply_once(coll, funcs.retrieve_m_types_formula_selectively, {"l_th_10_max_size": l_th_10_size,
                                                                                       "sh_th_10_max_size": sh_th_10_size})
        data = []
        # get tags 
        for ex in tqdm(coll_exs):
            if not "tags" in ex.keys():
                post_thread_id = ex["f_id"].split("_")[0]
                ex["tags"] = datab.apply_once(coll, funcs.retrieve_tag, {"post_th_id": post_thread_id})
                count = datab.apply_once(coll, funcs.add_tags, {"f_id": ex["f_id"], \
                                                                "tags": ex["tags"]})
            data.append([ex["f_id"], ex["m_type"], ex["lx_str"], ex["f_descriptor"], ex["tags"]])
        
        
        columns_str = ["fid", "mtype", "exprstr", "mention", "tags"]
        df = pd.DataFrame(data, columns=columns_str)
        df.to_csv("print_outs/untokenized_formula_data_formulas_" + str(coll) + ".csv", index=False, header=True)
       
    return 1


def tokenize_examples_from_file(coll_names, file_names):

    max_num_token_size = 30
    
    def check_for_long_tokens(arg):
        arg_str = arg
        if len(arg) > max_num_token_size:
            arg_str = arg.replace(".", "")
            if arg_str.isnumeric():
                arg_str = round(float(arg_str), 5)
        return arg_str
 
    @timeout(2)
    def exec_tokenization(arg):
        return get_tokens(arg)

    @timeout(2)
    def exec_type_tokenization(arg):
        return get_type_tokens(arg)

    def cell_to_tokens(arg):
        arg = check_for_long_tokens(arg)
        return_val = []
        try:
            return_val = exec_tokenization(arg)
        except Exception as e:
            ...
        return return_val


    def cell_to_type_tokens(arg):
        arg = check_for_long_tokens(arg)
        return_val = []
        try:
            return_val = exec_type_tokenization(arg)
        except Exception as e:
            ...
        return return_val

    coll_count = 0
    for filename in tqdm(file_names):
        coll_df = pd.read_csv(filename, lineterminator='\n', on_bad_lines="skip")
        print(coll_df.shape)
        coll_df["tokens"] = coll_df["exprstr"].map(cell_to_tokens)
        coll_df["type_tokens"] = coll_df["exprstr"].map(cell_to_type_tokens)
        coll_df.to_csv("print_outs/formula_data_formulas_" + str(coll_names[coll_count]) + ".csv", index=False, header=True)
        coll_count += 1

        #columns_str = ["fid", "mtype", "exprstr", "mention", "tokens", "type_tokens", "tags"]


#----------------------------------------------------------------------------------------------------------

"""
def add_tags_column_in_formulas(data, sel_coll_names, coll_sizes):

    count = 1
    for coll in sel_coll_names:
        print(coll + ": " + str(len(sel_coll_names)-1)+ " collections left")
        #migrated_count = data.apply_to_each(coll, funcs.migrate_tags_to_formulas, -1)
        migrated_count = data.apply_to_each_multi(coll, 16, funcs.migrate_tags_to_formulas, (coll_sizes[coll] + 1))
        count += 1
    return migrated_count


def add_tags_column_in_formulas_all(data, sel_coll_names): 
    count = 1
    migrated_total = 0
    for coll in sel_coll_names:
        print(coll + ": " + str(len(sel_coll_names)-1)+ " collections left")

        # for
        formula_id_tag_dict = data.apply_once(coll, funcs.migrate_tags_to_formulas_all, {})



        migrated_total += len(formula_id_tag_dict.keys())
        count += 1
    return migrated_total
"""


if __name__ == "__main__":

    log_file_path = Path(".") / "conf" / "log.txt"              # processing log
    db_settings_file_path = Path(".") / "conf" / "db_conf.json" # settings file for the db connection (local)
    data = MSE_DBS("linux", db_settings_file_path, log_file_path)
    
    ### Uncomment the following block to add tags to formulas
    ### (only formulas with "both" selection method are considered)
    """"
    sel_coll_names = ["algebra-precalculus", "analytic-geometry", "elementary-functions", \
                      "elementary-number-theory", "elementary-set-theory", "euclidean-geometry", \
                      "trigonometry"]

    coll_sizes = {"algebra-precalculus": 43604, 
                  "analytic-geometry": 5934,
                  "elementary-functions": 515, 
                  "elementary-number-theory": 34454,
                  "elementary-set-theory": 26535,
                  "euclidean-geometry": 8188,
                  "trigonometry": 27356}

    
    add_tags_column_in_formulas(data, sel_coll_names, coll_sizes) 
    """


    ### Uncomment the following block to retrieve all equations that do not yet have a 
    ### a semantic type
    """
    sel_coll_names = ["analytic-geometry", "elementary-functions", \
                      "elementary-number-theory", "elementary-set-theory", "euclidean-geometry", \
                      "trigonometry", "algebra-precalculus"]
    

    retrieve_examples_unk(data, sel_coll_names, count_per_coll=500)
    """

    ### Uncomment the following block to add tags to formulas (STEP 1)
    """
    sel_coll_names = ["algebra-precalculus", "analytic-geometry", "elementary-functions", \
                      "elementary-number-theory", "elementary-set-theory", "euclidean-geometry", \
                      "trigonometry"]

    coll_sizes = {"algebra-precalculus": 43604, 
                  "analytic-geometry": 5934,
                  "elementary-functions": 515, 
                  "elementary-number-theory": 34454,
                  "elementary-set-theory": 26535,
                  "euclidean-geometry": 8188,
                  "trigonometry": 27356}

    longer_than_ten_max_size = 10000
    shorter_than_ten_max_size = 10000
    num_migrated = retrieve_examples_and_write_to_file(data, sel_coll_names, longer_than_ten_max_size, \
                                                                             shorter_than_ten_max_size) 
    print("Done")
    """

    ### Uncomment the following block to get data from intermediate untokenized files and
    ### add tokenization (STEP 2)
    """
    sel_coll_names = ["algebra-precalculus", "analytic-geometry", "elementary-functions", \
                      "elementary-number-theory", "elementary-set-theory", "euclidean-geometry", \
                      "trigonometry"]
    """
    """
    sel_coll_names = ["elementary-set-theory", "euclidean-geometry", \
                      "trigonometry"]
    """
    sel_coll_names = ["trigonometry"]

    path_suffix = Path("print_outs") / ""

    sel_file_names = []
    for coll_name in sel_coll_names:
        file_name = path_suffix / ("untokenized_formula_data_formulas_" + coll_name + ".csv")
        sel_file_names.append(file_name)

    tokenize_examples_from_file(sel_coll_names, sel_file_names)


    
    
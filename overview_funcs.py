from mse_db import MSE_DBS # provides an interface for interaction with a local MongoDB instance
import funcs               # provides data processing functions

import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

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
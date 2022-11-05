from mse_db import MSE_DBS # provides an interface for interaction with a local MongoDB instance
import funcs               # provides data processing functions
from sem_math import PostThread, \
                     FormulaContextType, \
                     FormulaType, \
                     Comparer
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


def reformat_coll_names_to_labels(sel_coll_names):
    
    sel_coll_labels = [elem.replace("-", "-\n") for elem in sel_coll_names]
    return sel_coll_labels

# Chapter 3
# -----------------------------------------------------------------------------------------

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
    ax.set_ylabel('Absolute numbers')
    ax.set_title(title_str)
    ax.legend()
    plt.show()












# Chapter 4
# -----------------------------------------------------------------------------------------
from mse_db import MSE_DBS
from sem_math import PostThread, FormulaContextType, FormulaType, Comparer
import funcs

"""
    for i in range(len(sel_coll_names)):
        data.apply_to_each_multi(sel_coll_names[i], 4, funcs.migrate_formulas, coll_sizes[i])
"""
"""
    total_len, av = data.apply_once("elementary-functions", funcs.count_av_all_posts_once)      # counts all documents in threads collection -> ENTIRE DATASET
    print("There is a total of {} posts with an average of {:.2f} posts per post-thread".format(total_len, av))
"""
"""
    set_both_count, set_formula_count, set_context_count, set_context_r2_count = data.apply_once("elementary-functions", funcs.count_math_type_occurences)
    print(set_both_count)
    print(set_formula_count)
    print(set_context_count)
    print(set_context_r2_count)
"""



if __name__ == "__main__":

    log_file_name = "conf\\analyzer_log.txt"                          # processing log
    db_settings_file_name = "conf\db_conf.json"                       # settings file

    sel_coll_names = ["algebra-precalculus", "analytic-geometry", "elementary-functions", "elementary-number-theory", \
                      "elementary-set-theory", "euclidean-geometry", "trigonometry"]
    data = MSE_DBS(db_settings_file_name, log_file_name) 
    coll_sizes = [43604, 5934, 515, 34454, 26535, 8188, 27356]

    type_data = {"m_type": "SET"} 
    for coll in sel_coll_names:
        count_dict = data.apply_once(coll, funcs.count_m_type_occurences_once, type_data)
        print(count_dict)

    
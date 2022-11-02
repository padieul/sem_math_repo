from mse_db import MSE_DBS
from sem_math import PostThread, FormulaContextType, FormulaType, Comparer
import funcs




if __name__ == "__main__":

    log_file_name = "conf\\analyzer_log.txt"                          # processing log
    db_settings_file_name = "conf\db_conf.json"             # settings file

    data = MSE_DBS(db_settings_file_name, log_file_name) 
    total_len, av = data.apply_once("elementary-functions", funcs.count_av_all_posts_once)      # counts all documents in threads collection -> ENTIRE DATASET
    print("There is a total of {} posts with an average of {:.2f} posts per post-thread".format(total_len, av))
    
from mse_analyzer import MSE_Analyzer

SEL_TAGS = ["algebra-precalculus", \
            "elementary-functions", \
            "elementary-set-theory", \
            "elementary-number-theory", \
            "euclidean-geometry", \
            "analytic-geometry", \
            "trigonometry"]

def cat_func(db, cl, single_post_thread):
    
    count = 0

    tags = single_post_thread["posts"][0]["@Tags"]
    tags_list = tags.split("><")
    tags_list[0].replace("<","")
    tags_list[-1].replace(">","") 

    for tag in tags_list:
        if tag in SEL_TAGS:
            count = 0
            try:
                new_id = db[tag].insert_one(single_post_thread).inserted_id
                count = 1
            except:
                continue

    return count


def create_collections_func(db, cl):
    
    new_cols = []
    for tagname in SEL_TAGS:
        new_cols.append(db[tagname])


if __name__ == "__main__":
    
    log_file_name = "conf\copy_log.txt"                     # processing log
    db_settings_file_name = "conf\db_conf.json"             # settings file

    an1 = MSE_Analyzer(db_settings_file_name, log_file_name) 
    an1.apply_once("threads", create_collections_func)
    an1.apply_to_each("threads", cat_func)
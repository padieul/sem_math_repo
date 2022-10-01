from mse import MSE_DBS, MSE_Thread
import spacy

# extracts the tags from each initial post in a thread 
# and adds them to the thread as a list of strings
def get_tags_func(db, cl, coll_name, single_post_thread):

    count = 0
    _id = single_post_thread["_id"]
    tags = single_post_thread["posts"][0]["@Tags"]
    tags_list = tags.split("><")
    tags_list_new = [t.replace(" ", "").replace("<", "").replace(">", "") for t in tags_list]

    try:
        db[coll_name].update_one({"_id": _id}, {"$set": {"tags": tags_list_new}})
        count = 1
    except:
        ...
    
    return count


# copies threads that correspond to particular tags 
# to separate tag-specifics collections 
def cat_func(db, cl, coll_name, single_post_thread):

    SEL_TAGS = ["algebra-precalculus", \
            "elementary-functions", \
            "elementary-set-theory", \
            "elementary-number-theory", \
            "euclidean-geometry", \
            "analytic-geometry", \
            "trigonometry"]
    
    count = 0
    tags_list = single_post_thread["tags"]
    
    for tag in tags_list:
        if tag in SEL_TAGS:
            count = 0
            try:
                new_id = db[tag].insert_one(single_post_thread).inserted_id
                count = 1
            except:
                continue

    return count

# extract mathematical expressions (formulas) for 
# each post thread in a collection
def extract_formulas_func(db, cl, coll_name, single_post_thread):

    count = 0 
    _id = single_post_thread["_id"]
    mse_th_obj = MSE_Thread(single_post_thread) 
    formulas = mse_th_obj.get_formulas()
    formulas_count = len(formulas_count)
    tokenized_thread = mse_th_obj.get_tokenized_text() 

    try:
        db[coll_name].update_one({"_id": _id}, {"$set": {"formulas": formulas, 
                                                         "formulas_count": formulas_count, 
                                                         "tokenized_posts": tokenized_thread}})
        
        count = 1
    except:
        ...

    return count
    


if __name__ == "__main__":
    
    log_file_name = "conf\copy_log.txt"                     # processing log
    db_settings_file_name = "conf\db_conf.json"             # settings file

    data = MSE_DBS(db_settings_file_name, log_file_name) 
    #an1.apply_to_each("threads", get_tags_func)
    #nlp = spacy.load("en_core_web_sm")
    data.apply_to_each("elementary-set-theory", extract_formulas_func)
    
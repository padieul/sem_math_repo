from mse import MSE_DBS, MSE_Thread
import spacy
import re

TOTAL_COUNT = 0

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
# usage: data.apply_to_each("elementary-set-theory", extract_formulas_func)
def extract_formulas_func(db, cl, coll_name, single_post_thread):

    count = 0 
    _id = single_post_thread["_id"]
    mse_th_obj = MSE_Thread(single_post_thread) 
    formulas = mse_th_obj.get_formulas()
    formulas_count = len(formulas)
    tokenized_thread = mse_th_obj.get_tokenized_text() 

    try:
        db[coll_name].update_one({"_id": _id}, {"$set": {"formulas": formulas, 
                                                         "formulas_count": formulas_count, 
                                                         "tokenized_posts": tokenized_thread}})
        
        count = 1
    except:
        ...
    return count
    
# 
# 
## data.apply_to_each("elementary-set-theory", add_align_formulas_func)
def add_align_formulas_func(db, cl, coll_name, single_post_thread):
    
    count = 0 

    formulas_list = single_post_thread["formulas"]
    posts_list = [p["@Body"] for p in single_post_thread["posts"]] 

    try:

        count = 1
    except:
        ... 
    return count

## count occurence of the substring {begin}align ... {end}align
def count_aligns_func(db, cl, coll_name, single_post_thread):

    if str(single_post_thread["_id"]) == "6327106206a69a3f488d74f8":
        print("it")
    align_str = "begin{align}"
    posts_list = [p["@Body"] for p in single_post_thread["posts"]] 
    count = 0

    for post in posts_list:
        if align_str in post:
            count += 1

    return count

# something 
#
def extract_title_formulas(db, cl, coll_name, single_post_thread):

    count = 0 
    _id = single_post_thread["_id"]
    mse_th_obj = MSE_Thread(single_post_thread) 

    title_str = mse_th_obj.get_title_str()
    title_formulas = mse_th_obj.get_title_formulas()
    title_formulas_count = len(title_formulas)
    tokenized_title = mse_th_obj.get_tokenized_title() 

    title_dict = {}
    title_dict["title_str"] = title_str 
    title_dict["title_formulas_count"] = title_formulas_count 
    title_dict["title_formulas"] = title_formulas 
    title_dict["title_tokenized"] = tokenized_title

    
    try:
        db[coll_name].update_one({"_id": _id}, {"$set": {"title": title_dict}})
        count = 1
    except:
        ...
    
    
    return count


if __name__ == "__main__":
    
    print(TOTAL_COUNT)
    log_file_name = "conf\copy_log.txt"                     # processing log
    db_settings_file_name = "conf\db_conf.json"             # settings file

    data = MSE_DBS(db_settings_file_name, log_file_name) 
    #data.apply_to_each("elementary-set-theory", add_align_formulas_func)
    data.apply_to_each("elementary-set-theory", extract_title_formulas)
    print(data.get_count())
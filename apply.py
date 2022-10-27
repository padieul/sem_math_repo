from mse_db import MSE_DBS
from sem_math import PostThread, FormulaContextType, FormulaType, Comparer
import spacy
import re

import latex2mathml.converter


### CATEGORIZATION FUNCTIONS
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
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


### FORMULA EXTRACTION FUNCTIONS 
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# extract mathematical expressions (formulas) for 
# each post thread in a collection
# usage: data.apply_to_each("elementary-set-theory", extract_formulas_func)
def extract_formulas_func(db, cl, coll_name, single_post_thread):

    count = 0 
    _id = single_post_thread["_id"]
    mse_th_obj = PostThread(single_post_thread) 
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

## extract formulas from occurences of the substring {begin}align ... {end}align
def extract_aligns_func(db, cl, coll_name, single_post_thread):

    if str(single_post_thread["_id"]) == "6327106206a69a3f488d74f8":
        print("it")
    
    align_str = "begin{align}"
    posts_list = [p["@Body"] for p in single_post_thread["posts"]] 
    count = 0

    for post in posts_list:
        if align_str in post:
            print(single_post_thread["_id"])
            _id = single_post_thread["_id"]
            mse_th_obj = PostThread(single_post_thread) 
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

### TITLE RELATED FUNCTIONS 
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
# extracts formulas from post thread titels
# usage: data.apply_to_each("elementary-set-theory", extract_title_formulas)
def extract_title_formulas(db, cl, coll_name, single_post_thread):

    count = 0 
    _id = single_post_thread["_id"]
    mse_th_obj = PostThread(single_post_thread) 

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

# prints out extracted titles with parses, formulas and tokenization
# usage: data.apply_to_each("elementary-set-theory", print_out_titles)
def print_out_titles_context(db, cl, coll_name, single_post_thread):

    if single_post_thread["title"]["title_formulas_count"] > 0:

        title = single_post_thread["title"]["title_str"]
        title_tokenized = single_post_thread["title"]["title_tokenized"]
        title_formulas = single_post_thread["title"]["title_formulas"]
        title_formula_tokens = title_formulas.keys()

        new_title_tokenized = []
        title_tok_str = ""
        for token, dep in title_tokenized.items():
            title_tok_str += (token + " ")
        nlp = spacy.load("en_core_web_sm")
        doc = nlp(title_tok_str)

        count = 0
        for token in doc:
            if token.text in title_formula_tokens:
                i = 1
                while not i == 3:
                    #token_1 = doc[count - (i+1)].text 
                    #token_2 = doc[count - (i+2)].text 
                    #print(token_1)
                    #print(token_2)
                    prev_token = doc[count-i]
                    #print("prev token: " + str(prev_token.text) + " : "+ str(prev_token.pos_))
                    if not prev_token.pos_ == "SPACE":
                        if prev_token.pos_ == "NOUN" and not prev_token.text in title_formula_tokens:

                            print("----------------------------------------------------------------------------------------------------")
                            print(title)
                            print("formula: " + str(title_formulas[doc[count].text]))
                            latex_input = str(title_formulas[doc[count].text])
                            mathml_output = latex2mathml.converter.convert(latex_input)
                            print(mathml_output)
                            print("\t" + "prev_token: " + prev_token.text + ": " + str(prev_token.pos_))

                            print("token count: ", len(title_tokenized)) 
                            print("new token count: ", len(new_title_tokenized))

                            print(title_tokenized)
                            print(new_title_tokenized)
                            break
                    i += 1

                #print("\t" + doc[count-1].text + ": " + str(doc[count-1].pos_))
                #print("\t" + doc[count-2].text + ": " + str(doc[count-2].pos_))
            count += 1

    return 1


# prints out extracted text bodys with parses, formulas and tokenization
# usage: data.apply_to_each("elementary-set-theory", print_out_titles)
def print_out_posts_types(db, cl, coll_name, single_post_thread):
    total_formula_count = single_post_thread["formulas_count"]
    met_criteria_formula_count = 0
    if total_formula_count > 0:

        tokenized_posts = single_post_thread["tokenized_posts"]
        formulas_dict = single_post_thread["formulas"]
        formulas_dict_tokens = single_post_thread["formulas"].keys()
        #print("POST_THREAD #", single_post_thread["_id"])
        print("total_formula_count: ", total_formula_count)
        for post in tokenized_posts:

            count = 0
            for token in post:
                if token in formulas_dict_tokens:
                    #print("POST_THREAD #", single_post_thread["_id"])
                    print("*********************************************************************")
                    #print("")
                    if token == "0,q_1,-q_1,q_2,-q_2,q_3,-q_3,\ldots":
                        print(token)
                        print("doing")

                    token_list = []
                    formula_token = token
                    try:
                        for i in range(count-6, count+6, 1):
                            if i < 0 or i > (len(post) - 1):
                                continue
                            token_list.append(post[i]) 
                    except Exception as e:
                        print(e)

                    # type is determined by the textual context surrounding a formula string
                    formula_c_type = FormulaContextType("kb/type_context_keywords.json", token_list, formula_token, formulas_dict, 3)
                    #formula_c_type.determine_formula_type(conditions = {"has_pos": ("NOUN", "left"), "has_pos_between": ("PREP", "NOUN"), "type_keyword_pos": "NOUN"})
                    matching_rules = [ {"descriptor_pos": ("NOUN", "left"), "formula_dep": "not pobj"},  ### RULE 1
                                       {"descriptor_dep": "attr", "formula_dep": "nsubj"} ]              ### RULE 2
                    formula_c_type.find_type_descriptors(matching_rules)
                    formula_c_type.determine_formula_type(priority = 1)  # 0 - rule1, 1 - rule2


                    # type is determined by formula parser
                    formula_type = FormulaType(formulas_dict[formula_token], formula_token, formulas_dict)
                    formula_type.determine_formula_type()

                    # comparer object acts as arbitrator between formula_type and formula_c_type 
                    comp = Comparer(formula_c_type, formula_type)
                    final_type, textual_descr, decision_str = comp.decide_type("formula")
                    #print("---")
                    comp.print_out(final_type, textual_descr, decision_str)
                    #print(final_type)
                    if not final_type == "UNK":
                        met_criteria_formula_count += 1
                    
                count += 1

        try:
            ...
        except:
            ...


        print("met_criteria_formula_count: ", str(met_criteria_formula_count))
        print("TOTAL FORMULA COUNT: ", str(total_formula_count))
    return met_criteria_formula_count


### Type extraction from formulas and contexts
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------



#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------

### Statistics
#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------
def count_all_formulas(db, cl, coll_name, single_post_thread):
    formulas_count = single_post_thread["formulas_count"]
    return formulas_count


#--------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------------------------------------------------------------------------



if __name__ == "__main__":
    
    log_file_name = "conf\copy_log.txt"                     # processing log
    db_settings_file_name = "conf\db_conf.json"             # settings file

    data = MSE_DBS(db_settings_file_name, log_file_name) 
    """
    data.apply_to_each("elementary-set-theory", print_out_posts_types, limit = 100)
    print("TOTAL ---- MET CONDITIONS FORMULA_COUNT: ", str(data.get_count()))
    data.reset_count()
    data.apply_to_each("elementary-set-theory", count_all_formulas, limit = 100)
    print("TOTAL ---- ALL FORMULAS: ", str(data.get_count()))
    """
    #data.apply_to_each_multi("elementary-set-theory", 10, print_out_posts_types, limit = 3)

    data.apply_to_each_multi("elementary-set-theory", 8, print_out_posts_types, limit = 100)
    print("TOTAL ---- MET CONDITIONS FORMULA_COUNT: ", str(data.get_count()))
    #data.reset_count()
    #data.apply_to_each("elementary-set-theory", count_all_formulas, limit = 100)
    #print("TOTAL ---- ALL FORMULAS: ", str(data.get_count()))
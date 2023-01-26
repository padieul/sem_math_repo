from sem_math import PostThread, FormulaContextType, FormulaType, Comparer
import spacy


# CATEGORIZATION FUNCTIONS
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
# extracts the tags from each initial post in a thread
# and adds them to the thread as a list of strings
def get_tags_func(db, cl, coll_name, single_post_thread):

    count = 0
    _id = single_post_thread["_id"]
    tags = single_post_thread["posts"][0]["@Tags"]
    tags_list = tags.split("><")
    tags_list_new = [t.replace(" ", "").replace(
        "<", "").replace(">", "") for t in tags_list]

    try:
        db[coll_name].update_one(
            {"_id": _id}, {"$set": {"tags": tags_list_new}})
        count = 1
    except:
        ...

    return count


# copies threads that correspond to particular tags
# to separate tag-specifics collections
def cat_func(db, cl, coll_name, single_post_thread):

    SEL_TAGS = ["algebra-precalculus",
                "elementary-functions",
                "elementary-set-theory",
                "elementary-number-theory",
                "euclidean-geometry",
                "analytic-geometry",
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


# FORMULA EXTRACTION FUNCTIONS
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
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

# count occurence of the substring {begin}align ... {end}align


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

# extract formulas from occurences of the substring {begin}align ... {end}align


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


def migrate_formulas(db, cl, coll_name, single_post_thread):
    formulas_coll_name = coll_name + "_FORMULAS"
    count = 0

    unique_form_dict = {}
    post_thread_id = single_post_thread["_id"]

    for formula in single_post_thread["formulas"]:
        unique_form_dict = {}
        unique_form_dict["f_id"] = str(post_thread_id) + "_" + formula["id"]
        unique_form_dict["lx_str"] = formula["latex"]
        unique_form_dict["m_type"] = formula["type"]
        unique_form_dict["f_descriptor"] = formula["descriptor"]
        unique_form_dict["f_decision"] = formula["decision"]

        try:
            new_id = db[formulas_coll_name].insert_one(
                unique_form_dict).inserted_id

            count += 1
        except:
            ...

    return count

def migrate_tags_to_formulas(db, cl, coll_name, single_post_thread):
    formulas_coll_name = coll_name + "_FORMULAS"
    count = 0

    # db[coll_name].update_one({"_id": _id}, {"$set": {"title": title_dict}})
    unique_form_dict = {}
    post_thread_id = single_post_thread["_id"]

    tag_list = single_post_thread["tags"]
    for formula in single_post_thread["formulas"]:

        if formula["decision"] == "both" and not formula["type"] == "UNK":

            f_id = str(post_thread_id) + "_" + formula["id"]

            try:
                db[formulas_coll_name].update_one({"f_id": f_id}, {"$set": {"tags": tag_list}})

                count += 1
            except:
                ...

    return count



# TITLE RELATED FUNCTIONS
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------
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
                    # print(token_1)
                    # print(token_2)
                    prev_token = doc[count-i]
                    #print("prev token: " + str(prev_token.text) + " : "+ str(prev_token.pos_))
                    if not prev_token.pos_ == "SPACE":
                        if prev_token.pos_ == "NOUN" and not prev_token.text in title_formula_tokens:

                            print(
                                "----------------------------------------------------------------------------------------------------")
                            print(title)
                            print("formula: " +
                                  str(title_formulas[doc[count].text]))
                            latex_input = str(title_formulas[doc[count].text])
                            #mathml_output = latex2mathml.converter.convert(latex_input)
                            # print(mathml_output)
                            print("\t" + "prev_token: " +
                                  prev_token.text + ": " + str(prev_token.pos_))

                            print("token count: ", len(title_tokenized))
                            print("new token count: ",
                                  len(new_title_tokenized))

                            print(title_tokenized)
                            print(new_title_tokenized)
                            break
                    i += 1

                #print("\t" + doc[count-1].text + ": " + str(doc[count-1].pos_))
                #print("\t" + doc[count-2].text + ": " + str(doc[count-2].pos_))
            count += 1

    return 1


"""
    collection_name = "elementary-number-theory"
    size = 34454
    data.apply_to_each_multi(collection_name, 2, print_out_posts_types, limit = (size + 1))
    print("TOTAL ---- MET CONDITIONS FORMULA_COUNT: ", str(data.get_count()))
    data.reset_count()
    data.apply_to_each(collection_name, count_all_formulas, limit = -1)
    print("TOTAL ---- ALL FORMULAS: ", str(data.get_count()))
    """
# extracts mathematical types
# usage: data.apply_to_each("elementary-set-theory", extract_math_types)


def extract_math_types(db, cl, coll_name, single_post_thread):
    total_formula_count = single_post_thread["formulas_count"]
    met_criteria_formula_count = 0
    if total_formula_count > 0:

        _id = single_post_thread["_id"]
        tokenized_posts = single_post_thread["tokenized_posts"]
        formulas_dict = single_post_thread["formulas"]
        formulas_dict_tokens = single_post_thread["formulas"].keys()
        formulas_with_types = []

        for post in tokenized_posts:

            count = 0
            for token in post:
                if token in formulas_dict_tokens:

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
                    formula_c_type = FormulaContextType(
                        "kb/type_context_keywords.json", token_list, formula_token, formulas_dict, 3)

                    matching_rules = [{"descriptor_pos": ("NOUN", "left"), "formula_dep": "not pobj"},  # RULE 1
                                      {"descriptor_dep": "attr", "formula_dep": "nsubj"}]  # RULE 2

                    formula_c_type.find_type_descriptors(matching_rules)
                    formula_c_type.determine_formula_type(
                        priority=1)  # 0 - rule1, 1 - rule2

                    # type is determined by formula parser
                    formula_type = FormulaType(
                        formulas_dict[formula_token], formula_token, formulas_dict)
                    formula_type.determine_formula_type()

                    # comparer object acts as arbitrator between formula_type and formula_c_type
                    comp = Comparer(formula_c_type, formula_type)
                    final_type, textual_descr, decision_str = comp.decide_type(
                        "formula")
                    #comp.print_out(final_type, textual_descr, decision_str)

                    if not final_type == "UNK":
                        met_criteria_formula_count += 1

                    formula_dict = {}
                    formula_dict["id"] = token
                    formula_dict["latex"] = formulas_dict[token]
                    formula_dict["type"] = final_type
                    formula_dict["descriptor"] = textual_descr
                    formula_dict["decision"] = decision_str

                    formulas_with_types.append(formula_dict)

                count += 1

        try:
            db[coll_name].update_one(
                {"_id": _id}, {"$set": {"formulas": formulas_with_types}})
        except:
            ...

        print("met_criteria_formula_count: ", str(met_criteria_formula_count))
        print("TOTAL FORMULA COUNT: ", str(total_formula_count))
    return met_criteria_formula_count


# Type extraction from formulas and contexts
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------


# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------

# Statistics
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------

# APPLY ONLY ONCE
# --------------------------------------------------------------------------------------------------------------------

def count_all_formulas_once(db, cl, coll_name, data):
    total_formula_count = 0
    try:
        total_formula_dict = db[coll_name].aggregate([
            {
                "$group": {
                    "_id": "",
                    "formulasCount": {"$sum": "$formulas_count"}}
            },
            {
                "$project": {
                    "formulasCount": "$formulasCount"}
            }
        ])
        total_post_count = list(total_formula_dict)[0]["formulasCount"]
    except:
        ...
    return total_post_count


def formulas_av_once(db, cl, coll_name, data):
    total_formula_count = 0
    try:
        total_formula_dict = db[coll_name].aggregate([
            {
                "$group": {
                    "_id": "",
                    "formulasCount": {"$avg": "$formulas_count"}}
            },
            {
                "$project": {
                    "formulasCount": "$formulasCount"}
            }
        ])
        total_post_count = list(total_formula_dict)[0]["formulasCount"]
    except:
        ...
    return total_post_count


def count_av_all_posts_once(db, cl, coll_name, data):
    total_post_dict = None
    try:
        total_post_dict = db[coll_name].aggregate([
            {
                "$project": {
                    "_id": "$_id",
                    "postsLength": {"$size": "$posts"}}
            },
            {
                "$group": {
                    "_id": "",
                    "totalPostsLength": {"$sum": "$postsLength"},
                    "totalPostsAv": {"$avg": "$postsLength"}}
            },
            {
                "$project": {
                    "totalPostsLength": "$totalPostsLength",
                    "totalPostsAv": "$totalPostsAv"}
            }
        ])
    except Exception as e:
        print(e)

    total_post_stat = list(total_post_dict)[0]
    total_post_count = total_post_stat["totalPostsLength"]
    total_post_av = total_post_stat["totalPostsAv"]

    return total_post_count, total_post_av


"""
def count_m_type_occurences_once(db, cl, coll_name, data):
    coll_name = coll_name + "_FORMULAS"
    total_types_dict = {}
    
    try: 
        total_math_types = db[coll_name].aggregate([
            {
                "$project": {
                    "_id": "$_id",
                    "type": "$type",
                    "decision": "$decision"
                }
            },
            {
                "$project": {
                    "_id": "$_id",
                    "set": {"$cond": [{"$eq": ["$type", "SET"]},{int(1)},{int(0)}] },
                    "func": {"$cond": [{"$eq": ["$type", "FUNC"]},{int(1)},{int(0)}] },
                    "scal": {"$cond": [{"$eq": ["$type", "SCAL"]},{int(1)},{int(0)}] },
                    "unk": {"$cond": [{"$eq": ["$type", "UNK"]},{int(1)},{int(0)}] },
                    "both": {"$cond": [{"$eq": ["$decision", "both"]},{int(1)},{int(0)}] },
                    "context": {"$cond": [{"$eq": ["$decision", "context"]},{int(1)},{int(0)}] },
                    "context_r2": {"$cond": [{"$eq": ["$decision", "context (r2)"]},{int(1)},{int(0)}] },
                    "formula": {"$cond": [{"$eq": ["$decision", "formula"]},{int(1)},{int(0)}] },
                }
            },
            {
                "$project": {
                    "_id": "$_id",
                    "set_both": {"$cond": [{"$and": [
                                                        {"$eq": ["$set", int(1)]},
                                                        {"$eq": ["$formula", int(1)]}
                                                       ]
                                              }, 
                                              {int(1)},{int(0)}]},
                    "set_formula": {"$cond": [{"$and": [
                                                        {"$eq": ["$set", int(1)]},
                                                        {"$eq": ["$formula", int(1)]}
                                                       ]
                                              }, 
                                              {int(1)},{int(0)}]},
                    "set_context": {"$cond": [{"$and": [
                                                        {"$eq": ["$set", int(1)]},
                                                        {"$eq": ["$context", int(1)]}
                                                       ]
                                              }, 
                                              {int(1)},{int(0)}]},
                    "set_context_r2": {"$cond": [{"$and": [
                                                        {"$eq": ["$set", int(1)]},
                                                        {"$eq": ["$context_r2", int(1)]}
                                                       ]
                                              }, 
                                              {int(1)},{int(0)}]}

                }
            }, 
            {
                "$group": {
                    "_id": "",
                    "SetBothCount": {"$sum" : "$set_both"}, 
                    "SetFormulaCount": {"$sum": "$set_formula"},
                    "SetContextCount": {"$sum": "$set_context"},
                    "SetContextR2Count": {"$sum": "$set_context_r2"},
                    }
                  
            }, 
            {
                "$project": {
                    "SetBothCount": "$SetBothCount",
                    "SetFormulaCount": "$SetFormulaCount",
                    "SetContextCount": "$SetContextCount",
                    "SetContextR2Count": "$SetContextR2Count",
                    }
            }

        ])
    except Exception as e:
        print(e)

    total_types_dict = list(total_types_dict)[0]
    set_both_count = total_types_dict["SetBothCount"]
    set_formula_count = total_types_dict["SetFormulaCount"]
    set_context_count = total_types_dict["SetContextCount"]
    set_context_r2_count = total_types_dict["SetContextR2Count"]

    return (set_both_count, set_formula_count, set_context_count, set_context_r2_count)
"""

"""
"context": {"$cond:" {if: {"$eq": ["$f_decision", "context"]}, then: {1}, else: {0}}},
"context_r2": {"$cond:" {if: {"$eq": ["$f_decision", "context (r2)"]}, then: {1}, else: {0}}},
"formula": {"$cond:" {if: {"$eq": ["$f_decision", "formula"]}, then: {1}, else: {0}}}} 
"""

def count_m_type_occurences_once(db, cl, coll_name, data):

    sel_m_type = ""
    if not data == {}:
        sel_m_type = data["m_type"]

    coll_name = coll_name + "_FORMULAS"
    total_types_dict = {}

    try:
        total_types = db[coll_name].aggregate([
            {
                "$project": {
                                "f_id": "$f_id",
                                "ttype": { "$cond": [{ "$eq": ["$m_type", sel_m_type]}, 1, 0]},
                                "both":  { "$cond": [{"$eq": ["$f_decision", "both"]}, 1, 0]},
                                "formula":  { "$cond": [{"$eq": ["$f_decision", "formula"]}, 1, 0]},
                                "context":  { "$cond": [{"$eq": ["$f_decision", "context"]}, 1, 0]},
                                "context_r2":  { "$cond": [{"$eq": ["$f_decision", "context (r2)"]}, 1, 0]}
                            }      
            },
            {
                "$project": {
                                "f_id": "$f_id",
                                "ttype_both": { "$cond": [{ "$and": [{ "$eq": ["$ttype", 1] }, { "$eq": ["$both", 1] }] }, 1, 0 ] }, 
                                "ttype_context": { "$cond": [{ "$and": [{ "$eq": ["$ttype", 1] }, { "$eq": ["$context", 1] }] }, 1, 0 ] },
                                "ttype_context_r2": { "$cond": [{ "$and": [{ "$eq": ["$ttype", 1] }, { "$eq": ["$context_r2", 1] }] }, 1, 0 ] },
                                "ttype_formula": { "$cond": [{ "$and": [{ "$eq": ["$ttype", 1] }, { "$eq": ["$formula", 1] }] }, 1, 0 ] } 
                            }
            }, 
            {
                "$group": {
                                "_id": "",
                                "TypeBothCount": { "$sum": "$ttype_both" },
                                "TypeContextCount": { "$sum": "$ttype_context" },
                                "TypeContextR2Count": { "$sum": "$ttype_context_r2" }, 
                                "TypeFormulaCount": { "$sum": "$ttype_formula" }
                          }
            },
            {
                "$project": {
                                "TypeBothCount": "$TypeBothCount", 
                                "TypeContextCount": "$TypeContextCount", 
                                "TypeContextR2Count": "$TypeContextR2Count", 
                                "TypeFormulaCount": "$TypeFormulaCount" 
                            }
            }
        ])
    except Exception as e:
        print(e)
    total_types_dict = list(total_types)[0]

    return total_types_dict

def get_m_types_both_once(db, cl, coll_name, data):

    limit_count = data["limit_count"]
    coll_name = coll_name + "_FORMULAS"
    try:
        both_types = db[coll_name].find({"f_decision": "both", 
                                          "m_type": {"$ne": "UNK"}}).limit(limit_count)

    except Exception as e:
        print(e)

    both_types_list = []
    for type_dict in both_types:
        both_types_list.append(type_dict)

    return both_types_list

# usage: ONLY WITH apply_once
def count_all_post_threads_once(db, cl, coll_name, data):
    doc_count = 0
    try:
        doc_count = int(db[coll_name].count_documents({}))
    except:
        ...
    return doc_count

# for classification dataset creation
def retrieve_m_types_both_once(db, cl, coll_name, data):

    limit_count = data["limit_count"]
    coll_name = coll_name + "_FORMULAS"
    try:
        both_types = db[coll_name].find({"f_decision": "both", 
                                          "m_type": {"$ne": "UNK"}}).limit(limit_count)

    # {"f_decision": "formula", "m_type": {"$ne": "UNK"}, $expr: { $gt: [{ $strLenCP: '$lx_str' }, 20] }}
    except Exception as e:
        print(e)

    both_types_list = []
    for type_dict in both_types:
        both_types_list.append(type_dict)

    return both_types_list


def retrieve_m_types_unk_long(db, cl, coll_name, data):

    limit_count = data["limit_count"]
    coll_name = coll_name + "_FORMULAS"
    try:
        both_types = db[coll_name].find({"f_decision": "both", 
                                         "m_type": "UNK"}).limit(limit_count)

    except Exception as e:
        print(e)

    both_types_list = []
    for type_dict in both_types:
        both_types_list.append(type_dict)

    return both_types_list
# --------------------------------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------------------------------

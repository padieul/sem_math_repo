import json 
import spacy
from pymongo import MongoClient, errors
#from multiprocessing import Process, Value, Array, Pool
import multiprocess as mp
from itertools import product
from tqdm import tqdm
import re


class MSE_Thread:

    def __init__(self, post_thread):
        
        self._posts_txt = [p["@Body"] for p in post_thread["posts"]]
        self._posts_tokenized = []
        self._posts_formulas = {}

        self._title = post_thread["posts"][0]["@Title"]
        self._title_formulas = {}
        self._title_tokenized = {}

    def get_formulas(self):
        nlp = spacy.load("en_core_web_sm")

        temp_list = []
        counter = 0
        for txt in self._posts_txt:
            temp_list.append(self._substitute_formulas(counter, txt))
            counter += 1

        for txt in temp_list:
            doc = nlp(txt)
            self._posts_tokenized.append([token.text for token in doc])

        return dict(self._posts_formulas)

    def _substitute_formulas(self, counter, text):
        #matches = re.findall(r"(<span class=\"math-container\">\$.+?\$</span>)|()|(\$.+?\$)|(\d+ )", text)
        matches = re.findall(r"(<span class=\"math-container\">\$.+?(\$+)</span>)|(begin{align}(?s).+?end{align})|(\$.+?(\$+))|(\d+ )", text)
        
        counter1 = 0
        for match in matches:
            counter2 = 0
            for elem in match: 
                if not elem == "":
                    formula_id = "f" + "_" + str(counter) + "_" + str(counter1) + "_" + str(counter2) 
                    text = text.replace(elem, " " + formula_id + " ", 1)
                    elem = elem.replace("<span class=\"math-container\">", "")
                    elem = elem.replace("begin{align}", "")
                    elem = elem.replace("end{align}", "")
                    elem = elem.replace("</span>", "")
                    elem = elem.replace("$", "")
                    self._posts_formulas[formula_id] = elem
                    counter2 += 1
                    break
            counter1 += 1

        text = self._filter_out_markup(text)
        return text

    def _filter_out_markup(self, text):

        f_matches = re.findall(r"<a.+?>", text)
        for match in f_matches:
                if not match == "":
                    text = text.replace(match, " ", 1)

        text = text.replace("<blockquote>"," ").replace("</blockquote>", " ")
        text = text.replace("<strong>"," ").replace("</strong>", " ")
        text = text.replace("<p>"," ").replace("</p>"," ")
        text = text.replace("<\n>", " ").replace("</a>", " ")
        text = text.replace("<ul>", " ").replace("</ul>", " ")
        text = text.replace("<li>", " ").replace("</li>", " ")
        text = text.replace("<ol>", " ").replace("</ol>", " ")
        text = text.replace("<em>", " ").replace("</em>", " ")
        text = text.replace("<br>", " ")
        text = text.replace("\n", " ")
        text = text.replace("<", " ").replace(">", " ")
        text = text.replace("\"", " ")
    
        return text

    def get_title_formulas(self):
        
        nlp = spacy.load("en_core_web_sm")

        substituted_title_text = self._substitute_title_formulas(self._title)
        doc = nlp(substituted_title_text)
        for token in doc:
            self._title_tokenized[token.text] = token.dep_

        return self._title_formulas

    def get_tokenized_title(self):
         
        return self._title_tokenized

    def _substitute_title_formulas(self, text):
        matches = re.findall(r"(<span class=\"math-container\">\$.+?\$</span>)|(begin{align}(?s).+?end{align})|(\$.+?\$)|(\d+ )", text)
        
        counter = 0
        counter1 = 0
        for match in matches:
            counter2 = 0
            for elem in match: 
                if not elem == "":
                    formula_id = "f" + "_" + str(counter) + "_" + str(counter1) + "_" + str(counter2) 
                    text = text.replace(elem, " " + formula_id + " ", 1)
                    elem = elem.replace("<span class=\"math-container\">", "")
                    elem = elem.replace("</span>", "")
                    elem = elem.replace("$", "")
                    self._title_formulas[formula_id] = elem
                    counter2 += 1
            counter1 += 1

        text = self._filter_out_markup(text)
        return text

    def get_tokenized_text(self):
        return list(self._posts_tokenized)

    def get_title_str(self):
        return self._title



class MSE_DBS:

    def __init__(self, conf_type, sett_file_path, log_file_path = "conf\\analyzer_log.txt"):

        self._log_file_path = log_file_path
        self._sett_file_path = sett_file_path 

        self._sett = self._get_db_settings(self._sett_file_path, conf_type)
        #self._db, self._client = self._get_mongo_db()
        self._dbs, self._clients = [], []
        self._total_count = 0

    def _get_db_settings(self, s_filename, conf_type):

        with open(s_filename, "r") as f:
            temp_dict = json.load(f)
            if conf_type == "win":
                db_settings = temp_dict[conf_type]
            elif conf_type == "linux":
                db_settings = temp_dict[conf_type]
                db_settings["username"] = ""
                db_settings["password"] = ""

        f.close()
        return db_settings

    def _get_mongo_db(self):

        MONGODB_HOST = self._sett["host"] 
        MONGODB_PORT = self._sett["port"] 
        MONGODB_AUTHENTICATION_DB = self._sett["db"]

        if self._sett["username"] == "" and self._sett["password"] == "":
            uri_str = "mongodb://" + MONGODB_HOST + ":" + str(MONGODB_PORT)
        else:
            MONGODB_USER_NAME = self._sett["username"] 
            MONGODB_PASSWORD = self._sett["password"] 
            uri_str = "mongodb://" + MONGODB_USER_NAME + ":" + MONGODB_PASSWORD + "@" + MONGODB_HOST + ":" + str(MONGODB_PORT)

        client = MongoClient(uri_str)
        
        try:
            client.admin.command("ping")
        except errors.ConnectionFailure:
            print("Server not available")

        db = client[MONGODB_AUTHENTICATION_DB]
        return db,client


    def apply_to_each_conserve(self, all_threads_coll_name, func, limit):
        counter = 0
        counter_all = 0
        self._db, self._client = self._get_mongo_db()


        with self._client.start_session() as session:
            threads_cursor = self._db[all_threads_coll_name].find({}, no_cursor_timeout=True, batch_size=1, session=session)
            total_count = self._db[all_threads_coll_name].count_documents({})
            conservation_dict = {}
            limit_count = 0
            for post_thread in tqdm(threads_cursor, total = total_count):
                if limit_count == limit:
                    break
                counter_all += 1
                try:
                    token_dict = func(self._db, self._client, all_threads_coll_name, conservation_dict, post_thread)
                except:
                    continue
                limit_count += 1

        self._total_count += counter
        
        session.end_session()
        return conservation_dict


    def apply_to_each(self, all_threads_coll_name, func, limit):
        counter = 0
        self._db, self._client = self._get_mongo_db()

        with self._client.start_session() as session:
            threads_cursor = self._db[all_threads_coll_name].find({}, no_cursor_timeout=True, batch_size=1, session=session)
            total_count = self._db[all_threads_coll_name].count_documents({})
            token_dict = {}
            limit_count = 0
            for post_thread in tqdm(threads_cursor, total = total_count):
                if limit_count == limit:
                    break
                try:
                    counter += func(self._db, self._client, all_threads_coll_name, post_thread)
                except Exception as e:
                    print(e)
                    limit_count += 1
                    continue
                limit_count += 1

        self._total_count += counter
        
        session.end_session()



    def apply_to_each_multi(self, all_thread_coll_name, multi_num, func, limit):

        def apply_in_process(sett_dict, counter_ar, p_count, all_threads_coll_name, func, doc_interval):
            #print("ALIVE: " + str(p_count))
    
            ############
            MONGODB_HOST = sett_dict["host"] 
            MONGODB_PORT = sett_dict["port"] 
            MONGODB_AUTHENTICATION_DB = sett_dict["db"]

            if sett_dict["username"] == "" and sett_dict["password"] == "":
                uri_str = "mongodb://" + MONGODB_HOST + ":" + str(MONGODB_PORT)
            else:
                MONGODB_USER_NAME = sett_dict["username"] 
                MONGODB_PASSWORD = sett_dict["password"] 
                uri_str = "mongodb://" + MONGODB_USER_NAME + ":" + MONGODB_PASSWORD + "@" + MONGODB_HOST + ":" + str(MONGODB_PORT)

            client = MongoClient(uri_str)
            ############
            db = client[MONGODB_AUTHENTICATION_DB]
            #print("ALIVE II: " + str(p_count) + " -- doc: " + str(doc_interval))
            limit_left = doc_interval[0]
            limit_right = doc_interval[1]

            with client.start_session() as session:
                threads_cursor = db[all_threads_coll_name].find({}, no_cursor_timeout=True, batch_size=1, session=session)
                total_count = db[all_threads_coll_name].count_documents({})

                #print("ALIVE III: " + str(p_count) + "total count: " + str(total_count))
                
                limit_count = 0
                counter = 0
                
                if p_count == 0:
                    for post_thread in tqdm(threads_cursor, total = limit_right, dynamic_ncols=True, ):
                        #print("ALIVE IV: " + str(p_count) + " l,r: " + str(limit_left) + " | " + str(limit_right))
                        if limit_count < limit_left:
                            limit_count += 1
                            continue
                        if limit_count == limit_right:
                            break
                        #print("process: " + str(p_count) + ", doc: " + str(limit_count))
                        try:
                            counter += func(db, client, all_threads_coll_name, post_thread)
                        except Exception as e:
                            print(e)
                            limit_count += 1
                            continue
                        limit_count += 1
                else:
                    for post_thread in threads_cursor:
                        #print("ALIVE IV: " + str(p_count) + " l,r: " + str(limit_left) + " | " + str(limit_right))
                        #print("P: " + str(p_count) + ", limit_count: " + str(limit_count))
                        if limit_count < limit_left:
                            #print("P: " + str(p_count) + " smaller")
                            limit_count += 1
                            continue
                        if limit_count == limit_right:
                            #print("P: " + str(p_count) + " break")
                            break
                        #print("process: " + str(p_count) + ", doc: " + str(limit_count))
                        try:
                            counter += func(db, client, all_threads_coll_name, post_thread)
                        except Exception as e:
                            print(e)
                            limit_count += 1
                            continue
                        limit_count += 1

            counter_ar[p_count] += counter
            session.end_session()


        counter_ar = mp.Array('i', multi_num)

        p_intervals = self._calculate_access_intervals(multi_num, limit)
        
        processes = []
        for p_count in range(multi_num):
            #print(p_count)
            p = mp.Process(target=apply_in_process, args=(self._sett, counter_ar, p_count, all_thread_coll_name, func, p_intervals[p_count],))
            processes.append(p)
        for p in processes:
            #print("start")
            p.start()
        for p in processes:
            #print("join")
            p.join() 
        
        counter_list = list(counter_ar)
        print(counter_list)
        self._total_count = sum(counter_list)



    def _calculate_access_intervals(self, multi_num, limit):

        p_collection_intervals = []
        limit_mod = limit % multi_num
        if limit_mod == 0:
            limit_div = limit / multi_num
            for i in range(1,multi_num+1):
                if i == 1:
                    p_collection_intervals.append((0, int(limit_div - 1)))
                else:
                    p_collection_intervals.append((int(i*limit_div - limit_div - 1), int(i*limit_div - 1)))
        else:
            limit_div = (limit - limit_mod) / multi_num
            for i in range(1,multi_num+1):
                if i == 1:
                    p_collection_intervals.append((0, int(limit_div + limit_mod - 1)))
                else:
                    p_collection_intervals.append((int(i*limit_div - limit_div + limit_mod - 1), int(i*limit_div + limit_mod - 1)))

        return p_collection_intervals

    def apply_once(self, coll_name, func, data = {}):
        self._db, self._client = self._get_mongo_db()
        return_val = None
        with self._client.start_session() as session:
            try:
                return_val = func(self._db, self._client, coll_name, data)
            except Exception as e:
                print(e)
                
        session.end_session()
        return return_val

    def get_count(self):
        return self._total_count

    def reset_count(self):
        self._total_count = 0
    



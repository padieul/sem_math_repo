import json 
import spacy
from pymongo import MongoClient, ConnectionFailure
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

    def __init__(self, sett_file_path, log_file_path = "conf\\analyzer_log.txt"):

        self._log_file_path = log_file_path
        self._sett_file_path = sett_file_path 

        sett = self._get_db_settings(self._sett_file_path)
        self._db, self._client = self._get_mongo_db(sett)

        self._total_count = 0

    def _get_db_settings(self, s_filename):

        with open(s_filename, "r") as f:
            db_settings = json.load(f)
        f.close()
        return db_settings

    def _get_mongo_db(self, settings):

        MONGODB_USER_NAME = settings["username"] 
        MONGODB_PASSWORD = settings["password"] 
        MONGODB_HOST = settings["host"] 
        MONGODB_PORT = settings["port"] 
        MONGODB_SOURCE = settings["db"]
        MONGODB_AUTHENTICATION_DB = settings["db"]

        uri_str = "mongodb://" + MONGODB_USER_NAME + ":" + MONGODB_PASSWORD + "@" + MONGODB_HOST + ":" + str(MONGODB_PORT)
        client = MongoClient(uri_str)
        
        try:
            client.admin.command("ping")
        except ConnectionFailure: 
            print("Server not available")

        db = client[MONGODB_AUTHENTICATION_DB]
        return db,client


    def apply_to_each_conserve(self, all_threads_coll_name, func, limit):
        counter = 0
        counter_all = 0


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

    def apply_once(self, all_threads_coll_name, func):
        
        with self._client.start_session() as session:
            try:
                func(self._db, self._client)
            except:
                ...
                
        session.end_session()

    def get_count(self):
        return self._total_count

    def reset_count(self):
        self._total_count = 0
    
    


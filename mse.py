import json 
import spacy
from pymongo import MongoClient 
from tqdm import tqdm
import re


class MSE_Thread:

    def __init__(self, post_thread):
        
        self._posts_txt = [p["@Body"] for p in post_thread["posts"]]
        self._posts_tokenized = []
        self._posts_formulas = {}

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
        matches = re.findall(r"(<span class=\"math-container\">\$.+?\$</span>)|(\$.+?\$)|(\d+ )", text)
        
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
                    self._posts_formulas[formula_id] = elem
                    counter2 += 1
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


    def get_tokenized_text(self):
        return list(self._posts_tokenized)



class MSE_DBS:

    def __init__(self, sett_file_path, log_file_path = "conf\\analyzer_log.txt"):

        self._log_file_path = log_file_path
        self._sett_file_path = sett_file_path 

        sett = self._get_db_settings(self._sett_file_path)
        self._db, self._client = self._get_mongo_db(sett)

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


    def apply_to_each(self, all_threads_coll_name, func):
        counter = 0
        counter_all = 0

        with self._client.start_session() as session:
            threads_cursor = self._db[all_threads_coll_name].find({}, no_cursor_timeout=True, batch_size=1, session=session)
            total_count = self._db[all_threads_coll_name].count_documents({})

            for post_thread in tqdm(threads_cursor, total = total_count):
                counter_all += 1
                try:
                    counter += func(self._db, self._client, all_threads_coll_name, post_thread)
                except:
                    continue

        session.end_session()


    def apply_once(self, all_threads_coll_name, func):
        
        with self._client.start_session() as session:
            try:
                func(self._db, self._client)
            except:
                ...
                
        session.end_session()
    
    


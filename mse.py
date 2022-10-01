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
        for txt in self._posts_txt:
            temp_list.append(self._substitute_formulas(txt))

        for txt in temp_list:
            doc = nlp(txt)
            self._posts_tokenized.append([token.text for token in doc])

    def _substitute_formulas(self, text):
        forms = re.findall(r"<span class=\\\"math-container\\\">\.+</span>", text)
        print(forms)

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
    
    


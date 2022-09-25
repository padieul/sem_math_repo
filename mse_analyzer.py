import json 
from pymongo import MongoClient 
from tqdm import tqdm


class MSE_Analyzer:

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
        with self._client.start_session() as session:
            threads_cursor = self._db[all_threads_coll_name].find({}, no_cursor_timeout=True, batch_size=1, session=session)
            total_count = self._db[all_threads_coll_name].count_documents({})

            for post_thread in tqdm(threads_cursor, total = total_count):
                try:
                    counter += func(self._db, self._client, post_thread)
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
    
    


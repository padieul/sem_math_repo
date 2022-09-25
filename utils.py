import xml.dom.minidom
import xmltodict, json
from tqdm import tqdm
import glob
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

"""
import latex2mathml.converter


if __name__ == "__main__":

    latex_input = "\sqrt{2}"
    mathml_output = latex2mathml.converter.convert(latex_input)
    print(mathml_output)
"""

## ----------------------------------------------------------------------------------------
## FUNCTIONS FOR SLICING XML FILES AND CONVERSION TO JSON 
## usage:
"""
    file_name_str = "math.stackexchange.com\Votes.xml"
    posts_count = xml_to_str_chunks(filename = file_name_str, 
                                    slice_size = 100000,  
                                    limiting_tags=["<votes>", "</votes>"]) #["<posts>", "</posts>"] # "<tags>", "</tags>"
    print("count: ", posts_count)
"""
"""
    slice_json_file("math.stackexchange.com\\posts_json_slices", "json_output100000.json", 100)
""" 
## ----------------------------------------------------------------------------------------

def slice_to_json(count, r_list):
    xml_to_json_dict = {} 
    xml_to_json_dict["rows"] = r_list
    with open("json_output" + str(count) + ".json", "w") as xml_output_file:
        json.dump(xml_to_json_dict, xml_output_file)
    xml_output_file.close()


def xml_to_str_chunks(filename, slice_size, limiting_tags):
    xml_first_row_str = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    count = 0

    xml_to_json_dict = {} 
    row_list = []
    with open(filename, encoding="utf8") as xml_file:
        while True:
            
            line = xml_file.readline()

            if xml_first_row_str in line:
                    continue
            if limiting_tags[0] in line:
                continue
            if limiting_tags[1] in line:
                slice_to_json(count, row_list)
                break

            xml_dict = xmltodict.parse(line)

            row_list.append(xml_dict["row"])
            print("ROW # ",count, " ----------------------------------------------")
            count += 1

            if count % slice_size == 0:
                slice_to_json(count, row_list)
                row_list = []

        xml_file.close()

    return len(row_list)


def slice_json_file(rel_dir_part, file_name ,rows_size):
    with open(rel_dir_part + "\\" + file_name, "r") as f:
        data = json.load(f)
    f.close()

    print(len(data["rows"])) 
    print(json.dumps(data["rows"][0], indent=4, sort_keys=False))

## ----------------------------------------------------------------------------------------
## FUNCTIONS FOR STORING JSON DATA INTO MONGO DB
## usage:
"""
    saved_file_name = "math.stackexchange.com\posts_json_slices\json_output100000.json"     # already processed file
    log_file_name = "conf\storing_log.txt"                                                  # processing log
    db_settings_file_name = "conf\db_conf.json"                                             # mongo settings file
    
    sett = get_db_settings(db_settings_file_name)                                           # get database connection settings from file
    datab,client = get_mongo_db(sett)                                                              # connect to database

    post_file_names = glob.glob("math.stackexchange.com\posts_json_slices\*")               # get all json files with posts from directory
    post_file_names.sort()

    for post_file_name in post_file_names:
        
        if post_file_name == saved_file_name:                                               # ignore this file, since data already in db
            continue
        
        print("filename: ", post_file_name)
        count = post_threads_to_db(datab, post_file_name)
        print("number of threads: ", count)
        print("******************************************************************************")
        write_to_log(post_file_name, count, log_file_name)
"""
## ----------------------------------------------------------------------------------------

def get_db_settings(s_filename):
    
    with open(s_filename, "r") as f:
        db_settings = json.load(f)
    f.close()
    return db_settings

def write_to_log(post_file_name, thread_count, log_file_name):
    
    with open(log_file_name, "a") as log_file:
        log_file.write(post_file_name)
        log_file.write(" - ")
        log_file.write("number of threads: ") 
        log_file.write(str(thread_count))
        log_file.write("\n")
    log_file.close()


def get_mongo_db(settings): 

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

def post_threads_to_db(db, post_file_name):
    QUESTION_POST_ID = 1
    ANSWER_POST_ID = 2
    

    with open(post_file_name, "r") as f:
        posts = json.load(f)
    f.close()

    coll_name = post_file_name
    colllist = db.list_collection_names()
    if not coll_name in colllist:
        new_coll = db[coll_name]

    thread_counter = 0
    for row in tqdm(posts["rows"]):
        if row["@PostTypeId"] == str(QUESTION_POST_ID):
            thread_dict = {}
            thread_dict["thread_id"] = "thread" + "_" + row["@Id"] + "_" + str(thread_counter) 
            thread_dict["ini_post_id"] = row["@Id"]
            thread_dict["posts"] = [row,]
            thread_id = new_coll.insert_one(thread_dict).inserted_id
            thread_counter += 1

    for row in tqdm(posts["rows"]):
        if row["@PostTypeId"] == str(ANSWER_POST_ID):
            try:
                parent_id = row["@ParentId"]
                question_thread_posts = new_coll.find_one({"ini_post_id": str(parent_id)})["posts"]
                question_thread_posts.append(row)
                new_coll.update_one({"ini_post_id": str(parent_id)}, {"$set": {"posts": question_thread_posts}})
            except:
                continue

    return thread_counter

    
## ----------------------------------------------------------------------------------------
## FUNCTIONS FOR COPYING POSTS FROM PARTIAL COLLECTIONS IN DB TO A SINGLE (THREADS) COLLECTION
## ----------------------------------------------------------------------------------------

def copy_to_threads(db, client, post_file_name):
    threads_coll_name = "threads"
    copy_count = 0
    total_count = 0
    
    coll_name = post_file_name
    colllist = db.list_collection_names()
    if coll_name in colllist:
        with client.start_session() as session:
            threads_cursor = db[post_file_name].find({}, no_cursor_timeout=True, batch_size=1, session=session)
            total_count = db[post_file_name].count_documents({})
            for post_thread in tqdm(threads_cursor):
                thread_id = post_thread["thread_id"]

                """
                if not db[threads_coll_name].count_documents({"thread_id": thread_id}) == 0: 
                    continue
                else:
                    new_id = db[threads_coll_name].insert_one(post_thread).inserted_id
                    copy_count += 1
                """ 
                try:
                    new_id = db[threads_coll_name].insert_one(post_thread).inserted_id
                    copy_count += 1
                except:
                    continue



        session.end_session()
    return copy_count,total_count

def write_to_copy_log(post_file_name, num_copied, num_total, log_file_name):
    
    with open(log_file_name, "a") as log_file:
        log_file.write(post_file_name)
        log_file.write(" - ")
        log_file.write("threads - copied | total: ") 
        log_file.write(str(num_copied))
        log_file.write(" | ")
        log_file.write(str(num_total))
        log_file.write("\n")
    log_file.close()
    


## ----------------------------------------------------------------------------------------

if __name__ == "__main__":
    saved_file_names = ["math.stackexchange.com\posts_json_slices\json_output100000.json",  \
                        "math.stackexchange.com\posts_json_slices\json_output1000000.json", \
                        "math.stackexchange.com\posts_json_slices\json_output1100000.json", \
                        "math.stackexchange.com\posts_json_slices\json_output1200000.json", \
                        "math.stackexchange.com\posts_json_slices\json_output1300000.json"  ]     # already processed file
    log_file_name = "conf\copy_log.txt"                                                     # processing log
    db_settings_file_name = "conf\db_conf.json"                                             # mongo settings file
    
    sett = get_db_settings(db_settings_file_name)                                           # get database connection settings from file
    datab,client = get_mongo_db(sett)                                                       # connect to database

    post_file_names = glob.glob("math.stackexchange.com\posts_json_slices\*")               # get all json files with posts from directory
    post_file_names.sort()

    for post_file_name in post_file_names:
        
        if post_file_name in saved_file_names:                                               # ignore this file, since data already in db
            continue
        
        print("filename: ", post_file_name)
        num_copied, num_total = copy_to_threads(datab, client, post_file_name)
        print("******************************************************************************")
        write_to_copy_log(post_file_name, num_copied, num_total, log_file_name)
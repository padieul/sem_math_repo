import xml.dom.minidom
import xmltodict, json
from tqdm import tqdm
import glob
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure



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

def get_db_settings(s_filename):
    
    with open(s_filename, "r") as f:
        db_settings = json.load(f)
    f.close()
    return db_settings


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
    return db

def post_threads_to_db(db, coll_name, post_file_name):
    QUESTION_POST_ID = 1
    ANSWER_POST_ID = 2
    

    with open(post_file_name, "r") as f:
        posts = json.load(f)
    f.close()

    thread_counter = 0
    for row in tqdm(posts["rows"]):
        if row["@PostTypeId"] == str(QUESTION_POST_ID):
            thread_dict = {}
            thread_dict["thread_id"] = "thread" + "_" + row["@Id"] + "_" + str(thread_counter) 
            thread_dict["ini_post_id"] = row["@Id"]
            thread_dict["posts"] = [row,]
            thread_id = db[coll_name].insert_one(thread_dict).inserted_id
            thread_counter += 1

    for row in tqdm(posts["rows"]):
        if row["@PostTypeId"] == str(ANSWER_POST_ID):
            try:
                parent_id = row["@ParentId"]
                question_thread_posts = db[coll_name].find_one({"ini_post_id": str(parent_id)})["posts"]
                question_thread_posts.append(row)
                db[coll_name].update_one({"ini_post_id": str(parent_id)}, {"$set": {"posts": question_thread_posts}})
            except:
                continue

    return thread_counter
    

if __name__ == "__main__":
    
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

    sett = get_db_settings("db_conf.json")
    datab = get_mongo_db(sett) 

    saved_file_name = "math.stackexchange.com\posts_json_slices\json_output100000.json"

    post_file_names = glob.glob("math.stackexchange.com\posts_json_slices\*")
    post_file_names.sort()
    for post_file_name in post_file_names:
        if post_file_name == saved_file_name:
            continue
        print("Filename: ", post_file_name)
        count = post_threads_to_db(datab, "threads", post_file_name)
        print("Total number of threads: ", count)
    
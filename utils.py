import xml.dom.minidom
import xmltodict, json





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



if __name__ == "__main__":
    
    """
    file_name_str = "math.stackexchange.com\Votes.xml"
    posts_count = xml_to_str_chunks(filename = file_name_str, 
                                    slice_size = 100000,  
                                    limiting_tags=["<votes>", "</votes>"]) #["<posts>", "</posts>"] # "<tags>", "</tags>"
    print("count: ", posts_count)
    """

    slice_json_file("math.stackexchange.com\\posts_json_slices", "json_output100000.json", 100)
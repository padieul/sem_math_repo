import xml.dom.minidom
from lxml import etree 
from io import StringIO, BytesIO
import xmltodict, json



def read_xml_file_simple(filename):
    doc = xml.dom.minidom.parse(filename)
    print(doc.nodeName) 
    
    print(doc.firstChild.tagName)

    rows = doc.getElementsByTagName("row")
    print("%d row:" % rows.length)
    counter = 0
    for row in rows:
        if counter == 10:
            break
        print("POST ID: ",row.getAttribute("Id"))
        #print(row.getAttribute("PostTypeId"))
        print("CREATION_DATE: ",row.getAttribute("CreationDate"))
        print("TITLE: ", row.getAttribute("Title"))
        print("BODY: ", row.getAttribute("Body"))
        counter += 1


def read_xml_file_advanced(filename):
    doc = xml.dom.minidom.parse(filename)
    print(doc.nodeName) 
    first_child = doc.firstChild
    for elem in first_child:
        print(elem)


def read_xml_file_iteratively(file_str):

    context = etree.iterparse(StringIO(file_str))
    for action, elem in context:
         print("%s: %s" % (action, elem.tag))

def xml_to_str_chunks(filename):
    xml_first_row_str = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
    count = 0

    xml_to_json_dict = {} 
    row_list = []
    with open(filename, "r") as xml_file:
        while True:

            count += 1
            print("LINE # ",count, " ----------------------------------------------")
            line = xml_file.readline()
            if xml_first_row_str in line:
                    continue
            if "<posts>" in line:
                continue

            xml_line = xml.dom.minidom.parseString(line)
            print(xml_line.nodeName)
            print(xml_line.firstChild.tagName)
            rows = xml_line.getElementsByTagName("row")
            print("%d row:" % rows.length)
            counter = 0
            for row in rows:
                if counter == 10:
                    break
                print("POST ID: ",row.getAttribute("Id"))
                #print(row.getAttribute("PostTypeId"))
                print("CREATION_DATE: ",row.getAttribute("CreationDate"))
                print("TITLE: ", row.getAttribute("Title"))
                print("BODY: ", row.getAttribute("Body"))


                
                counter += 1
            xml_dict = xmltodict.parse(line)
            row_list.append(xml_dict["row"])

            #json_str = json.dumps(xml_dict)
            
           
            #print("Line{}: {}".format(count, line.strip()))
            if count == 10:
                break

        xml_to_json_dict["rows"] = row_list
        with open("json_output.json", "w") as xml_output_file:
            json.dump(xml_to_json_dict, xml_output_file)
        xml_output_file.close()
        xml_file.close()



class XmlToChunks:

    def __init__():
        xml_first_row_str = "<?xml version=\"1.0\" encoding=\"utf-8\"?>"
        n = 10000

    def slice(filename, destination_dir = " "):
        
        count = 0
        with open(filename, "r") as xml_file:
            while True:

                count += 1
                line = xml_file.readline()
                if self.xml_first_row_str in line:
                    continue
                print("Line{}: {}".format(count, line.strip()))
                if count == n:
                    break

        
            xml_file.close()



if __name__ == "__main__":
    

    """
    # do something
    file_name_str = "math.stackexchange.com\Posts.xml"
    #read_xml_file_advanced(file_name_str)
    xml_to_str_chunks(file_name_str)
    """

    file_name_str = "math.stackexchange.com\Posts.xml"
    xml_to_str_chunks(file_name_str)
    #xml_ch = XmlToChunks()
    #xml_ch.slice(file_name_str)
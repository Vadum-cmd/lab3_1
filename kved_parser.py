"""
Read data from kved.json data dictionary file and save entered by user data result into kved_results.json file
kved.json data sources : https://data.gov.ua/dataset/f8a741b9-af17-48e2-8178-8e161c244549/resource/878a36b5-31af-4c36-86e6-5dbf432e9331/download/kved.json
"""
import json
import re


def parse_json_data(classCode: str) -> dict:
    """
    Function to parsed data from file based on input ClassCode.
    Function will return only first occurence.
    """
    result = {"Class_Name": "",
              "Group_Name": "",
              "Division_Name": "",
              "Section_Name": "",
              "Class_Count": 0,
              "Division_Count": 0,
              "Group_Count": 0
              }
    # Find node in json data
    for section in data["sections"][0]:
        section_name = section["sectionName"]
        for division in section["divisions"]:
            division_name = division["divisionName"]
            division_num = len(section["divisions"])
            for group in division["groups"]:
                group_name = group["groupName"]
                group_num = len(division["groups"])
                for group_class in group["classes"]:
                    if group_class["classCode"] == classCode:
                        class_name = group_class["className"]
                        class_num = len(group["classes"])
                        result = {"Class_Name": class_name,
                                  "Group_Name": group_name,
                                  "Division_Name": division_name,
                                  "Section_Name": section_name,
                                  "Class_Count": int(class_num),
                                  "Division_Count": int(division_num),
                                  "Group_Count": int(group_num)
                                  }
    return result


def format_output_data(class_code):
    """
    Function return re-formatted json data.
    """
    result_json = parse_json_data(class_code)

    kved_result_json = {"name": result_json['Class_Name'],
                        "type": "class",
                        "parent": { "name": result_json['Group_Name'],
                                    "type": "group",
                                    "num_children": result_json['Class_Count'],
                                    "parent": { "name": result_json['Division_Name'],
                                                "type": "division",
                                                "num_children": result_json['Group_Count'],
                                                "parent": {"name": result_json['Section_Name'],
                                                           "type": "section",
                                                           "num_children": result_json['Division_Count']
                                                           }
                                                }
                                    }
                        }

    return kved_result_json


def save_output_to_file(out_data, file_path: str='kved_results.json') -> str:
    '''
    Save result to datafile
    '''
    with open(file_path, 'w', encoding="utf-8") as outfile:
        json.dump(out_data, outfile, indent=4, ensure_ascii=False)

    return file_path

# Read input data and do validation to make sure format is correct(##.##)
while 1 :
    v_class_code = input("Please enter value for class code in format ##.##(with leading zero, e.g 01.11) : ")
    if re.match(r"^\d{0,2}(\.\d{1,2})?$", v_class_code):
        print ("Class code accepted : " + v_class_code)
        break
    else:
        print("Invalid value, please try again")

v_class_code = "01.11"
#print(v_class_code)

# Load JSON data
source_datafile = "kved.json"
data = json.load(open(source_datafile, encoding="utf-8"))
# Parse, Format and Save output data
output_data = format_output_data(v_class_code)
print (output_data)
# Save results to file
result_datafile = save_output_to_file(output_data, 'kved_results.json')
#print (result_datafile)

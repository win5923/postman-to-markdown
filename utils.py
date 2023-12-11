import argparse
import json
import re
import requests


# options:
# -j, --json-dir: Path to json file
def set_args():
    parser = argparse.ArgumentParser(description='Process some data with an json file')
    parser.add_argument('-j', '--json-dir', required=True, help='Path to json file')

    return parser.parse_args()

def read_json_file(json_file_path):
        with open(json_file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

# Convert extracted text to markdown.
def convert_to_markdown(test_texts):
    Test_Dict = test_texts["test_dict"]
    request_method =test_texts["request_method"]
    Request_Body =test_texts["request_body"]
    Colletcion_Tests = test_texts["collection_tests"]
    Request_Url = test_texts["request_url"]
    Response_Body = test_texts["response_body"]
    Request_Name =test_texts["request_name_list"]
    Request_Body_Name = []
    # for key in Test_Dict:
    #     Request_Name.append(key)



    markdown_output = "### Collection Tests\n\n"
    markdown_output += "These tests will execute all of the following requests.\n\n"
    markdown_output += "??? note \"Test case description\"\n"
    for text in Colletcion_Tests:
        markdown_output += f"    * {text} : To be written.\n\n"

    markdown_output +="| Test name                | Pass conditions | \n"
    markdown_output += "|----------------------|-------------------------------------------------| \n"
    for text in Colletcion_Tests:
        markdown_output += f"| {text}          | To be written.                                  |\n"
    
    for text in request_method:
        markdown_output += f"\n## {text}\n\n"
        for text in Request_Name:
            markdown_output += f"\n### {text}\n\n"
            value = Request_Url[text]
            markdown_output += f"`{value}`\n\n"    
            markdown_output += "=== \"Test Case 1\"\n"
            markdown_output += "    ??? note \"Test case description\"\n"
            for value in Test_Dict[text]:
                markdown_output += f"           * {value} : To be written.\n"
            if text in Request_Body:
                value = Request_Body[text].replace('\r', '')
                markdown_output += "\n    ``` json\n"
                markdown_output += "    # Request body example\n"
                markdown_output += "    {"
                markdown_output += f"\n   {value[5:-2]}"
                markdown_output += "\n    }\n"
                markdown_output += "    ```\n"
            if text in Response_Body:
                value = Response_Body[text]
                markdown_output += "\n    ``` json\n"
                markdown_output += "    # Response body example\n"
                markdown_output += "    {"
                markdown_output += f"\n    {value}\n"
                markdown_output += "    }\n"
                markdown_output += "    ```\n"


            markdown_output += "\n | Test name                   | Pass conditions                                           | Regex              | Regex Example        | Criteria match                       |\n"
            markdown_output += " |-----------------------------|-------------------------------------------|--------------------|-----------------------|---------------------------------------|\n"
            for value in Test_Dict[text]:
                markdown_output += f"| {value} |   To be written.                              |                    |                       |                                       |\n"
    return markdown_output
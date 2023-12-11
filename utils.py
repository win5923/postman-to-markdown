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
    test_dicct = test_texts["test_dicct"]
    request_method =test_texts["request_method"]
    request_body =test_texts["request_body"]
    colletcion_tests = test_texts["collection_tests"]
    request_url = test_texts["request_url"]
    response_body = test_texts["response_body"]
    request_name =test_texts["request_name_dict"]
    request_body_Name = []


    markdown_output = "### Collection Tests\n\n"
    markdown_output += "These tests will execute all of the following requests.\n\n"
    markdown_output += "??? note \"Test case description\"\n"
    for text in colletcion_tests:
        markdown_output += f"    * {text} : To be written.\n\n"

    markdown_output +="| Test name                | Pass conditions | \n"
    markdown_output += "|----------------------|-------------------------------------------------| \n"
    for text in colletcion_tests:
        if text == "Status code is 200":
            markdown_output += f"| {text}          | The response status code is 200.                                  |\n"
        elif text == "Response time is less than 3000ms":
            markdown_output += f"| {text}          | The response time is less than 3000ms.                                  |\n"    
        elif text == "Response body type is JSON":
            markdown_output += f"| {text}          | The response is in JSON format.                                  |\n"    
    
    for text in request_method:
        markdown_output += f"\n## {text}\n\n"
        for key in request_name[text]:
            markdown_output += f"\n### {key}\n\n"
            value = request_url[key]
            markdown_output += f"`{value}`\n\n"    
            markdown_output += "=== \"Test Case 1\"\n"
            markdown_output += "    ??? note \"Test case description\"\n"
            for value in test_dicct[key]:
                markdown_output += f"           * {value} : To be written.\n"
            if key in request_body:
                value = request_body[key].replace('\r', '')
                markdown_output += "\n    ``` json\n"
                markdown_output += "    # Request body example\n"
                markdown_output += "    {"
                markdown_output += f"\n   {value[5:-2]}"
                markdown_output += "\n    }\n"
                markdown_output += "    ```\n"
            if key in response_body:
                value = response_body[key]
                markdown_output += "\n    ``` json\n"
                markdown_output += "    # Response body example\n"
                markdown_output += "    {"
                markdown_output += f"\n    {value}\n"
                markdown_output += "    }\n"
                markdown_output += "    ```\n"

            markdown_output += "\n | Test name                   | Pass conditions                                           | Regex              | Regex Example        | Criteria match                       |\n"
            markdown_output += " |-----------------------------|-------------------------------------------|--------------------|-----------------------|---------------------------------------|\n"
            for value in test_dicct[key]:
                if value == "Response body type is JSON":
                    markdown_output += f"| {value} |   The response is in JSON format.                              |                    |                       |                                       |\n"
                elif value == "Verify Data Integrity":
                    markdown_output += f"| {value} |   The data in each response object conforms to the rules.                              |                    |                       |                                       |\n"
                elif value == "Response content-type is text/plain":
                    markdown_output += f"| {value} |   The Content-Type header of the Response is text/plain.                              |                    |                       |                                       |\n"
                elif value == "Verify Json Schema":
                    markdown_output += f"| {value} |   The response matches the defined JSON schema.                              |                    |                       |                                       |\n"  
                else:
                    markdown_output += f"| {value} |   To be written.                              |                    |                       |                                       |\n"       
    
    return markdown_output
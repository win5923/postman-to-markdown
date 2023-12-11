import re
import json
import requests

class PostmanCollectionExtractor:
    def __init__(self, json_data):
        self.json_data = json_data
        self.request_method = []        # Store methods used in postman.
        self.request_name_dict = {}     # Store the request name in a dict with different methods as key.
        self.collection_tests = []      # Store collection text.
        self.request_url = {}           # Store the request url in a dict with each request name as key.
        self.test_dict = {}             # Store the text in a dict with each request name as key.
        self.request_body = {}          # Store the request body in a dict with each request name as key.
        self.response_body = {}         # Store the response body in a dict with each request name as key.
        self.collection_variables = {}  # Store collection variables.
        self.pattern = re.compile(r"pm\.test\(['\"](.*?)['\"]")   
        self.pattern_url = re.compile(r'\{\{(\w+)\}\}')

        # Headers required for the request
        self.headers = {
            'Content-Type': 'application/json;',
            'Accept': 'application/json'
        }

    # Extract collection variables.
    def extract_collection_variables(self):
        for variable in self.json_data['variable']:
            key = variable['key']
            self.collection_variables[key] = variable['value']

    # Extract request method and request name and test.
    def extract_tests(self):
        for main_item in self.json_data['item']:
            for sub_item in main_item.get('item', []):
                self.request_method.append(sub_item.get('name', []))
                current_method = sub_item.get('name', [])
                
                for test_item in sub_item.get('item', []):
                    request_name = test_item.get('name', None)
                    if current_method not in self.request_name_dict:
                        self.request_name_dict[current_method] = []
                    self.request_name_dict[current_method].append(request_name)
                    
                    for event in test_item.get('event', []):
                        if event['listen'] == 'test':
                            for script_line in event['script']['exec']:
                                match = self.pattern.search(script_line)
                                if match:
                                    if request_name not in self.test_dict:
                                        self.test_dict[request_name] = []
                                    self.test_dict[request_name].append(match.group(1))

    # Extract requset url.
    def extract_request_url(self):
        for main_item in self.json_data['item']:
            for sub_item in main_item.get('item', []):
                for test_item in sub_item.get('item', []):
                    request_name = test_item.get('name', None)

                    if request_name not in self.request_url:
                        original_url = test_item['request']['url']['raw']
                        replaced_url = self.pattern_url.sub(
                            lambda m: self.collection_variables.get(m.group(1), m.group(0)), original_url)
                        self.request_url[request_name] = replaced_url

    # Extract resquest body.
    def extract_request_body(self):
        for main_item in self.json_data['item']:
            for sub_item in main_item.get('item', []):
                for test_item in sub_item.get('item', []):
                    request_name = test_item.get('name', None)

                    if request_name not in self.request_body:
                        self.request_body[request_name] = ""
                        request = test_item.get('request', [])
                        body = request.get('body', [])

                        if body != []:
                            replaced_body = self.pattern_url.sub(
                                lambda m: self.collection_variables.get(m.group(1), m.group(0)), body.get('raw', None))
                            self.request_body[request_name] += replaced_body

    # Send request and get response.
    def extract_response_body(self):
        for main_item in self.json_data['item']:
            for sub_item in main_item.get('item', []):
                for test_item in sub_item.get('item', []):
                    request_name = test_item.get('name', None)
                    current_method = sub_item.get('name', [])

                    if request_name not in self.response_body:
                        base_url = self.request_url[request_name]
                        base_body = self.request_body[request_name]
                        self.response_body[request_name] = ""

                        if current_method == "POST":
                            response_data = requests.post(base_url, data=base_body, headers=self.headers)
                            response_str = response_data.json()

                            try:
                                response_str = str(response_str)
                                response_json = json.loads(response_str)
                                if isinstance(response_json, list):
                                    self.response_body[request_name] += json.dumps(response_json[1])
                                elif isinstance(response_json, dict):
                                    new_dict = {}
                                    for key in response_json:
                                        value = response_json[key]
                                        if isinstance(value, list) and len(value) > 0:
                                            new_dict[key] = value[0]
                                        else:
                                            new_dict = response_json
                                    self.response_body[request_name] += json.dumps(new_dict)
                            except json.JSONDecodeError as e:
                                self.response_body[request_name] += response_str
                        
                        elif current_method == "GET":
                            response_data = requests.post(base_url, data=base_body, headers=self.headers)
                            response_str = response_data.json()

                            try:
                                response_str = str(response_str)
                                response_json = json.loads(response_str)
                                if isinstance(response_json, list):
                                    self.response_body[request_name] += json.dumps(response_json[1])
                                elif isinstance(response_json, dict):
                                    new_dict = {}
                                    for key in response_json:
                                        value = response_json[key]
                                        if isinstance(value, list) and len(value) > 0:
                                            new_dict[key] = value[0]
                                        else:
                                            new_dict = response_json
                                    self.response_body[request_name] += json.dumps(new_dict)
                            except json.JSONDecodeError as e:
                                self.response_body[request_name] += response_str

    # Extract collection tests.
    def extract_collection_tests(self):
        for event in self.json_data['event']:
            for script_line in event['script']['exec']:
                match = self.pattern.search(script_line)
                if match:
                    self.collection_tests.append(match.group(1))

    def extract_all_data(self):
        self.extract_collection_variables()
        self.extract_tests()
        self.extract_request_url()
        self.extract_request_body()
        self.extract_response_body()
        self.extract_collection_tests()

        

        return {
            "request_method": self.request_method,
            "test_dict": self.test_dict,
            "request_body": self.request_body,
            "collection_tests": self.collection_tests,
            "request_url": self.request_url,
            "response_body": self.response_body,
            "request_name_dict": self.request_name_dict
        }
        

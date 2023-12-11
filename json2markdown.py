from utils import read_json_file, set_args, convert_to_markdown
from extractor import PostmanCollectionExtractor

class JsonToMarkdownConverter:
    def __init__(self, json_file_path, markdown_file_path):
        self.json_file_path = json_file_path
        self.markdown_file_path = markdown_file_path

    def save_markdown_content(self, markdown_content):
        with open(self.markdown_file_path, 'w', encoding='utf-8') as md_file:
            md_file.write(markdown_content)

    def convert_json_to_markdown(self):
        print("Generating markdown file ...")
        json_data = read_json_file(self.json_file_path)
        postman_extractor = PostmanCollectionExtractor(json_data)
        pm_test_texts = postman_extractor.extract_all_data()
        markdown_content = convert_to_markdown(pm_test_texts)
        self.save_markdown_content(markdown_content)
        print(f"Markdown content saved to {self.markdown_file_path}")

if __name__ == "__main__":
    args = set_args()
    
    json_file_path = args.json_dir
    markdown_file_path = './output_markdown_file.md'

    converter = JsonToMarkdownConverter(json_file_path, markdown_file_path)
    converter.convert_json_to_markdown()

import os
import re

def replace_string_in_files(root_dir, old_string, new_string):
    old_string_pattern = re.escape(old_string)
    for root, _, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # if file_path.endswith(".py") == False and file_path.endswith(".ipynb") == False:
            if file_path.endswith(".ipynb") == False:
                continue

            with open(file_path, 'r', encoding='utf-8') as f:
                print(f"reading file {file_path}")
                content = f.read()
            replaced_content = re.sub(old_string_pattern, new_string, content)
            if content != replaced_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(replaced_content)

root_dir = '/Users/abhishek/git/Awesome-CloudOps-Automation/'
old_string = "https://unskript.com/assets/favicon.png"
new_string = 'https://storage.googleapis.com/unskript-website/assets/favicon.png'
replace_string_in_files(root_dir, old_string, new_string)


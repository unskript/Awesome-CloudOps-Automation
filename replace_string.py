import os
import re
import sys

def replace_string_in_files(root_dir, old_string, new_string):
    old_string_pattern = re.escape(old_string)
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith("ipynb") == False:
                continue
            file_path = os.path.join(root, file)
            print(f"Processing file {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            replaced_content = re.sub(old_string_pattern, new_string, content)
            if content != replaced_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    print(f"Modifying file {file_path}")
                    f.write(replaced_content)

root_dir = sys.argv[1]

if os.path.isdir(root_dir) is False:
  print(f"given directory {root_dir} is not valid")
  exit(-1)

old_string = 'https://www.unskript.com/assets/favicon.png'
new_string = 'https://storage.googleapis.com/unskript-website/assets/favicon.png'
replace_string_in_files(root_dir, old_string, new_string)


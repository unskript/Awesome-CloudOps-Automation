import inspect
import re
import os
import importlib
from subprocess import run

def git_top_dir() -> str:
    """git_top_dir returns the output of git rev-parse --show-toplevel 

    :rtype: string, the output of the git rev-parse --show-toplevel command
    """
    run_output = run(["git", "rev-parse", "--show-toplevel"], capture_output=True)
    top_dir = run_output.stdout.strip()
    top_dir = top_dir.decode('utf-8')
    return top_dir

# Get the top-level directory of the Git repository
folder_path = git_top_dir()

def check_method_signature(param, method_name):
    if re.search(r"egion", param):
        # checks if that riff is "region" exactly
        pattern = r"(?<![^\s(,])region(?=\s|:|\))"
        return bool(re.findall(pattern, param+")"))
    else:
        return True

def check_module_methods(module):
    has_region = True
    module_act = importlib.util.module_from_spec(module)
    module_source = inspect.getsource(module_act)
    method_matches = re.findall(r"def (.*?)\)", module_source, flags=re.DOTALL)
    for method_match in method_matches:
        method_name = re.findall(r"(\w+)\s*\(", method_match)
        method_match_new = method_match.replace(method_name[0], "")
        if not check_method_signature(method_match_new, method_name[0]):
            has_region = False
    return has_region

if __name__ == '__main__':   
    current_file = os.path.abspath(__file__)
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.py') and os.path.abspath(file) != current_file:
                file_path = os.path.join(root, file)
                module_name = os.path.splitext(file)[0]
                try:
                    module = importlib.util.spec_from_file_location(module_name,file_path)
                    if not check_module_methods(module):
                        print(f"Error in module {file_path}")
                except Exception as e:
                    print(f"Error importing module {file_path}: {str(e)}")

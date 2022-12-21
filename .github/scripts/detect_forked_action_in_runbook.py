import json
import sys
import boto3
import sys
import os
import glob
from smart_open import smart_open

def read_file_contents(file_name):
    with open(file_name, mode= "r", encoding= "utf-8") as f:
        myfile = json.loads(f.read())
    return myfile

def check_code_block(l1,l2):
    l = [True if i in l1 else False for i in l2]
    check = all(l)
    return check

def create_code_lists(runbook,code_snippets):
    l1=[]
    l2=[]
    for x in runbook['cells']:
        if x['cell_type']=='code':
            for k,v in x['metadata'].items():
                if k=='action_uuid':
                    for each_element in code_snippets["properties"]["snippets"]["default"]:
                        for key,value in each_element.items():
                            #Checks if there is a UUID for the lego, if not, it is a custom lego (which has no UUID)
                            if key=='uuid':
                                if value==v:
                                    runbook_code_list = x["source"]
                                    snippets_code_list = each_element["code"]
                                    part_1="".join(snippets_code_list)
                                    code_1 = re.sub("\(err, hdl, args\).(.)*","",part_1)
                                    part_2="".join(runbook_code_list)
                                    part_3=re.sub("\n","",part_2)
                                    part_4 = re.sub("task.configure.(.)*", "",part_3)
                                    code_2 = re.sub("\(err, hdl, args\).(.)*","",part_4)
                                    #l1 has code from the code_snippets file obtained from S3
                                    l1.append(code_1)
                                    #l2 has code from the runbook file
                                    l2.append(code_2)
    return l1,l2

def get_file_from_s3(snippet_file: str):
    s3 = boto3.resource('s3')
    # build_number = 762
    # file_path = 's3://unskript-jenkins-dev/code_snippets/'+'build-'+str(build_number)+'/code_snippets.json'
    with smart_open(snippet_file, 'rb') as s3_source:
        s3_source.seek(0)
        file_contents = s3_source.read()
        json_file = json.loads(file_contents)
    return json_file


def main(code_snippet_file: str or None, ipynb_files: list or None):
    retVal = False

    if code_snippet_file is None:
        return False 
    
    if os.environ.get('USE_S3_SNIPPETS'):
        #Fetch the latest code snippet from S3 bucket
        # By default, we will be doing the read_local_code_snippets 
        # as it is more current.
        code_snippets = get_file_from_s3(code_snippet_file)
        
    
    # Fetch all  runbooks in awesome directory and run it with the checker
    #ipnb_files = glob.glob(awesome_dir + '/*/*.ipynb')

    for ipynb_file in ipynb_files:
        runbook = read_file_contents(ipynb_file)
        #Fetch the matching code for the legos using action UUID
        l1,l2=create_code_lists(runbook,code_snippets)
        #Check if the code matches
        if check_code_block(l1,l2):
            print(f"All Legos are pristine for {ipynb_file}")
            retVal = True
        else:
            print(f"Legos are forked for {ipynb_file}")
            return False 
    
    return retVal 
   
if __name__ == "__main__":
    # First argument would be the code-snippets file
    # Second argument would be the awesome directory 
    if len(sys.argv) > 1:
        if main(sys.argv[1], sys.argv[2:]):
            sys.exit(0)
        else:
            sys.exit(-1)

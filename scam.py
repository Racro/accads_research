import json
import os 

path = '/home/ritik/Downloads/2_19_Anno'

# Crawl through the directory and subdirectories to get all json files
json_files = []
for root, dirs, files in os.walk(path):
    for file in files:
        if file.endswith('.json'):
            json_files.append(os.path.join(root, file))

# Load the json files
files_of_interest = []

count = 0
for file in json_files:
    with open(file, 'r') as f:
        data = json.load(f)
        for i in data:    
            for j in i['annotations']:
                if j['completed_by']['email'] == 'cat.mai@nyu.edu' or j['completed_by']['email'] == 'ritik.r@nyu.edu': 
                    if 'malware' in str(j['result']) or 'scam' in str(j['result']):
                        fp = i['data']['image'].split('://')[1]
                        print(file, ',', fp)
                        os.system(f"cp /run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/{fp} ../scam/{file.split('/')[-1].replace('.json', '')}_{fp.split('/')[-1]}")
                        count += 1
            

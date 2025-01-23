import os
import json
import sys

fpath = '/home/ritik/Downloads/11_20_anno2/'
json_files = [fpath+f for f in os.listdir(fpath) if f.endswith('.json')]

manual_anno = {}
llm_anno = {}
common_anno = {}

for i in json_files: 
    a = json.load(open(i, 'r')) 
    # print(type(a))
    for d in a: 
        # print(type(d))
        key = (i.split('/')[-1].split('.')[0], d['data']['image'].split('/')[-1])
        # print('key', key)
        common_anno[key] = [[], []]
        llm_anno[key] = []

        for ann in d['annotations']: 
            # print(ann) 
            for res in ann["result"]: 
                if 'choices' in res["value"].keys():
                    if ann['completed_by']['email'] == 'jj3545@nyu.edu':
                        common_anno[key][0].append(res["value"]['choices'][0].split('(')[0].strip())
                    elif ann['completed_by']['email'] == 'ritik.r@nyu.edu':
                        common_anno[key][1].append(res["value"]['choices'][0].split('(')[0].strip())
                    else:
                        print("ERROR in annotator name")
                        sys.exit(0)
             
# csv_path = '/home/ritik/Downloads/llm_annot2_prompt4.csv'
csv_path = '/home/ritik/Downloads/llm_annot2_prompt4.csv'
import csv

with open(csv_path, 'r') as file:
    csv_reader = csv.reader(file)
    next(csv_reader)  # Skip the first line
    for row in csv_reader:
        try:
            key = (row[3], row[1])
            # print('key: ', key)
            # row[-2] = row[-2].replace("\'", "\"")
            
            # prompt3_with_explanations
            anno = json.loads(row[2].replace("{\'", "{\"").replace("\'}", "\"}").replace("\':", "\":").replace("], \'", "], \"").replace("\', \'", "\", \"").replace("[\'", "[\"").replace(": \'", ": \"").replace("\']", "\"]").replace("\", \'", "\", \"").replace("\'", ""))
            # print(1, anno)
            # print(row[-2])
            # anno = json.loads(row[-2])
            
            # prompt3_with_explanations
            # if len(anno.keys()) == 0:
            #     anno_keys = []
            # else:
            #     anno_keys = list(anno.keys())
            #     # print(anno)
            #     for i in range(len(anno_keys)):
            #         if 'explanation' in anno_keys[i]:
            #             llm_anno[key].append(anno['explanation'])
            #             anno_keys[i] = 'DELETE'
            #             continue
            #         anno_keys[i] = anno_keys[i].split('(')[0].strip('\n').strip().strip('"')
            # common_anno[key].append(anno)

            common_anno[key].append(anno['categories'])
            # count += 1
            # llm_anno[key].append(anno['explanations'])
            # print(anno['explanations'])
        except Exception as e:
            print('Error:', e, key)
            print(row[2].replace("{\'", "{\"").replace("\'}", "\"}").replace("\':", "\":").replace("], \'", "], \"").replace("\', \'", "\", \"").replace("[\'", "[\"").replace(": \'", ": \"").replace("\']", "\"]").replace("\", \'", "\", \"").replace("\'", ""))
            common_anno[key].append(['enter'])
# Write data to CSV 
# with open('common_csv_prompt4.csv', 'w', newline='') as csvfile:
with open('common_csv_prompt4_4o.csv', 'w', newline='') as csvfile:
# with open('common_csv_prompt4_with_explanations.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)

    # # Write header (optional)
    # writer.writerow(['source', 'filename', 'Julia', 'Ritik', 'LLM', 'explanation'])

    # for key, columns in common_anno.items():
    #     row = []
    #     row.append(key[0])
    #     row.append(key[1])
    #     for values_list in columns:
    #         # print(len(values_list))
    #         # Join inner list into a string, separated by commas
    #         value = ','.join(values_list)
    #         row.append(value)
    #     row.append(llm_anno[key])
    #     writer.writerow(row)

    # Write header (optional)
    writer.writerow(['Julia', 'Ritik', 'LLM'])

    for key, columns in common_anno.items():
        row = []
        # row.append(key[0])
        # row.append(key[1])
        for values_list in columns:
            # Join inner list into a string, separated by commas
            value = ','.join(values_list)
            row.append(value)
        # row.append(llm_anno[key])
        writer.writerow(row)



    
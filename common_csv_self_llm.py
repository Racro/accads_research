import os
import json
import sys
import pandas as pd

fpath = '/home/ritik/Downloads/12_20_anno/Anno_3_nolinks/'
json_files = [fpath+f for f in os.listdir(fpath) if f.endswith('.json')]

# List of annotator emails (provided explicitly)
annotator_email_list = [
    "hh3649@nyu.edu",
    "pr2480@nyu.edu",
    "cat.mai@nyu.edu",
    "mm13032@nyu.edu",
    "tdl7738@nyu.edu",
    "ritik.r@nyu.edu",
    "jj3545@nyu.edu"
]

# Placeholder for missing annotations
placeholder = "DNA"

common_anno = []
    
# Function to process LLM annotations from JSON
def process_llm_annotations_from_json(llm_annotations_file):
    with open(llm_annotations_file, 'r') as file:
        llm_data = json.load(file)
    llm_annotations_dict = {}
    for filename, annotation in llm_data.items():
        annotation_data = json.loads(annotation)
        if annotation_data["problematic"] == "True":
            llm_annotations_dict[(filename.split('/')[1], filename.split('/')[0])] = annotation_data.get("category", "Unknown Category")
        else:
            llm_annotations_dict[(filename.split('/')[1], filename.split('/')[0])] = "[]"
    return llm_annotations_dict

def process_manual_annotation_old():
    # manual_anno = {}
    # common_anno = {}

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

def process_manual_annotation_new():
    for f in json_files:
        # Read the JSON file
        with open(f, 'r') as file:
            json_data = json.load(file)

    # Process each image entry in the JSON file
        for entry in json_data:
            filename = entry['data']['image'].split('/')[-1]
            annotations = entry.get('annotations', [])
            
            # Create a dictionary to map email to choices value
            email_to_choices = {email: placeholder for email in annotator_email_list}
            
            for annotation in annotations:
                email = annotation['completed_by']['email']
                if annotation.get('result') == []:
                    email_to_choices[email] = ""  # Empty result recorded as empty string
                elif annotation.get('result'):
                    # Collect all 'choices' values for this annotator
                    all_choices = [result['value']['choices'] for result in annotation['result'] if result['type'] == 'choices']
                    flattened_choices = [choice for sublist in all_choices for choice in sublist]
                    email_to_choices[email] = " ; ".join(flattened_choices) if flattened_choices else ""
            
            # Merge data for JSON output
            merged_entry = {
                "Filename": filename,
                "JSON Filename": f.split('.')[0].split('/')[-1],
                "Annotations": email_to_choices
            }
            common_anno.append(merged_entry)

            # Add a row with filename, JSON filename, and annotations
            # row_data = [filename, f.split('/')[-1].split('.')[0]] + [email_to_choices[email] for email in annotator_email_list]
            # common_anno.append(row_data)
    
process_manual_annotation_new()

# Process LLM annotations from JSON
llm_annotations_file = 'llm_annotation.json'  # Update this with the actual file path
llm_annotations_dict = process_llm_annotations_from_json(llm_annotations_file)

# Add LLM annotations to the merged data
for entry in common_anno:
    llm_annotation = llm_annotations_dict.get((entry["Filename"], entry["JSON Filename"]), "DNA")
    entry["LLM Annotation"] = llm_annotation

# Convert merged data to DataFrame for CSV
csv_rows = []
for entry in common_anno:
    row = {
        "Filename": entry["Filename"],
        "JSON Filename": entry["JSON Filename"],
        **entry["Annotations"],
        "LLM Annotation": entry["LLM Annotation"]
    }
    csv_rows.append(row)

final_output_df = pd.DataFrame(csv_rows)

# Save the final merged data to a JSON file
final_merged_json_path = 'merged_annotations_rest.json'
with open(final_merged_json_path, 'w') as json_output_file:
    json.dump(common_anno, json_output_file, indent=4)

# Save the final merged data to a CSV file
final_output_csv_path = 'merged_annotations_rest.csv'
# final_output_df.to_csv(final_output_csv_path, index=False, sep='|')
final_output_df.to_csv(
    final_output_csv_path,
    index=False,
    sep='|',  # Delimiter remains '|'
    quoting=3,  # Quote all fields
    quotechar='"',  # Use double quotes for quoting
    escapechar='\\'  # Escape special characters like quotes
)

print(f"Merged JSON saved at: {final_merged_json_path}")
print(f"Merged CSV saved at: {final_output_csv_path}")    
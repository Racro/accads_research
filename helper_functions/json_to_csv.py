import json
import os
import csv
import re 

def via_jsons():
    # Folder containing the JSON files
    input_folder = "/home/ritik/Downloads/11_20_anno2/"
    output_csv = "output.csv"

    # Function to clean choices by removing text in parentheses
    def clean_choice_text(choice):
        # Use regex to extract text before '('
        return re.split(r"\s*\(", choice)[0]

    def extract_annotations(task):
        ritik_annotation = []
        julia_annotation = []

        for annotation in task["annotations"]:
            annotator_email = annotation["completed_by"]["email"]
            result = annotation.get("result", [])
            
            # Extract and clean all "choices"
            choices = [
                clean_choice_text(choice)
                for res in result
                if res["type"] == "choices" and "choices" in res["value"]
                for choice in res["value"]["choices"]
            ]

            if annotator_email == "ritik.r@nyu.edu":
                ritik_annotation = choices
            elif annotator_email == "jj3545@nyu.edu":
                julia_annotation = choices
        
        return ritik_annotation, julia_annotation


    # Function to process a single JSON file
    def process_json_file(json_file, source):
        with open(json_file, "r") as f:
            data = json.load(f)
        
        rows = []
        for task in data:
            img_name = os.path.basename(task["data"]["image"])
            ritik_annotation, julia_annotation = extract_annotations(task)
            rows.append({
                "img_name": img_name,
                "ritik_annotation": json.dumps(ritik_annotation),
                "julia_annotation": json.dumps(julia_annotation),
                "source": source
            })
        return rows

    # Gather data from all JSON files
    all_rows = []
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".json"):
            source = os.path.splitext(file_name)[0]  # Use the file name (without extension) as source
            file_path = os.path.join(input_folder, file_name)
            all_rows.extend(process_json_file(file_path, source))

    # Write to CSV
    with open(output_csv, "w", newline="") as csvfile:
        fieldnames = ["img_name", "ritik_annotation", "julia_annotation", "source"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)

    print(f"CSV file generated: {output_csv}")

def llm_json():
    llm = json.load(open('llm_annotation.json', 'r'))
    header = ['', 'img_name', 'llm_annotation',	'source']

    try:
        data = []

        for key in llm.keys():
            sub_data = []
            filename = key.split('/')[1]
            source = key.split('/')[0]

            anno = json.loads(llm[key])
            # print(anno)
            if anno['problematic'] == False:
                sub_data = ['0', filename, [], source]
            else:
                sub_data = ['0', filename, anno['category'], source]
            data.append(sub_data)

        with open('llm_anno_ritik.csv', mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write the header row
            if header:
                writer.writerow(header)

            # Write the data rows
            writer.writerows(data)
        
        print(f"Data successfully written")
    except Exception as e:
        print(f"Error writing to CSV file: {e}")

llm_json()

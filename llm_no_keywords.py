import base64
from openai import OpenAI
import os
import pandas as pd
import json
import requests

# # Initialize OpenAI API with your key
api_key = os.getenv("OPENAI_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_KEY environment variable.")

# # Initialize OpenAI client
client = OpenAI(api_key=api_key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
    # return image_file
        return base64.b64encode(image_file.read()).decode('utf-8')

csv_file = '/home/ritik/work/pes/accads_research/ground_truth.csv'
df = pd.read_csv(csv_file)

# Extract the first two columns
selected_columns = df.iloc[:, :2]

# Iterate over each row excluding the header
rows = selected_columns.itertuples(index=False, name=None)

# Display the rows
row_list = []
for row in rows:
    row_list.append(row)

all_annot = {}
explanations = {}

interesting_files = [
    # 'www.21usdeal.com_192a_7_adshot_3.png',
    'www.allears.net_9d72_5_adshot_1.png',
    # 'www.biblegateway.com_67f2_4_adshot_0.png',
    # 'www.dailynous.com_8f33_4_adshot_1.png',
    # 'www.globalnews.ca_c026_7_adshot_3.png',
    # 'www.jansatta.com_6ff2_8_adshot_4.png',
    # 'www.legacy-wow.com_c1db_4_adshot_0.png',
    # 'www.motherjones.com_433a_7_adshot_3.png'
]

for (key, row) in row_list:
    filename = key.split("'")[1]
    json_filename = row.split("'")[1]
    
    ocr_text = json.load(open(f'accads_crawler/image_hashing/ocr_{json_filename}.json', 'r'))[filename]
    # print(ocr_text)

    # if filename not in interesting_files:
    #     continue
    image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/annotation_tasks/selected_adshots_{json_filename}/{filename}'
    if not os.path.exists(image_folder):
        image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/annotation_tasks/selected_adshots_{json_filename}_nolinks/{filename}'
        print('MISMATCH', filename, json_filename)
    if not os.path.exists(image_folder):
        all_annot[image_folder] = 'DNA'
        explanations[image_folder] = 'DNA'
        continue

    base64_image = encode_image(image_folder)
    print(ocr_text)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
    # body = {
        messages = [
        {
            "role": "user",
            "content": 
                # f"""Analyze the attached ad and determine if it is problematic or not strictly based on the taxonomy.
                # image:  "data:image/png;base64,{base64_image}"
                # """
                [
                    {  
                        "type": "text",
                        "text": """Analyze the attached ad and determine if it is problematic or non-problematic strictly based on the taxonomy. If problematic, return the category title you find it to be belonging to as the key value. Otherwise return an empty string as the key value"""
                    },
                    {
                        "type": "text",
                        "text": f"{ocr_text}"
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url":  f"data:image/png;base64,{base64_image}"
                        },
                    },
                ],
        },
        {
            "role": "system",
            "content":
                """You are an expert in evaluating online display advertisements based on a taxonomy derived from ad exchange policies and user perception studies. Analyze the provided advertisement screenshot to determine if it is problematic, strictly using the provided taxonomy. 
                ## 
                The text present (OCR output) in the ad creative is also provided as an additional input for processing and identifying any problematic behaviour.
                ##
                The taxonomy includes a title and definition for each category. Use the definitions and your own understanding as primary guides.  
                ##  
                Be conservative in your classification: Only classify if the ad clearly and confidently fits a category. If in doubt, classify it as non-problematic.  
                ##
                Return a JSON object with the following structure:  
                1. A `categories` key containing a list of applicable categories. If non-problematic, return an empty list as the value.  
                2. An `explanations` key providing a rationale for each identified category. Include detailed reasoning for each flagged category.  
                ##  
                For screenshots with multiple ads, return the superset of categories covering all ads.
                ###
                Taxonomy:
                1. Regulations
                Definition: Ads deemed inappropriate for younger audiences (Below 18 years) due to product or content nature. 
                ##
                2. Inappropriate or Offensive Content
                Definition: Ads containing language, visuals, or themes that may be offensive, graphic, or disrespectful towards certain individuals or communities.
                ##
                3. Deceptive Claims and Exaggerated Benefits 
                Definition: Ads that make unverified or exaggerated claims about a product's or service's effectiveness, often with the intent to mislead consumers. Unlike Dark Patterns, these ads include specific claims in their content, rather than relying solely on clickbait tactics.
                ##
                4. Dark Patterns and Manipulative Design
                Definition: Ads that use deceptive design techniques to manipulate user behavior, such as clicking, subscribing, or sharing information unintentionally.
                ##
                5. User Experience Disruption
                Definition: Ads that degrade the user experience by being overly intrusive, annoying, or difficult to navigate
                ##
                6. Political and Socially Sensitive Topics
                Definition: Ads related to political topics that could polarize or manipulate public opinion, especially during sensitive times like elections.
                """
        },
        ],
        temperature=0,
        response_format={'type':'json_object'}
    )

    
    res = response.choices[0].message.content
    print(res)
    # all_annot.append(res)
    try:
        res = json.loads(res)
        all_annot[image_folder] = ';'.join(res["categories"])
        explanations[image_folder] = res["explanations"]
    except:
        all_annot[image_folder] = res
        explanations[image_folder] = res
    json.dump(all_annot, open('llm_annotation_dict_no_keywords.json', 'w'))
    json.dump(explanations, open('llm_annotation_explanations_no_keywords.json', 'w'))

df['llm_annotation'] = list(all_annot.values())
df['explanations'] = list(explanations.values())
df.to_csv('llm_annotation_no_keywords.csv', index=False)
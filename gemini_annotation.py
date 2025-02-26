import os
import base64
import pandas as pd
import json
import requests
import sys
import re
from PIL import Image
import google.generativeai as genai
from portkey_ai import Portkey
# from google.generativeai.types import GenerateContentConfig

portkey = Portkey(
    base_url="https://ai-gateway.apps.cloud.rt.nyu.edu/v1/",
    api_key="hvjetSyLGAc0U8Ry2qHr2VCr0Cku",  # Replace with your Portkey API key
    virtual_key="vertex-ai-hpc-i-c1b146",  # Replace with your virtual key for Google
)

# Configure the system instructions (taxonomy details) and other parameters
system_instruction = """You are an expert in evaluating online display advertisements based on a taxonomy derived from ad exchange policies and user perception studies. Analyze the provided advertisement screenshot to determine if it is problematic, strictly using the provided taxonomy. 
    ## 
    The text present (OCR output) in the ad creative is also provided as an additional input for processing and identifying any problematic behaviour.
    ##
    The taxonomy includes a title, definition, keywords, and notes for each category. Strictly use the definitions, keywords, and notes as primary guides. The keywords are exhaustive and represent the themes covered in each category.  
    ##  
    Be conservative in your classification: Only classify if the ad clearly and confidently fits a category. If in doubt, classify it as non-problematic.  
    ##
    Since it is a multi-label classification, multiple categories can be chosen. Return a JSON object with the following structure:  
    1. A `categories` key containing a list of applicable categories. If non-problematic, return an empty list as the value.  
    2. An `explanations` key providing a rationale for each identified category. Include detailed reasoning for each flagged category.  
    ##  
    For screenshots with multiple ads, return the superset of categories covering all ads. 
    ###
    Taxonomy:
    1. Regulations
    Definition: Ads deemed inappropriate for younger audiences (Below 18 years) due to product or content nature. 
    Keywords: sexually suggestive, Cannabinoids, alcohol, gambling/sweepstakes, cosmetic interventions, hazardous goods, drug use, Weight-reduction regimes or establishments, Lottery, E-Cigarettes, Prescription-only medicines, Dating sites
    #
    Note: 
    - Classify only if clear evidence like explicit exposure, provocative poses, or overtly suggestive context exists; avoid bias towards modeling images. 
    - Sexually suggestive ads should be classified into both `Regulations` and `Inappropriate or Offensive Content` if the content is derogatory or explicit.
    ##
    2. Inappropriate or Offensive Content
    Definition: Ads containing language, visuals, or themes that are offensive, hateful, or disrespectful towards general public and not focused groups.
    Keywords: Sexually explicit, offensive language, violent acts, hate speech, hookup, graphic images, racially insensitive, conspiracy theories, disrespectful religious/sacred content/profanity, trafficking, social issues, hacking
    #
    Note: 
    - Merely mentioning potentially sensitive topics (e.g., violence, religion) does not automatically make the ad offensive unless it is presented in a disturbing, demeaning, or shocking manner.
    - References to brand or domain names that contain edgy words or horror themes are not automatically classified as offensive.
    ##
    3. Deceptive Claims and Exaggerated Benefits 
    Definition: Ads that make unverified or exaggerated claims about a product's or service's effectiveness, often with the intent to mislead consumers. Unlike Dark Patterns, these ads include specific claims in their content, rather than relying solely on clickbait tactics.
    Keywords: 
        Health claims - No disclosure, Reasons for conditions, miracle cure, weight loss, scientifically proven, Dietary supplements, cosmetic beauty treatments, mental health services, false vaccine information, cheap substitutes
        Financial Claims - get rich quick, financial freedom, investment returns, guaranteed profits, False Tax Promises, Crypto Gain Misrepresentation, debt relief
        Environmental Claims - No disclosure, greenwashing (eco-friendly, sustainable, green product, carbon-neutral, environmentally safe), eco-friendly, ethical sourcing, organic, waste reduction claims
        Other Impossible Claims - overpromising, instant results, transform your life, best in the world/market, one-of-a-kind, never-before-seen, guaranteed satisfaction, exclusive deal, legal claims
    #
    Note: 
    - No disclosures are required for finance-related ads offering incentives like 'up to a certain amount' for account openings. 
    - Focus on identifying financial claims that appear fraudulent or excessively unrealistic, rather than scrutinizing all claims.
    ##
    4. Dark Patterns and Manipulative Design
    Definition: Ads that use deceptive design techniques to manipulate user behavior, such as clicking, subscribing, or sharing information unintentionally.
    Keywords: clickbait, social engineering, scarcity tactics, confirmshaming, countdown timers, fake buttons, sensationalism, fake testimonials, fake celebrity endorsements, urgency, last chance, your data is at risk, fear tactics, emergency, danger, don't miss out, Incomplete sentences using ...
    #
    Note: 
    - If the substring '...' is present in the provided ad text (**ocr text**) or the Ad image, it should always be classified as **Dark Patterns and Manipulative Design**. 
    - Fake or multiple buttons present in the Ad image are problematic as well. 
    ##
    5. User Experience Disruption  
    Definition: Ads that degrade the user experience by being overly intrusive, misleading, repetitive, or lck of advertiser information. This includes ads with unnatural, or highly manipulated imagery that causes confusion or doubt about authenticity.  
    Keywords: annoying, intrusive (revealing locations), auto-playing video, difficult-to-close pop-ups, disruptive ad formats, ad loading speed, unclear labeling of sponsored content. Ad quality (image), No Information (text/image) - for context.  
    #
    Note:
    - Ads containing **map snippets** indicating proximity to the user's location are considered intrusive, classify them as **User Experience Disruption**.
    - Multiple **identical or nearly identical ads** (same text and design) appearing in close proximity in the ad screenshot, classify them as **User Experience Disruption**. 
    - Ignore popup notifications originating from or local to the website itself.
    ##
    6. Political and Socially Sensitive Topics
    Definition: Ads related to political topics that could polarize or manipulate public opinion, especially during sensitive times like elections.
    Keywords: No disclosure (endorsements), election campaigns, fake endorsements, fake news, propaganda (climate change, LGBTQ rights, racial justice, religious freedom, abortion, immigration policy), defaming candidates
    #
    Note: 
    - Classify specific propaganda ads if the content undermines trust or portrays a person or entity in a detrimental or questionable manner.
"""

def encode_image(image_path):
    # This function is kept in case you need a base64 version.
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Load your CSV file and extract the first two columns
csv_file = '/home/ritik/work/pes/accads_research/json_and_csv/ground_truth.csv'
df = pd.read_csv(csv_file)
selected_columns = df.iloc[:, :2]
rows = selected_columns.itertuples(index=False, name=None)

row_list = []
for row in rows:
    row_list.append(row)

all_annot = {}
explanations = {}

patterns = ['search', 'suv deals', 'suchergebnisse', 'suchanzeigen']

for (key, row) in row_list[:2]:
    # Extract file and json filenames from the CSV values
    filename = key.split("'")[1]
    json_filename = row.split("'")[1]

    # Load OCR text from the corresponding JSON file
    ocr_path = f'accads_crawler/image_hashing/ocr_{json_filename}.json'
    ocr_text = json.load(open(ocr_path, 'r'))[filename]

    # Determine the image file path (try one folder, then another)
    image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/annotation_tasks/selected_adshots_{json_filename}/{filename}'
    if not os.path.exists(image_folder):
        image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/annotation_tasks/selected_adshots_{json_filename}_nolinks/{filename}'
        print('MISMATCH', filename, json_filename)
    if not os.path.exists(image_folder):
        all_annot[image_folder] = 'DNA'
        explanations[image_folder] = 'DNA'
        continue  # Skip to next row if image is not found

    # Open the image using Pillow
    try:
        ad_image = Image.open(image_folder)
    except Exception as e:
        print(f"Error opening image {image_folder}: {e}")
        all_annot[image_folder] = 'Error'
        explanations[image_folder] = str(e)
        continue

    # For Gemini API, we build a multimodal prompt as a list:
    # 1. The user instruction
    # 2. The OCR text extracted from the ad
    # 3. The image (as a PIL Image object)
    contents = [
        system_instruction,
        ocr_text,
        ad_image,
        "Analyze the attached ad and determine if it is problematic or non-problematic strictly based on the taxonomy. If problematic, return the category title you find it to be belonging to as the key value. Otherwise return an empty string as the key value. Analyze all possible sub-ad images present as well. Identify the brand name from the ad image and report it as a separate key *brand*. If multiple ads exist, report 'multiple brands'. If no brand identification is possible, report *None* in the value."
    ]


    # Call the Gemini Flash API (using the 1.5 Flash 8B model)
    response = portkey.chat.completions.create(
    messages=[
        {"role": "system", "content": "You are not a helpful assistant"},
        {"role": "user", "content": "Say this is a test"},
    ],
    model="gemini-1.5-flash-8b",
)


    res = response.text
    print(res)

    try:
        res = json.loads(res)
        print(res)
        # Optionally add extra explanations based on OCR content
        res["explanations_extra"] = []

        if '...' in ocr_text and 'Dark Patterns and Manipulative Design' not in res.get('categories', []):
            res.setdefault("categories", []).append('Dark Patterns and Manipulative Design')
            res["explanations_extra"].append('The substring "..." is present in the OCR output or ad image.')

        if res.get('brand') in ['None'] or any(re.search(pattern, ocr_text.lower()) for pattern in patterns):
            if 'User Experience Disruption' not in res.get("categories", []):
                res.setdefault("categories", []).append('User Experience Disruption')
                res["explanations_extra"].append('Ads with no clear advertiser information are classified under User Experience Disruption.')

        all_annot[image_folder] = ';'.join(res.get("categories", []))
        explanations[image_folder] = res.get("explanations", [])
    except Exception as e:
        print('ERROR parsing response:', res, e)
        all_annot[image_folder] = res
        explanations[image_folder] = res

    json.dump(all_annot, open('llm_annotation_dict.json', 'w'))
    json.dump(explanations, open('llm_annotation_explanations.json', 'w'))

df['llm_annotation'] = list(all_annot.values())
df['explanations'] = list(explanations.values())
df.to_csv('llm_annotation_offensive.csv', index=False)

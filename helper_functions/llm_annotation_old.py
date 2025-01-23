import base64
from openai import OpenAI
import os
import pandas as pd
import json
import requests

# # Initialize OpenAI API with your key
# api_key = os.getenv("OPENAI_KEY")
# if not api_key:
#     raise ValueError("OpenAI API key not found. Please set the OPENAI_KEY environment variable.")

# # # Initialize OpenAI client
# client = OpenAI(api_key=api_key)

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
for (key, row) in row_list:
    filename = key.split("'")[1]
    json_filename = row.split("'")[1]
    
    image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/annotation_tasks/selected_adshots_{json_filename}/{filename}'
    if not os.exists(image_folder):
        image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/annotation_tasks/selected_adshots_{json_filename}_nolinks/{filename}'
        print('MISMATCH', filename, json_filename)
    if not os.exists(image_folder):
        all_annot[image_folder] = 'DNA'
        continue

    base64_image = encode_image(image_folder)

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
                        "text": """Analyze the attached ad and determine if it is problematic or not strictly based on the taxonomy. If problematic, return the category title you find it to be belonging to as the key value. Otherwise return an empty string as the key value"""
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
                """You are an expert trained to evaluate online display advertisements based on a specific taxonomy derived from various ad exchanges' ads policies and user perception studies. Your task is to analyze the provided advertisement screenshot to determine whether it is problematic or not, strictly based on the provided taxonomy. If the ad is problematic, classify it into one or more of the given taxonomy categories and return a JSON object with a "categories" key containing a list of the applicable category(s) as values. If not, return an empty strong as value to the "categories" key.
                ##
                The taxonomy contains a title, definition and set of keywords. The set of keywords are exhaustive and are representative of the different themes covered in the category. 
                ##
                Be conservative in your classification: Classify only if the ad clearly and confidently fits a category. Use the given definitions and keywords along with your understanding of each category as guiding anchors to identify problematic aspects.
                Return a JSON object with a "categories" key containing a list of the category(s) as values, plus an "explanations" key that provides your rationale for flagging the identified categories.

                ###
                Taxonomy:
                1. Age-Based (Inappropriate for Below 18 Audiences)
                Definition: Ads deemed inappropriate for younger audiences due to product or content nature. For example, ads that are sexually suggestive, alcohol, gambling, prohibited for minors, cosmetic interventions, hazardous goods, drug use, graphic violence, nudity, intense language, etc.
                ##
                2. Inappropriate or Offensive Content
                Definition: Ads with offensive or graphic themes disrespecting individuals or communities. For example, ads that use offensive language, violent acts, hate speech, sexually explicit, graphic images, racially insensitive, conspiracy theories, religious content, etc.
                Examples:
                    Ads using racial stereotypes or derogatory language targeting specific communities.
                    Ads depicting explicit violence, such as injury or combat scenes, without appropriate content warnings.
                Edge Cases: 
                    Ads that is not targeted at specific communities or individuals.
                ##
                3. Deceptive and Exaggerated Claims/Benefits 
                Definition: Ads promoting unverified claims like health claims and benefits (miracle cure, weight loss, scientifically proven, Dietary supplements, cosmetic beauty treatments, mental health services, etc.), promising financial returns without evidence (get rich quick, financial freedom, investment returns, guaranteed profits, crypto and blockchain, debt relief, etc.), making unverified claims about environmental benefits (greenwashing eco-friendly, sustainable, green product, carbon-neutral, environmentally safe, sustainable, eco-friendly, ethical sourcing, waste reduction claims, etc.), and other impossible claims.
                Note: No disclosures are required for the ads claiming upto a certain amount in lieu of account opening, etc for finance related ads.
                Examples:
                    Ads claiming "miracle cure for diabetes" without evidence.
                Edge Cases:
                    Ads stating "may help reduce symptoms" with disclosures.
                Examples:
                    Ads claiming "get rich quick" with no supporting evidence.
                    Edge Cases:
                    Ads for financial services with clear disclosures like "results may vary."
                    Ads promoting established crypto wallets or exchanges with clear disclosures.
                    Ads describing risks transparently, such as "Investments are subject to market risk."
                    Ads from established financial institutions provising interest rates/cashbacks with certain terms should be fine.
                Edge Cases:
                    Claims may be permissible if supported by verifiable evidence, appropriate disclosures, or regulatory/legal endorsements.
                ##
                4. Dark Patterns and Manipulative Design
                Definition: Ads using deceptive UI techniques to manipulate user behavior such as through the use of clickbait tectics, sensationalism, social engineering, scarcity or urgency or fear tactics, confirmshaming, fake testimonials/endorsements, etc.
                Examples:
                    Ads with countdown timers suggesting artificial urgency to push users into impulsive purchases.
                    Fake “X” buttons that lead to clicks rather than closing the ad.
                Edge Cases: 
                    Ads using urgency (e.g., "Limited time only!") but labeled as promotional content.
                ##
                5. User Experience Disruption
                Definition: Ads that negatively affect user experience by being intrusive or difficult to navigate. For example, ads that are annoying, intrusive, auto-playing video, difficult-to-close pop-ups, disruptive ad formats, ad loading speed, unclear labels, poor ad quality (image/text), minimal context, ambiguity, lack of clear messaging, etc.
                Examples:
                    Ads that automatically play sound or video, interrupt user activity.
                    Pop-up ads that are difficult to close, often with hidden or misleading exit buttons.
                Edge Cases: 
                    Ads with easily muted videos that don't hinder browsing.
                ##
                6. Fraud and Scam Content
                Definition: Ads promoting fraudulent schemes aimed at financially exploiting users such as subscription fraud, fake certificates, counterfeit currency, fake review manipulation, scam behavior, crypto scams, brand impersonation, unauthorized use, copyright violation, stolen images, etc.
                Examples:
                    Ads offering “certificates” or “licenses” with no valid accreditation or proof of authenticity.
                    Fake investment opportunities promise high returns with no financial backing or evidence.
                Edge Cases: 
                    Ads for legitimate online courses offering verifiable certificates.
                    Ads for crypto wallets or exchanges with clear disclosures.
                ##
                7. Political and Socially Sensitive Topics
                Definition: Ads related to political, social, or controversial topics that could polarize or manipulate public opinion such as having no poper disclaimer, election campaigns, controversial topics, social issues, influence, fake news, propaganda (climate change, LGBTQ rights, racial justice, religious freedom, abortion, immigration policy), etc.
                Ads supporting specific political candidates or parties, especially if they use misinformation to sway opinion.
                        Ads addressing controversial issues (e.g., climate change, social justice) that might exploit or manipulate emotional responses.
                    Edge Cases: 
                        Public service announcements or verified campaigns promoting social awareness.
                        Neutral content discussing political or social issues without bias or manipulation.                            
                """
        },
        ],
        temperature=0,
        response_format={'type':'json_object'}
    )

    
    res = response.choices[0].message.content
    print(res)
    # all_annot.append(res)
    all_annot[image_folder] = res

    json.dump(all_annot, open('llm_annotation_dict.json', 'w'))

df['llm_annotation'] = list(all_annot.values())
df.to_csv('llm_annotation.csv', index=False)
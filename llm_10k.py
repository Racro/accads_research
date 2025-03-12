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

fpath = '/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/llm_10k/'
folders = [f for f in os.listdir(fpath)]

all_annot = json.load(open('llm_annotation_dict_10k.json', 'r'))
explanations = json.load(open('llm_annotation_explanations_10k.json', 'r'))

annot_keys = []
for i in all_annot.keys():
    annot_keys.append('/'.join(i.split('/')[-2:]))

errors = []

for folder in folders:
    images = [i for i in os.listdir(fpath+folder)]

    for filename in images:        
        try:
            ocr_text = json.load(open(f'accads_crawler/image_hashing/ocr_{folder}.json', 'r'))[filename]
            if f'{folder}/{filename}' in annot_keys:
                print('already present')
                continue
            # print(ocr_text)

            # if filename not in interesting_files:
            #     continue
            image_folder = fpath+folder+'/'+filename
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
                                "text": """Analyze the attached ad and determine if it is problematic or non-problematic strictly based on the taxonomy. If problematic, return the category title you find it to be belonging to as the key value. Otherwise return an empty string as the key value
                                ###
                                If the ad images looks like a bad screenshot without images/text or a black/white screen, return an empty `category title` with `explanations` as `bad image`
                                """
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
                        The taxonomy includes a title, definition, keywords, and notes for each category. Use the definitions, keywords, and notes as primary guides. The keywords are exhaustive and represent the themes covered in each category.  
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
                        Keywords: sexually suggestive, Cannabinoids, alcohol, gambling/sweepstakes, cosmetic interventions, hazardous goods, drug use, graphic violence, intense language, Weight-reduction regimes or establishments, Lottery, E-Cigarettes, Prescription-only medicines, Dating sites
                        #
                        Note: Classify as sexually suggestive only if clear evidence like explicit exposure, provocative poses, or overtly suggestive context exists; avoid bias towards modeling images.
                        ##
                        2. Inappropriate or Offensive Content
                        Definition: Ads containing language, visuals, or themes that may be offensive, graphic, or disrespectful towards certain individuals or communities.
                        Keywords: offensive language, violent acts, hate speech, sexually explicit, hookup, graphic images, racially insensitive, conspiracy theories, disrespectful religious/sacred content/profanity, Cannabinoids, trafficking, social issues, hacking
                        #
                        Note: Depictions of religion or related elements are considered non-problematic unless they explicitly involve defamation or disrespect.
                        ##
                        3. Deceptive Claims and Exaggerated Benefits 
                        Definition: Ads that make unverified or exaggerated claims about a product's or service's effectiveness, often with the intent to mislead consumers. Unlike Dark Patterns, these ads include specific claims in their content, rather than relying solely on clickbait tactics.
                        Keywords: 
                            Health claims - No disclosure, Reasons for conditions, miracle cure, weight loss, scientifically proven, Dietary supplements, cosmetic beauty treatments, mental health services, false vaccine information, cheap substitutes
                            Financial Claims - get rich quick, financial freedom, investment returns, guaranteed profits, False Tax Promises, Crypto Gain Misrepresentation, debt relief
                            Environmental Claims - No disclosure, greenwashing (eco-friendly, sustainable, green product, carbon-neutral, environmentally safe), eco-friendly, ethical sourcing, organic, waste reduction claims
                            Other Impossible Claims - overpromising, instant results, transform your life, best in the world/market, one-of-a-kind, never-before-seen, guaranteed satisfaction, exclusive deal, legal claims
                        #
                        Note: No disclosures are required for finance-related ads offering incentives like 'up to a certain amount' for account openings. Focus on identifying financial claims that appear fraudulent or excessively unrealistic, rather than scrutinizing all claims.
                        ##
                        4. Dark Patterns and Manipulative Design
                        Definition: Ads that use deceptive design techniques to manipulate user behavior, such as clicking, subscribing, or sharing information unintentionally.
                        Keywords: clickbait, social engineering, scarcity tactics, confirmshaming, countdown timers, fake buttons, sensationalism, fake testimonials, fake celebrity endorsements, urgency, last chance, your data is at risk, fear tactics, emergency, danger, don't miss out, Incomplete sentences using ...
                        #
                        Note: If the substring '...' is present in the provided ad text (ocr output) or the Ad image and its representing an incompleted sentence, it should always be classified as Dark Patterns and Manipulative Design. Also fake or multiple buttons present in the Ad image are problematic as well. 
                        ##
                        5. User Experience Disruption
                        Definition: Ads that degrade the user experience by being overly intrusive, annoying, or difficult to navigate
                        Keywords: annoying, intrusive (revealing locations), auto-playing video, difficult-to-close pop-ups, disruptive ad formats, ad loading speed, unclear labeling of sponsored content. Ad quality (image), No Information (text/image) - for context
                        #
                        Note: Ignore fake popup notifications originating from the website itself. Classify as 'User Experience Disruption' only if the popup is clearly an ad. Also ads with no clear advertiser information falls into this category.
                        ##
                        6. Political and Socially Sensitive Topics
                        Definition: Ads related to political topics that could polarize or manipulate public opinion, especially during sensitive times like elections.
                        Keywords: No disclosure (endorsements), election campaigns, fake endorsements, fake news, propaganda (climate change, LGBTQ rights, racial justice, religious freedom, abortion, immigration policy), defaming candidates
                        #
                        Note: Classify specific propaganda ads if the content undermines trust or portrays a person or entity in a detrimental or questionable manner.
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
            json.dump(all_annot, open('llm_annotation_dict_10k.json', 'w'), indent=4)
            json.dump(explanations, open('llm_annotation_explanations_10k.json', 'w'), indent=4)
        except Exception as e:
            print(e)
            errors.append((e, f'{folder}/{filename}'))

json.dump(errors, open('errors_10k.json', 'w'))

# df['llm_annotation'] = list(all_annot.values())
# df['explanations'] = list(explanations.values())
# df.to_csv('llm_annotation.csv', index=False)
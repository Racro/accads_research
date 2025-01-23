import base64
from openai import OpenAI
import os
import pandas as pd
import json
import requests

# Initialize OpenAI API with your key
api_key = os.getenv("OPENAI_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_KEY environment variable.")

URL = "https://genai-prod-nyu-rit-ai-apicast-production.apps.cloud.rt.nyu.edu/chat-openai?gateway=default"

headers = {
    "AUTHORIZATION_KEY": api_key,
    "rit_access": "266|rr3953|gpt-4o-mini",
    "rit_timeout": "60",
    "Content-Type": "application/json"}

# # Initialize OpenAI client
# client = OpenAI(api_key=api_key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
    # return image_file
        return base64.b64encode(image_file.read()).decode('utf-8')

csv_file = '/home/ritik/work/pes/accads_research/common_csv_prompt3_with_explanations.csv'
df = pd.read_csv(csv_file)

# Extract the first two columns
selected_columns = df.iloc[:, :2]

# Iterate over each row excluding the header
rows = selected_columns.itertuples(index=False, name=None)

# Display the rows
row_list = []
for row in rows:
    row_list.append(row)

all_annot = []
for (key, row) in row_list:
    image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/selected_adshots_{key}/'
    image_files = [f for f in os.listdir(image_folder)]

    if row in image_files:
        print (row, row in image_files)
        image_path = image_folder + row

        base64_image = encode_image(image_path)

        # response = client.chat.completions.create(
        #   model="gpt-4o",
        body = {
            'messages': [
            {
                "role": "user",
                "content": 
                    # f"""Analyze the attached ad and determine if it is problematic or not strictly based on the taxonomy.
                    # image:  "data:image/png;base64,{base64_image}"
                    # """
                    [
                        {  
                            "type": "text",
                            "text": """Analyze the attached ad and determine if it is problematic or not strictly based on the taxonomy."""
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
                    """You are an expert ad analyst. Your task is to determine if an ad is problematic according to a predefined taxonomy of problematic categories. If the ad is problematic, classify it into one of the categories and identify a matching keyword from the taxonomy. Be conservative and provide your results only if confident. Output the result as a JSON object.
                    ###
                    Taxonomy:
                    1. Regulations (Age-Based (Inappropriate for below 18 audiences)) - 
                        Definition: Ads targeting or featuring content deemed inappropriate for younger audiences or sensitive groups due to the nature of the product or service.
                        Keywords: sexually suggestive, Cannabinoids, alcohol, gambling/sweepstakes, cosmetic interventions, hazardous goods, drug use, graphic violence, intense language, Weight-reduction regimes or establishments, Lottery, E-Cigarettes, Prescription-only medicines
                        Examples:
                            Ads promoting alcohol, gambling, or cosmetic surgery services, especially if displayed on platforms accessible to minors.
                            Ads with sexually suggestive imagery or language targeting a general audience without age restrictions.
                        Edge Cases: 
                            Ads for non-alcoholic beer branded for a general audience.
                            Ads may be acceptable if they include proper age-gating or explicit disclosures.
                    ##    
                    2. Inappropriate or Offensive Content - 
                        Definition: Ads containing language, visuals, or themes that may be offensive, graphic, or disrespectful towards certain individuals or communities.
                        Keywords: offensive language, violent acts, hate speech, sexually explicit, hookup dating, graphic images, racially insensitive, conspiracy theories, disrespectful religious/sacred content/profanity, Cannabinoids, trafficking, social issues 
                        Examples:
                            Ads using racial stereotypes or derogatory language targeting specific communities.
                            Ads depicting explicit violence, such as injury or combat scenes, without appropriate content warnings.
                        Edge Cases: 
                            Ads that is not targeted at specific communities or individuals.
                    ##
                    3. Deceptive and Exaggerated Claims/Benefits (Health Claims) -
                        Definition: Ads that make unverified or exaggerated claims about a product's or service's effectiveness, often intending to mislead the consumer.
                        Keywords: No disclosure, miracle cure, weight loss, scientifically proven, Dietary supplements, cosmetic beauty treatments, mental health services, false vaccine information
                        Examples:
                            Ads claiming "miracle cure for diabetes" without evidence.
                            Edge Cases:
                            Ads stating "may help reduce symptoms" with disclosures.
                    ##
                    4. Deceptive and Exaggerated Claims/Benefits (Financial Claims)
                        Keywords: No disclosure, get rich quick, financial freedom, investment returns, guaranteed profits, False Tax Promises, Crypto Gain Misrepresentation, debt relief
                        Examples:
                            Ads claiming "get rich quick" with no supporting evidence.
                            Edge Cases:
                            Ads for financial services with clear disclosures like "results may vary."
                            Ads promoting established crypto wallets or exchanges with clear disclosures.
                            Ads describing risks transparently, such as "Investments are subject to market risk."
                            Ads from established financial institutions provising interest rates/cashbacks with certain terms should be fine.
                    ##
                    5. Deceptive and Exaggerated Claims/Benefits (Environmental and ethical claims)
                        Keywords: No disclosure, overpromising, greenwashing (eco-friendly, sustainable, green product, carbon-neutral, environmentally safe), eco-friendly, ethical sourcing, fair trade, organic, waste reduction claims
                        Examples:
                            Ads claiming "100% sustainable" without verification
                        Edge Cases:
                            Ads mentioning "supports sustainability efforts" with clear disclosures.
                    ##
                    6. Deceptive and Exaggerated Claims/Benefits (Other Impossible claims)
                        Keywords: instant results, transform your life, best in the world/market, one-of-a-kind, never-before-seen, guaranteed satisfaction, exclusive deal, legal claims
                        Examples:
                            Ads promoting a product as "the only one of its kind" without credible proof. Claims of "100% customer satisfaction" without valid supporting data.
                        Edge Cases:
                            Claims may be permissible if supported by verifiable evidence, appropriate disclosures, or regulatory/legal endorsements.
                    ##
                    7. Dark patterns and manipulative design
                        Definition: Ads that use deceptive design techniques to manipulate user behavior, such as clicking, subscribing, or sharing information unintentionally.
                        Keywords: clickbait, social engineering, scarcity tactics, confirmshaming, countdown timers, fake buttons, sensationalism, fake testimonials, fake celebrity endorsements, urgency, last chance, your data is at risk, fear tactics, emergency, danger, don’t miss out
                        Examples:
                            Ads with countdown timers suggesting artificial urgency to push users into impulsive purchases.
                            Fake “X” buttons that lead to clicks rather than closing the ad.
                        Edge Cases: 
                            Ads using urgency (e.g., "Limited time only!") but labeled as promotional content.
                    ##
                    8. User Experience Disruption
                        Definition: Ads that degrade the user experience by being overly intrusive, annoying, or difficult to navigate.
                        Keywords: annoying, intrusive, auto-playing video, difficult-to-close pop-ups, disruptive ad formats, ad loading speed, unclear labeling of sponsored content. Ad quality (image), No Information (text/image) - for context
                        Examples:
                            Ads that automatically play sound or video, interrupt user activity.
                            Pop-up ads that are difficult to close, often with hidden or misleading exit buttons.
                        Edge Cases: 
                            Ads with easily muted videos that don't hinder browsing.
                    ##
                    9. Fraud and Scam Content
                        Definition: Ads promoting fraudulent schemes or products, often aimed at financially exploiting or deceiving users.
                        Keywords: subscription fraud, fake certificates, counterfeit currency, fake review manipulation, scam behavior, crypto scams, brand impersonation, unauthorized use, copyright violation, stolen images
                        Examples:
                            Ads offering “certificates” or “licenses” with no valid accreditation or proof of authenticity.
                            Fake investment opportunities promise high returns with no financial backing or evidence.
                        Edge Cases: 
                            Ads for legitimate online courses offering verifiable certificates.
                            Ads for crypto wallets or exchanges with clear disclosures.
                    ##
                    10. Political Content and Propaganda
                        Definition: Ads related to political topics that could polarize or manipulate public opinion, especially during sensitive times like elections.
                        Keywords: No disclosure, election campaigns, endorsements, fake news, propaganda (climate change, LGBTQ rights, racial justice, religious freedom, abortion, immigration policy), defaming candidates
                        Examples:
                            Ads supporting specific political candidates or parties, especially if they use misinformation to sway opinion.
                            Ads addressing controversial issues (e.g., climate change, social justice) that might exploit or manipulate emotional responses.
                        Edge Cases: 
                            Public service announcements or verified campaigns promoting social awareness.
                            Neutral content discussing political or social issues without bias or manipulation.
                    """
            },
            ],
            'temperature': 0
        }

        res = requests.post(URL, headers=headers, json = body)
        # res = response.choices[0].message.content
        print(res)
        all_annot.append(res.json())
        break
    else:
        print (row['img_name'], "MISSING IMAGE IN SOURCE FOLDER")
        all_annot.append("MISSING IMAGE IN SOURCE FOLDER")

json.dump(all_annot, open('llm_annotation.json', 'w'))
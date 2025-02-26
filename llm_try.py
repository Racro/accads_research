import base64
from openai import OpenAI
import os
import pandas as pd
import json
import requests
import sys

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
    # 'www.allears.net_9d72_5_adshot_1.png',
    # 'www.biblegateway.com_67f2_4_adshot_0.png',
    # 'www.dailynous.com_8f33_4_adshot_1.png',
    # 'www.globalnews.ca_c026_7_adshot_3.png',
    # 'www.jansatta.com_6ff2_8_adshot_4.png',
    # 'www.legacy-wow.com_c1db_4_adshot_0.png',
    # 'www.motherjones.com_433a_7_adshot_3.png'

    # 'control_under_18/www.bjpenn.com_4bab_11_adshot_7.png',
    # 'adblock_under_18/www.about-air-compressors.com_56f9_5_adshot_1.png',
    # 'adblock_under_18/www.joemygod.com_15a6_8_adshot_4.png',
    # 'control_germany/www.tvline.com_5f27_7_adshot_3.png',
    # 'control_US/www.rollingstone.com_5c4c_11_adshot_7.png',
    # 'adblock_over_18/www.actumma.com_db89_4_adshot_0.png',
    # 'adblock_germany/www.bigblueview.com_a1ea_8_adshot_4.png',
    # 'control_under_18/www.extremehowto.com_b2c4_4_adshot_0.png',
    # 'adblock_under_18/www.fark.com_e1f3_5_adshot_1.png',
    # 'adblock_under_18/www.montagna.tv_f955_4_adshot_0.png',
    # 'control_over_18/www.redstate.com_9363_4_adshot_0.png',
    # 'control_over_18/www.slashfilm.com_dcfb_31_adshot_27.png',
    # 'control_over_18/www.westernjournal.com_e3df_9_adshot_6.png',
    # 'control_US/www.pjmedia.com_9ebb_8_adshot_4.png',
    # 'adblock_over_18/www.zimbabwesituation.com_3756_6_adshot_5.png',
    # 'control_US/www.tmz.com_2f4f_8_adshot_4.png',
    # 'adblock_US/www.womanandhome.com_f75e_7_adshot_3.png',
    # 'control_over_18/www.hiconsumption.com_122d_5_adshot_1.png',

    'control_under_18/www.acte-deces.fr_2628_4_adshot_0.png',
    # 'control_under_18/www.gameitnow.com_d37f_5_adshot_1.png',
    # 'control_under_18/www.mundoboaforma.com.br_b4e0_7_adshot_4.png',
    # 'control_under_18/www.mundodeportivo.com_8060_4_adshot_2.png',
    # 'adblock_under_18/www.bjpenn.com_4bab_5_adshot_1.png',
    # 'adblock_under_18/www.bleachernation.com_f599_11_adshot_7.png',
    # 'adblock_under_18/www.journaldesfemmes.fr_7b53_6_adshot_2.png',
    # 'control_germany/www.giallozafferano.it_fd0d_6_adshot_2.png',
    # 'control_germany/www.mydramalist.com_ff20_5_adshot_1.png',
    # 'control_over_18/www.basketnews.lt_7327_7_adshot_3.png',
    # 'control_over_18/www.ski.com.au_5661_4_adshot_0.png',
    # 'control_over_18/www.techbric.com_6189_7_adshot_3.png',
    # 'control_over_18/www.curlingzone.com_9ab3_8_adshot_4.png',
    # 'control_over_18/www.road.cc_7aa4_7_adshot_4.png',
    # 'control_over_18/www.turnoffthelights.com_a84c_4_adshot_0.png',
    # 'control_over_18/www.wnd.com_957e_4_adshot_0.png',
    # 'control_US/www.allfamous.org_eb00_4_adshot_0.png',
    # 'control_US/www.curlingzone.com_1376_7_adshot_3.png',
    # 'control_US/www.genealogy.com_b9b3_7_adshot_3.png',
    # 'control_US/www.indgovtjobs.in_10d0_8_adshot_4.png',
    # 'control_US/www.manoramaonline.com_4f66_5_adshot_1.png',
    # 'control_US/www.shaalaa.com_d38d_5_adshot_1.png',
    # 'adblock_over_18/www.nme.com_c9af_9_adshot_5.png',
    # 'adblock_over_18/www.sbnation.com_6c93_11_adshot_7.png',
    # 'adblock_US/www.baby-chick.com_5c44_5_adshot_2.png',
]

# for row in interesting_files:
#     filename = row.split("/")[1]
#     json_filename = row.split("/")[0]
#     image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/annotation_tasks/selected_adshots_{json_filename}/{filename}'
#     if not os.path.exists(image_folder):
#         image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/annotation_tasks/selected_adshots_{json_filename}_nolinks/{filename}'
#         print('MISMATCH', filename, json_filename)
#     # os.system(f'eog {image_folder}')
#     os.system(f'cp {image_folder} ../user_disruption/')
#     # input()
#     continue

# sys.exit(0)


# for (key, row) in row_list:
    # filename = key.split("'")[1]
    # json_filename = row.split("'")[1]
for row in interesting_files:
    filename = row.split("/")[1]
    json_filename = row.split("/")[0]
    
    ocr_text = json.load(open(f'accads_crawler/image_hashing/ocr_{json_filename}.json', 'r'))[filename]
    # print(ocr_text)

    # if f'{json_filename}/{filename}' not in interesting_files:
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
                        "text": """Identify the brand name from the ad image. If no brand identification is possible, report *None*"""
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
                - Sexually suggestive ads should be classified into both **Regulations** and **Inappropriate or Offensive Content** if the content is derogatory or explicit.
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
                - No disclosures are required for **finance-related** ads offering incentives like 'up to a certain amount' for account openings. Focus on identifying financial claims that appear fraudulent or excessively unrealistic, rather than scrutinizing all claims.
                ##
                4. Dark Patterns and Manipulative Design
                Definition: Ads that use deceptive design techniques to manipulate user behavior, such as clicking, subscribing, or sharing information unintentionally.
                Keywords: clickbait, social engineering, scarcity tactics, confirmshaming, countdown timers, fake buttons, sensationalism, fake testimonials, fake celebrity endorsements, urgency, last chance, your data is at risk, fear tactics, emergency, danger, don't miss out, Incomplete sentences using ...
                #
                Note: 
                - If the substring '...' is present in the provided ad text (ocr output) or the ad image, it should always be classified as **Dark Patterns and Manipulative Design**. 
                - Also fake or multiple buttons present in the Ad image are problematic as well. 
                ##
                5. User Experience Disruption  
                Definition: Ads that degrade the user experience by being overly intrusive, misleading, repetitive, or lck of advertiser information. This includes ads with unnatural, or highly manipulated imagery that causes confusion or doubt about authenticity.  
                Keywords: annoying, intrusive (revealing locations), auto-playing video, difficult-to-close pop-ups, disruptive ad formats, ad loading speed, unclear labeling of sponsored content. Ad quality (image), No Information (text/image) - for context.  
                #
                Note:
                - Ads containing **map snippets** indicating proximity to the user's location are considered intrusive, classify them as **User Experience Disruption**.
                - Multiple **identical or nearly identical ads** (same text and design) appearing in close proximity in the ad screenshot, classify them as **User Experience Disruption**. 
                ##
                6. Political and Socially Sensitive Topics
                Definition: Ads related to political topics that could polarize or manipulate public opinion, especially during sensitive times like elections.
                Keywords: No disclosure (endorsements), election campaigns, fake endorsements, fake news, propaganda (climate change, LGBTQ rights, racial justice, religious freedom, abortion, immigration policy), defaming candidates
                #
                Note: 
                - Classify specific propaganda ads if the content undermines trust or portrays a person or entity in a detrimental or questionable manner.
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
    json.dump(all_annot, open('llm_annotation_dict.json', 'w'))
    json.dump(explanations, open('llm_annotation_explanations.json', 'w'))

df['llm_annotation'] = list(all_annot.values())
df['explanations'] = list(explanations.values())
df.to_csv('llm_annotation_offensive.csv', index=False)
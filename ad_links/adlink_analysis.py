import openai
import json
import os
import time
import requests

# Initialize OpenAI API with your key
# api_key = os.getenv("OPENAI_KEY")
# if not api_key:
#     raise ValueError("OpenAI API key not found. Please set the OPENAI_KEY environment variable.")

# # Initialize OpenAI client
# client = openai.OpenAI(api_key=api_key)

# Initialize OpenAI API with your key
api_key = os.getenv("OPENAI_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_KEY environment variable.")

URL = "https://genai-prod-nyu-rit-ai-apicast-production.apps.cloud.rt.nyu.edu/chat-openai?gateway=default"

headers = {
    "AUTHORIZATION_KEY": api_key,
    "rit_access": "266|rr3953|gpt-4o",
    "rit_timeout": "60",
    "Content-Type": "application/json"
}

# Function to extract ad exchange or server information using Chat API
def get_ad_info_from_url(url):
    try:
        # prompt = f"Identify the ad exchange/server, middle parties and the Advertiser (if possible) for the following URL - {url}. Also for abbreviated names or acronyms, mention their parent company as well. Please be very brief and dont explain (less than 50 words for each url). Use the format: Entity (Role)."

        # response = client.chat.completions.create(
        #     model="gpt-4o-mini",
        #     messages=[
        #         {"role": "system", "content": "You are an expert in analyzing ad-related URLs."}, {"role": "user", "content": prompt}],
        #     max_tokens=300,
        #     temperature=0.2,
        #     # logprobs=5  # Enable prompt caching
        # )

        body = {
            'messages': [
                {
                    "role": "user",
                    "content": 
                        f"Identify the entities for the url: {url}"
                },
                {
                    "role": "system",
                    "content":
                        """
                        You are an expert in analysing Display ad URLs. Your task is to determine the companies (Entities) that play the (role) of ad exchange/server, middle parties and the Advertiser (if possible) for the Ad using the provided URL. Also for abbreviated names or acronyms, mention their parent company as well. If there are multiple entities in a single role, output all of them with spearated commas.
                        ###
                        Please be conservative in your approach and only return results if you are sure. Return an empty list otherwise. 
                        Output format: Entity1 (Role1), Entity2 (Role2)"
                        """
                },
            ],
            'temperature': 0
        }

        res = requests.post(URL, headers=headers, json = body)
        print(res.json()['choices'][0]['message']['content'].strip())
        return res.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error processing batch: {e}")
        return [None] * len(url)
    
# def process_openai_output(fpath_input, fpath_output):
#     data = json.load(open(fpath_input, 'r'))
    
# Load the list of URLs to analyze
lst = ['control_US', 'control_germany', 'control_over_18', 'control_under_18', 'accads_US', 'accads_germany', 'accads_over_18', 'accads_under_18']

for keyword in lst:
    num_links_path = f'/home/ritik/work/pes/accads_research/num_links_{keyword}.json'
    num_links = json.load(open(num_links_path, 'r'))

    # Prepare URLs to be processed
    ads_links = {}
    for paths in num_links.keys():
        ads = num_links[paths]
        ad_data = json.load(open(paths, 'r'))
        for ad in ads:
            ads_links[ad] = ad_data[ad]["links"][0]

    # json.dump(ads_links, open(f'ad_links_{keyword}.json', 'w'))

    # Process URLs in batches and save results
    exchange_info = {}
    # ads_keys = list(ads_links.keys())

    output_file = f'rit_exchange_info_{keyword}.json'
    for ad in ads_links.keys():
        print(ad)
        info = get_ad_info_from_url(ads_links[ad])
        
        # Store the results
        exchange_info[ad] = info
        
        # Save to file after each batch to prevent data loss in case of interruption
        json.dump(exchange_info, open(output_file, 'w'))

    print(f"Processing complete. Exchange information saved for keyword: {keyword}.")
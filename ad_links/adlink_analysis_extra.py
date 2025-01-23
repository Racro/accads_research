import openai
import json
import os
import time
import requests
import ast

def ensure_list(input_string):
    try:
        # Attempt to evaluate the string as a Python literal
        result = ast.literal_eval(input_string)
        if isinstance(result, list):
            return result
    except (ValueError, SyntaxError):
        pass
    # If the input isn't a list or valid structure, wrap it in a list
    return [str(input_string)]
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
    "rit_access": "266|rr3953|gpt-4o-mini",
    "rit_timeout": "60",
    "Content-Type": "application/json"
}

# Function to extract ad exchange or server information using Chat API
def get_ad_info_from_url(urls):
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
                        f"Identify the entities for the urls: {str(urls)}"
                },
                {
                    "role": "system",
                    "content":
                        """
                        You are an expert in analysing Display ad URLs. Your task is to determine the companies (Entities) that play the (role) of ad exchange/server, middle parties and the Advertiser (if possible) for the Ad using the provided list of URLs. Also for abbreviated names or acronyms, mention their parent company as well. If there are multiple entities in a single role, output all of them with spearated commas.
                        ###
                        All the provided urls are from the ads appearing on the same website. You have the find the superset of all the entities appearing in the same role across all the links.
                        For example, website A has [l1, l2, l3] as links and advertiser1 belongs to l1 and advertiser2 belongs to l2. You should return [advertiser1, advertiser2] (Ad Exchange/Server). SImilarly for other roles.
                        ###
                        Please be conservative in your approach and only return results if you are sure. Return an empty list otherwise. Take time to analyse each url carefully and then return the results.
                        ###
                        Output format: [list of Entities (Ad Exchange/Servers), list of entities (Middle Parties), list of entities (Advertisers)]". No need to output aything other than the list. Omit same names within the same list. Trim the number of entities per role to 50.
                        """
                },
            ],
            'temperature': 0,
            'max_tokens': 2000
        }

        res = requests.post(URL, headers=headers, json = body)
        print(res.json()['choices'][0]['message']['content'].strip())
        return res.json()['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Error processing batch: {e}", res.json())
        return [None] * len(urls)
    
# def process_openai_output(fpath_input, fpath_output):
#     data = json.load(open(fpath_input, 'r'))
    
# Load the list of URLs to analyze
lst = ['control_US', 'control_germany', 'control_over_18', 'control_under_18', 'accads_US', 'accads_germany', 'accads_over_18', 'accads_under_18']

for keyword in lst:
    num_links_path = f'/home/ritik/work/pes/accads_research/ad_sizes_{keyword}.json'
    num_links = json.load(open(num_links_path, 'r'))

    # Prepare URLs to be processed
    ads_links = {}
    for fname in num_links.keys():
        ads_links[fname] = []
        ads = num_links[fname]
        # ad_data = json.load(open(paths, 'r'))
        for ad in ads:
            ads_links[fname].append(ad[0])

    # json.dump(ads_links, open(f'ad_links_{keyword}.json', 'w'))

    # Process URLs in batches and save results
    exchange_info = {}
    # ads_keys = list(ads_links.keys())

    output_file = f'rit_exchange_info_{keyword}_extra.json'
    for ad in ads_links.keys():
        try:
            print(ad)
            info = get_ad_info_from_url(ads_links[ad])
            
            # Store the results
            exchange_info[ad] = ensure_list(info)
            
            # Save to file after each batch to prevent data loss in case of interruption
            json.dump(exchange_info, open(output_file, 'w'))
        except Exception as e:
            print(e)
            print(info)
            exchange_info[ad] = []
            json.dump(exchange_info, open(output_file, 'w'))

    print(f"Processing complete. Exchange information saved for keyword: {keyword}.")
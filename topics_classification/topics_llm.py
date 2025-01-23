import openai
import json
import os
import time
import requests
import subprocess

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
                        f"Identify the IAB categories for the url: {url}"
                },
                {
                    "role": "system",
                    "content":
                        """
                        You are an expert in analysing website URLs and identifying which IAB category it belongs to. Your task is to determine the specific IAB category that the website belongs to based on prior knowledge on the website content. Please stick to the specific categories as included in the IAB taxonomy. There are mostly 1 category but there could be multiple too.
                        If you cannot find any category, take some time back and slowly rethink to come up with the category. If still not, try to guess the closest category.
                        ###
                        For example:
                        www.novelfull.com - ['/Books & Literature']
                        www.boursorama.com - ['/News/Business News', '/Finance/Investing', '/Finance/Banking']
                        www.wired2fish.com - ['/Hobbies & Leisure/Outdoors/Fishing']
                        ###
                        Please be conservative in your approach and only return results if you are sure without hallucinations. Return an empty list otherwise. 
                        Output format: [Category1, Category2, etc]"
                        """
                },
            ],
            'temperature': 0
        }

        res = requests.post(URL, headers=headers, json = body)
        # print(res.json()['choices'][0]['message']['content'].strip())
        try:
            return res.json()['choices'][0]['message']['content'].strip()
        except Exception as e:
            print(e, res.json())
    except Exception as e:
        print(f"Error processing batch: {e}")
        return [None] * len(url)
    

f = open('../accads_crawler/websites_1500.txt', 'r')
# websites = f.read().splitlines()
websites = json.load(open('no_result_websites.json', 'r'))
# print(websites)
# topics = {}
topics = json.load(open('website_topics_llm.json', 'r'))

for site in websites:
    for i in range(3):
        tld = site
        if 'http' in site:
            site = site.split('://')[1] 
            tld = site.split('/')[0]
            # print(tld)
        result = get_ad_info_from_url(tld)

        if result == None or result == "[]":
            continue
    topics[tld] = result
    print(tld, result)

    # print(tld, lines)

json.dump(topics, open('website_topics_llm.json', 'w'))
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
                        f"""Classify the given JavaScript into one of the seven categories based on following data:
                        ##
                        SOURCE URL - {src_name}
                        ##
                        SOURCE CODE - {src}
                        """
                },
                {
                    "role": "system",
                    "content": 
                        """
                        You are an expert at analyzing JavaScript files based on both their public source URL and the provided source code. In case source URL is not present or clear, resort to source code based analysis. Your task is to classify each JavaScript instance into one of the predefined categories. If none of the categories fit, classify it under "Others," which covers topics outside the first six categories.

                        The seven categories are:  
                        1. User Interface (UI) & DOM Interaction  
                        2. Data Processing & Business Logic  
                        3. API & Network Communication  
                        4. Asynchronous Programming & Task Management  
                        5. State Management & Storage  
                        6. Error Handling, Security & Optimization  
                        7. Others  

                        Take a thoughtful approach when determining the correct category. If you're unsure, take a moment to reconsider and identify the closest match. Only return results when you are certain, and avoid speculative guesses.

                        ### Examples:
                            - SOURCE URL - https://example.com/ui-handler.js, SOURCE - '// Toggles the visibility of a modal on button click
                            document.getElementById('open-modal').addEventListener('click', function () {
                                const modal = document.getElementById('modal');
                                if (modal.style.display === 'none') {
                                    modal.style.display = 'block';
                                } else {
                                    modal.style.display = 'none';
                                }
                            });' - User Interface (UI) & DOM Interaction
                            - SOURCE URL - https://api.example.com/fetch-data.js, SOURCE - '// Fetches data from a remote API and logs the response
                            async function fetchData() {
                                try {
                                    const response = await fetch('https://api.example.com/data');
                                    if (!response.ok) {
                                        throw new Error('Network response was not ok');
                                    }
                                    const data = await response.json();
                                    console.log(data);
                                } catch (error) {
                                    console.error('Error fetching data:', error);
                                }
                            }

                            fetchData();' - API & Network Communication

                        ### Output format:  
                        `Category`

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
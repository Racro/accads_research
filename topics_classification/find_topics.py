import json
import os
import subprocess

f = open('../accads_crawler/websites_1500.txt', 'r')
websites = f.read().splitlines()
# print(websites)
# topics = {}
topics = json.load(open('website_topics.json', 'r'))

for site in websites:
    if 'http' in site:
        site = site.split('://')[1] 
    tld = site.split('/')[0]
    # print(tld)
    result = subprocess.run(['python3.10', 'topics_classifier/classify.py', '-ct', 'topics-api', '-i', tld, '-ohr'], capture_output=True, text=True)

    lines = result.stdout.splitlines()
    for i in range(len(lines)):
        lines[i] = lines[i].split(tld)[1].strip()
    
    for topic in lines:
        topics[tld] = lines

    print(tld, lines)
json.dump(topics, open('website_topics.json', 'w'))
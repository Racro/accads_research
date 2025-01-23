# Agreement Value: 42.00% (562 matches out of 1338) - For all level agreement
# Agreement Value: 71.38% (955 matches out of 1338) - For 1st level agreement

import json
from rapidfuzz import fuzz
import sys

topics = json.load(open('website_topics.json', 'r'))
topics_llm = json.load(open('website_topics_llm.json', 'r'))

topics_llm_trimmed = {}
for key in topics_llm.keys():
    lst = []
    new_lst = []
    try:
        # for top in json.loads(topics_llm[key].replace("'", "\"")):
        for top in topics_llm[key]:
            if top[0] != "/":
                new_lst.append('/' + top)
                top = top.split('/')[0]
            else:
                new_lst.append(top)
                top = top.split('/')[1]
            # print(top)
            lst.append(top)
    except Exception as e:
        print(e)
        print(topics_llm[key])
        sys.exit(0)
        break
    topics_llm_trimmed[key] = lst
    topics_llm[key] = new_lst

unclassified = {}

combined = {}
topic_keys = list(topics.keys()) 
for key in topic_keys:
    if topics[key] == []:
        unclassified[key] = []
        del topics[key]
    # else:
    #     for i in range(len(topics[key])):
    #         topics[key][i] = topics[key][i].split('/')[1]

for key in topics_llm.keys():
    if key in unclassified.keys():
        continue
    # print(topics_llm[key])
    topics[key] = (list(set(topics[key])), list(set(topics_llm[key])))
# sys.exit(0)

# Fuzzy match function
def fuzzy_match(list1, list2, threshold=80):
    for item1 in list1:
        for item2 in list2:
            if fuzz.ratio(item1.lower(), item2.lower()) >= threshold or item2 in item1:
                return True
    # print(list1, list2)        
    return False

# Calculate agreement
matches = []
for site, categories in topics.items():
    if fuzzy_match(categories[0], categories[1]):
        matches.append(site)

# Agreement value
total_entries = len(topics)
agreement = len(matches) / total_entries * 100

print(f"Agreement Value: {agreement:.2f}% ({len(matches)} matches out of {total_entries})")

# for site in list(unclassified.keys()):
#     unclassified[site] = topics_llm[site]
# json.dump(unclassified, open('unclassification.json', 'w'))
# json.dump(topics_llm, open('website_topics_llm.json', 'w'))

# Find the topic cluster
topic_cluster = {}
for key in topics.keys():
    if topics[key] == []:
        topics[key] = topics_llm[key]
    else:
        topics[key] = topics[key][0]
    for top in topics[key]:
        top = top.split('/')[1]
        if top in topic_cluster.keys():
            topic_cluster[top] += 1
        else:
            topic_cluster[top] = 0
json.dump(dict(sorted(topic_cluster.items(), key=lambda item: item[1])), open('topic_cluster.json', 'w'))
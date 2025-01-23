import json

csvf = open('/home/ritik/work/pes/accads_research/llm_annotation_10k.csv', 'r')
cats = json.load(open('website_all_sankey.json', 'r'))

lines = csvf.read().splitlines()[1:]

# print(lines[1].split('\t'))
# for i in range(10):
#     print(lines[i])
# print(len(lines[1]))

data = {}
count = 0
for i in range(len(lines)):
    try:
        lst = lines[i].split('\t')
        # print(lst)
        site = lst[0].strip("{}'").split('_')[0]
        if 'definition' in site:
            continue
        cat = cats[site]
        key = lst[1].strip("{}'")

        if key not in data.keys():
            data[key] = [{}, {}]
        
        if lst[2] == '':
            data[key][1][cat] = data[key][1].get(cat, 0) + 1
        else:
            data[key][0][cat] = data[key][0].get(cat, 0) + 1
    except Exception as e:
        # print(e)
        print(count)
        print(key)
        count += 1

clusters = {
    "Finance & Business": ["Finance", "Business & Industrial", "Real Estate"], 
    "Lifestyle & Wellness": ["Beauty & Fitness", "Home & Garden", "Food & Drink", "Shopping"], 
    "Arts & Culture": ["Arts & Entertainment", "Books & Literature", "Hobbies & Leisure"], 
    "Travel & Mobility": ["Travel & Transportation", "Autos & Vehicles"], 
    "Sports & Recreation": ["Sports", "Games"], 
    "Digital Engagement": ["Online Communities", "Internet & Telecom"], 
    "Human Connections": ["People & Society", "Pets & Animals"], 
    "Current Affairs": ["News", "Law & Government"], 
    "Remaining Topics": ["Jobs & Education"] 
}

cluster_freq = {
    "Finance & Business": 0, 
    "Lifestyle & Wellness": 0, 
    "Arts & Culture": 0, 
    "Travel & Mobility": 0, 
    "Sports & Recreation": 0, 
    "Digital Engagement": 0, 
    "Human Connections": 0, 
    "Current Affairs": 0, 
    "Remaining Topics": 0
}

plot_data = {}
for key in data:
    plot_data[key] = [{}, {}]
    for cat in data[key][0].keys():
        for bc in clusters.keys():
            if cat in clusters[bc]:
                plot_data[key][0][bc] = plot_data[key][0].get(bc, 0) + data[key][0][cat]
                cluster_freq[bc] += data[key][0][cat]
                break
    for cat in data[key][1].keys():
        for bc in clusters.keys():
            if cat in clusters[bc]:
                plot_data[key][1][bc] = plot_data[key][1].get(bc, 0) + data[key][1][cat]
                cluster_freq[bc] += data[key][1][cat]
                break

json.dump(cluster_freq, open('cluster_freq.json', 'w'))
json.dump(plot_data, open('plot_data.json', 'w'))
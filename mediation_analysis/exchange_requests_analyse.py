import json
import numpy as np

a = json.load(open('exchange_requests_data_02_23.json'))['reqs']
b = json.load(open('exchange_requests_data_US.json'))['reqs']

a_keys = set(a.keys())
b_keys = set(b.keys())

# print(a_keys - b_keys)

a_lst = np.array([])
a_unique = set()
b_lst = np.array([])
b_unique = set()

for key in a_keys:
    diff = set(a[key]['adblock'].keys()) - set(a[key]['control'].keys())
    # if len(diff) > 0:
    a_lst = np.append(a_lst, len(diff))
    a_unique.update(diff)
for key in b_keys:
    diff = set(b[key]['adblock'].keys()) - set(b[key]['control'].keys())
    # if len(diff) > 0:
    b_lst = np.append(b_lst, len(diff))
    b_unique.update(diff)

print(a_lst)
print(np.mean(a_lst), np.mean(b_lst))
print(np.median(a_lst), np.median(b_lst))
print(np.std(a_lst), np.std(b_lst))

print(len(a_unique), len(b_unique), len(b_unique - a_unique))

## Mediation Analysis
med_analysis = {}
p_np = json.load(open('p_np.json', 'r'))

for key in (a_keys & b_keys):
    a_diff = set(a[key]['adblock'].keys()) - set(a[key]['control'].keys())
    b_diff = set(b[key]['adblock'].keys()) - set(b[key]['control'].keys())

    website = key.split('_')[0]
    
    pr_control = p_np['p']['control_US'].get(website, 0)
    pr_adblock = p_np['np']['adblock_US'].get(website, 0)

    if pr_control == 0 and pr_adblock == 0:
        continue

    med_analysis[website] = {'ctrl-ctrl': [len(a_diff), pr_control], 'adb-ctrl': [len(b_diff), pr_adblock]}

json.dump(med_analysis, open('med_analysis.json', 'w'))

print(len(a_keys))
for key in (a_keys & b_keys):
    a_diff = set(a[key]['adblock'].keys()) - set(a[key]['control'].keys())
    b_diff = set(b[key]['adblock'].keys()) - set(b[key]['control'].keys())

    website = key.split('_')[0]
    
    pr_control = p_np['p']['control_US'].get(website, -1) + p_np['p']['control_germany'].get(website, -1) + p_np['p']['control_under_18'].get(website, -1) + p_np['p']['control_over_18'].get(website, -1)
    pr_adblock = p_np['np']['adblock_US'].get(website, -1) + p_np['np']['adblock_germany'].get(website, -1) + p_np['np']['adblock_under_18'].get(website, -1) + p_np['np']['adblock_over_18'].get(website, -1)

    if pr_control == -4 or pr_adblock == -4:
        continue
    else:
        pr_control = p_np['p']['control_US'].get(website, 0) + p_np['p']['control_germany'].get(website, 0) + p_np['p']['control_under_18'].get(website, 0) + p_np['p']['control_over_18'].get(website, 0)
        
        pr_adblock = p_np['np']['adblock_US'].get(website, 0) + p_np['np']['adblock_germany'].get(website, 0) + p_np['np']['adblock_under_18'].get(website, 0) + p_np['np']['adblock_over_18'].get(website, 0) 

    med_analysis[website] = {'ctrl-ctrl': [len(a_diff), pr_control], 'adb-ctrl': [len(b_diff), pr_adblock]}

json.dump(med_analysis, open('med_analysis_all.json', 'w'))

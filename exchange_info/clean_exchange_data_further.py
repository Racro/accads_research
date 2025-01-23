import os
import json

files = [f for f in os.listdir('./') if f.startswith('cleaned')]

cats = ["Ad Exchange/Server", "Middle Parties", "Advertisers"]

blacklist_terms = ['parent company', 'various', 'potential', 'parameter', 'tracking', 'gclid', 'dclid']
fuzzy_change = [('alphabet', 'google'), ('meta', 'facebook'), ('google', 'google'), ('facebook', 'facebook'), ('amazon', 'amazon')]
# 4th check len = 1

for f in files:
    d = json.load(open(f, 'r'))
    for site in list(d.keys()):
        for cat in cats:
            lst = d[site][cat].split(',')
            new_lst = []
            for term in lst:
                term = term.lower().strip()
                check = 0
                if term == 'inc':
                    continue
                if len(term) <= 2:
                    continue
                if check == 0:
                    for i in blacklist_terms:
                        if i in term:
                            check = 1
                            break
                if check == 0:
                    for i in fuzzy_change:
                        if i[0] in term:
                            new_lst.append(i[1])
                            check = 1
                            break
                if check == 0:
                    new_lst.append(term)
            if len(new_lst) == 0:
                d[site][cat] = 'N/A'
            else:
                new_lst = list(set(new_lst))
                d[site][cat] = ','.join(new_lst)

    json.dump(d, open(f, 'w'), indent=4)
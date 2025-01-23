import os
import json

keyword1 = 'adblock_under_18'
keyword2 = 'accads_under_18'

filtered = json.load(open(f'accads_crawler/image_hashing/images_dedup_{keyword1}.json' ,'r'))
links_present = json.load(open(f'num_links_{keyword2}.json' ,'r'))
folder_path = '/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/over_18/control/adshots/'
target_path = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/selected_adshots_{keyword1}_nolinks'

# for key in links_present.keys():
#     for adshot in links_present[key]:
#         fpath = folder_path + adshot
#         if fpath in filtered:
#             os.system(f'cp {fpath} {target_path}')

all_adshots = []
for key in links_present.keys():
    for adshot in links_present[key]:
        all_adshots.append(adshot)

for fpath in filtered:
    fname = fpath.split('/')[-1]
    print(fname)
    if fname in all_adshots:
        continue
    else:
        os.system(f'cp {fpath} {target_path}')
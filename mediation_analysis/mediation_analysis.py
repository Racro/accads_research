import json
import numpy as np
import os
import sys
from mediation_analysis_llm import *
from exchange_requests import extract_urls

data_path = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/data_backup' 
# data_new = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/data_backup/data_02_23'
# data_old = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/data_backup/data_US'

lst_adb_new = [f for f in os.listdir(f'{data_path}/data_02_23/adblock') if f.endswith('.json')]
lst_adb_old = [f for f in os.listdir(f'{data_path}/data_US/adblock') if f.endswith('.json')]
lst_ctrl_new = [f for f in os.listdir(f'{data_path}/data_02_23/control') if f.endswith('.json')]
lst_ctrl_old = [f for f in os.listdir(f'{data_path}/data_US/control') if f.endswith('.json')]

full_list = list(set(lst_adb_new) & set(lst_adb_old) & set(lst_ctrl_new) & set(lst_ctrl_old))

def get_exchange_info(fp):
    reqs, a, b, c, d, reqs_all, if_exchange = extract_urls(fp, 'reqs')
    imgs, links, frameurl = extract_urls(fp, 'ads')
    return [set(reqs), set(a), set(b), set(c), set(d),set(reqs_all), set(if_exchange), set(imgs), set(links), set(frameurl)]
    # url_dict = {}    
    # for url in reqs:
    #     if url not in url_dict:
    #         url_dict[url] = 1
    #     else:
    #         url_dict[url] += 1
    # return url_dict.keys()


cases = ['control', 'adblock']
folders = ['data_US', 'data_02_23']
website_pool = []
prob_dict = {}
exchanges_dict = {}
data = {}
for folder in folders:
    prob_dict[folder] = {}
    exchanges_dict[folder] = {}
    for case in cases:
        prob_dict[folder][case] = {}
        exchanges_dict[folder][case] = {}

for filename in full_list:
    website = filename.split('.json')[0]
    print(website)
    # if filename not in lst_new:
    #     continue
    a = json.load(open(f'{data_path}/data_US/adblock/{filename}', 'r'))
    try:
        if a['data']['ads']["scrapeResults"]["nAdsScraped"] > 0:
            data[website] = {}
            website_pool.append(filename)
            # print(a['data']['ads']["scrapeResults"]["nAdsScraped"], b['data']['ads']["scrapeResults"]["nAdsScraped"])
            
            for folder in folders:
                exchange_info_control = ''
                for case in cases:
                    prob_dict[folder][case][website] = []
                    exchanges_dict[folder][case][website] = []
                    os.system(f'mkdir -p mediation_analysis/{folder}/{case}/{website}')
                    os.system(f"cp {data_path}/{folder}/{case}/{filename} mediation_analysis/{folder}/{case}/{website}") # json
                    
                    # if case is control
                    if case == 'control':
                        exchange_info_control = get_exchange_info(f'{data_path}/{folder}/{case}/{filename}')
                    # if case is adblock
                    if case == 'adblock':
                        image_files = [f for f in os.listdir(f'{data_path}/{folder}/{case}/adshots/') if f.startswith(website)]
                        prob = 0
                        all_ads = 0
                        for image_file in image_files:
                            os.system(f"cp {data_path}/{folder}/{case}/adshots/{image_file} mediation_analysis/{folder}/{case}/{website}")
                            llm_output = return_llm_output(f'{data_path}/{folder}/{case}/adshots/{image_file}')

                            if 'categories' not in llm_output:
                                continue
                            print(llm_output)
                            if llm_output['categories'] != []:
                                prob += 1
                                all_ads += 1
                                prob_dict[folder][case][website].append(image_file)
                            else:
                                all_ads += 1
                        exchange_info_adblock = get_exchange_info(f'{data_path}/{folder}/{case}/{filename}')

                        if all_ads == 0:
                            continue
                        exchanges_dict[folder][case][website] = [len(exchange_info_adblock[0] - exchange_info_control[0]), len(exchange_info_adblock[1] - exchange_info_control[1]), len(exchange_info_adblock[2] - exchange_info_control[2]), len(exchange_info_adblock[3] - exchange_info_control[3]), len(exchange_info_adblock[4] - exchange_info_control[4]), len(exchange_info_adblock[5] - exchange_info_control[5]), list(exchange_info_adblock[0] - exchange_info_control[0]), list(exchange_info_adblock[1] - exchange_info_control[1]), list(exchange_info_adblock[2] - exchange_info_control[2]), list(exchange_info_adblock[3] - exchange_info_control[3]), list(exchange_info_adblock[4] - exchange_info_control[4]), list(exchange_info_adblock[5] - exchange_info_control[5]), list(exchange_info_adblock[6] - exchange_info_control[6]), list(exchange_info_adblock[7] - exchange_info_control[7]), list(exchange_info_adblock[8] - exchange_info_control[8]), list(exchange_info_adblock[9] - exchange_info_control[9])]

                        data[website][folder] = [len(exchange_info_adblock[0] - exchange_info_control[0]), len(exchange_info_adblock[1] - exchange_info_control[1]), len(exchange_info_adblock[2] - exchange_info_control[2]), len(exchange_info_adblock[3] - exchange_info_control[3]), len(exchange_info_adblock[4] - exchange_info_control[4]), len(exchange_info_adblock[5] - exchange_info_control[5]), len(exchange_info_adblock[6] - exchange_info_control[6]), len(exchange_info_adblock[7] - exchange_info_control[7]), len(exchange_info_adblock[8] - exchange_info_control[8]), len(exchange_info_adblock[9] - exchange_info_control[9]), np.around(prob/all_ads, 2), prob, all_ads]
        json.dump(prob_dict, open('mediation_analysis_prob_dict_new.json', 'w'))
        json.dump(data, open('mediation_analysis_data_new.json', 'w'))
        json.dump(exchanges_dict, open('mediation_analysis_exchanges_dict_new.json', 'w'))
        print('*'*50)
    except Exception as e:
        print(e)
        print('*'*50)
        continue
        # print(e)
        # print(a['data']['ads'])
        # sys.exit(0)


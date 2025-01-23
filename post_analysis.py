import os
import json
import subprocess
import time

def num_links(fpath_input, fpath_output):
    files = [os.path.join(fpath_input, f) for f in os.listdir(fpath_input) if os.path.isfile(os.path.join(fpath_input, f))]
    count = 0
    ad_exchange_ads = {}

    for file in files:
        check = 0
        lst = []
        data = json.load(open(file, 'r'))
        for ad in data.keys():
            if len(data[ad]["links"]) > 0:
                check = 1
                count += 1
                lst.append(ad)

        if check:
            ad_exchange_ads[file] = lst

    json.dump(ad_exchange_ads, open(fpath_output, 'w'))

def check_if_ad(url, resource):
    try:
        # Run the Node.js script
        result = subprocess.run(['node', 'mytest.js', '--url', url, '--resource', resource], capture_output=True, text=True, check=True)

        # print(result.stdout)
        if result.stdout == '':
            return False
        else:
            return True

    except Exception as e:
        print(f"Error in check_ad: {e}")
        return False

def sizes(fpath_input, fpath_output): # detect ads and find size; json.load()["data"]["requests"] - this is a list of packets
    files = [(os.path.join(fpath_input, f), f.split('_')[0]) for f in os.listdir(fpath_input) if (os.path.isfile(os.path.join(fpath_input, f)) and f.lower().endswith('.json'))]

    ad_size_data = {}

    # f = open(fpath_output, 'w')

    for (file, website) in files:
        keyword = ''
        if 'www' in website:
            keyword = website.split('www.')[1]

        try:
            reqs = json.load(open(file, 'r'))["data"]["requests"]
            if website not in ad_size_data.keys():
                ad_size_data[website] = []
        except Exception as e:
            print(e, keyword)
            continue

        all_pkts = []
        for packet in reqs:
            try:
                resource = packet["url"]
                if keyword in resource:
                    continue
                status = int(packet["status"])
                size = 0
                if status == 200:
                    size = int(packet["size"])
                    all_pkts.append((resource, size))
            except KeyError as k:
                continue
            except Exception as e:
                print('Exception:', e)
        
        original_directory = os.getcwd()
        target_directory = '/home/ritik/work/pes/accads_research/Ad-BlockerResearch/2. Resources (js)/blacklist_parser'

        try:
            # Change to the target directory
            os.chdir(target_directory)
            print(f"Changed to directory: {os.getcwd()}")

            ad_pkts = []
            for pkt in all_pkts:
                ret = check_if_ad(website, pkt[0])
                # print(pkt, ret)
                if ret:
                    ad_pkts.append(pkt)
            
            ad_size_data[website].extend(ad_pkts)

            os.chdir(original_directory)
            print(f"Returned to original directory: {os.getcwd()}")

        except Exception as e:
            print(f"Error: {e}", keyword)
            os.chdir(original_directory)
            print(f"Returned to original directory: {os.getcwd()}")

        json.dump(ad_size_data, open(fpath_output, 'w'))
    # f.close()

def avg_ads(fpath_input, fpath_output): #ads/page, fpath_input - adData
    files = [os.path.join(fpath_input, f) for f in os.listdir(fpath_input) if os.path.isfile(os.path.join(fpath_input, f))]
    
    lst = []
    for file in files:
        data = json.load(open(file, 'r'))
        count_ads = len(data.keys())
        if count_ads == 0:
            continue
        lst.append(count_ads)
    
    json.dump(lst, open(fpath_output, 'w'))

keyword = 'US'

adb_path = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/adblock'
control_path = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/control/'

# Avg_Ads
# avg_ads(f'{control_path}/adData', f'avg_ads_control_{keyword}.json')
# time.sleep(5)
# avg_ads(f'{adb_path}/adData', f'avg_ads_accads_{keyword}.json')
# time.sleep(5)

# # Num_Links
# num_links(f'{control_path}/adData', f'num_links_control_{keyword}.json')
# time.sleep(5)
# num_links(f'{adb_path}/adData', f'num_links_accads_{keyword}.json')
# time.sleep(5)

#Ad_Sizes
# sizes(f'{control_path}', f'ad_sizes_control_{keyword}.json')
# time.sleep(5)
sizes(f'{adb_path}', f'ad_sizes_accads_{keyword}_new.json')
time.sleep(5)
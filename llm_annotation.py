import base64
from openai import OpenAI
import os
import pandas as pd
import json
import requests
import sys
import re
import time
# # Initialize OpenAI API with your key
api_key = os.getenv("OPENAI_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set the OPENAI_KEY environment variable.")

# # Initialize OpenAI client
client = OpenAI(api_key=api_key)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
    # return image_file
        return base64.b64encode(image_file.read()).decode('utf-8')
    
def check_dp(strr):
    # check if an alphanumeric character is followed by a '...' or ' ...' ('a  ...' should not be considered)
    # return True if found, False otherwise
    pattern = r"\w(?:(?<! )\.\.\.| \.\.\.)"
    return bool(re.search(pattern, strr))

csv_file = '/home/ritik/work/pes/accads_research/json_and_csv/ground_truth.csv'
df = pd.read_csv(csv_file)

# Extract the first two columns
selected_columns = df.iloc[:, :2]

# Iterate over each row excluding the header
rows = selected_columns.itertuples(index=False, name=None)

# Display the rows
row_list = []
for row in rows:
    row_list.append(row)

all_annot = {}
explanations = {}

# interesting_files = [
#     # 'www.21usdeal.com_192a_7_adshot_3.png',
#     # 'www.allears.net_9d72_5_adshot_1.png',
#     # 'www.biblegateway.com_67f2_4_adshot_0.png',
#     # 'www.dailynous.com_8f33_4_adshot_1.png',
#     # 'www.globalnews.ca_c026_7_adshot_3.png',
#     # 'www.jansatta.com_6ff2_8_adshot_4.png',
#     # 'www.legacy-wow.com_c1db_4_adshot_0.png',
#     # 'www.motherjones.com_433a_7_adshot_3.png'

#     # 'control_under_18/www.bjpenn.com_4bab_11_adshot_7.png',
#     # 'adblock_under_18/www.about-air-compressors.com_56f9_5_adshot_1.png',
#     # 'adblock_under_18/www.joemygod.com_15a6_8_adshot_4.png',
#     # 'control_germany/www.tvline.com_5f27_7_adshot_3.png',
#     # 'control_US/www.rollingstone.com_5c4c_11_adshot_7.png',
#     # 'adblock_over_18/www.actumma.com_db89_4_adshot_0.png',
#     # 'adblock_germany/www.bigblueview.com_a1ea_8_adshot_4.png',
#     # 'control_under_18/www.extremehowto.com_b2c4_4_adshot_0.png',
#     # 'adblock_under_18/www.fark.com_e1f3_5_adshot_1.png',
#     # 'adblock_under_18/www.montagna.tv_f955_4_adshot_0.png',
#     # 'control_over_18/www.redstate.com_9363_4_adshot_0.png',
#     # 'control_over_18/www.slashfilm.com_dcfb_31_adshot_27.png',
#     # 'control_over_18/www.westernjournal.com_e3df_9_adshot_6.png',
#     # 'control_US/www.pjmedia.com_9ebb_8_adshot_4.png',
#     # 'adblock_over_18/www.zimbabwesituation.com_3756_6_adshot_5.png',
#     # 'control_US/www.tmz.com_2f4f_8_adshot_4.png',
#     # 'adblock_US/www.womanandhome.com_f75e_7_adshot_3.png',
#     # 'control_over_18/www.hiconsumption.com_122d_5_adshot_1.png',

#     'control_under_18/www.acte-deces.fr_2628_4_adshot_0.png',
#     # 'control_under_18/www.gameitnow.com_d37f_5_adshot_1.png',
#     # 'control_under_18/www.mundoboaforma.com.br_b4e0_7_adshot_4.png',
#     # 'control_under_18/www.mundodeportivo.com_8060_4_adshot_2.png',
#     # 'adblock_under_18/www.bjpenn.com_4bab_5_adshot_1.png',
#     # 'adblock_under_18/www.bleachernation.com_f599_11_adshot_7.png',
#     # 'adblock_under_18/www.journaldesfemmes.fr_7b53_6_adshot_2.png',
#     # 'control_germany/www.giallozafferano.it_fd0d_6_adshot_2.png',
#     # 'control_germany/www.mydramalist.com_ff20_5_adshot_1.png',
#     # 'control_over_18/www.basketnews.lt_7327_7_adshot_3.png',
#     # 'control_over_18/www.ski.com.au_5661_4_adshot_0.png',
#     # 'control_over_18/www.techbric.com_6189_7_adshot_3.png',
#     # 'control_over_18/www.curlingzone.com_9ab3_8_adshot_4.png',
#     # 'control_over_18/www.road.cc_7aa4_7_adshot_4.png',
#     # 'control_over_18/www.turnoffthelights.com_a84c_4_adshot_0.png',
#     # 'control_over_18/www.wnd.com_957e_4_adshot_0.png',
#     # 'control_US/www.allfamous.org_eb00_4_adshot_0.png',
#     # 'control_US/www.curlingzone.com_1376_7_adshot_3.png',
#     # 'control_US/www.genealogy.com_b9b3_7_adshot_3.png',
#     # 'control_US/www.indgovtjobs.in_10d0_8_adshot_4.png',
#     'control_US/www.manoramaonline.com_4f66_5_adshot_1.png',
#     # 'control_US/www.shaalaa.com_d38d_5_adshot_1.png',
#     # 'adblock_over_18/www.nme.com_c9af_9_adshot_5.png',
#     # 'adblock_over_18/www.sbnation.com_6c93_11_adshot_7.png',
#     # 'adblock_US/www.baby-chick.com_5c44_5_adshot_2.png',
# ]

interesting_files_ued = ['adblock_germany/www.21usdeal.com_192a_7_adshot_3.png','adblock_germany/www.alternet.org_3260_4_adshot_0.png','adblock_germany/www.alternet.org_e9ce_4_adshot_0.png','adblock_germany/www.mmamania.com_423c_4_adshot_0.png','adblock_germany/www.cartune.me_1256_4_adshot_0.png','adblock_germany/www.footmercato.net_a9b9_5_adshot_1.png','adblock_germany/www.globalnews.ca_c026_7_adshot_3.png','adblock_germany/www.healthprep.com_cffb_5_adshot_1.png','adblock_germany/www.joemygod.com_2210_9_adshot_5.png','adblock_germany/www.miniwebtool.com_29a8_9_adshot_5.png','adblock_germany/www.mundoboaforma.com.br_b4e0_4_adshot_0.png','adblock_germany/www.phys.org_c71a_4_adshot_0.png','adblock_germany/www.puntodebreak.com_c0fe_4_adshot_0.png','control_under_18/www.acte-deces.fr_2628_4_adshot_0.png','control_under_18/www.gutefrage.net_9bb9_4_adshot_1.png','control_under_18/www.lake-link.com_c4a0_5_adshot_1.png','control_under_18/www.landsearch.com_f4f4_4_adshot_0.png','control_under_18/www.mapsofindia.com_5703_5_adshot_1.png','control_under_18/www.maxifoot.fr_b158_4_adshot_0.png','control_under_18/www.menshairstylesnow.com_58e8_6_adshot_2.png','control_under_18/www.mundoboaforma.com.br_b4e0_7_adshot_4.png','control_under_18/www.mundodeportivo.com_8060_4_adshot_2.png','control_under_18/www.nymag.com_5531_8_adshot_4.png','control_under_18/www.spendwithpennies.com_6a5b_4_adshot_0.png','control_under_18/www.theatlantic.com_9764_6_adshot_2.png','control_under_18/www.abc4.com_c637_5_adshot_1.png','control_under_18/www.behindthesteelcurtain.com_7240_6_adshot_8.png','control_under_18/www.dailypaws.com_a23c_7_adshot_3.png','control_under_18/www.onegreenplanet.org_4446_13_adshot_9.png','control_under_18/www.parlons-basket.com_93a3_9_adshot_5.png','control_under_18/www.rochesterfirst.com_2e25_5_adshot_1.png','adblock_under_18/www.cougarboard.com_5b5d_4_adshot_0.png','adblock_under_18/www.fark.com_e1f3_5_adshot_1.png','adblock_under_18/www.menshairstylesnow.com_58e8_13_adshot_9.png','adblock_under_18/technical.city_b667_5_adshot_1.png','adblock_under_18/www.about-air-compressors.com_56f9_5_adshot_1.png','adblock_under_18/www.babelio.com_52be_5_adshot_1.png','adblock_under_18/www.bleachernation.com_f599_11_adshot_7.png','adblock_under_18/www.boatsales.com.au_c011_5_adshot_1.png','adblock_under_18/www.developgoodhabits.com_7be2_8_adshot_5.png','adblock_under_18/www.eafinder.com_26e0_4_adshot_0.png','adblock_under_18/www.footmercato.net_a9b9_14_adshot_10.png','adblock_under_18/www.happierhuman.com_5815_7_adshot_4.png','adblock_under_18/www.joemygod.com_15a6_8_adshot_4.png','adblock_under_18/www.journaldesfemmes.fr_7b53_6_adshot_2.png','adblock_under_18/www.maddenratings.com_827c_4_adshot_0.png','adblock_under_18/www.miniwebtool.com_3e01_6_adshot_2.png','adblock_under_18/www.montagna.tv_f955_4_adshot_0.png','adblock_under_18/www.phys.org_c71a_4_adshot_0.png','adblock_under_18/www.roadsnacks.net_2577_4_adshot_0.png','adblock_under_18/www.wfla.com_b2d2_5_adshot_1.png','control_germany/www.armyrecognition.com_4485_5_adshot_2.png','control_germany/www.breitbart.com_6eb0_5_adshot_1.png','control_germany/www.cambridge-news.co.uk_1ba3_14_adshot_11.png','control_germany/www.chicago.suntimes.com_428e_9_adshot_6.png','control_germany/www.consumersearch.com_d028_6_adshot_2.png','control_germany/www.giallozafferano.it_fd0d_6_adshot_2.png','control_germany/www.indiatv.in_50d8_7_adshot_3.png','control_germany/www.mydramalist.com_ff20_5_adshot_1.png','control_germany/www.racefans.net_ce87_5_adshot_1.png','control_germany/www.theweathernetwork.com_8aea_8_adshot_4.png','control_germany/www.eatingwell.com_918c_6_adshot_2.png','control_germany/www.eksisozluk.com_5078_5_adshot_1.png','control_germany/www.fastfoodmenuprices.com_f782_13_adshot_9.png','control_germany/www.galwaybeo.ie_f41d_7_adshot_4.png','control_germany/www.gpone.com_e752_12_adshot_8.png','control_germany/www.healthprep.com_cffb_5_adshot_1.png','control_germany/www.mamanatural.com_6dd2_9_adshot_5.png','control_germany/www.notthebee.com_fbd6_7_adshot_3.png','control_germany/www.nypost.com_6737_13_adshot_11.png','control_germany/www.vogue.com_377e_10_adshot_6.png','control_germany/www.wamiz.com_73b2_5_adshot_1.png','control_over_18/www.basketnews.lt_7327_7_adshot_3.png','control_over_18/www.orlandosentinel.com_b312_8_adshot_7.png','control_over_18/www.ski.com.au_5661_4_adshot_0.png','control_over_18/www.techbric.com_6189_7_adshot_3.png','control_over_18/www.allfamous.org_eb00_10_adshot_6.png','control_over_18/www.bolavip.com_863b_6_adshot_3.png','control_over_18/www.cope.es_efe0_7_adshot_3.png','control_over_18/www.dailynous.com_8f33_6_adshot_5.png','control_over_18/www.iheartcraftythings.com_9209_10_adshot_6.png','control_over_18/www.listelist.com_c6e9_5_adshot_1.png','control_over_18/www.parlons-basket.com_93a3_8_adshot_4.png','control_over_18/www.pride.com_7cf9_14_adshot_10.png','control_over_18/www.pride.com_7cf9_8_adshot_4.png','control_over_18/www.slashfilm.com_dcfb_31_adshot_27.png','control_over_18/www.surf-forecast.com_c7e3_5_adshot_1.png','control_over_18/www.texomashomepage.com_c60a_5_adshot_1.png','control_over_18/www.thecollector.com_bfdc_4_adshot_0.png','control_over_18/www.theroar.com.au_ee26_13_adshot_9.png','control_over_18/www.theroar.com.au_ee26_5_adshot_1.png','control_over_18/www.wnd.com_957e_4_adshot_0.png','control_US/www.allfamous.org_eb00_4_adshot_0.png','control_US/www.boatsonline.com.au_57c1_5_adshot_1.png','control_US/www.coingecko.com_60ad_5_adshot_1.png','control_US/www.dafont.com_1266_6_adshot_2.png','control_US/www.denver7.com_8fb8_4_adshot_0.png','control_US/www.genealogy.com_b9b3_7_adshot_3.png','control_US/www.indgovtjobs.in_10d0_8_adshot_4.png','control_US/www.manoramaonline.com_4f66_5_adshot_1.png','control_US/www.popsci.com_d01b_12_adshot_8.png','control_US/www.prevention.com_2e8f_11_adshot_7.png','control_US/www.shaalaa.com_d38d_5_adshot_1.png','adblock_over_18/www.accuweather.com_e42e_5_adshot_1.png','adblock_over_18/www.crazygames.com_497f_4_adshot_0.png','adblock_over_18/www.cutthatdesign.com_cf5e_4_adshot_0.png','adblock_over_18/www.homebrewtalk.com_6b13_5_adshot_2.png','adblock_over_18/www.about-air-compressors.com_56f9_6_adshot_2.png','adblock_over_18/www.actumma.com_db89_4_adshot_0.png','adblock_over_18/www.billboard.com_69ef_7_adshot_3.png','adblock_over_18/www.dinamalar.com_be41_4_adshot_0.png','adblock_over_18/www.ndtv.in_5afa_9_adshot_5.png','adblock_over_18/www.nme.com_c9af_13_adshot_9.png','adblock_over_18/www.nme.com_c9af_9_adshot_5.png','adblock_over_18/www.onegreenplanet.org_4446_8_adshot_4.png','adblock_over_18/www.sbnation.com_6c93_11_adshot_7.png','adblock_over_18/www.scotsman.com_a779_4_adshot_0.png','adblock_over_18/www.soxprospects.com_97c7_5_adshot_1.png','adblock_over_18/www.sportsmockery.com_9262_4_adshot_0.png','adblock_over_18/www.thelallantop.com_a8a2_6_adshot_4.png','adblock_over_18/www.theprint.in_cf7a_4_adshot_0.png','adblock_over_18/www.theprint.in_cf7a_6_adshot_2.png','adblock_over_18/www.time.com_2e49_4_adshot_0.png','adblock_over_18/www.upi.com_1802_5_adshot_3.png','adblock_over_18/www.zone-turf.fr_23b6_4_adshot_0.png','adblock_US/www.rvusa.com_31a3_5_adshot_1.png','adblock_US/www.allakhazam.com_e54d_5_adshot_1.png','adblock_US/www.cartune.me_1256_5_adshot_1.png','adblock_US/www.fbref.com_3cd9_5_adshot_1.png','adblock_US/www.geny.com_10d3_5_adshot_1.png','adblock_US/www.hirunews.lk_d55d_4_adshot_0.png','adblock_US/www.jpost.com_03ea_4_adshot_0.png']

# interesting_files_1 = [('www.attractivenesstest.com_1ce6_5_adshot_1.png', 'adblock_germany'),('www.mundoboaforma.com.br_b4e0_4_adshot_0.png', 'adblock_germany'),('www.nzherald.co.nz_2d93_5_adshot_1.png', 'adblock_germany'),('www.nzherald.co.nz_bd49_5_adshot_1.png', 'adblock_germany'),('www.bjpenn.com_4bab_11_adshot_7.png', 'control_under_18'),('www.cardgames.io_3e46_4_adshot_0.png', 'control_under_18'),('www.about-air-compressors.com_56f9_5_adshot_1.png', 'adblock_under_18'),('www.boatsales.com.au_c011_5_adshot_1.png', 'adblock_under_18'),('www.gardeningknowhow.com_ee57_4_adshot_0.png', 'adblock_under_18'),('www.gazzettadimodena.it_2e77_4_adshot_0.png', 'adblock_under_18'),('www.joemygod.com_15a6_8_adshot_4.png', 'adblock_under_18'),('www.miniwebtool.com_3e01_6_adshot_2.png', 'adblock_under_18'),('www.tvline.com_5f27_7_adshot_3.png', 'control_germany'),('www.eksisozluk.com_5078_5_adshot_1.png', 'control_germany'),('www.eresmama.com_0aab_12_adshot_8.png', 'control_germany'),('www.khaleejtimes.com_69ea_10_adshot_7.png', 'control_over_18'),('www.theroar.com.au_ee26_7_adshot_3.png', 'control_over_18'),('www.rollingstone.com_5c4c_11_adshot_7.png', 'control_US'),('www.actumma.com_db89_4_adshot_0.png', 'adblock_over_18'),('www.rugbydump.com_d06d_4_adshot_0.png', 'adblock_over_18'),('www.zimbabwesituation.com_3756_6_adshot_5.png', 'adblock_over_18'),('www.food52.com_f17d_6_adshot_2.png', 'adblock_US'),('www.geny.com_10d3_5_adshot_1.png', 'adblock_US')]


for row in interesting_files_ued:
    filename = row.split('/')[1]
    json_filename = row.split('/')[0]
    image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/annotation_tasks/selected_adshots_{json_filename}/{filename}'
    if not os.path.exists(image_folder):
        image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/annotation_tasks/selected_adshots_{json_filename}_nolinks/{filename}'
        print('MISMATCH', filename, json_filename)
    os.system(f'eog {image_folder}')
    # os.system(f'cp {image_folder} ../user_disruption/')
    # input()
    time.sleep(0.5)

sys.exit(0)

# int_files = [
# ('control_under_18','www.theatlantic.com_9764_6_adshot_2.png'),
# ('control_under_18','www.abc4.com_c637_5_adshot_1.png'),
# ('adblock_under_18','www.happierhuman.com_5815_7_adshot_4.png'),
# ('adblock_under_18','www.roadsnacks.net_2577_4_adshot_0.png'),
# ('control_germany','www.indiatv.in_50d8_7_adshot_3.png'),
# ('control_germany','www.racefans.net_ce87_5_adshot_1.png'),
# ('control_germany','www.eatingwell.com_918c_6_adshot_2.png'),
# ('control_germany','www.fastfoodmenuprices.com_f782_13_adshot_9.png'),
# ('control_germany','www.mamanatural.com_6dd2_9_adshot_5.png'),
# ('control_over_18','www.bolavip.com_863b_6_adshot_3.png'),
# ('control_over_18','www.pride.com_7cf9_14_adshot_10.png'),
# ('control_US','www.indgovtjobs.in_509d_6_adshot_2.png'),
# ('adblock_over_18','www.boxing247.com_90c6_9_adshot_6.png'),
# ('adblock_over_18','www.cutthatdesign.com_cf5e_4_adshot_0.png'),
# ('adblock_over_18','www.homebrewtalk.com_6b13_5_adshot_2.png'),
# ('adblock_over_18','www.ndtv.in_5afa_9_adshot_5.png'),
# ('adblock_over_18','www.nme.com_c9af_13_adshot_9.png'),
# ('adblock_over_18','www.theprint.in_cf7a_4_adshot_0.png'),
# ('adblock_US','www.fbref.com_3cd9_5_adshot_1.png')
# ]

patterns = ['\bsearches', '\bsearch for\b', '\bsearch ad', '\bgosearch', '\bsearchtopics\b', 'suv deals', '\bsuchergebnisse\b', '\bsuchanzeigen\b']

for (key, row) in int_files:
# for (key, row) in row_list:
    # filename = key.split("'")[1]
    # json_filename = row.split("'")[1]
    filename = row
    json_filename = key

# for row in interesting_files:
#     lst = row.split('_')
#     if lst[2].startswith('www'):
#         filename = '_'.join(lst[2:]) #row.split("/")[1]
#         json_filename = '_'.join(lst[:2]) #row.split("/")[0]
#     else:
#         filename = '_'.join(lst[3:]) #row.split("/")[1]
#         json_filename = '_'.join(lst[:3]) #row.split("/")[0]

    # json_filename = 'control_over_18'
    # filename = 'www.texomashomepage.com_c60a_5_adshot_1.png'

    ocr_text = json.load(open(f'accads_crawler/image_hashing/ocr_{json_filename}.json', 'r'))[filename]

    # if f'{json_filename}/{filename}' not in interesting_files:
    #     continue
    image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/annotation_tasks/selected_adshots_{json_filename}/{filename}'
    if not os.path.exists(image_folder):
        image_folder = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/annotation_tasks/selected_adshots_{json_filename}_nolinks/{filename}'
        print('MISMATCH', filename, json_filename)
    if not os.path.exists(image_folder):
        all_annot[image_folder] = 'DNA'
        explanations[image_folder] = 'DNA'

    base64_image = encode_image(image_folder)
    # print(ocr_text)
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
        # body = {
            messages = [
            {
                "role": "user",
                "content": 
                    # f"""Analyze the attached ad and determine if it is problematic or not strictly based on the taxonomy.
                    # image:  "data:image/png;base64,{base64_image}"
                    # """
                    [
                        {  
                            "type": "text",
                            "text": """Analyze the attached ad and determine if it is problematic or non-problematic strictly based on the taxonomy. If problematic, return the category title you find it to be belonging to as the key value. Otherwise return an empty string as the key value. Analyse all possible sub ad images present as well."""
                        },
                        {
                            "type": "text",
                            "text": f"{ocr_text}"
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url":  f"data:image/png;base64,{base64_image}"
                            },
                        },
                    ],
            },
            {
                "role": "system",
                "content":
                    """You are an expert in evaluating online display advertisements based on a taxonomy derived from ad exchange policies and user perception studies. Analyze the provided advertisement screenshot to determine if it is problematic, strictly using the provided taxonomy. For the ad images, you should also identify advertiser information. 
                    ##
                    **Advertiser information**:
                    Extract the advertiser's name from visible brand logos, text, or symbols in the ad image -- looking for unique fonts, stylized text, distinct colors, or logo designs that stand out from the main content.
                    - For Taboola and Outbrain ads, consider the advertiser as the publisher's name below each ad title. 
                    - Ads with obscure advertiser names that resemble english sentences should be categorized as *logo*.
                    - Ad screenshots with multiple advertisers should be classified as *multiple advertisers*. 
                    ## 
                    The text present (OCR output) in the ad creative is also provided as an additional input for processing and identifying any problematic behaviour.
                    ##
                    The taxonomy includes a title, definition, keywords, and notes for each category. Strictly use the definitions, keywords, and notes as primary guides. The keywords are exhaustive and represent the themes covered in each category.  
                    ##  
                    Be conservative in your classification: Only classify if the ad clearly and confidently fits a category. If in doubt, classify it as non-problematic.   
                    ##
                    Since it is a multi-label classification, multiple categories can be chosen. Return a JSON object with the following structure:  
                    1. A `categories` key containing a list of applicable categories. If non-problematic, return an empty list as the value.  
                    2. An `explanations` key providing a rationale for each identified category. Include detailed reasoning for each flagged category.
                    3. An `advertiser` key containing the advertiser name identified in the ad image. If multiple ads exist, report 'multiple advertiser'. If no advertiser identification is possible or no subtitle is present, report *None* in the value.  
                    ##  
                    For screenshots with multiple ads, return the superset of categories covering all ads.
                    ###
                    Taxonomy:
                    1. Regulations
                    Definition: Ads deemed inappropriate for younger audiences (Below 18 years) due to product or content nature. 
                    Keywords: sexually suggestive, Cannabinoids, alcohol, gambling/sweepstakes, cosmetic interventions, hazardous goods, drug use, Weight-reduction regimes or establishments, Lottery, E-Cigarettes, Prescription-only medicines, Dating sites
                    #
                    Note: 
                    - Classify only if clear evidence like explicit exposure, provocative poses, or overtly suggestive context exists; avoid bias towards modeling images. 
                    - Sexually suggestive ads should be classified into both `Regulations` and `Inappropriate or Offensive Content` if the content is derogatory or explicit.
                    ##
                    2. Inappropriate or Offensive Content
                    Definition: Ads containing language, visuals, or themes that are offensive, hateful, or disrespectful towards general public and not focused groups.
                    Keywords: Sexually explicit, offensive language, violent acts, hate speech, hookup, graphic images, racially insensitive, conspiracy theories, disrespectful religious/sacred content/profanity, trafficking, social issues, hacking
                    #
                    Note: 
                    - Merely mentioning potentially sensitive topics (e.g., violence, religion) does not automatically make the ad offensive unless it is presented in a disturbing, demeaning, or shocking manner.
                    - References to advertiser or domain names that contain edgy words or horror themes are not automatically classified as offensive.
                    ##
                    3. Deceptive Claims and Exaggerated Benefits 
                    Definition: Ads that make unverified or exaggerated claims about a product's or service's effectiveness, often with the intent to mislead consumers. Unlike Dark Patterns, these ads include specific claims in their content, rather than relying solely on clickbait tactics.
                    Keywords: 
                        Health claims - No disclosure, Reasons for conditions, miracle cure, weight loss, scientifically proven, Dietary supplements, cosmetic beauty treatments, mental health services, false vaccine information, cheap substitutes
                        Financial Claims - get rich quick, financial freedom, investment returns, guaranteed profits, False Tax Promises, Crypto Gain Misrepresentation, debt relief
                        Environmental Claims - No disclosure, greenwashing (eco-friendly, sustainable, green product, carbon-neutral, environmentally safe), eco-friendly, ethical sourcing, organic, waste reduction claims
                        Other Impossible Claims - overpromising, instant results, transform your life, best in the world/market, one-of-a-kind, never-before-seen, guaranteed satisfaction, exclusive deal, legal claims
                    #
                    Note: 
                    - No disclosures are required for finance-related ads offering incentives like 'up to a certain amount' for account openings. 
                    - Focus on identifying financial claims that appear fraudulent or excessively unrealistic, rather than scrutinizing all claims.
                    ##
                    4. Dark Patterns and Manipulative Design
                    Definition: Ads that use deceptive design techniques to manipulate user behavior, such as clicking, subscribing, or sharing information unintentionally.
                    Keywords: clickbait, social engineering, scarcity tactics, confirmshaming, countdown timers, fake buttons, sensationalism, fake testimonials, fake celebrity endorsements, urgency, last chance, your data is at risk, fear tactics, emergency, danger, don't miss out, Incomplete sentences using ...
                    #
                    Note: 
                    - Fake or multiple buttons present in the Ad image should be classified as *Dark Patterns and Manipulative Design*.
                    - Search ads with multiple clickable rows should be classified as *Dark Patterns and Manipulative Design* 
                    ##
                    5. User Experience Disruption  
                    Definition: Ads that degrade the user experience by being overly intrusive, misleading, repetitive, or lck of advertiser information. This includes ads with unnatural, or highly manipulated imagery that causes confusion or doubt about authenticity.  
                    Keywords: annoying, intrusive (revealing locations), auto-playing video, difficult-to-close pop-ups, disruptive ad formats, ad loading speed, unclear labeling of sponsored content. Ad quality (image), No Information (text/image) - for context.  
                    #
                    Note:
                    - Ads containing **map snippets** that indicate proximity to the user's location are considered intrusive, classify them as **User Experience Disruption**.
                    - Different ads with **identical images** within the ad screenshot, are classified them as **User Experience Disruption**. Multiple but different ads appearing in the same screenshot are not disruption.
                    - Ignore popup notifications originating from or local to the website itself.
                    ##
                    6. Political and Socially Sensitive Topics
                    Definition: Ads related to political topics that could polarize or manipulate public opinion, especially during sensitive times like elections.
                    Keywords: No disclosure (endorsements), election campaigns, fake endorsements, fake news, propaganda (climate change, LGBTQ rights, racial justice, religious freedom, abortion, immigration policy), defaming candidates
                    #
                    Note: 
                    - Classify specific propaganda ads if the content undermines trust or portrays a person or entity in a detrimental or questionable manner.
                    """
            },
            ],
            temperature=0,
            response_format={'type':'json_object'}
        )

        res = response.choices[0].message.content
    # print(res)
    except Exception as e:
        print('ERROR l261:', e)
        res = "{}"
    # res = {"categories": [], "explanations": [], "brand": "multiple brands"}

    # all_annot.append(res)
    try:
        res = json.loads(res)
        # print(res)
        if "explanations" not in res.keys():
            res["explanations"] = {}
        elif type(res["explanations"]) == list:
            res["explanations"] = {}
        # res["explanations_extra"] = []

        # Add Dark patterns due to '...'
        if check_dp(ocr_text) and 'Dark Patterns and Manipulative Design' not in res['categories']:
            res["categories"].append('Dark Patterns and Manipulative Design')
            res["explanations"]['dp'] = "DP artificially added"
        
        # Add User Experience Disruption due to brand name not being present
        print(res)
        print(ocr_text)
        if res['advertiser'] == 'None' or any(re.search(pattern, ocr_text.lower()) for pattern in patterns):
            if 'User Experience Disruption' not in res["categories"]:
                res["categories"].append('User Experience Disruption')
                res["explanations"]['ued'] = 'UED artifically added'

        print(res)
        all_annot[image_folder] = ';'.join(res["categories"])
        explanations[image_folder] = res["explanations"]
    except:
        print('ERROR', res)
        all_annot[image_folder] = res
        explanations[image_folder] = res
    json.dump(all_annot, open('llm_annotation_dict_4o.json', 'w'))
    json.dump(explanations, open('llm_annotation_explanations_4o.json', 'w'))

df['llm_annotation'] = list(all_annot.values())
df['explanations'] = list(explanations.values())
df.to_csv('llm_annotation_4o.csv', index=False)
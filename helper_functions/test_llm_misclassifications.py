import os

import signal

def handler(signum, frame):
    print('Ctrl+C was pressed. Exiting gracefully.')
    exit(0)

signal.signal(signal.SIGINT, handler)

keyword = 'adblock_germany'

images = [
'technical.city_b667_4_adshot_0.png',
'technical.city_b667_6_adshot_2.png',
'www.21usdeal.com_0a19_5_adshot_1.png',
'www.21usdeal.com_0a19_7_adshot_3.png',
'www.21usdeal.com_192a_5_adshot_1.png',
'www.21usdeal.com_192a_6_adshot_2.png',
'www.a-z-animals.com_302f_4_adshot_10.png',
'www.a-z-animals.com_a82e_4_adshot_0.png',
'www.accuweather.com_8b67_4_adshot_0.png',
'www.accuweather.com_8b67_5_adshot_1.png',
'www.accuweather.com_8b67_6_adshot_2.png',
'www.accuweather.com_8b67_7_adshot_3.png',
'www.accuweather.com_aae7_5_adshot_1.png',
'www.accuweather.com_aae7_7_adshot_3.png',
'www.accuweather.com_c314_5_adshot_1.png',
'www.accuweather.com_c314_6_adshot_2.png',
'www.accuweather.com_c314_7_adshot_3.png',
'www.accuweather.com_e42e_5_adshot_1.png',
'www.accuweather.com_e42e_7_adshot_3.png',
'www.agroinform.hu_c586_4_adshot_0.png',
'www.allears.net_9d72_5_adshot_1.png',
'www.allkpop.com_cff8_5_adshot_2.png',
'www.allkpop.com_cff8_8_adshot_5.png',
'www.allmusic.com_0843_6_adshot_2.png',
'www.allmusic.com_74cf_4_adshot_0.png',
'www.allmusic.com_8e53_6_adshot_2.png'
]

fpath = f'/run/user/1001/gvfs/smb-share:server=storage.rcs.nyu.edu,share=adblockers/selected_adshots_{keyword}/'
try:
    for image in images:
        img = fpath + image
        print(image)
        os.system(f'eog {img}')
except KeyboardInterrupt:
    print('Ctrl+C was pressed. Exiting gracefully.')
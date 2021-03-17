import time
import re
from selenium import webdriver
from editing import *
import misc as m
from youtube import *
from pexels import *
import os
import subprocess
from make_videos import *
import datetime

name = 'andrew'
#name = 'caleb'
path_dict = {
    'andrew': '/Users/andrewswanback/Documents/sd',
    'caleb': '/Users/calebstevens/Documents/selenium_data'
}
path = path_dict[name]
def set_dir(name,filename=''):
    if name == '':
        if filename != '':
            return path+'/'+filename
        else:
            return path
    if filename == '':
        full_path = '{}/{}'.format(path, name)
        if not os.path.exists(full_path):
            os.mkdir(full_path)
    else:
        dir_path = '{}/{}'.format(path, name)
        full_path = '{}/{}/{}'.format(path, name,filename)
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    return full_path

if __name__ == "__main__":

    # Youtube settings
    query = "that's a lot of chickens"
    duration = 750      # seconds
    number = 12
    max_length = 40     # seconds

    # Tiktok settings
    tiktok_num = 10

    # Reddit settings
    # reddit_num = 0

    _temp = query.replace(' ', '-')
    folder_name = _temp.replace("'", '-')
    folder_name += "-0"
    i=1
    while folder_name in os.listdir(path):
        folder_name = folder_name[0:-2]+f'-{i}'
        i += 1
    folder = set_dir(folder_name)
    if query != '' and (duration > 0 or number > 0):
        start_time = time.time()

        # ----Only mess with this part-------------------------------------------------------------
        #get_yt_videos(query, folder,max_length=max_length,number=yt_number)
        #tik_tok_farmer(folder,tiktok_num)
        #reddit_retardation(folder,reddit_num) will go here as well

        #concat(folder,resolution='720p')

        #------------------------------------------------------------------------------------------
        print(f'Execution time - {datetime.timedelta(seconds =round(time.time()-start_time))}')
        notify('Selenium','','Process finished')


    #   Trimming -------------------------------------------------------------------------------------------------------
    #   Change video number to which one you want to trim
    #   Change start to whenever clip should start
    #   Change end or duration based on desire, leave other as zero
    vid_num = -1
    if vid_num != -1:
        trim_file(folder+f'/video{vid_num}.mp4',start=0,end=0,dur=0)


    # Cleaning ---------------------------------------------------------------------------------------------------------
    # deletes all original videos in folder, keeps the re-encoded ones
    # set 'hard' to 'True' to hard clean, removing everything except source links and final compilation
    folder_to_clean = ''
    if folder_to_clean != '':
        m.clean(folder+'/'+folder_to_clean,hard=False)

    # ------------------------------------------------------------------------------------------------------------------
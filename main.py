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
import tiktok_experimental as tiktok
import misc

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

    use_query_as_folder_name = True        # False while only using tiktok, True while using yt
    use_tiktok_and_yt_same_folder = False   # True for adding everything in same comp

    # Youtube settings
    query = "that's a lot of chickens"
    duration = 750      # seconds
    number = 12
    max_length = 40     # seconds

    # Tiktok settings
    tiktok_num = 10

    folder_name = 'tiktok-0'
    if(use_query_as_folder_name):
        _temp = query.replace(' ', '-')
        # noinspection PyRedeclaration
        folder_name = _temp.replace("'", '-')
        folder_name += "-0"
    if(use_tiktok_and_yt_same_folder):
        folder_name = 'Tiktok-yt-comp-0'
    i=1
    while folder_name in os.listdir(path):
        if(i < 10):
            folder_name = folder_name[0:-1]+f'{i}'
        else:
            folder_name = folder_name[0:-2] + f'{i}'
        i += 1
    folder = set_dir(folder_name) # Folder setup
    if query != '' and (duration > 0 or number > 0):
        start_time = time.time()

        # ----Only mess with this part-------------------------------------------------------------
        get_yt_videos(query, folder,max_length=max_length,number=number)

        #print(os.listdir(path+'/tiktok23'))
        #print(os.path.getmtime(path+'/tiktok-1/Untitled.rtf'))
       # print(os.path.getctime(path + '/tiktok-1/dfb639e8778ac4d89539.mp4'))
        #file = max([os.path.join(path+'/tiktok-1', f) for f in os.listdir(path+'/tiktok-1')], key=os.path.getctime)
       # print(file)

        #tiktok.tik_tok_farmer(folder,tiktok_num)
        #reddit_retardation(folder,reddit_num) will go here as well
        #concat(path+"/Selenium",resolution='tiktok')
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
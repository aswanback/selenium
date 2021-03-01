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

name = 'andrew'
#name = 'caleb'
path_dict = {
    'andrew': '/Users/andrewswanback/Documents/sd',
    'caleb': '/Users/calebstevens/Documents/selenium_data'
}
path = path_dict[name]  #anytime you need to use your full filepath, use 'path'
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

    #   Making compilations --------------------------------------------------------------------------------------------
    #   1. Fill out info below
    #   2. Comment out 'concat()'
    #   3. Run
    #   4. Audit videos and trim as neccessary
    #   5. Comment out 'get_yt_videos()', uncomment 'concat()'
    #   6. Run again, finished
    video_name = ''
    query = 'it do go down'
    duration = 60

    folder = set_dir(video_name)
    if video_name != '' and query != '' and duration != 0:
        #get_yt_videos(query, folder, duration=duration)
        concat(folder)
        notify('Selenium','','Process finished')
        pass

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
        m.clean(folder_to_clean,hard=False)

    # ------------------------------------------------------------------------------------------------------------------
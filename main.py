import time
import re
from selenium import webdriver
from editing import *
from misc import *
from youtube import *
from pexels import *
import os
import subprocess

##################
#name = 'andrew'
name = 'caleb'
##################

path_dict = {
    'andrew': '/Users/andrewswanback/Documents/selenium_data',
    'caleb': '/Users/calebstevens/Documents/Selenium_data'
}
path = path_dict[name]  #anytime you need to use your full filepath, use 'path'

def set_dir(name,filename=''):
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
    #dir_1 = set_dir('photos')
    #get_pexel_photos('wave',dir_1)

    #dir_2 = set_dir('videos')
    #get_pexel_videos('wave',dir_2)

    #dir_3 = set_dir('audio')
    #get_yt_audios(dir_3)


    #dir_4 = set_dir('untrimmed','video3.mp4')
    #dir_5 = set_dir('trimmed')
    #trim(dir_4,dir_5+'/new.mp4','00:00:02',end='00:00:18')

    #img = set_dir('new_photos_1','pexel_photo_wave_0.jpeg')
    #audio = set_dir('audio','123.mp3')
    #video = set_dir('video_out','out.mp4')
    #video1 = set_dir('untrimmed','10mins.mp4')
    #dub_video(video1,audio,video,video_is_longer=True)
    #print(get_length(video1))
    #dub_photo(img,audio,video)
    #filepath = set_dir('calebtest')
    get_yt_videos("it do go down", "/users/calebstevens/downloads/Videos", 9)

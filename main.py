import time
import re
from selenium import webdriver
from editing import *
from misc import *
from youtube import *
from pexels import *

##################
name = 'andrew'
#name = 'caleb'
##################

path_dict = {
    'andrew': '/Users/andrewswanback/Documents/selenium_data',
    'caleb': '/Users/calebstevens/Downloads'
}
path = path_dict[name]  #anytime you need to use your full filepath, use 'path'

def set_dir(name):
    full_path = '{}/{}'.format(path,name)
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    return full_path


if __name__ == "__main__":
    #dir_1 = set_dir('photos')
    #get_pexel_photos('wave',dir_1)

    #dir_2 = set_dir('videos')
    #get_pexel_videos('wave',dir_2)

    dir_3 = set_dir('audio')
    get_yt_audios(dir_3)




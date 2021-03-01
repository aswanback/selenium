import time
import re
from selenium import webdriver
from editing import *
from misc import *
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


#######################################################################################################################
if __name__ == "__main__":

    video_name = 'f'
    query = 'it do go down'
    duration = 60

    folder = set_dir(video_name)
    if video_name != '' and query != '' and duration != 0:

        #get_yt_videos(query, folder, duration=duration)
        #Audit videos, trim, then uncomment 'concat' and comment out 'get_yt_videos'
        #concat(folder)
        pass

    #Trimming
    #vid_num = 1
    #trim_file(folder+'/video{}.mp4'.format(vid_num),start=0,end=0,dur=0)

import time
import re
from selenium import webdriver
from editing import *
import misc
from youtube import *
from pexels import *
import os
import subprocess
from make_videos import *

name = 'andrew'
#name = 'caleb'
path_dict = {
    'andrew': '/Users/andrewswanback/Documents/selenium_data',
    'caleb': '/Users/calebstevens/Documents/selenium_data'
}
path = path_dict[name]  #anytime you need to use your full filepath, use 'path'
def set_dir(name,filename=''):
    if name == '':
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

#######################################################################################################################
if __name__ == "__main__":
    folder = set_dir('inaugural_video')
    name = set_dir('inaugural_video','mememe.mp4')
    meme('it do go down',folder,name,duration=12*60)

    #folder = set_dir('massage')
    #relax(folder,folder+'/photos','videos','waves')
    #check_folder = subprocess.run(['[', '-d', '"/Users/andrewswanback/Documents/selenium_data/massage"', ']', '&&', 'echo', '"0"', '||', 'echo', '"1"'])
   # print(check_folder)
    #get_length()
    #misc.notify(title='Selenium', subtitle='Meme video update', message='process finished')
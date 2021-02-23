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

##################
name = 'andrew'
#name = 'caleb'
##################

path_dict = {
    'andrew': '/Users/andrewswanback/Documents/selenium_data',
    'caleb': '/Users/calebstevens/Documents/selenium_data'
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

    #dir_3 = set_dir('audiotest')
    #get_yt_audios(dir_3)

    #concat('/Users/andrewswanback/Desktop/list.txt','/Users/andrewswanback/Desktop/out.mp4')
    #dir_4 = set_dir('untrimmed','video3.mp4')
    #dir_5 = set_dir('trimmed')
    #trim(dir_4,dir_5+'/new.mp4','00:00:02',end='00:00:18')

    #img = set_dir('new_photos_1','pexel_photo_wave_0.jpeg')
    #audio = set_dir('audio','123.mp3')
    #video = set_dir('video_out','out.mp4')
    #video1 = set_dir('untrimmed','10mins.mp4')
    #dub_video(video1,audio,video)
    #print(get_length(video1))
    #dub_photo(img,audio,video)
    #filepath = set_dir('calebtest')
    #get_yt_videos('cats', filepath, duration=1000)
    #folder = set_dir('inaugural_video')
    #name = set_dir('inaugural_video','why_are_you_gay?.mp4')
    #meme('the quiet Kid in class',folder,name,duration=2*60)
    #concat(folder+'/listfile.txt',name)
    #dir_8 = set_dir('massage')#
    #yt_repost_downloader('massage music',dir_8,number=20)
    #listfile = set_dir('memetest','listfile.txt')
    #batch_trim(listfile,'timestamp')

    #string = 'thisisa6filename 9 81'
    #print(re.findall(r'(?<=\s)(?:\d+)',string))
    folder = set_dir('massage')

    relax(folder,folder+'/photos','videos','waves')

    #check_folder = subprocess.run(['[', '-d', '"/Users/andrewswanback/Documents/selenium_data/massage"', ']', '&&', 'echo', '"0"', '||', 'echo', '"1"'])

   # print(check_folder)
    #get_length()
    #misc.notify(title='Selenium', subtitle='Meme video update', message='process finished')


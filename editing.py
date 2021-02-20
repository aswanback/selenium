import time
import re
import requests  # to get image from the web
import shutil  # to save it locally
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import subprocess

from misc import *
from youtube import *
from pexels import *

def concat(listfile,outname):
    os.system('ffmpeg -f concat -safe 0 -i {} -c copy {}'.format(listfile,outname))
    #os.system("ffmpeg -safe 0 -f concat -segment_time_metadata 1 -i {} -vf select=concatdec_select -af aselect=concatdec_select, aresample=async=1 {}".format(listfile,outname))
    #str = 'ffmpeg -f concat -safe 0 -i mylist.txt -c copy output.wav'
    return


def trim(_input,output,start,end=0,dur=0):
    if dur != 0:
        os.system('ffmpeg -i {} -ss {} -t {} -async 1 {}'.format(_input,start,dur,output))
    elif end != 0:
        os.system('ffmpeg -i {} -ss {} -to {} -async 1 {}'.format(_input,start,end,output))
    return


def dub_photo(img,audio,video): #no overwriting files with same name, will crash
    #os.system('ffmpeg -loop 1 -y -i {} -i {} -shortest {}'.format(img,audio,video))
    os.system('ffmpeg -loop 1 -i {} -i {} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {}'.format(img,audio,video))
    return


def dub_video(video,audio,output,video_is_longer=True):
    len_video = get_length(video)
    len_audio = get_length(audio)
    if len_video >= len_audio:
        os.system('ffmpeg -i {} -i {} -c:v copy -map 0:v:0 -map 1:a:0 {}'.format(video,audio,output))
    else:
        os.system('ffmpeg -i {} -i {} -c:v copy -map 0:v:0 -map 1:a:0 -shortest {}'.format(video, audio, output))
    return


def get_length(filename):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',filename], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return float(result.stdout)

import time
import re

import numpy as n
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

#TODO


def concat(listfile,outname):
    lfile = open(listfile,'r')
    newlfilepath = re.findall(r'(?:/).+(?:/)',listfile)[0]
    #print(newlfilepath)
    newlfile = open(newlfilepath+'newlistfile.txt','w')
    filenames_unedited = [line.strip("\n") for line in lfile if line != "\n"]

    width_height = []
    filenames = []
    past_dec_frame_rate = 1
    for i in range(len(filenames_unedited)):
        filenames.append(filenames_unedited[i][6:-1])
        fileinfo = str(subprocess.run(['ffprobe','-v', 'error', '-select_streams', 'v:0','-show_entries','stream=width,height','-of','csv=s=x:p=0',filenames[i]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout)
        frame_rate_info = str(subprocess.run(['ffprobe','-v', 'error', '-select_streams', 'v:0','-show_entries','stream=r_frame_rate','-of','csv=s=x:p=0',filenames[i]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout)
        frame_rate = re.findall(r'\d+/\d+',frame_rate_info)[0]
        [numerator,denominator] = re.split('/',frame_rate)
        dec_frame_rate = float(numerator)/float(denominator)
        if dec_frame_rate > past_dec_frame_rate:
            final_frame_rate = '{}/{}'.format(float(numerator),float(denominator))
        past_dec_frame_rate = dec_frame_rate
        print('fr',dec_frame_rate)
        filesize = re.findall(r'(?:\d+)x(?:\d+)',fileinfo)[0]
        width_height.append(re.split('x',filesize))
    print('fin',final_frame_rate)
    width_max_index = n.nanargmax(width_height[:][1])
    h = width_height[width_max_index][0]
    w = width_height[width_max_index][1]
   # print('h',h,' w',w)
    #print(filenames)
    ###TODO os.system('ffmpeg -y -hide_banner -loglevel error -stats -i {} -c copy {}final.mp4'.format(filenames[0],newlfilepath))
    for i in range(0,len(filenames)):
        os.system('ffmpeg -y -hide_banner -loglevel error -stats -i {} -map 0:v -map 0:a -use_wallclock_as_timestamps 1 -r {} {}'.format(filenames[i],final_frame_rate,filenames[i][0:-4]+'-a.mp4'))
        os.system('ffmpeg -y -hide_banner -loglevel error -stats -i {} -vf "scale=w=1280:h=720:force_original_aspect_ratio=1,pad=1280:720:(ow-iw)/2:(oh-ih)/2" -c:v libx264 -c:a aac {}'.format(filenames[i][0:-4]+'-a.mp4',filenames[i][0:-4]+'-edited.mp4'))
        #os.system('ffmpeg -y -hide_banner -loglevel error -stats -i {} -vf scale={}:-2,setsar=1:1 -c:v libx264 -c:a copy {}'.format(filenames[i],w,filenames[i][0:-4]+'-edited.mp4'))
        #newfileinfo = str(subprocess.run(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=width,height', '-of','csv=s=x:p=0', filenames[i]], stdout=subprocess.PIPE, stderr=subprocess.STDOUT).stdout)
        #os.system('ffprobe {}'.format(filenames[i]))
        #print('newfileinfo',newfileinfo,i)
        #os.system('ffmpeg -y -hide_banner -loglevel error -stats -i "concat:{}final.mp4 | {}" -c copy {}final.mp4'.format(newlfilepath,filenames[i][0:-4]+'-edited.mp4',newlfilepath))
        #os.system('ffmpeg -y -i {} -i {} -filter_complex "[0:v:0][0:a:0][1:v:0][1:a:0]concat=n=2:v=1:a=1[outv][outa]" -map "[outv]" -map "[outa]" {}'.format(final,filenames[i], outname))
        #os.system('ffmpeg -i {} -i {} -filter_complex "[0:v]scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:(ow-iw)/2:(oh-ih)/2[v0]; [v0][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]" -map "[v]" -map "[a]" -c:v libx264 -c:a aac -movflags +faststart {}'.format(final,filenames[i],w,h,w,h,outname))
        #os.system('ffmpeg -y -i {} -vf scale={}:-2,setsar=1:1 -c:v libx264 -c:a copy {}'.format(filenames[i],width,filenames[i][0:-4]+'-adjusted.mp4'))
        #os.system('ffmpeg -i {} -vf "scale={}:{}:force_original_aspect_ratio=decrease,pad={}:{}:-1:-1:color=black" -y {}'.format(filenames[i],width,height,width,height,filenames[i][0:-4]+'-adjusted.mp4'))
        final = outname
        print('loop num',i)
    for i in range(len(filenames)):
        filenames[i] = filenames[i][0:-4]+'-edited.mp4'
        newlfile.write('file '+"'{}'\n".format(filenames[i]))
    lfile.close()
    newlfile.close()
    print('escaped loop')
    #final = filenames[0]
    #print('we got here')
    #for i in range(1,len(filenames)):
    #    print('loopy time {}'.format(i))
    #    os.system('ffmpeg -i {} -i {} -filter_complex "[0:0] [0:1] [1:0] [1:1] concat=n=2:v=1:a=1 [v] [a]" -map [v] -map [a] {}'.format(final,filenames[i],outname))
    os.system('ffmpeg -y -hide_banner -loglevel error -stats -safe 0 -f concat -segment_time_metadata 1 -i {} -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 {}'.format(newlfilepath+'newlistfile.txt',outname))
    #os.system('ffmpeg -y -f concat -safe 0 -i {} -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 {}'.format(newlfilepath+'newlistfile.txt',outname))
    #'ffmpeg -i opening.mkv -i ending.mkv -filter_complex "[0:v] [0:a] [1:v] [1:a] concat=n=2:v=1:a=1 [v] [a]" -map "[v]" -map "[a]" output.mkv'
    #os.system('ffmpeg -f concat -safe 0 -i {} -c {}'.format(newlfilepath+'newlistfile.txt',outname))
    #os.system('ffmpeg -safe 0 -f concat -segment_time_metadata 1 -i {} -vf select=concatdec_select -af aselect=concatdec_select {}'.format(newlfilepath+'newlistfile.txt',outname))
    return


def trim(_input,output=0,start=0,end=0,dur=0):
    if output == 0:
        output = _input
    if dur != 0:
        os.system('ffmpeg -i {} -ss {} -t {} -async 1 {}'.format(_input,start,dur,output))
    elif end != 0:
        os.system('ffmpeg -i {} -ss {} -to {} -async 1 {}'.format(_input,start,end,output))
    return


def dub_photo(img,audio,video): #no overwriting files with same name, will crash
    #os.system('ffmpeg -loop 1 -y -i {} -i {} -shortest {}'.format(img,audio,video))
    os.system('ffmpeg -loop 1 -i {} -i {} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {}'.format(img,audio,video))
    return


def dub_video(video,audio,output):
    len_video = get_length(video)
    len_audio = get_length(audio)
    if len_video >= len_audio:
        os.system('ffmpeg -i {} -i {} -c:v copy -map 0:v:0 -map 1:a:0 -y {}'.format(video,audio,output))
    else:
        os.system('ffmpeg -i {} -i {} -c:v copy -map 0:v:0 -map 1:a:0 -shortest -y {}'.format(video, audio, output))
    return


def get_length(filename):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',filename], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return float(result.stdout)


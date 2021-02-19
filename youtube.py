import time
from selenium import webdriver
import requests  # to get image from the web
import shutil  # to save it locally
import random as r
import os

from editing import *
from misc import *
from pexels import *


#Get youtube videos based on keywords, etc
def get_yt_videos():

    return

#get youtube free audio
def get_yt_audios(filepath):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': '{}'.format(filepath)}
    chrome_options.add_experimental_option('prefs', prefs)
    web = webdriver.Chrome(options=chrome_options, executable_path='chrome/chromedriver')
    web.get('https://www.youtube.com/audiolibrary')
    web.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input').send_keys('imabot757@gmail.com')
    #TODO:sleep
    time.sleep(3)
    web.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    #sleep
    time.sleep(3)
    web.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys('botsaredumb')
    #sleep
    time.sleep(3)
    web.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    #sleep
    time.sleep(3)
    download_buttons = web.find_elements_by_id('download')
    for i in download_buttons:
        i.click()
        time.sleep(4) #TODO: fix
    print('downloaded {} audio files to {}'.format(len(download_buttons),filepath))
    web.quit()
    return

#start an upload but let user finish it
def start_yt_upload():

    return

#finish tasks from start_upload
def finish_yt_upload():

    return


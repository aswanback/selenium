import time
from selenium import webdriver
import requests  # to get image from the web
import shutil  # to save it locally
import random as r
import os
from editing import *
from misc import *
from pexels import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

#Get youtube videos based on keywords, etc
def get_yt_videos(query,filepath,number=0,duration=0):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': filepath}
    chrome_options.add_experimental_option('prefs', prefs)
    web = webdriver.Chrome(options=chrome_options, executable_path='chrome/chromedriver')
    '''
    web.get("https://www.youtube.com/results?search_query=" + str(query))
    web.find_element_by_xpath('//*[@id="video-title"]').click()
    url = web.current_url
    time.sleep(2)
    web.get('https://yt1s.com/youtube-to-mp4')
    paste = web.find_element_by_id("s_input")
    time.sleep(2)
    paste.send_keys(url)
    paste.send_keys(Keys.RETURN)
    time.sleep(5)
    dwnld_button = web.find_element_by_link_text('Download')
    dwnld_button.click()
    time.sleep(2)
    web.get("https://www.youtube.com/results?search_query=" + str(query))
    web.find_element_by_xpath('//*[@id="video-title"]').click()
    time.sleep(2)
    ActionChains(web) \
            .key_down(Keys.SHIFT) \
            .key_down("n") \
            .perform()
    time.sleep(2)
    '''
    web.get("https://www.youtube.com/results?search_query=" + str(query))
    web.find_element_by_xpath('//*[@id="video-title"]').click()
    time.sleep(4)
    current_url = web.current_url
    for i in range(number):
        print('video',i)
        time.sleep(3)
        #web.get(current_url)

        current_url = web.current_url
        print('assigning url {}'.format(current_url))
        print('got url')
        web.get('https://yt1s.com/youtube-to-mp4?q={}'.format(current_url))
        print('mp4 site')
        time.sleep(8)
        #paste = web.find_element_by_class_name("search__input")
        #time.sleep(1)
        #print('pasting url {} {}'.format(current_url,type(current_url)))

        #paste.send_keys('i am fucking gay')
        #print('im gay')
        #time.sleep(8)
        #print('paste')
        #paste.send_keys(Keys.RETURN)
        #time.sleep(3)
        dwnld_button = web.find_element_by_link_text('Download')
        dwnld_button.click()
        print('download')
        time.sleep(4)

        #web.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w')
        web.get(current_url)
        ActionChains(web) \
            .key_down(Keys.SHIFT) \
            .key_down("n") \
            .perform()
        print('new video')
        time.sleep(2)


    #if not duration == 0:   #do by duration
    #    dur = 0

        #dur += get_length(...)

   # if not number == 0:  #by by num
   #     iterations = number


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


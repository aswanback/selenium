import time
from selenium import webdriver
import requests  # to get image from the web
import shutil  # to save it locally
import random as r
import os

from selenium.webdriver.support.wait import WebDriverWait
import editing
import misc
from pexels import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#######################################################################
def get_yt_videos(query,filepath,number=0,duration=0):
    ##SETUP USE MODE##
    use_dur = False
    use_num = False
    if duration != 0:
        use_dur = True
    if number != 0:
        use_num = True

    ##SETUP LISTFILE
    listfile = open(filepath+'/listfile.txt', "w")

    ##SETUP CHROME##
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': filepath}
    chrome_options.add_experimental_option('prefs', prefs)
    web = webdriver.Chrome(options=chrome_options, executable_path='chrome/chromedriver')
    web.get("https://www.youtube.com/results?search_query=" + str(query))
    starting_url = web.current_url
    web.find_element_by_xpath('//*[@id="video-title"]').click()
    while (starting_url == web.current_url):
        time.sleep(0.5)

    dur = 0
    num_vids = 0
    while(True):
        ##PUT RIGHT LINK INTO YT1S.COM##
        current_url = web.current_url
        #thumb = web.find_element_by_id('thumbnail')
        #link = thumb.get_attribute('href')
        web.get('https://yt1s.com/youtube-to-mp4?q={}'.format(current_url))

        ##DOWNLOAD##
        WebDriverWait(web, 15).until(EC.presence_of_element_located((By.LINK_TEXT, 'Download')))
        dwnld_button = web.find_element_by_link_text('Download')
        dwnld_button.click()

        ##CHECK DOWNLOAD COMPLETE##
        misc.wait_download_complete(filepath)

        ##LENGTH OF NEWEST FILE##
        #for f in os.listdir(filepath):
        #    r = f.replace(" ", "")
        #    if (r != f):
        #        os.rename(f, r)
        file = max([os.path.join(filepath, f) for f in os.listdir(filepath)], key=os.path.getctime)
        newfile = file.replace(' ','-')
        os.rename(file,newfile)
        listfile.write('file '+"'{}'\n".format(newfile))
        dur += editing.get_length(newfile)
        print(dur)
        num_vids += 1

        ##NEW VIDEO##
        web.get(current_url)
        time.sleep(1)
        WebDriverWait(web, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'ytp-next-button')))
        web.find_element_by_class_name('ytp-next-button').click()
        elapsed = 0
        while (current_url == web.current_url):
            time.sleep(0.5)
            elapsed += 0.5
            if elapsed > 6:
                web.find_element_by_class_name('ytp-next-button').click()
            print('waiting')

        ##BREAK IF COMPLETE##
        if use_dur and dur >= duration:
            listfile.close()
            web.close()
            return filepath+'/listfile.txt'
        elif use_num and num_vids>=number:
            web.close()
            listfile.close()
            return filepath+'/listfile.txt'


########################################################################################
def get_yt_audios(filepath):    #TODO: Add filters
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': '{}'.format(filepath)}
    chrome_options.add_experimental_option('prefs', prefs)
    web = webdriver.Chrome(options=chrome_options, executable_path='chrome/chromedriver')
    wait = WebDriverWait(web, 15)
    web.get('https://www.youtube.com/audiolibrary')

    xp1 = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input'
    login = WebDriverWait(web, 10).until(EC.presence_of_element_located((By.XPATH, xp1)))
    login.send_keys('imabot757@gmail.com')

    xp2 = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button'
    login_button = WebDriverWait(web, 10).until(EC.presence_of_element_located((By.XPATH, xp2)))
    login_button.find_element_by_xpath(xp2).click()

    xp3 = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input'
    password = WebDriverWait(web, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
    password.send_keys('botsaredumb')

    xp4 = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button'
    password_button = WebDriverWait(web, 10).until(EC.presence_of_element_located((By.XPATH, xp4)))
    password_button.click()

    down_wait = WebDriverWait(web, 10).until(EC.presence_of_element_located((By.ID, 'download')))
    download_buttons = web.find_elements_by_id('download')
    for i in download_buttons:
        i.click()
        misc.wait_download_complete(filepath)
    print('downloaded {} audio files to {}'.format(len(download_buttons),filepath))
    web.quit()
    return

#start an upload but let user finish it
def start_yt_upload():

    return

#finish tasks from start_upload
def finish_yt_upload():

    return




#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 18 11:11:58 2021

@author: calebstevens
"""
from selenium.webdriver.common.keys import Keys
import time
import re
import requests  # to get image from the web
import shutil  # to save it locally
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random as r
import os

if __name__ == "__main__":
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': '/Users/calebstevens/Downloads/Videos'}
    chrome_options.add_experimental_option('prefs', prefs)
    web = webdriver.Chrome(chrome_options=chrome_options, executable_path='chrome/chromedriver')

    web.get('https://www.youtube.com')

    wait = WebDriverWait(web, 3)
    presence = EC.presence_of_element_located
    visible = EC.visibility_of_element_located

    # Navigate to url with video being appended to search_query
    video = 'That quiet kid in class'
    web.get("https://www.youtube.com/results?search_query=" + str(video))

    # play the video
    web.find_element_by_xpath('//*[@id="video-title"]').click()

    url = web.current_url

    time.sleep(2)

    web.get('https://yt1s.com/youtube-to-mp4')
    paste = web.find_element_by_id("s_input")

    time.sleep(2)

    paste.send_keys(url)
    paste.send_keys(Keys.RETURN)

    time.sleep(2)

    dwnld_button = web.find_element_by_link_text('Download')
    dwnld_button.click()




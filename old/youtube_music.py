import time
import re
import requests  # to get image from the web2
import shutil  # to save it locally
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random as r
import os
from misc import *

if __name__ == "__main__":
    web = webdriver.Chrome('../chrome/chromedriver')
    web.get('https://www.youtube.com/audiolibrary')
    web.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input').send_keys('imabot757@gmail.com')
    pause()
    web.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    pause()
    web.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input').send_keys('botsaredumb')
    pause()
    web.find_element_by_xpath('/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button').click()
    pause()
    download_buttons = web.find_elements_by_id('download')
    Initial_path = '/Users/andrewswanback/Downloads'
    for i in download_buttons:
        i.click()
        time.sleep(r.uniform(4,5))
        filename = max([os.path.join(Initial_path, f) for f in os.listdir(Initial_path)], key=os.path.getctime)
        shutil.move(filename, os.path.join(Initial_path, r"music/"))

        #time.sleep(r.uniform(4,5))
    web.quit()
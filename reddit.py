import action as action
from selenium.webdriver.chrome import options
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
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from editing import *
import misc



'def reddit_farmer(subreddit, timeframe, number,filepath, ):'
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': "/users/calebstevens/documents/Selenium_data/reddit"}
chrome_options.add_experimental_option('prefs', prefs)


chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)
chrome_options.add_argument("--disable-notifications")

web = webdriver.Chrome(executable_path='chrome/chromedriver', options=chrome_options)

web.get("https://www.reddit.com/"+"r/memes"+"/")

time.sleep(1)
subject = web.find_element_by_class_name("_3Oa0THmZ3f5iZXAQ0hBJ0k")
subject.click()

url = web.current_url

web.get('https://viddit.red/')

download = web.find_element_by_xpath("/html/body/section[1]/div/div[1]/div/form/div/input")
download.send_keys(url)

download = web.find_element_by_xpath("/html/body/section[1]/div/div[1]/div/form/div/div/button")
download.click()

time.sleep(5)

donwnload = web.find_element_by_id("dlbutton")
download.click()

#Actions action= new Actions(driver);
#action.contextClick(Image).build().perform();
#web.navigate().back()




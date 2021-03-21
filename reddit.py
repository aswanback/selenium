from selenium.webdriver.chrome import options
from selenium.webdriver.common.keys import Keys
import time
import re
import requests  # to get image from the web
import shutil  # to save it locally
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import random as r
import os
from selenium.webdriver.common.action_chains import ActionChains
from editing import *
import misc

def reddit(folder,subreddit):  #def reddit_farmer(subreddit, timeframe, number,filepath, ):
    get = misc.getme(folder)
    try:
        get.site("https://www.reddit.com/" + subreddit + "/")
        url = get.by_xpath("/html/body/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div[3]/div[1]/div[4]/div[3]/div/div/div[2]/div[3]/div/div[2]/div/a").get_attribute('href')
        get.site(url)
        get.by_class_name("_3Oa0THmZ3f5iZXAQ0hBJ0k").click()
        get.web.switch_to.window(get.web.window_handles[1])
        new_url = get.current_url()
        print(new_url)
        filename = new_url.translate({ord(i): None for i in '/:'})
        misc.download_by_link(url=new_url,filepath=folder,filename=filename)
    finally:
        time.sleep(10)
        get.close()



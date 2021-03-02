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
from selenium.webdriver.common.action_chains import ActionChains

#make files go right place
chrome_options = webdriver.ChromeOptions()
prefs = {'download.default_directory': "/users/calebstevens/documents/Selenium_data/tiktok/"}
chrome_options.add_experimental_option('prefs', prefs)

#delta 7 going dark
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

web = webdriver.Chrome(executable_path='chrome/chromedriver',options=chrome_options)

#Open Browser



def tik_tok_farmer(filepath, number):
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': filepath}
    chrome_options.add_experimental_option('prefs', prefs)

    # delta 7 going dark
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    web = webdriver.Chrome(executable_path='chrome/chromedriver', options=chrome_options)

    web.get("https://www.facebook.com/login.php?skip_api_login=1&api_key=1862952583919182&kid_directed_site=0&app_id=1862952583919182&signed_next=1&next=https%3A%2F%2Fwww.facebook.com%2Fv2.9%2Fdialog%2Foauth%2F%3Fclient_id%3D1862952583919182%26response_type%3Dtoken%26redirect_uri%3Dhttps%253A%252F%252Fwww.tiktok.com%252Flogin%252F%26state%3D%257B%2522client_id%2522%253A%25221862952583919182%2522%252C%2522network%2522%253A%2522facebook%2522%252C%2522display%2522%253A%2522popup%2522%252C%2522callback%2522%253A%2522_hellojs_63fpml0k%2522%252C%2522state%2522%253A%2522%2522%252C%2522redirect_uri%2522%253A%2522https%253A%252F%252Fwww.tiktok.com%252Flogin%252F%2522%252C%2522scope%2522%253A%2522basic%2522%257D%26scope%3Dpublic_profile%26auth_type%3Dreauthenticate%26display%3Dpopup%26ret%3Dlogin%26fbapp_pres%3D0%26logger_id%3De330b458-cfb2-495b-9e00-babb25070a77%26tp%3Dunspecified&cancel_url=https%3A%2F%2Fwww.tiktok.com%2Flogin%2F%3Ferror%3Daccess_denied%26error_code%3D200%26error_description%3DPermissions%2Berror%26error_reason%3Duser_denied%26state%3D%257B%2522client_id%2522%253A%25221862952583919182%2522%252C%2522network%2522%253A%2522facebook%2522%252C%2522display%2522%253A%2522popup%2522%252C%2522callback%2522%253A%2522_hellojs_63fpml0k%2522%252C%2522state%2522%253A%2522%2522%252C%2522redirect_uri%2522%253A%2522https%253A%252F%252Fwww.tiktok.com%252Flogin%252F%2522%252C%2522scope%2522%253A%2522basic%2522%257D%23_%3D_&display=popup&locale=en_US&pl_dbl=0")
    login = web.find_element_by_xpath("/html/body/div/div[2]/div[1]/form/div/div[1]/div/input")
    login.send_keys("nrubenstein0405@gmail.com")

    login = web.find_element_by_xpath("/html/body/div/div[2]/div[1]/form/div/div[2]/div/input")
    login.send_keys("nacny123")

    login = web.find_element_by_xpath("/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]/input")
    login.click()

    time.sleep(10)

    feed = web.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a[2]")
    feed.click()

    time.sleep(1)

    video = web.find_element_by_class_name("item-video-container")
    video.click()

    time.sleep(1)
    '''


    url = web.current_url

    time.sleep(1)


    web.get("https://qload.info/")

    time.sleep(1)

    search = web.find_element_by_xpath("/html/body/main/div[1]/div[2]/div/form/div/input")
    search.send_keys(url)

    download1 = web.find_element_by_xpath("/html/body/main/div[1]/div[2]/div/form/div/div/button")
    download1.click()

    time.sleep(15)

    web.get("https://www.tiktok.com/following?lang=en")

    time.sleep(2)

    newvid = web.find_element_by_class_name("item-video-container")
    newvid.click()

    time.sleep(1)
    '''
    url = web.current_url

    for num in range (number):

        time.sleep(1)

        web.get("https://qload.info/")

        time.sleep(1)

        search = web.find_element_by_xpath("/html/body/main/div[1]/div[2]/div/form/div/input")
        search.send_keys(url)

        download1 = web.find_element_by_xpath("/html/body/main/div[1]/div[2]/div/form/div/div/button")
        download1.click()

        time.sleep(12)

        web.get("https://www.tiktok.com/following?lang=en")
        bs = web.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a[1]")
        bs.click()

        time.sleep(1)

        bs2 = web.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a[2]")
        bs2.click()
        time.sleep(2)

        newvid = web.find_element_by_class_name("item-video-container")
        newvid.click()

        time.sleep(1)

        next_tok = web.find_element_by_class_name("arrow-right")
        for i in range(num+1):
            time.sleep(1)
            next_tok.click()

        url = web.current_url
    return


tik_tok_farmer("/Users/calebstevens/documents/Selenium_data/tiktok", 10)



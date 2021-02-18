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
import random as r
import os

def download_img_by_link(image_url, filepath, filename):
    r = requests.get(image_url,
                     stream=True)  # Open the url image, set stream to True, this will return the stream content.
    if r.status_code == 200:  # Check if the image was retrieved successfully
        r.raw.decode_content = True  # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        with open('{}/{}'.format(filepath, filename), 'wb') as f:  # Open a local file with wb permission.
            shutil.copyfileobj(r.raw, f)
    else:
        print('{} couldn\'t be retreived'.format(filename))

r.seed()
def pause():
    time.sleep(r.uniform(0.7,1.2))

def getDownLoadedFileName(waitTime):
    web.execute_script("window.open()")
    # switch to new tab
    web.switch_to.window(web.window_handles[-1])
    # navigate to chrome downloads
    web.get('chrome://downloads')
    # define the endTime
    endTime = time.time()+waitTime
    while True:
        try:
            # get downloaded percentage
            downloadPercentage = web.execute_script(
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('#progress').value")
            # check if downloadPercentage is 100 (otherwise the script will keep waiting)
            if downloadPercentage == 100:
                # return the file name once the download is completed
                return web.execute_script("return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList downloads-item').shadowRoot.querySelector('div#content  #file-link').text")
        except:
            pass
        time.sleep(1)
        if time.time() > endTime:
            break

if __name__ == "__main__":
    web = webdriver.Chrome('chrome/chromedriver')
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
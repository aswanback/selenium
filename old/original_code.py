
#FROM MAIN.PY
'''
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

path = {
    'andrew': '/Users/andrewswanback/Downloads/dummy',
    'caleb': '/Users/calebstevens/Downloads/dummy'
}

def download_img_by_link(image_url, filepath, filename):
    r = requests.get(image_url, stream=True) # Open the url image, set stream to True, this will return the stream content.
    if r.status_code == 200:    # Check if the image was retrieved successfully
        r.raw.decode_content = True # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        with open('{}/{}'.format(filepath,filename), 'wb') as f: # Open a local file with wb permission.
            shutil.copyfileobj(r.raw, f)
    else:
        print('{} couldn\'t be retreived'.format(filename))

#def download_filter_youtube_music(filepath,filename,num_tracks=1,mood='', genre='', track_title='', duration=''):

if __name__ == "__main__":
    web = webdriver.Chrome('chrome/chromedriver')
    web.get('http://www.pexels.com/');
    search = web.find_element_by_xpath('/html/body/header/section/div/form/div[1]/input')
    search.send_keys("wave")
    search.submit()
    pics = web.find_elements_by_class_name('photos__column')
    matches = re.findall(r'(?=data-big-src=").+(?!\"\s).+?',web.page_source) #re.findall(r'(?:https://images.pexels.com)/photos/.+(?:\")', driver.page_source) #re.findall(r'(?:href=")/photo/.+(?:\">)',driver.page_source)
    new = []
    for i in range(len(matches)):
        new.append(re.split(r'\s',matches[i]))
    for i in range(len(new)):
        new[i] = new[i][0][14:-1]

    filepath = path['andrew']
    filename = []
    num_written = 0
    #print(len(new))
    for i in range(len(new)-1):
        #print(i, new[i])

        image_url = new[i]
        try:
            filename = re.findall(r'(?:pexels-photo-)\d+(?:\.jpeg)',new[i])[0]
        except:
            filename = 'default-{}'.format(i)
        finally:
            download_img_by_link(image_url, filepath, filename)
            num_written += 1
    print('{} of {} files written'.format(num_written,len(new)-1))
    # time.sleep(10)
    web.quit()
'''

#FROM Video_acquisition.py

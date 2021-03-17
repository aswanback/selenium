import urllib.request
from pexels import *
import os
import editing
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def clear(folder):
    os.system('rm {}/*'.format(folder))

def clean(folder,hard=False):
    if hard == True:
        remove_list = [name for name in os.listdir(folder) if ('.txt' or '.DS_Store' or 'comp.mp4') not in name]
    else:
        remove_list = [name for name in os.listdir(folder) if ('.txt' or '-e.mp4' or '.DS_Store' or 'comp.mp4')not in name]
    for i in remove_list:
        os.system('rm {}'.format(folder+'/'+i))

def folder_duration(folder):
    total = 0
    for i in os.listdir(folder):
        total += editing.get_length(i)
    return total

def download_video_by_link(url,filepath,filename):
    urllib.request.urlretrieve(url, '{}/{}.mp4'.format(filepath,filename))

def download_img_by_link(image_url, filepath, filename):
    r = requests.get(image_url, stream=True) # Open the url image, set stream to True, this will return the stream content.
    if r.status_code == 200:    # Check if the image was retrieved successfully
        r.raw.decode_content = True # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        with open('{}/{}'.format(filepath,filename), 'wb') as f: # Open a local file with wb permission.
            shutil.copyfileobj(r.raw, f)
    else:
        print('{} couldn\'t be retrieved'.format(filename))

def wait_download_complete(folder,timeout=20):
    still_working = True
    elapsed = 0
    while still_working and elapsed < timeout:
        still_working = False
        time.sleep(1)
        elapsed += 1
        for filename in os.listdir(folder):
            if filename.endswith('.crdownload'):
                still_working = True

def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))

class getme:
    timeout = 20
    chrome_options = webdriver.ChromeOptions()
    web2 = webdriver.Chrome(executable_path='chrome/chromedriver', options=chrome_options)
    def __init__(self,folder):
        prefs = {'download.default_directory': folder}
        self.chrome_options.add_experimental_option('prefs', prefs)
        # self.chrome_options.add_argument("--incognito")
        # self.chrome_options.add_argument("--mute-audio")
        # self.chrome_options.add_argument("--headless")
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        self.chrome_options.add_experimental_option('useAutomationExtension', False)
        self.chrome_options.add_extension('extension_5_1_0_0.crx')
    def by_class_name(self,class_name):
        time.sleep(0.2)
        WebDriverWait(self.web2, self.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        return self.web2.find_element_by_class_name(class_name)
    def by_xpath(self,xpath):
        time.sleep(4)
        WebDriverWait(self.web2, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        a = self.web2.find_element_by_xpath(xpath)
        return a
    def by_id(self,id):
        time.sleep(0.2)
        WebDriverWait(self.web2, self.timeout).until(EC.presence_of_element_located((By.ID, id)))
        return self.web2.find_element_by_id(id)
    def by_link_text(self,link_text):
        time.sleep(0.2)
        WebDriverWait(self.web2, self.timeout).until(EC.presence_of_element_located((By.LINK_TEXT, link_text)))
        return self.web2.find_element_by_xpath(link_text)
    def site(self,site):
        time.sleep(0.2)
        self.web2.get(site)
    def current_url(self):
        return self.web2.current_url
    def close(self):
        self.web2.close()
    def click_id(self,id):
        a = WebDriverWait(self.web2, self.timeout).until(EC.element_to_be_clickable((By.ID,id)))
        a.click()
    def click_xpath(self,xpath):
        a = WebDriverWait(self.web2, self.timeout).until(EC.element_to_be_clickable((By.XPATH,xpath)))
        a.click()
    def click_class_name(self,class_name):
        a = WebDriverWait(self.web2, self.timeout).until(EC.element_to_be_clickable((By.CLASS_NAME,class_name)))
        a.click()
    def click_link_text(self,link_text):
        a = WebDriverWait(self.web2, self.timeout).until(EC.element_to_be_clickable((By.LINK_TEXT,link_text)))
        a.click()
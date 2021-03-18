import urllib.request
from pexels import *
import os
import editing
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import shutil

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

def wait_until_download_complete(folder,timeout=20):
    still_working = True
    elapsed = 0
    time.sleep(0.1)
    while still_working and elapsed<timeout:
        while(len(os.listdir(folder)) == 0):
            time.sleep(0.2)
            print("empty")
        still_working = False
        for filename in os.listdir(folder):
            if filename.endswith('.crdownload'):
                print(f"doing some shit {filename}")
                still_working = True
        time.sleep(0.2)
        elapsed += 0.2

def latest_download_file(path):
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    return newest

def wait_download_complete(filepath):
    fileends = "crdownload"
    while "crdownload" == fileends:
        time.sleep(0.4)
        newest_file = editing.latest_download_file(filepath)
        if "crdownload" in newest_file:
            fileends = "crdownload"
        else:
            fileends = "none"

def notify(title, subtitle, message):
    t = '-title {!r}'.format(title)
    s = '-subtitle {!r}'.format(subtitle)
    m = '-message {!r}'.format(message)
    os.system('terminal-notifier {}'.format(' '.join([m, t, s])))






class getme:
    timeout = 20
    def __init__(self,folder):
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': folder}
        chrome_options.add_experimental_option('prefs', prefs)
        #chrome_options.add_argument("--incognito")
        chrome_options.add_argument("--mute-audio")
        #chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_extension('extension_5_1_0_0.crx')
        self.web2 = webdriver.Chrome(executable_path='chrome/chromedriver', options=chrome_options)
        self.folder = folder

    def by_id(self,x):
        class_var = by_var(web2=self.web2, timeout=self.timeout, folder=self.folder, _method_var=x, METHOD='id')
        self._method_var = x
        return class_var.element
    def by_name(self,x):
        class_var = by_var(web2=self.web2, timeout=self.timeout, folder=self.folder, _method_var=x, METHOD='name')
        self._method_var = x
        return class_var.element
    def by_class_name(self,x):
        class_var = by_var(web2=self.web2, timeout=self.timeout, folder=self.folder, _method_var=x, METHOD='class_name')
        self._method_var = x
        return class_var.element
    def by_xpath(self,x):
        class_var = by_var(web2=self.web2, timeout=self.timeout, folder=self.folder, _method_var=x, METHOD='xpath')
        self._method_var = x
        return class_var.element
    def by_link_text(self,x):
        class_var = by_var(web2=self.web2, timeout=self.timeout, folder=self.folder, _method_var=x, METHOD="link_text")
        self._method_var = x
        return class_var.element

    def site(self, site):
        time.sleep(0.2)
        self.web2.get(site)

    def current_url(self):
        return self.web2.current_url

    def close(self):
        self.web2.close()

    '''
    def by_class_name(self,class_name):
        time.sleep(0.2)
        WebDriverWait(self.web2, self.timeout).until(EC.presence_of_element_located((By.CLASS_NAME, class_name)))
        return self.web2.find_element_by_class_name(class_name)
    def by_xpath(self,xpath):
        time.sleep(0.2)
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
    def click_by_id(self,id):
        a = WebDriverWait(self.web2, self.timeout).until(EC.element_to_be_clickable((By.ID,id)))
        a.click()
    def click_by_xpath(self, xpath):
        a = WebDriverWait(self.web2, self.timeout).until(EC.element_to_be_clickable((By.XPATH,xpath)))
        a.click()
    def click_by_class_name(self,class_name):
        a = WebDriverWait(self.web2, self.timeout).until(EC.element_to_be_clickable((By.CLASS_NAME,class_name)))
        a.click()
    def click_by_link_text(self,link_text):
        a = WebDriverWait(self.web2, self.timeout).until(EC.element_to_be_clickable((By.LINK_TEXT,link_text)))
        a.click()
    def send_keys_by_xpath(self,xpath,sent_keys):
        a = WebDriverWait(self.web2, self.timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))
        a.send_keys(sent_keys)
    '''


class by_var(getme):
    element = 12
    def __init__(self, folder, web2, _method_var, timeout,METHOD):
        if METHOD == "id":
            self.element = WebDriverWait(web2, timeout).until(EC.presence_of_element_located((By.ID, _method_var)))
        if METHOD == "name":
            self.element = WebDriverWait(web2, timeout).until(EC.presence_of_element_located((By.NAME, _method_var)))
        if METHOD == "class_name":
            self.element = WebDriverWait(web2, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, _method_var)))
        if METHOD == "xpath":
            self.element = WebDriverWait(web2, timeout).until(EC.presence_of_element_located((By.XPATH, _method_var)))
        if METHOD == "link_text":
            self.element = WebDriverWait(web2, timeout).until(EC.presence_of_element_located((By.LINK_TEXT, _method_var)))
        super().__init__(folder)

    def click(self):
        print(self.element)
        self.element.click()
    def send_keys(self,keys):
        self.element.send_keys(keys)
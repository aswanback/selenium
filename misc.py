import urllib.request
from old.pexels import *
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
        remove_list = [name for name in os.listdir(folder) if ('.txt' or '.DS_Store' or 'comp.mp4' or 'final.mp4') not in name]
    else:
        remove_list = [name for name in os.listdir(folder) if ('.txt' or '-e.mp4' or '.DS_Store' or 'comp.mp4' or 'final.mp4')not in name]
    for i in remove_list:
        os.system('rm {}'.format(folder+'/'+i))
def folder_duration(folder):
    total = 0
    for i in os.listdir(folder):
        total += editing.get_length(i)
    return total
def batch_rename(folder,active):
    if active:
        file = [f for f in os.listdir(folder) if f != 'archive.txt']
        i = 1
        newfile = 'video1.mp4'
        while newfile in os.listdir(folder):
            newfile = f'video{i}.mp4'
            i+=1
        os.rename(folder+'/'+file, folder+'/'+newfile)
        time.sleep(0.1)
    else:
        file = [f for f in os.listdir(folder) if f != 'archive.txt']
        for f in file:
            new1 = f.replace(' ','-')
            newfile = new1[11:]
            os.rename(folder + '/' + f, folder+'/'+newfile)

def download_by_link(url, filepath, filename):
    r = requests.get(url, stream=True) # Open the url image, set stream to True, this will return the stream content.
    if r.status_code == 200:    # Check if the image was retrieved successfully
        r.raw.decode_content = True # Set decode_content value to True, otherwise the downloaded image file's size will be zero.
        with open('{}/{}'.format(filepath,filename), 'wb') as f: # Open a local file with wb permission.
            shutil.copyfileobj(r.raw, f)
    else:
        print('{} couldn\'t be retrieved'.format(filename))
def wait_until_download_complete(folder,timeout=20):
    still_working = True
    elapsed = 0.0
    time.sleep(0.1)
    while still_working and elapsed<timeout:
        while(len(os.listdir(folder)) == 0):
            time.sleep(0.2)
            #print("empty")
        still_working = False
        for filename in os.listdir(folder):
            if '.crdownload' in filename:
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
        newest_file = latest_download_file(filepath)
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
    def __init__(self,folder,incognito=False,headless=False,mute=False):
        chrome_options = webdriver.ChromeOptions()
        prefs = {'download.default_directory': folder}
        chrome_options.add_argument("--disable-notifications")
        chrome_options.add_experimental_option('prefs', prefs)
        if(incognito):
            chrome_options.add_argument("--incognito")
        if(mute):
            chrome_options.add_argument("--mute-audio")
        if(headless):
            chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_extension('extension_5_1_0_0.crx')
        self.web = webdriver.Chrome(executable_path='chrome/chromedriver', options=chrome_options)
        self.folder = folder
    def by_id(self,x):
        id = by_var(web2=self.web, timeout=self.timeout, _method_var=x, METHOD='id')
        return id.element
    def by_name(self,x):
        name = by_var(web2=self.web, timeout=self.timeout, _method_var=x, METHOD='name')
        self._method_var = x
        return name.element
    def by_class_name(self,x):
        class_name = by_var(web2=self.web, timeout=self.timeout, _method_var=x, METHOD='class_name')
        self._method_var = x
        return class_name.element
    def by_xpath(self,x):
        xpath = by_var(web2=self.web, timeout=self.timeout, _method_var=x, METHOD='xpath')
        self._method_var = x
        return xpath.element
    def by_link_text(self,x):
        link_text = by_var(web2=self.web, timeout=self.timeout, _method_var=x, METHOD="link_text")
        self._method_var = x
        return link_text.element
    def by_css_selector(self,x):
        css = by_var(web2=self.web, timeout=self.timeout, _method_var=x, METHOD="css")
        self._method_var = x
        return css.element

    def site(self,url):
        self.web.get(url)
        '''if first_site:
            starting_url = self.web.current_url
        else:
            starting_url = '0'
        self.web.get(url)
        time.sleep(0.2)
        elapsed = 0.0
        while self.web.current_url == starting_url:
            time.sleep(0.2)
            elapsed += 0.2
            if elapsed > 4 and elapsed.is_integer():
                print(f'Stalled for {elapsed}')
            if elapsed >= 20:
                print(f'Timeout in get.site({url}')'''
    def wait_until_move_from(self,url):
        elapsed = 0.0
        while self.web.current_url == url:
            time.sleep(0.2)
            elapsed += 0.2
            if elapsed > 4 and elapsed.is_integer():
                print(f'Stalled for {elapsed}')
            if elapsed >= 20:
                print(f'Timeout in get.site({url}')
    def current_url(self):
        return self.web.current_url
    def back(self):
        self.web.execute_script("window.history.go(-1)")
    def close(self):
        self.web.close()

    def archive(self,url):
        archive = open(self.folder + '/archive.txt', 'a')
        archive.write(url + '\n')
        archive.close()
    def master_archive(self,url):
        video_title = self.by_css_selector('h1.title yt-formatted-string').text
        master_archive = open('master_archive.txt', 'a')
        master_archive.write(url + ' ' + video_title + '\n')
        master_archive.close()

    def yt_duration(self):
        length_of_video = self.by_class_name('ytp-time-duration').text
        match = re.findall(r'(\d+):(\d+)', length_of_video)
        while len(match) == 0:
            length_of_vid = self.by_class_name('ytp-time-duration').text
            match = re.findall(r'(\d+):(\d+)', length_of_vid)
        time_secs = int(match[0][0]) * 60 + int(match[0][1])
        return time_secs

class by_var(object):
    element = 12
    def __init__(self, web2, _method_var, timeout,METHOD):
        if METHOD == "id":
            self.element = WebDriverWait(web2, timeout).until(EC.presence_of_element_located((By.ID, _method_var)),message="Couldn't get by id")
        if METHOD == "name":
            self.element = WebDriverWait(web2, timeout).until(EC.presence_of_element_located((By.NAME, _method_var)),message="Couldn't get by name")
        if METHOD == "class_name":
            self.element = WebDriverWait(web2, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, _method_var)),message="Couldn't get by class name")
        if METHOD == "xpath":
            self.element = WebDriverWait(web2, timeout).until(EC.presence_of_element_located((By.XPATH, _method_var)),message="Couldn't get by xpath")
        if METHOD == "link_text":
            self.element = WebDriverWait(web2, timeout).until(EC.presence_of_element_located((By.LINK_TEXT, _method_var)),message="Couldn't get by link text")
        if METHOD == "css":
            self.element = WebDriverWait(web2, timeout).until(EC.presence_of_element_located((By.CSS_SELECTOR, _method_var)),message="Couldn't get by css selector")
    def click(self):
        #print(self.element)
        self.element.click()
    def send_keys(self,keys):
        self.element.send_keys(keys)
    def text(self):
        return self.element.text
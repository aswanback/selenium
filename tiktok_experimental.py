import time
import re
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from editing import *
import misc

def tik_tok_farmer(folder, number):
    get = getme(folder)  # set up get class

    # chrome_options.add_argument("--incognito")
    # chrome_options.add_argument("--headless")

    '''
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': folder}
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    web2 = webdriver.Chrome(executable_path='chrome/chromedriver', options=chrome_options)
    '''
    try:
        site1 = 'https://www.facebook.com/login.php?skip_api_login=1&api_key=1862952583919182&kid_directed_site=0&app_id=1862952583919182&signed_next=1&next=https%3A%2F%2Fwww.facebook.com%2Fv2.9%2Fdialog%2Foauth%2F%3Fclient_id%3D1862952583919182%26response_type%3Dtoken%26redirect_uri%3Dhttps%253A%252F%252Fwww.tiktok.com%252Flogin%252F%26state%3D%257B%2522client_id%2522%253A%25221862952583919182%2522%252C%2522network%2522%253A%2522facebook%2522%252C%2522display%2522%253A%2522popup%2522%252C%2522callback%2522%253A%2522_hellojs_63fpml0k%2522%252C%2522state%2522%253A%2522%2522%252C%2522redirect_uri%2522%253A%2522https%253A%252F%252Fwww.tiktok.com%252Flogin%252F%2522%252C%2522scope%2522%253A%2522basic%2522%257D%26scope%3Dpublic_profile%26auth_type%3Dreauthenticate%26display%3Dpopup%26ret%3Dlogin%26fbapp_pres%3D0%26logger_id%3De330b458-cfb2-495b-9e00-babb25070a77%26tp%3Dunspecified&cancel_url=https%3A%2F%2Fwww.tiktok.com%2Flogin%2F%3Ferror%3Daccess_denied%26error_code%3D200%26error_description%3DPermissions%2Berror%26error_reason%3Duser_denied%26state%3D%257B%2522client_id%2522%253A%25221862952583919182%2522%252C%2522network%2522%253A%2522facebook%2522%252C%2522display%2522%253A%2522popup%2522%252C%2522callback%2522%253A%2522_hellojs_63fpml0k%2522%252C%2522state%2522%253A%2522%2522%252C%2522redirect_uri%2522%253A%2522https%253A%252F%252Fwww.tiktok.com%252Flogin%252F%2522%252C%2522scope%2522%253A%2522basic%2522%257D%23_%3D_&display=popup&locale=en_US&pl_dbl=0'
        #web.get(site1)
        get.site(site1)

        xpath = "/html/body/div/div[2]/div[1]/form/div/div[1]/div/div/input"
        get.send_keys_by_xpath(xpath,"nrubenstein0405@gmail.com")
        #WebDriverWait(web2, 20).until(EC.presence_of_element_located((By.XPATH, xpath)))
        #login = web.find_element_by_xpath(xpath)

        xpath = "/html/body/div/div[2]/div[1]/form/div/div[2]/div/div/input"
        get.send_keys_by_xpath(xpath,"nacny123")
        #login = web2.find_element_by_xpath(xpath)

        xpath = "/html/body/div/div[2]/div[1]/form/div/div[3]/label[2]"
        #login = web2.find_element_by_xpath(xpath)
        get.click_by_xpath(xpath)

        #WebDriverWait(web2, 120).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a[2]")))
        #bruh = web.find_element_by_xpath("/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a[2]")

        xpath = "/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a[2]"
        get.click_by_xpath(xpath)
        #get.click_xpath(xpath)

        #time.sleep(1)
        #time.sleep(0.1)
        #WebDriverWait(web2, 120).until(EC.presence_of_element_located((By.CLASS_NAME, "item-video-container")))
        #video = web2.find_element_by_class_name("item-video-container")
        get.click_by_class_name("item-video-container")

        time.sleep(0.5)

        url = get.current_url()
        for num in range(number):
            time.sleep(0.5)
            get.site("https://qload.info/")
            time.sleep(1)
            xpath = "/html/body/main/div[1]/div[2]/div/form/div/input"
            #WebDriverWait(web2, 120).until(EC.presence_of_element_located((By.XPATH, xpath)))
            #search = web2.find_element_by_xpath("/html/body/main/div[1]/div[2]/div/form/div/input")
            get.send_keys_by_xpath(xpath,url)
            #print(search)
            #search.send_keys(url)

            xpath = "/html/body/main/div[1]/div[2]/div/form/div/div/button"
            #download1 = web2.find_element_by_xpath(xpath)
            get.click_by_xpath(xpath)

            #print(f'Downloading {num_vids + 1} - Duration: {time_secs}')
            #misc.wait_download_complete(folder)
            #num_vids += 1  # Download video
            time.sleep(10)
            '''
            time.sleep(1)
            file = max([os.path.join(folder, f) for f in os.listdir(folder) if f != 'archive.txt'],
                       key=os.path.getctime)
            i = 1
            newfile = 'video1.mp4'
            while newfile in os.listdir(folder):
                newfile = f'video{i}.mp4'
                i += 1
            newfile = folder + '/' + newfile
            os.rename(file, newfile)
            time.sleep(0.1)
            #print(f'Downloaded  {num_vids}  Duration: {datetime.timedelta(seconds=round(dur))}')
            '''
            #print(f'oslistdir{os.listdir(folder)}')
            get.site("https://www.tiktok.com/following?lang=en")
            xpath = "/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a[1]"
            get.click_by_xpath(xpath)
            #bs = web2.find_element_by_xpath(xpath)

            time.sleep(0.1)
            xpath = "/html/body/div[1]/div/div[2]/div[1]/div/div[1]/div/div[1]/div[1]/a[2]"
            #WebDriverWait(web2, 120).until(EC.presence_of_element_located((By.XPATH, xpath)))
            #bs2 = web2.find_element_by_xpath(xpath)
            get.click_by_xpath(xpath)

            time.sleep(0.2)
            #WebDriverWait(web2, 120).until(EC.presence_of_element_located((By.CLASS_NAME, "item-video-container")))
            #newvid = web2.find_element_by_class_name("item-video-container")
            get.click_by_class_name("item-video-container")

            for i in range(num+1):
                time.sleep(0.1)
                #WebDriverWait(web2, 120).until(EC.presence_of_element_located((By.CLASS_NAME, "arrow-right")))
                #next_tok = web2.find_element_by_class_name("arrow-right")
                get.click_by_class_name("arrow-right")
                time.sleep(0.1)

            url = get.current_url()
    finally:
        files = os.listdir(folder)
        for i in range(len(files)):
            os.rename(folder+'/'+files[i],folder+'/'+f"video{i}.mp4")
        time.sleep(15)
        get.close()
        #web.close()

#tik_tok_farmer("/Users/andrewswanback/documents/sd/tiktok", 10)
#concat("/users/calebstevens/documents/Selenium_data/tiktok",resolution='tiktok')

import time
from selenium import webdriver
import os
import re
from selenium.webdriver.support.wait import WebDriverWait
import misc
from pexels import *
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import editing

def get_yt_videos(query, folder, max_length=100,number=0, duration=0):
    use_dur = False
    use_num = False
    if duration > 0:
        use_dur = True
    if number > 0:
        use_num = True
    dur = 0
    num_vids = 0  # Set up number, dur
    get = misc.getme(folder,mute=True)
    get.site("https://www.youtube.com/results?search_query=" + str(query))
    starting_url = get.current_url()
    get.by_xpath('//*[@id="video-title"]').click()
    while starting_url == get.current_url():
        time.sleep(0.2) # Set up Chrome and load youtube
    if 'archive.txt' in os.listdir(folder):
        archive = open(folder + '/archive.txt', 'r')
        url_list = [i[0:-2] for i in archive.readlines()]
        archive.close()
        print(url_list)
    else:
        url_list = [] # Archive.txt
    try:
        while True:
            current_url = get.current_url()
            time.sleep(0.5)
            length_of_video = get.by_class_name('ytp-time-duration').text
            match = re.findall(r'(\d+):(\d+)',length_of_video)
            while len(match) == 0:
                length_of_vid = get.by_class_name('ytp-time-duration').text
                match = re.findall(r'(\d+):(\d+)', length_of_vid)
            time_secs = int(match[0][0])*60+int(match[0][1]) # Get video duration before download
            print(f'video duration: {time_secs}')

            if current_url in url_list:
                print("Skipping this video")
                get.by_class_name('ytp-next-button').click()
                elapsed = 0
                while current_url == get.current_url():
                    time.sleep(0.2)
                    elapsed += 0.2
                    if elapsed > 4:
                        print('Stalled for {}'.format(int(elapsed)))  # Go to next video + stall message
                        get.by_class_name('ytp-next-button').click()

            if current_url not in url_list and time_secs > max_length:
                print('video too long, getting alternate...')
                #get.site(current_url)
                time.sleep(0.4)
                #TODO: FIND THE GODDAMN XPATH OR SOME SHIT IDFK
                #xpath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[3]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer[1]/div[1]/ytd-thumbnail/a"
                #class_name = "yt-simple-endpoint style-scope ytd-compact-video-renderer"
                #thumb_list = get.by_id('thumbnail').get_attribute('href')
                #rel_xpath = "(//a[@id='video-title'])[position()>1]"
                #second_vid = get.by_xpath(rel_xpath).get_attribute('href')
                get.by_class_name('ytp-next-button').click()
                elapsed = 0
                #second_vid = f'https://www.youtube.com{thumb_list}'
                #get.site(second_vid)
                while current_url == get.current_url():
                    time.sleep(0.2)
                    elapsed += 0.2
                    if elapsed > 4:
                        print(f'Stalled for {elapsed:.1f}')
                        #get.site(second_vid) # Get second video in list + stall message
                        get.by_class_name('ytp-next-button').click()
                print("new video got from skip")

            if current_url not in url_list and time_secs < max_length:
                archive = open(folder + '/archive.txt', 'a')
                archive.write(current_url+'\n')
                archive.close()
                url_list.append(current_url) # Archive and url_list
                get.site(f'https://yt1s.com/youtube-to-mp4?q={current_url}')
                get.by_link_text("Download").click()
                print(f'Downloading {num_vids+1} - Duration: {time_secs}')
                misc.wait_download_complete(folder)
                num_vids += 1 # Download video
                time.sleep(1)
                file = max([os.path.join(folder, f) for f in os.listdir(folder) if f != 'archive.txt'], key=os.path.getctime)
                i = 1
                newfile = 'video1.mp4'
                while newfile in os.listdir(folder):
                    newfile = f'video{i}.mp4'
                    i+=1
                newfile = folder+'/'+newfile
                os.rename(file, newfile)
                time.sleep(0.1)
                dur += editing.get_length(newfile) # Rename video
                print(f'Downloaded  {num_vids}') #  Total duration: {datetime.timedelta(seconds =round(dur))}')
                get.site(current_url)
                time.sleep(1)
                get.by_class_name('ytp-next-button').click()
                elapsed = 0
                while current_url == get.current_url():
                    time.sleep(0.2)
                    elapsed += 0.2
                    if elapsed > 4:
                        print('Stalled for {}'.format(int(elapsed))) # Go to next video + stall message
                        get.by_class_name('ytp-next-button').click()

            if (use_dur and dur >= duration) or (use_num and num_vids>=number):
                get.close()
                return # Break if complete
    finally:
        time.sleep(10)
        get.close()

def get_yt_audios(filepath):    #TODO: Add filters
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': '{}'.format(filepath)}
    chrome_options.add_experimental_option('prefs', prefs)
    web = webdriver.Chrome(options=chrome_options, executable_path='chrome/chromedriver')
    #wait = WebDriverWait(web, 15)
    web.get('https://www.youtube.com/audiolibrary')

    xp1 = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div/div[1]/div/div[1]/input'
    login = WebDriverWait(web, 10).until(EC.presence_of_element_located((By.XPATH, xp1)))
    login.send_keys('imabot757@gmail.com')

    xp2 = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button'
    login_button = WebDriverWait(web, 10).until(EC.presence_of_element_located((By.XPATH, xp2)))
    login_button.find_element_by_xpath(xp2).click()

    #xp3 = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[1]/div/form/span/section/div/div/div[1]/div[1]/div/div/div/div/div[1]/div/div[1]/input'
    password = WebDriverWait(web, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
    password.send_keys('botsaredumb')

    xp4 = '/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button'
    password_button = WebDriverWait(web, 10).until(EC.presence_of_element_located((By.XPATH, xp4)))
    password_button.click()

    #down_wait = WebDriverWait(web, 10).until(EC.presence_of_element_located((By.ID, 'download')))
    download_buttons = web.find_elements_by_id('download')
    for i in download_buttons:
        i.click()
        misc.wait_download_complete(filepath)
    print('downloaded {} audio files to {}'.format(len(download_buttons),filepath))
    web.quit()
    return
def yt_repost_downloader(query, folder, number=0, view_cutoff=0):
    ##SETUP LISTFILE
    #intro_path = ''  # TODO: find
    #os.system('cp {}/intro.mp4 {}'.format(intro_path, folder))
    listfile = open(folder + '/listfile.txt', "w")
    #listfile.write('file ' + "'{}'".format(folder + '/intro.mp4'))

    ##SETUP CHROME
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': folder}
    chrome_options.add_experimental_option('prefs', prefs)
    web = webdriver.Chrome(options=chrome_options, executable_path='chrome/chromedriver')
    web.get("https://www.youtube.com/results?search_query=" + str(query))
    time.sleep(1)

    ##ADD CC AND VIEW COUNT FILTERS
    path1 = '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/div/ytd-toggle-button-renderer/a/paper-button'
    WebDriverWait(web, 15).until(EC.presence_of_element_located((By.XPATH, path1)))
    web.find_element_by_xpath(path1).click()

    path2 = '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[4]/ytd-search-filter-renderer[5]/a'
    WebDriverWait(web, 15).until(EC.presence_of_element_located((By.XPATH, path2)))
    web.find_element_by_xpath(path2).click()

    path3 = '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/div/ytd-toggle-button-renderer/a/paper-button'
    WebDriverWait(web, 15).until(EC.presence_of_element_located((By.XPATH,path3)))
    web.find_element_by_xpath(path3)

    path4 = '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[1]/div[2]/ytd-search-sub-menu-renderer/div[1]/iron-collapse/div/ytd-search-filter-group-renderer[5]/ytd-search-filter-renderer[3]/a'
    WebDriverWait(web, 15).until(EC.presence_of_element_located((By.XPATH, path4)))
    web.find_element_by_xpath(path4)


    ##GET LINKS
    links = []
    fails = 0
    while len(links) < number and fails < 10:
        WebDriverWait(web, 15).until(EC.presence_of_element_located((By.ID, 'video-title')))
        titles = web.find_elements_by_id("video-title")
        #num_views = web2.find_elements_by_class_name('style-scope ytd-video-meta-block')
        #num_views = web2.find_elements_by_xpath('//*[@id="metadata-line"]')
        #view_strs = []
        #num_views_2 = len(num_views)*[0]

        #for i in range(len(num_views)):
           # print(i)
            #"//*[@id="metadata-line"]/span[1]"
           # '/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]'
            #num_views_0 = web2.find_element_by_xpath('//*[@id="contents"]/following-siblings::ytd-video-renderer[1]/div[1]/div/div[1]/ytd-video-meta-block/div[1]/div[2]/span[1]')
            #num_views_1 = web2.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[2]/div[1]/div/div[1]/ytd-video-meta-block/div[1]/div[2]/span[1]')
            #num_views_2 = web2.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[2]/div[1]/div/div[1]/ytd-video-meta-block/div[1]/div[2]/following-sibling::span')

            #print('t',num_views_0)
            #print(num_views_2)
            #view_strs.append(num_views_2[i].text)
            #time.sleep(0.1)


        for j in range(len(titles)):
            new_link = titles[j].get_attribute('href')
            if new_link not in links:
                links.append(new_link)
            '''
            if 'watching' in view_strs[j]:
                continue
            print('-',view_strs[j],'-')
            disp = re.findall(r'(?:\d+).\d*\w*\sviews',view_strs[j])[0]
            print(disp)
            if 'K' in disp:
                disp = float(disp[0:-8])*1000
            elif 'M' in disp:
                disp = float(disp[0:-8])*1000000
            elif len(disp) == 0:
                exit(1)
            else:
                disp = float(disp[0:-8])

            if disp < view_cutoff:
                print('skip: lower than view cutoff')
                fails += 1
                continue
            '''

        web.find_element_by_css_selector('body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.1)
    print(links)
    print(len(links))
    for _link in links:
        if _link != None:
            ##DOWNLOAD##
            web.get('https://yt1s.com/youtube-to-mp4?q={}'.format(_link))
            WebDriverWait(web, 15).until(EC.presence_of_element_located((By.LINK_TEXT, 'Download')))
            dwnld_button = web.find_element_by_link_text('Download')
            dwnld_button.click()
            misc.wait_download_complete(folder)
            file = max([os.path.join(folder, f) for f in os.listdir(folder)], key=os.path.getctime)
            newfile = file.replace(' ', '-')
            os.rename(file, newfile)
            listfile.write('file ' + "'{}'\n".format(newfile))
    web.close()
def start_yt_upload():
    print('go fuck yourself this aint ready yet')
    return
def finish_yt_upload():
    print('if the start upload isnt finished then obvioulsy this isnt either')

    return
def get_yt_videos_archive_1(query, folder, number=0, duration=0):
    ##SET UP USE MODE##
    use_dur = False
    use_num = False
    if duration > 0:
        use_dur = True
    if number > 0:
        use_num = True

    ##SET UP CHROME##
    chrome_options = webdriver.ChromeOptions()
    prefs = {'download.default_directory': folder}
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--mute-audio")
    #chrome_options.add_argument("--headless")
    web = webdriver.Chrome(options=chrome_options, executable_path='chrome/chromedriver')
    web.get("https://www.youtube.com/results?search_query=" + str(query))
    starting_url = web.current_url
    web.find_element_by_xpath('//*[@id="video-title"]').click()
    while starting_url == web.current_url:
        time.sleep(0.2)
    archive = open(folder + '/archive.txt', 'r')
    url_list = [i[0:-2] for i in archive.readlines()]
    archive.close()
    print(url_list)
    dur = 0
    num_vids = 0
    while True:
        ##PUT RIGHT LINK INTO YT1S.COM##
        current_url = web.current_url
        if current_url not in url_list:
            archive = open(folder + '/archive.txt', 'a')
            archive.write(current_url+'\n')
            archive.close()
            url_list.append(current_url)
            web.get('https://yt1s.com/youtube-to-mp4?q={}'.format(current_url))

            ##DOWNLOAD##
            WebDriverWait(web, 120).until(EC.presence_of_element_located((By.LINK_TEXT, 'Download')))
            dwnld_button = web.find_element_by_link_text('Download')
            dwnld_button.click()

            ##CHECK DOWNLOAD COMPLETE##
            print('Downloading {}'.format(num_vids+1))
            misc.wait_download_complete(folder)
            num_vids += 1

            ##LENGTH OF NEWEST FILE##
            file = max([os.path.join(folder, f) for f in os.listdir(folder)], key=os.path.getctime)
            i = 1
            newfile = f'video1.mp4'
            while newfile in os.listdir(folder):
                newfile = f'video{i}.mp4'
                i+=1
            newfile = folder+'/'+newfile
            os.rename(file, newfile)
            time.sleep(0.1)
            dur += editing.get_length(newfile)
            print(f'Downloaded  {num_vids}  Duration: {datetime.timedelta(seconds =round(dur))}')

            ##NEW VIDEO##
            web.get(current_url)
            time.sleep(1)
            WebDriverWait(web, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'ytp-next-button')))
            web.find_element_by_class_name('ytp-next-button').click()
            elapsed = 0
            while current_url == web.current_url:
                time.sleep(0.2)
                elapsed += 0.2
                if elapsed > 4:
                    print('Stalled for {}'.format(int(elapsed)))
                    web.find_element_by_class_name('ytp-next-button').click()

            ##BREAK IF COMPLETE##
            if (use_dur and dur >= duration) or (use_num and num_vids>=number):
                web.close()
                return

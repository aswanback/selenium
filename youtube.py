from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import datetime
import editing
import time
import re
import os
import random
import misc

def get_yt_videos(query, folder, max_length=100,number=0, duration=0,batch_rename=True):
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
    get.wait_until_move_from(starting_url)

    if 'archive.txt' in os.listdir(folder):
        archive = open(folder + '/archive.txt', 'r')
        url_list = [i[0:-2] for i in archive.readlines()]
        archive.close()
    else:
        url_list = []  # archive.txt

    try:
        while True:
            current_url = get.current_url()
            time.sleep(0.2)
            time_secs = get.yt_duration()

            # Go next, already got it
            if current_url in url_list:
                time.sleep(0.5)
                get.by_class_name('ytp-next-button').click()

            # Go back, this video is too long
            if current_url not in url_list and time_secs > max_length:
                print('video too long, getting alternate...')
                time.sleep(0.2)
                get.back() # go back
                if get.current_url() == starting_url:                   # catch ad on first page exception
                    get.by_xpath('//*[@id="video-title"]').click()
                    get.wait_until_move_from(starting_url)
                    continue

                vid_number = random.randint(2,6)
                xpath = f'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[3]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer[{vid_number}]/div[1]/ytd-thumbnail/a'
                #xpath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[3]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer[1]/div[1]/ytd-thumbnail/a"
                new_vid_url = get.by_xpath(xpath).get_attribute('href')
                get.site(new_vid_url)
                get.wait_until_move_from(current_url)

            # Get this video
            if current_url not in url_list and time_secs < max_length:
                if get.current_url() == starting_url:                   # catch ad on first page exception
                    get.by_xpath('//*[@id="video-title"]').click()
                    get.wait_until_move_from(starting_url)

                get.master_archive(current_url)
                get.archive(current_url)
                url_list.append(current_url)

                # Go to downloader
                get.site(f'https://yt1s.com/youtube-to-mp4?q={current_url}')
                get.by_link_text("Download").click()
                print(f'Downloading {num_vids+1} - Duration: {time_secs}')
                misc.wait_until_download_complete(folder)
                num_vids += 1 # Download video
                time.sleep(1)

                # Add length to dur
                file = max([os.path.join(folder, f) for f in os.listdir(folder) if f != 'archive.txt'], key=os.path.getctime)
                dur += editing.get_length(file)

                '''i = 1
                newfile = 'video1.mp4'
                while newfile in os.listdir(folder):
                    newfile = f'video{i}.mp4'
                    i+=1
                newfile = folder+'/'+newfile
                os.rename(file, newfile)
                time.sleep(0.1)
                dur += editing.get_length(newfile) # Rename video'''
                print(f'Downloaded  {num_vids}')  #Duration: {datetime.timedelta(seconds =round(dur))}')

                get.site(current_url)
                time.sleep(0.5)

                vid_number = random.randint(1, 2)
                xpath = f'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[3]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer[{vid_number}]/div[1]/ytd-thumbnail/a'
                # xpath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[3]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer[1]/div[1]/ytd-thumbnail/a"
                new_vid = get.by_xpath(xpath).get_attribute('href')
                get.site(new_vid)
                get.wait_until_move_from(current_url)

            if (use_dur and dur >= duration) or (use_num and num_vids>=number):
                return # Break if complete
    finally:
        misc.batch_rename(folder=folder,active=batch_rename)
        time.sleep(10)
        get.close()

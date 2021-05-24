from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from editing import get_length
import time
import os
import random
from misc import getme, batch_rename, path, wait_until_download_complete,set_dir

def get_yt_videos(query, duration, max_length=5*60,foldername=None):
    if foldername is None:
        fi = 0
        mod_query = query.translate({ord(i): '-' for i in '/ '})
        while mod_query + f'{fi}' in os.listdir(path):
            fi += 1
        foldername = mod_query + f'{fi}'
    folder = set_dir(foldername)
    get = getme(folder,mute=True)

    if 'archive.txt' in os.listdir(folder):
        archive = open(folder + '/archive.txt', 'r')
        url_list = [i[0:-2] for i in archive.readlines()]
        archive.close()
    else:
        url_list = []  # archive.txt


    get.site("https://www.youtube.com/results?search_query=" + query)
    starting_url = get.current_url()
    get.by_xpath('//*[@id="video-title"]').click()
    get.wait_until_move_from(starting_url)

    try:
        num_vids = 0
        dur = 0
        video_too_long_count = 0
        while True:
            current_url = get.current_url()
            time.sleep(0.2)
            time_secs = get.yt_duration()

            # Go next, already got it
            if current_url in url_list:
                time.sleep(0.5)
                get.by_class_name('ytp-next-button').click()

            # Go back, this video is too long
            elif time_secs > max_length:
                print('video too long, getting alternate...')
                video_too_long_count += 1
                if(video_too_long_count > 4):       # go back twice
                    print('Going back another video')
                    video_too_long_count = 0
                    get.back()
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
            elif time_secs < max_length:
                video_too_long_count = 0
                if get.current_url() == starting_url:                   # catch ad on first page exception
                    get.by_xpath('//*[@id="video-title"]').click()
                    get.wait_until_move_from(starting_url)

                get.master_archive(current_url)
                get.archive(current_url)
                url_list.append(current_url)

                # Go to downloader
                get.site(f'https://yt1s.com/youtube-to-mp4')#?q={current_url}')

                get.by_class_name('search__input').send_keys(current_url)
                get.by_xpath('//*[@id="search-form"]/button').click()
                get.by_link_text("Download").click()
                print(f'Downloading {num_vids+1} - Duration: {time_secs}')
                wait_until_download_complete(folder)
                num_vids += 1 # Download video
                time.sleep(1)

                # Add length to dur
                file = max([os.path.join(folder, f) for f in os.listdir(folder) if f != 'archive.txt'], key=os.path.getctime)
                dur += get_length(file)

                print(f'Downloaded  {num_vids}')  #Duration: {datetime.timedelta(seconds =round(dur))}')

                get.site(current_url)
                time.sleep(0.5)

                vid_number = random.randint(1, 2)
                xpath = f'/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[3]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer[{vid_number}]/div[1]/ytd-thumbnail/a'
                # xpath = "/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[2]/div/div[3]/ytd-watch-next-secondary-results-renderer/div[2]/ytd-compact-video-renderer[1]/div[1]/ytd-thumbnail/a"
                new_vid = get.by_xpath(xpath).get_attribute('href')
                get.site(new_vid)
                get.wait_until_move_from(current_url)

            if dur >= duration:
                return # Break if complete
    finally:
        batch_rename(folder)
        time.sleep(10)
        get.close()

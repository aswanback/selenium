
import os
import time
from selenium.webdriver.common.keys import Keys
from misc import set_dir, download_by_link, getme, path

def reddit(subreddit,number,foldername=None):
    if foldername is None:
        fi = 0
        while f'reddit-{subreddit[2:]}' + f'{fi}' in os.listdir(path):
            fi += 1
        foldername = f'reddit-{subreddit[2:]}' + f'{fi}'
    folder = set_dir(foldername)
    get = getme(folder)

    try:
        get.site("https://www.reddit.com/" + subreddit + "/")
        img_paths = set()
        vid_paths = set()

        print("Collecting",end='')
        while len(img_paths)+len(vid_paths) < number:
            print('.', end='')
            img_elems = get.by_class_names("_2_tDEnGMLxpM6uOa2kaDB3")
            img_paths.update([i.get_attribute('src') for i in img_elems])
            video_elems = get.by_css_selectors("source")
            vid_paths.update([i.get_attribute('src') for i in video_elems])
            get.web.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        print('')

        #print(img_paths)
        #print(vid_paths)

        os.mkdir(folder+'/images')
        os.mkdir(folder+'/videos')

        i = 0
        print('Downloading...')
        for img in img_paths:
            if '.jpg' in img:
                download_by_link(img, folder+'/images', f'image{i}.jpg')
                i+=1
            elif '.png' in img:
                download_by_link(img, folder+'/images', f'image{i}.png')
                i+=1
            else:
                print(f"error: {img} not accepted format")
                return

        i = 0
        for vid in vid_paths:
            if 'mp4' in vid:
                filename = f'video{i}.mp4'
                download_by_link(vid, folder+'/videos', filename)
                i+=1
            elif 'gif' in vid:
                print('gif file format')
                filename = f'gif{i}.gif'
                download_by_link(vid, folder+'/videos', filename)
                i+=1
            elif 'mpg' in vid:
                print('mpg file format')
                filename = f'video{i}.mpg'
                download_by_link(vid, folder+'/videos', filename)
                i+=1
            elif 'm3u8' in vid:
                os.system(f'ffmpeg -y -hide_banner -loglevel error -stats -i "{vid}" {folder}/videos/video{i}.mp4')
                i+=1
            else:
                print(f'error: {vid} not accepted format')
                return
    finally:
        time.sleep(10)
        get.close()

#reddit("r/memes", 10,'/users/calebstevens/documents/Selenium_data/reddit/', )
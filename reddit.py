import os
import time
import datetime
from selenium.webdriver.common.keys import Keys
from misc import set_dir, download_by_link, getme, get_path, folder_duration

def reddit(foldername, subreddit, number, filter, subfilter='all', download_images=False, download=True):
    if subfilter not in ['hour','day','week','month','year','all']:
        raise Exception('Unsupported reddit subfilter')
    if filter == 'top':
        subfilter = '/?t=' + subfilter
    else:
        subfilter = ''

    print(subreddit)
    folder = set_dir(foldername)
    get = getme(folder)
    img_paths = set()
    vid_paths = set()

    get.site("https://www.reddit.com/" + subreddit + "/"+ filter + subfilter)
    print("\tCollecting",end='')
    while len(vid_paths) < number and len(img_paths) < 1000:
        prev_vid_len = len(vid_paths)
        get.web.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        try:
            img_elems = get.by_class_names("_2_tDEnGMLxpM6uOa2kaDB3")
            img_paths.update([i.get_attribute('src') for i in img_elems])
        finally:
            pass
        try:
            video_elems = get.by_css_selectors("source")
            vid_paths.update([i.get_attribute('src') for i in video_elems])
        finally:
            pass
        if len(vid_paths) > prev_vid_len:
            print((len(vid_paths)-prev_vid_len)*'.', end='')
            img_archive = open(f'{folder}/img-{filter}-{subfilter[4:]}.txt', 'w')
            vid_archive = open(f'{folder}/vid-{filter}-{subfilter[4:]}.txt', 'w')
            img_archive.writelines(i + '\n' for i in img_paths)
            vid_archive.writelines(v + '\n' for v in vid_paths)
            img_archive.close()
            vid_archive.close()
    img_archive = open(f'{folder}/img-{filter}-{subfilter[4:]}.txt', 'w')
    vid_archive = open(f'{folder}/vid-{filter}-{subfilter[4:]}.txt', 'w')
    img_archive.writelines(i + '\n' for i in img_paths)
    vid_archive.writelines(v + '\n' for v in vid_paths)
    img_archive.close()
    vid_archive.close()

    time.sleep(2)
    get.close()

    print('')
    print(f'\tCollected {len(vid_paths)} videos and {len(img_paths)} images')

    if download:
        print('\tDownloading...',end='')
        if download_images:
            i = 1
            for img in img_paths:
                if i < 10:
                    s = 0
                else:
                    s = ''
                if '.jpg' in img:
                    download_by_link(img, folder, f'image{s}{i}.jpg')
                    i+=1
                elif '.png' in img:
                    download_by_link(img, folder, f'image{s}{i}.png')
                    i+=1
                else:
                    print(f"error: unsupported format {img}")

        i = 1
        for vid in vid_paths:
            if i <10:
                s = 0
            else:
                s = ''
            if 'mp4?' in vid:
                download_by_link(vid, folder, f'video{s}{i}.mp4')
                print('.',end='')
                i+=1
            elif 'm3u8?' in vid:
                os.system(f'ffmpeg -y -hide_banner -loglevel error -i "{vid}" {folder}/video{s}{i}.mp4')
                print('.',end='')
                i+=1
            elif '.gif?' in vid:
                download_by_link(vid,folder,f'video{s}{i}.gif')
                print('.',end='')
                i+=1
            else:
                print(f'error: unsupported format {vid}')
        print('\n\tDone')





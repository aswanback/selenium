import os
import time
import datetime
from selenium.webdriver.common.keys import Keys
from misc import set_dir, download_by_link, getme, get_path, folder_duration

def reddit(subreddit,number,filter,subfilter='all',get_images=True, foldername=None):

    s = subfilter
    if s != 'hour' and s != 'day' and s != 'week' and s != 'month' and s != 'year' and s != 'all':
        print("Not accepted subfilter param, choose 'hour', 'day', 'week', 'month', 'year', or 'all'")
        return
    subfilter = '/?t=' + subfilter
    if filter != 'top':
        subfilter = ''

    path = get_path()
    if foldername is None:
        fi = 1
        while f'{subreddit}-{filter}-{subfilter[4:]}-{fi}' in os.listdir(path):
            fi += 1
        foldername = f'{subreddit}-{filter}-{subfilter[4:]}-{fi}'

    folder = set_dir(foldername)
    get = getme(folder)

    img_paths = set()
    vid_paths = set()

    get.site("https://www.reddit.com/" + subreddit + "/"+ filter + subfilter)
    print("Collecting",end='')
    count = 0
    while len(vid_paths) < number and len(img_paths) < 1000:
        if get_images:
            img_elems = get.by_class_names("_2_tDEnGMLxpM6uOa2kaDB3")
            img_paths.update([i.get_attribute('src') for i in img_elems])
        video_elems = get.by_css_selectors("source")
        vid_paths.update([i.get_attribute('src') for i in video_elems])
        get.web.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        if count % 10 == 0:
            print('.', end='')
            vid_archive = open(f'{folder}/{filter}-{subfilter[4:]}-vids.txt', 'w')
            vid_archive.writelines(v + '\n' for v in vid_paths)
            vid_archive.close()
            if get_images:
                img_archive = open(f'{folder}/{filter}-{subfilter[4:]}-imgs.txt', 'w')
                img_archive.writelines(i + '\n' for i in img_paths)
                img_archive.close()
        count += 1
    print('\nFinished')

    img_archive = open(f'{folder}/img-{filter}-{subfilter[4:]}.txt', 'w')
    vid_archive = open(f'{folder}/vid-{filter}-{subfilter[4:]}.txt', 'w')
    img_archive.writelines(i + '\n' for i in img_paths)
    vid_archive.writelines(v + '\n' for v in vid_paths)
    img_archive.close()
    vid_archive.close()

    time.sleep(5)
    get.close()

    print(f'Collected {len(vid_paths)} videos',end='')
    if get_images:
        print('and {len(img_paths)} images',end='')
    print('')

    i = 1
    print('Downloading...')
    for img in img_paths:
        if '.jpg' in img:
            download_by_link(img, folder, f'image{i}.jpg')
            i+=1
        elif '.png' in img:
            download_by_link(img, folder, f'image{i}.png')
            i+=1
        else:
            print(f"error: {img} not accepted format")
            return

    i = 1
    for vid in vid_paths:
        if i <10:
            s = 0
        else:
            s = ''
        if 'mp4' in vid:
            filename = f'video{s}{i}.mp4'
            download_by_link(vid, folder, filename)
            i+=1
        elif 'gif' in vid:
            print('gif file format')
            filename = f'gif{s}{i}.gif'
            download_by_link(vid, folder, filename)
            i+=1
        elif 'mpg' in vid:
            print('mpg file format')
            filename = f'video{s}{i}.mpg'
            download_by_link(vid, folder, filename)
            i+=1
        elif 'm3u8' in vid:
            os.system(f'ffmpeg -y -hide_banner -loglevel error -stats -i "{vid}" {folder}/video{s}{i}.mp4')
            i+=1
        else:
            print(f'error: {vid} not accepted format')
            return

    print(f"Duration: {datetime.timedelta(seconds=folder_duration(folder))}")




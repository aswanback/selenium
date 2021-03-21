from editing import *
import misc
from youtube import *


def get_pexel_photos(query, filepath):
    web = webdriver.Chrome('chrome/chromedriver')
    web.get('http://www.pexels.com/search/{}'.format(query))
    elements = web.find_elements_by_class_name('photo-item__img')
    links = []
    for e in elements:
        old_str = e.get_attribute('data-big-src')
        links.append(old_str)
        #links.append(re.findall(r'(?:https://).+(?="\s)', old_str)[0])
    web.quit()
    for i in range(len(links)):
        filename = 'pexel_photo_{}_{}.jpeg'.format(query, i)
        misc.download_img_by_link(links[i], filepath, filename)
    print('downloaded {} photos to {}'.format(len(links), filepath))
    web.quit()
    return


def get_pexel_videos(query,filepath):
    listfile = open(filepath + '/listfile.txt', "w")
    web = webdriver.Chrome('chrome/chromedriver')
    web.get('http://www.pexels.com/search/videos/{}'.format(query))
    elements = web.find_elements_by_class_name('photo-item__video')
    links = []
    for e in elements:
        old_str = e.get_attribute('innerHTML')
        links.append(re.findall(r'(?:https://).+(?="\s)',old_str)[0])
    web.quit()

    for i in range(len(links)):
        filename = 'pexel_video_{}_{}'.format(query,i)
        listfile.write("file '{}/{}.mp4'\n".format(filepath,filename))
        misc.download_video_by_link(links[i],filepath,filename)
    print('downloaded {} videos to {}'.format(len(links), filepath))
    listfile.close()


import urllib.request
from pexels import *
import os
from editing import get_length

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
        total += get_length(i)
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

def latest_download_file(path):
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    return newest

def wait_download_complete(filepath):
    fileends = "crdownload"
    while "crdownload" == fileends:
        time.sleep(1)
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

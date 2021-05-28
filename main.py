import datetime
import time
import reddit as r
from youtube import get_yt_videos
from tiktok import tik_tok_farmer
from misc import path

if __name__ == "__main__":
    start_time = time.time()

    r.reddit('r/memes',50)
    #get_yt_videos(query='can you tell the time?',duration=5*60,max_length=60)
    #tik_tok_farmer(number=30)

    print(f'Execution time - {datetime.timedelta(seconds=round(time.time() - start_time))}')
    #notify('Selenium', '', 'Process finished')




    # Available Functions

    # Editing
    # concat(folder, resolution='720p')
    # trim_file(_input, output=0, start=0, end=0, dur=0)
    # batch_trim(listfile, dur_or_timestamp)
    # dub_photo(img, audio, video)  # no overwriting files with same name, will crash
    # dub_video(video, audio, output)
    # get_length(filename)

    # Misc
    # set_dir(foldername, filename='')
    # clear(folder)
    # clean(folder,hard=False)
    # folder_duration(folder)
    # batch_rename(folder,active)
    # download_by_link(url, filepath, filename)
    # wait_until_download_complete(folder,timeout=20)

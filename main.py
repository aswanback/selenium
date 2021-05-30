import datetime
import time
import reddit as r
from youtube import get_yt_videos
from tiktok import tik_tok_farmer
from misc import get_path, folder_duration,set_dir,clean_folder,getme
from editing import concat
from distributor import distribute
from tags import tag_analyzer

if __name__ == "__main__":
    path = get_path()
    start_time = time.time()
    set_dir('r')

    tag_analyzer('meme compilations', 100)

    # sub_list = ['r/aww','r/Pigifs','r/cats']
    # percents_list = [50,10,40]
    #
    # for sub in sub_list:
    #     #r.reddit(foldername=sub, subreddit=sub, number=15, filter='hot', subfilter='all', download_images=False)
    #     pass
    #
    # dest_folder = set_dir('dist_test2')
    # distribute(dest_folder,5*60,sub_list,percents_list,delete_originals=False)
    # concat(dest_folder)

    #clean_folder(dest_folder,exception_list=['final.mp4','finalr.mp4','zcomp.mp4','zcompr.mp4'])

    #r.reddit('r/holdmyfeedingtube',20,'top',download_images=False)
    #folder = set_dir('r-holdmyfeedingtube-top-all-7/videos')
    #concat(folder,random_dbl=True)
    #get_yt_videos(query='can you tell the time?',duration=5*60,max_length=60)
    #tik_tok_farmer(number=30)
    #print(f"Duration: {datetime.timedelta(seconds=folder_duration(folder))}") #Print duration of folder

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

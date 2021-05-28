import datetime
import time
import reddit as r
from youtube import get_yt_videos
from tiktok import tik_tok_farmer
from misc import get_path, folder_duration,set_dir,clean_folder,getme
from editing import concat
from distributor import distribute
from tags import tag_analyzer


category_dict = {
    'chaos': [['r/abruptchaos','r/unexpected','r/watchthingsfly','r/maybemaybemaybe','r/yesyesyesno', 'r/perfectlycutscreams','r/holdmycosmo'],[15,20,10,20,15,10,10]],
    'maybe': [['r/maybemaybemaybe', 'r/nononoyes', 'r/yesyesyesno','r/holdmycosmo', 'r/tiktokcringe'],[25,25,25,10,15]],
    'pain': [['r/publicfreakout', 'r/fightporn', 'r/streetfights',  'r/instantregret', 'r/holdmyfeedingtube','r/holdmyfries'],[10,20,15,20,20,15]],
    'dumb': [['r/instantregret', 'r/holdmyfeedingtube', 'r/publicfreakout', 'r/holdmybeer','r/holdmycosmo', 'r/holdmyfries'],[30,15,10,15,15,15]],
    'animals': [['r/aww', 'r/cats', 'r/Catswhoyell', 'r/AnimalsBeingJerks', 'r/Pigifs', 'r/Eyebleach', 'r/StartledCats', 'r/AnimalsBeingDerps', 'r/chonkers', 'r/tippytaps'],[15, 5, 5, 10, 5, 10, 5, 20, 15, 10]],
    'satisfaction': [['r/bettereveryloop', 'r/Satsifyingasfuck', 'r/oddlysatisfying', 'r/powerwashingporn', 'r/blackmagicfuckery'],[25,25,30,10, 10]]
    'all': ['r/blackmagicfuckery', 'r/publicfreakout', 'r/fightporn', 'r/streetfights', 'r/contagiouslaughter', 'r/shittymobilegameads', 'r/holdmyfries', 'r/holdmybeer', 'r/watchthingsfly', 'r/unexpected', 'r/memes', 'r/dankmemes', 'r/holdmyfeedingtube', 'r/tiktokcringe', 'r/shitposting', 'r/gayspiderbrothel', 'r/perfectlycutscreams', 'r/abruptchaos', 'r/instantregret', 'r/holdmycosmo', 'r/maybemaybemaybe', 'r/nononoyes', 'r/yesyesyesno']
}

def get_videos(category, number_from_each, filter,subfilter='all'):
    cat = category_dict[category]
    sub_list = cat[0]
    percents_list = cat[1]
    for sub in sub_list:
        r.reddit(foldername=sub+f'-{filter}-{subfilter}', subreddit=sub, number=number_from_each, filter=filter, subfilter=subfilter, download_images=False)

def make_videos(category, destination_foldername, duration, outro_path,delete_originals=True):
    cat = category_dict[category]
    sub_list = cat[0]
    percents_list = cat[1]
    dest_folder = set_dir(destination_foldername)
    distribute(dest_folder,duration,sub_list,percents_list,delete_originals=delete_originals)
    concat(dest_folder,outro_path=outro_path)


if __name__ == "__main__":
    path = get_path()
    start_time = time.time()
    set_dir('r')

    ls = 4*[]
    ls[0] = ['Animal', 'cute animals', 'cute animal compilations', 'cats', 'cute cats', 'animal memes']
    ls[1] = ['Oddly Satisfying', 'Satisfaction', 'Satisfying videos']
    ls[2] = ['Memes', 'dank memes', 'meme compilation', 'dank meme compilation']
    ls[3] = ['Dumbest people', 'instant regret','stupid people','stupidest people']
    tag_analyzer(ls[0], 100,'animal-tag-analysis')


    #get_videos('all',15,'top', subfilter='all')
   # make_videos('chaos','chaos_comp_test',11*60,outro_path='outro720.mp4', delete_originals=False)

# Analyze Tags
# Descireoptions



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

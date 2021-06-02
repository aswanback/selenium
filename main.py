import datetime
import nltk
import time
import reddit as r
from youtube import get_yt_videos
from tiktok import tik_tok_farmer
from misc import get_path, folder_duration,set_dir,clean_folder,notify
from editing import concat
from distributor import distribute
from tags import metadata_analyzer

category_dict = {
    'chaos': [['r/abruptchaos','r/unexpected','r/watchthingsfly','r/maybemaybemaybe','r/yesyesyesno', 'r/perfectlycutscreams','r/holdmycosmo'],[15,20,10,20,15,10,10]],
    'maybe': [['r/maybemaybemaybe', 'r/yesyesyesno','r/holdmycosmo', 'r/tiktokcringe'],[25,25,25,10,15]],
    'pain': [['r/publicfreakout', 'r/fightporn', 'r/streetfights',  'r/instantregret', 'r/holdmyfeedingtube','r/holdmyfries'],[10,20,15,20,20,15]],
    'dumb': [['r/instantregret', 'r/holdmyfeedingtube', 'r/publicfreakout', 'r/holdmybeer','r/holdmycosmo', 'r/holdmyfries'],[30,15,10,15,15,15]],
    'animals': [['r/aww', 'r/cats', 'r/Catswhoyell', 'r/AnimalsBeingJerks', 'r/Pigifs', 'r/Eyebleach', 'r/StartledCats', 'r/AnimalsBeingDerps', 'r/chonkers', 'r/tippytaps'],[15, 5, 5, 10, 5, 10, 5, 20, 15, 10]],
    'satisfaction': [['r/Satisfyingasfuck', 'r/oddlysatisfying', 'r/powerwashingporn', 'r/FastWorkers','r/woahdude'],[25,25,30,10,10]],
    'memes': [['r/bettereveryloop','r/memes', 'r/dankmemes', 'r/shitposting', 'r/gayspiderbrothel', 'r/shittymobilegameads', 'r/tiktokcringe','r/contagiouslaughter','r/blackmagicfuckery','r/holdmycosmo'],[10,15,15,15,5,5,20,5,5,5]],
    'all': [[ 'r/contagiouslaughter', 'r/shittymobilegameads', 'r/holdmyfries', 'r/holdmybeer', 'r/watchthingsfly', 'r/unexpected', 'r/memes', 'r/dankmemes', 'r/holdmyfeedingtube', 'r/tiktokcringe', 'r/shitposting', 'r/gayspiderbrothel', 'r/perfectlycutscreams', 'r/abruptchaos', 'r/instantregret', 'r/holdmycosmo', 'r/maybemaybemaybe', 'r/yesyesyesno'],[0]]
}
    #'r/blackmagicfuckery', 'r/publicfreakout', 'r/fightporn','r/streetfights',

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

    #get_videos('satisfaction', 15, filter='hot', subfilter='month')
    make_videos('satisfaction','satisfaction_1',11*60,outro_path='outro720.mp4', delete_originals=False)

    # For single sub videos:
    # sub = 'r/blackmagicfuckery'
    # r.reddit(foldername=sub, subreddit=sub, number=15, filter='hot', subfilter='all', download_images=False)
    # concat(set_dir(sub),outro=SOMETHING)

    # clean_folder(dest_folder,exception_list=['final.mp4','finalr.mp4','zcomp.mp4','zcompr.mp4'])
    # print(f"Duration: {datetime.timedelta(seconds=folder_duration(folder))}") #Print duration of folder

    print(f'\nExecution time - {datetime.timedelta(seconds=round(time.time() - start_time))}')
    # notify('Selenium', '', 'Process finished')




    # ls = [None] * 5
    # ls[0] = ['cute animals', 'cute animals compilation', 'animal compilation', 'cutest animals', 'cats', 'cute cats', 'animal memes']
    # ls[1] = ['Oddly Satisfying', 'Satisfaction', 'Satisfying videos']
    # ls[2] = ['Memes', 'dank memes', 'meme compilation', 'dank meme compilation']
    # ls[3] = ['Dumbest people', 'instant regret','stupid people','stupidest people']
    # ls[4] = ['reddit','best of reddit','reddit compilations','funny reddit']
    # metadata_analyzer(queries=ls[4], number_vids_each=50, ngram_count=6, foldername='metadata/reddit',headless=False)

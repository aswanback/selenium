import editing
import youtube
import os
import misc
import subprocess
import pexels
import main

def meme(query, folder, outname, number=0, duration=0):
    #os.system('rm {}/*'.format(folder))
    #listfile = youtube.get_yt_videos(query, folder, number, duration)
    listfile = main.set_dir('inaugural_video','listfile.txt')
    #misc.notify(title='Selenium', subtitle='meme video update', message='listfile ready to edit')
    dur_time = input("Enter 'dur' or 'timestamp' when done editing listfile. If no edits, enter 'none': ")
    if dur_time != 'none':
        editing.batch_trim(listfile,dur_time)
    editing.concat(listfile,outname)
    misc.notify(title='Selenium', subtitle='meme video update', message='process finished')

def relax(folder, photo_video_folder, p_v_format, pexel_query, number=1):

   # check_folder = subprocess.run('[ -d "/Users/andrewswanback/Documents/selenium_data/massage" ] && echo 0 || echo 1')
    #if(check_folder):
    #    pass
        #os.system('rm {}/*'.format(photo_video_folder))
    # youtube.get_yt_videos('relaxing music',folder,number)
    print("In 'relax': youtube videos downloaded")
    if p_v_format == 'photos':
        pexels.get_pexel_photos(pexel_query, photo_video_folder)
    elif p_v_format == 'videos':
        pexels.get_pexel_videos(pexel_query, photo_video_folder)
    print("In 'relax': pexels videos downloaded")
    px_listfile = open(photo_video_folder+'/listfile.txt','r')
    yt_listfile = open(folder+'/listfile.txt','r')
    px_filenames_raw = [line.strip("\n") for line in px_listfile if line != "\n"]
    px_filenames = px_filenames_raw[:][5:-2]
    yt_filenames_raw = [line.strip("\n") for line in px_listfile if line != "\n"]
    yt_filenames = yt_filenames_raw[:][5:-2]
    px_lengths = []
    yt_lengths = []
    px_dur = 0
    yt_dur = 0
    for i in px_filenames:
        px_lengths.append(editing.get_length(i))
        px_dur += editing.get_length(i)
    for i in yt_filenames:
        yt_lengths.append(editing.get_length(i))
        yt_dur += editing.get_length(i)

    px_listfile.close()




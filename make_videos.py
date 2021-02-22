import editing
import youtube
import os
import misc

def meme(query, folder, outname, number=0, duration=0):
    os.system('rm {}/*'.format(folder))
    listfile = youtube.get_yt_videos(query, folder, number, duration)
    misc.notify(title='Selenium', subtitle='meme video update', message='listfile ready to edit')
    dur_time = input("Enter 'dur' or 'timestamp' when done editing listfile. If no edits, enter 'none': ")
    if dur_time != 'none':
        editing.batch_trim(listfile,dur_time)
    editing.concat(listfile,outname)
    misc.notify(title='Selenium', subtitle='meme video update', message='process finished')



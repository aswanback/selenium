import editing
import youtube

def meme(query,filepath,outname,number=0,duration=0):
    listfile = youtube.get_yt_videos(query, filepath, number, duration)
    editing.concat(listfile,outname)
import subprocess
import os
import re
from misc import get_path
import random

def concat(folder,resolution='720p',outro_path='outro720.mp4',random_dbl=True, remove_txts=False,audio_path='audio'):
    if resolution == '1080p':
        w = 1920
        h = 1080
    elif resolution == '720p':
        w = 1280
        h = 720
    elif resolution == 'tiktok':
        w = 576
        h = 1024
    else:
        print('unsupported resolution')
        return # Resolution solving

    files = [name for name in os.listdir(folder) if 'video' in name and '-e.mp4' not in name and '-a.mp4' not in name]
    files.sort()

    list_names = [f"file '{name[0:-4]}-e.mp4'\n" for name in os.listdir(folder) if 'video' in name and '-e.mp4' not in name and '-a.mp4' not in name]
    list_names.sort()
    zlist = open(folder + '/zlist.txt', "w")
    zlist.writelines(list_names)
    zlist.close()

    for i in files:
        filename_orig = folder+'/'+i
        filename_new = filename_orig[0:-4]+'-e.mp4'
        if (i[0:-4] + '-e.mp4') not in os.listdir(folder):
            print(f'converting {i}...',end='')
            video_codec = str(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1',filename_orig]))[2:-3]
            audio_codec = str(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1',filename_orig]))[2:-3]
            wxh = str(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height', '-of', 'csv=p=0:s=x',filename_orig]))
            [width,height] = re.split('x',wxh)
            width = width[2:]
            height = height[0:-3]
            #print(f'wid{width}, h{height}')

            if audio_codec == None or audio_codec == '':
                print('adding audio and encoding...')
                path = get_path()
                audio_files = [i for i in os.listdir(path+'/'+audio_path)]
                dub_video(filename_orig,random.choice(audio_files),filename_orig[0:-4]+'-a.mp4')
                #os.system(f'ffmpeg -y -hide_banner -loglevel error -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i {filename_orig} -c:v copy -c:a aac -shortest {filename_orig[0:-4]+"-a.mp4"}')
                os.system(f'ffmpeg -y -hide_banner -loglevel error -i {filename_orig[0:-4]+"-a.mp4"} -vf "scale=w={w}:h={h}:force_original_aspect_ratio=1,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2" -map 0:v -map 0:a -use_wallclock_as_timestamps 1 -r 30 -c:v libx264 -c:a aac {filename_new}')
            elif audio_codec != 'aac' or video_codec != 'h264':
                print('encoding...')
                os.system(f'ffmpeg -y -hide_banner -loglevel error -i {filename_orig} -vf "scale=w={w}:h={h}:force_original_aspect_ratio=1,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2" -map 0:v -map 0:a -use_wallclock_as_timestamps 1 -r 30 -c:v libx264 -c:a aac {filename_new}')
            elif width != w or height != h:
                print('padding...')
                os.system(f'ffmpeg -y -hide_banner -loglevel error -i {filename_orig} -vf "scale=w={w}:h={h}:force_original_aspect_ratio=1,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2" -map 0:v -map 0:a -use_wallclock_as_timestamps 1 -r 30 {filename_new}')
            else:
                print('no conversion needed')
                os.rename(filename_orig,filename_new) # Reencode and pad if neccessary
        else:
            print(f'{i} already converted')

    ##CONCATENATION
    print('concatenating videos...')
    os.system(f'ffmpeg -y -hide_banner -loglevel error -safe 0 -f concat -segment_time_metadata 1 -i {folder+"/zlist.txt"} -c copy {folder+"/zcomp.mp4"}')

    if outro_path != None:
        zlisto = open(folder + '/zlisto.txt', 'w')
        zlisto.write(f"file '{folder}/zcomp.mp4'\n")
        zlisto.write(f"file '{folder}/{outro_path}'\n")
        zlisto.close() # zlist setup

        if outro_path not in os.listdir(folder):
            os.system(f'cp {outro_path} {folder}')
        print('adding intro/outro...')
        os.system(f'ffmpeg -y -hide_banner -loglevel error -safe 0 -f concat -segment_time_metadata 1 -i {folder+"/zlisto.txt"} -c copy {folder}/final.mp4')

    if random_dbl:
        print('Creating randomized version...')
        zlistr = open(folder + '/zlistr.txt', 'w')
        random.shuffle(list_names)
        zlistr.writelines(list_names)
        zlistr.close()

        print('\tconcatenating videos...')
        os.system(f'ffmpeg -y -hide_banner -loglevel error -safe 0 -f concat -segment_time_metadata 1 -i {folder + "/zlistr.txt"} -c copy {folder + "/zcompr.mp4"}')

        if outro_path != None:
            zlistor = open(folder + '/zlistor.txt', 'w')
            zlistor.write(f"file '{folder}/zcompr.mp4'\n")
            zlistor.write(f"file '{folder}/{outro_path}'\n")
            zlistor.close()
            if outro_path not in os.listdir(folder):
                os.system(f'cp {outro_path} {folder}')
            print('\tadding intro/outro...')
            os.system(f'ffmpeg -y -hide_banner -loglevel error -safe 0 -f concat -segment_time_metadata 1 -i {folder + "/zlistor.txt"} -c copy {folder}/finalr.mp4')

    if remove_txts:
        rm_list = ['zlist.txt','zlistor.txt','zlist.txt','zlistr.txt']
        for file in rm_list:
            os.system(f'rm -f {file}')
    print('finished')
    return

def trim_file(_input, output=0, start=0, end=0, dur=0):
    #print('Starting individual trim')
    if output == 0:
        output = _input
    temp = _input[0:-4]+'-temp.mp4'
    if dur != 0:
        os.system('ffmpeg -y -hide_banner -loglevel error -stats -i {} -ss {} -t {} -async 1 {}'.format(_input,start,dur,temp))
        os.system('mv {} {}'.format(output,_input))
    elif end != 0:
        os.system('ffmpeg -y -hide_banner -loglevel error -stats -i {} -ss {} -to {} -async 1 {}'.format(_input,start,end,temp))
        os.system('mv {} {}'.format(temp, output))
    #print('Individual trim complete')
    return

def batch_trim(listfile,dur_or_timestamp):
    print('Starting batch trim')
    lfile = open(listfile, 'r')  # open file with paths
    filenames_unedited = [line.strip("\n") for line in lfile if line != "\n"]  # get filenames in list
    filenames_edited = []
    trim_ranges = []
    for i in range(len(filenames_unedited)):
        filename_edited = re.findall(r'(?:/Users/).+(?:\.mp4)',filenames_unedited[i])[0]
        trim_range = re.findall(r'(?<=\s)(?:\d+)',filenames_unedited[i])
        if float(trim_range[1]) == 0:
            print('One file purposefully omitted from trimming')
            continue
        filenames_edited.append(filename_edited)
        trim_ranges.append(trim_range)
        if dur_or_timestamp == 'timestamp':
            trim_file(filename_edited,output=0,start=int(trim_range[0]),end=int(trim_range[1]))
            print('One file trimmed')
        elif dur_or_timestamp == 'dur':
            trim_file(filename_edited,output=0, start=int(trim_range[0]),dur=int(trim_range[1]))
            print('One file trimmed')
    return

def dub_photo(img,audio,video): #no overwriting files with same name, will crash
    #os.system('ffmpeg -loop 1 -y -i {} -i {} -shortest {}'.format(img,audio,video))
    os.system('ffmpeg -loop 1 -i {} -i {} -c:v libx264 -tune stillimage -c:a aac -b:a 192k -pix_fmt yuv420p -shortest {}'.format(img,audio,video))
    return

def dub_video(video,audio,output):
    len_video = get_length(video)
    len_audio = get_length(audio)
    if len_video >= len_audio:
        os.system('ffmpeg -i {} -i {} -c:v copy -map 0:v:0 -map 1:a:0 -y {}'.format(video,audio,output))
    else:
        os.system('ffmpeg -i {} -i {} -c:v copy -map 0:v:0 -map 1:a:0 -shortest -y {}'.format(video, audio, output))
    return

def get_length(filename):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',filename], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    return float(result.stdout)


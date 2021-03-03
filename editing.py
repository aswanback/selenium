from misc import *
from youtube import *
import subprocess
import os

def concat(folder,resolution='720p'):
    #SET UP INTRO/OUTRO
    if resolution == '1080p':
        w = 1920
        h = 1080
    elif resolution == '720p':
        w = 1280
        h = 720
    else:
        print('unsupported resolution')
        return
    intro_path = '' #main.set_dir('' + 'intro.mp4')
    outro_path = main.set_dir('' + f'outro{h}.mp4')

    #MAKE LIST FILE
    listfile = open(folder + '/listfile.txt', "w")
    files = [name for name in os.listdir(folder) if 'video' in name and '-e.mp4' not in name]
    files.sort()

    ##MAKE LISTFILE AND REENCODE VIDEOS
    file_num = 1
    for i in files:
        filename_orig = folder+'/'+i
        filename_new = filename_orig[0:-4]+'-e.mp4'
        if (i[0:-4] + '-e.mp4') not in os.listdir(folder):
            print(f'converting video {file_num}...  ',end='')
            #GET CODEC AND DIMENSION PROPERTIES
            video_codec = str(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'v:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1',filename_orig]))
            audio_codec = str(subprocess.check_output(['ffprobe', '-v', 'error', '-select_streams', 'a:0', '-show_entries', 'stream=codec_name', '-of', 'default=noprint_wrappers=1:nokey=1',filename_orig]))
            wxh = str(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries', 'stream=width,height', '-of', 'csv=p=0:s=x',filename_orig]))
            #MODIFY RAW TERMINAL OUTPUT
            video_codec = video_codec[2:-3]
            audio_codec = audio_codec[2:-3]
            [width,height] = re.split('x',wxh)
            width = width[2:]
            height = height[0:-5]
            print(f'wid{width}, h{height}')

            #REENCODE, PAD IF NECESSARY
            key = re.findall(r'(?:video\d+-e.mp4)',filename_new)
            if key in os.listdir(folder):
                continue


            if audio_codec != 'aac' or video_codec != 'h264':
                print('encoding...')
                os.system(f'ffmpeg -y -hide_banner -loglevel error -stats -i {filename_orig} -vf "scale=w={w}:h={h}:force_original_aspect_ratio=1,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2" -map 0:v -map 0:a -use_wallclock_as_timestamps 1 -r 30 -c:v libx264 -c:a aac {filename_new}')
            elif width != w or height != h:
                print('padding...')
                os.system(f'ffmpeg -y -hide_banner -loglevel error -stats -i {filename_orig} -vf "scale=w={w}:h={h}:force_original_aspect_ratio=1,pad={w}:{h}:(ow-iw)/2:(oh-ih)/2" -map 0:v -map 0:a -use_wallclock_as_timestamps 1 -r 30 {filename_new}')
            else:
                print('no conversion needed')
                os.rename(filename_orig,filename_new)

        else:
            print(f'{i} already converted')
        listfile.write("file '{}'\n".format(filename_new))
        file_num += 1

    ##CONCATENATION
    listfile.close()
    comp_path = folder+'/comp.mp4'
    print('concatenating videos...')
    os.system(f'ffmpeg -y -hide_banner -loglevel error -stats -safe 0 -f concat -segment_time_metadata 1 -i {folder+"/listfile.txt"} -c copy {comp_path}')

    iolist = open(folder + '/iolist.txt', 'w')
    if intro_path != '':
        if f'intro{h}.mp4' not in os.listdir(folder):
            os.system('cp {} {}'.format(intro_path, folder))
        iolist.write(f"file '{folder}/intro{h}.mp4'\n")
    iolist.write(f"file '{folder}/comp.mp4'\n")
    if outro_path != '':
        if f'outro{h}.mp4' not in os.listdir(folder):
            os.system('cp {} {}'.format(outro_path, folder))
        iolist.write(f"file '{folder}/outro{h}.mp4'\n")
    iolist.close()
    print('adding intro/outro...')
    os.system(f'ffmpeg -y -hide_banner -loglevel error -stats -safe 0 -f concat -segment_time_metadata 1 -i {folder+"/iolist.txt"} -c copy {folder}/final.mp4')
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


from misc import *
from youtube import *
import numpy as n

def concat(listfile,outname):
    ##OPENING FILES
    lfile = open(listfile,'r')                                                  #open file with paths
    newlfilepath = re.findall(r'(?:/).+(?:/)',listfile)[0]                      #grab working dir path
    newlfile = open(newlfilepath+'newlistfile.txt','w')                         #make new listfile
    filenames_unedited = [line.strip("\n") for line in lfile if line != "\n"]   #get filenames in list

    ###GETTING LOTS OF VIDEO INFO###
    #width_height = []
    filenames = []
    #past_dec_frame_rate = 1
    for i in range(len(filenames_unedited)):
        filename = re.findall(r'(?:/Users).+(?:\.mp4)',filenames_unedited[i])[0]
        filenames.append(filename)   #correct filepath/names
    print(filenames)
        #height_width_info = str(subprocess.run(['ffprobe','-v', 'error', '-select_streams', 'v:0','-show_entries','stream=width,height','-of','csv=s=x:p=0',filenames[i]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout)
        #print(height_width_info)
        #filesize = re.findall(r'(?:\d+)x(?:\d+)', height_width_info)
        #print(filesize)
        #width_height.append(re.split('x', filesize[0]))

        ##GET FRAME RATE
        #frame_rate_info = str(subprocess.run(['ffprobe','-v', 'error', '-select_streams', 'v:0','-show_entries','stream=r_frame_rate','-of','csv=s=x:p=0',filenames[i]],stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout)
        #frame_rate = re.findall(r'\d+/\d+',frame_rate_info)[0]
        #[numerator,denominator] = re.split('/',frame_rate)
        #dec_frame_rate = float(numerator)/float(denominator)
        ##MAXIMIZE FRAME RATE
        #if dec_frame_rate > past_dec_frame_rate:
        #    final_frame_rate = '{}/{}'.format(float(numerator),float(denominator))
        #past_dec_frame_rate = dec_frame_rate

    #GET MAX WIDTH - UNUSED
    #width_max_index = n.nanargmax(width_height[:][1])
    #h = width_height[width_max_index][0]
    #w = width_height[width_max_index][1]

    ##FORMAT THE VIDEOS WITH RIGHT WIDTH, HEIGHT, TIMESTAMPS, CODEC, ASPECT RATIO
    for i in range(0,len(filenames)):
        #os.system('ffmpeg -y -hide_banner -loglevel error -stats -i {} -map 0:v -map 0:a -use_wallclock_as_timestamps 1 -r {} {}'.format(filenames[i],final_frame_rate,filenames[i][0:-4]+'-a.mp4'))
        os.system('ffmpeg -y -hide_banner -loglevel error -stats -i {} -vf "scale=w=1920:h=1080:force_original_aspect_ratio=1,pad=1920:1080:(ow-iw)/2:(oh-ih)/2" -map 0:v -map 0:a -use_wallclock_as_timestamps 1 -r 30 -c:v libx264 -c:a aac {}'.format(filenames[i],filenames[i][0:-4]+'-edited.mp4'))

    ##WRITE NEW FILE WITH RIGHT NAMES
    for i in range(len(filenames)):
        filenames[i] = filenames[i][0:-4]+'-edited.mp4'
        newlfile.write('file '+"'{}'\n".format(filenames[i]))
    lfile.close()
    newlfile.close()

    ##CONCAT OPERATION
    os.system('ffmpeg -y -hide_banner -loglevel error -stats -safe 0 -f concat -segment_time_metadata 1 -i {} -vf select=concatdec_select -af aselect=concatdec_select,aresample=async=1 {}'.format(newlfilepath+'newlistfile.txt',outname))
    return



def trim_file(_input, output=0, start=0, end=0, dur=0):
    if output == 0:
        output = _input
    temp = _input[0:-4]+'-temp.mp4'
    if dur != 0:
        os.system('ffmpeg -y -hide_banner -loglevel error -stats -i {} -ss {} -t {} -async 1 {}'.format(_input,start,dur,temp))
        os.system('mv {} {}'.format(output,_input))
    elif end != 0:
        os.system('ffmpeg -y -hide_banner -loglevel error -stats -i {} -ss {} -to {} -async 1 {}'.format(_input,start,end,temp))
        os.system('mv {} {}'.format(temp, output))
    return

def batch_trim(listfile,dur_or_timestamp):
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
        print('One file trimmed')
        filenames_edited.append(filename_edited)
        trim_ranges.append(trim_range)
        if dur_or_timestamp == 'timestamp':
            trim_file(filename_edited,output=0,start=int(trim_range[0]),end=int(trim_range[1]))
        elif dur_or_timestamp == 'dur':
            trim_file(filename_edited,output=0, start=int(trim_range[0]),dur=int(trim_range[1]))
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


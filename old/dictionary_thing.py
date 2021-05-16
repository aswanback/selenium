s = {
    # ------------------------------------------
    'concat': False,  # concat all videos in the folder(s) you just downloaded,
    'folder_to_concat': 'can-you-tell-the-time?3',  # unless 'folder_to_concat' is not None, then it'll do that folder
    'chosen_resolution': '720p',  # choices are '720p', '1080p' and 'tiktok'
    # ------------------------------------------
    'youtube': {
        'Run_this?': False,
        'query': '\"that quiet Kid in the class-\"',
        'folder_name': 'default',
        'number': 0,  # set this to 0 to ignore it
        'duration': 5 * 60,  # total comp duration - set this to 0 to ignore it
        'max_length': 40,
    },
    # ------------------------------------------
    'tiktok': {
        'Run_this?': False,
        'folder_name': 'default',
        'number': 12,
    },
    # -------------------------------------------
    'reddit': {
        'Run_this?': False,
        'folder_name': 'default',
        'subreddit': 'r/memes',
        'num_imgs': 20,
    },
    # -------------------------------------------
    'use_same_folder_for_all': False,  # do you want to use the same folder for tiktok, reddit and/or youtube?
    'folder_name_for_all': 'default',  # unused unless above True
    'replace_folders': False,  # replace your folder every time you run or make a new one?

    'resolution': {
        'youtube': '720p',
        'tiktok': 'tiktok',
        'reddit': '720p',
        'multimedia': '720p'
    },
    # -------------------------------------------

    'clean': {
        'Run_this?': False,
        '/path/to/folder': None,  # path starting from your directory already set up
        'hard?': False  # hard?=True will remove everything from a meme folder except the final comp and links txt file
    },
    'trim': {
        'Run_this?': False,
        'folder_of_video': None,
        'video_name_to_trim': None,
        'start': 0,
        'end': 0,  # leave as zero to use 'duration'
        'duration': 0,  # leave as zero to use 'end' timestamp
    },
    'notify?': False,  # get a notification when python has finished?
    'defaults': {
        # youtube default is based on query
        'multimedia': 'multi_source',
        'tiktok': 'tiktok',
        'reddit': 'reddit',
    }
}

default_comp_name = s['defaults']['multimedia']
default_yt_name = s['youtube']['query'].translate({ord(i): '-' for i in '/ '})
default_rd_name = s['defaults']['reddit']
default_tt_name = s['defaults']['tiktok']
# figure out what to call the folder if it's all in same folder
if s['use_same_folder_for_all']:
    if s['folder_name_for_all'] == 'default':
        comp_i = 1
        if not s['replace_folders']:
            while default_comp_name + f'{comp_i}' in os.listdir(path): comp_i += 1
        name = default_comp_name + f'{comp_i}'

    else:
        default_name = s['folder_name_for_all']
        comp_i = 1
        if not s['replace_folders']:
            while default_name + f'{comp_i}' in os.listdir(path): comp_i += 1
        name = default_name + f'{comp_i}'

    yt_name = name
    tt_name = name
    rd_name = name
# figure out what to call it if all in different folders
else:
    yt_name = default_yt_name
    yt_i = 1
    if not s['replace_folders']:
        while default_yt_name + f'{yt_i}' in os.listdir(path): yt_i += 1
        yt_name = default_yt_name + f'{yt_i}'
    if s['youtube']['folder_name'] != 'default':
        yt_name = s['youtube']['folder_name']

    tt_name = default_tt_name
    tt_i = 1
    if not s['replace_folders']:
        while default_tt_name + f'{tt_i}' in os.listdir(path): tt_i += 1
        tt_name = default_tt_name + f'{tt_i}'
    if s['tiktok']['folder_name'] != 'default':
        tt_name = s['tiktok']['folder_name']

    rd_name = default_yt_name
    rd_i = 1
    if not s['replace_folders']:
        while default_rd_name + f'{rd_i}' in os.listdir(path):
            rd_i += 1
        rd_name = default_rd_name + f'{rd_i}'
    if s['reddit']['folder_name'] != 'default':
        rd_name = s['reddit']['folder_name']

youtube_dir = "you should not see this message - youtube_dir error"  # initialize these to purposefully crash
tiktok_dir = "you should not see this message - tiktok_dir error"
reddit_dir = "you should not see this message - reddit_dir error"

if s['youtube']['Run_this?']:  # set directory name if running it
    youtube_dir = set_dir(yt_name)
    get_yt_videos(s['youtube']['query'], youtube_dir, s['youtube']['max_length'], s['youtube']['number'],
                  s['youtube']['duration'])
if s['tiktok']['Run_this?']:
    tiktok_dir = set_dir(tt_name)
    tiktok.tik_tok_farmer(tiktok_dir, s['tiktok']['number'])
if s['reddit']['Run_this?']:
    reddit_dir = set_dir(rd_name)
    reddit(reddit_dir, s['reddit']['subreddit'], number=s['reddit']['num_imgs'])

# Concat videos
if s['concat']:
    if s['folder_to_concat'] is None:
        if s['use_same_folder_for_all']:
            concat(set_dir(yt_name), resolution=s['resolution']['multimedia'])
        else:
            if s['youtube']['Run_this?']:
                concat(youtube_dir, resolution=s['resolution']['youtube'])

            if s['tiktok']['Run_this?']:
                concat(tiktok_dir, resolution=s['resolution']['tiktok'])

            if s['reddit']['Run_this?']:
                concat(reddit_dir, resolution=s['resolution']['reddit'])
    else:
        concat(set_dir(s['folder_to_concat']), resolution=s['chosen_resolution'])

# Clean folder
if s['clean']['Run_this?']:
    misc.clean(path + '/' + s['clean']['/path/to/folder'], hard=s['clean']['hard?'])

# Trim a file
if s['trim']['Run_this?']:
    trim_file(s['trim']['folder_of_video'] + s['trim']['video_name_to_trim'], start=s['trim']['start'],
              end=s['trim']['end'], dur=s['trim']['dur'])

# Show run time, notify if wanted
print(f'Execution time - {datetime.timedelta(seconds=round(time.time() - start_time))}')
if s['notify?']:
    notify('Selenium', '', 'Process finished')  # Long aids code to run everything and version solve the folders



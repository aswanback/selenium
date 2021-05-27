import os
from misc import set_dir, get_path

def distribute(folder_base_name,*args):
    path = get_path()
    fi = 1
    while f'{folder_base_name}-{fi}' in os.listdir(path):
        fi += 1
    foldername = f'{folder_base_name}-{fi}'
    dest_folder = set_dir(foldername)

    dist_list = []

    sub_folders = args[1::2]
    percents = args[::2]




    for filepath in dist_list:
        os.system(f'cp {path+filepath} {dest_folder+"/."}')
    print(f'Finished making {foldername}')
import os
import random
import datetime
import subprocess

from misc import set_dir, get_path, folder_duration

def distribute(dest_folder,duration,src_folder_list,src_percents_list,delete_originals=True):
    assert len(src_percents_list) == len(src_folder_list)
    assert sum(src_percents_list) == 100

    num_list = [int(20/100*i) for i in src_percents_list]
    master_file_set = set()
    while folder_duration(dest_folder) < duration:

        file_list = []
        for i in range(len(src_folder_list)):
            file_list.extend(get_random_vids_paths(src_folder_list[i],num_list[i]))

        file_list = [i for i in file_list if min([subprocess.run(['cmp','-s',f,i]).returncode for f in file_list if f != i]) == 1]
        if len(master_file_set) > 0:
            file_list = [i for i in file_list if min([subprocess.run(['cmp','-s',f,i]).returncode for f in master_file_set]) == 1]
        master_file_set.update(file_list)

        for filepath in file_list:
            i = 0
            s = 0
            while f'video{s}{i}.mp4' in os.listdir(dest_folder):
                if i < 9:
                    s = 0
                else:
                     s = ''
                i += 1
            os.system(f'cp -f {filepath} {dest_folder+f"/video{s}{i}.mp4"}')
            if delete_originals:
                os.system(f'rm -f {filepath}')
    path = get_path()
    print(f'Finished making {dest_folder[len(path)+1:]}, duration: {datetime.timedelta(seconds=int(folder_duration(dest_folder)))}')


def get_random_vids_paths(folder, number):
    path = get_path()
    full_list = [f'{path}/{folder}/{i}' for i in os.listdir(path+'/'+folder) if '.mp4' in i] #TODO: add '-e'
    random.shuffle(full_list)
    if len(full_list) < number:
        raise Exception(f'Not enough videos in {folder}, need at least {number} (likely many more)')
    path_list = random.sample(full_list,number)
    #print(f'paths {path_list}')
    return path_list
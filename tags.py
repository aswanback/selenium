import re
from misc import getme, get_path
import numpy as np
import matplotlib.pyplot as plt
import operator
from tabulate import tabulate
from selenium.webdriver.common.keys import Keys

def get_tags(url_list,mute=True,headless=True):
    get = getme(mute=mute,headless=headless)
    tagmat = []
    view_list = []
    for url in url_list:
        get.site(url)
        page_src = get.web.page_source
        #print(page_src)
        tags = re.findall('<meta name="keywords" content="(.*?)"',page_src)[0]
        views_str = re.findall('{"viewCount":{"simpleText":"(.*?) views"},',page_src)[0]
        views = int(views_str.replace(',',''))
        taglist = tags.split(', ')
        # print(taglist)
        view_list.append(views)
        tagmat.append(taglist)
    get.close()
    return tagmat,view_list

def analyze_tags(url_list,tag_filename,mute=True,headless=True):
    tag_lists,view_list = get_tags(url_list,mute=mute,headless=headless)
    print('Collected tags')

    flat_list = []
    for list in tag_lists:
        flat_list.extend(list)
    tag_dict = dict.fromkeys(flat_list, 0)
    for i in range(len(flat_list)):
        tag_dict[flat_list[i]] += 100/len(url_list)

    score_dict = dict.fromkeys(flat_list,0)
    for j in range(len(tag_lists)):
        for i in range(len(tag_lists[j])):
            score_dict[tag_lists[j][i]] += tag_dict[tag_lists[j][i]]*view_list[j]

    sorted_tags = sorted(score_dict.items(), key=operator.itemgetter(1))[::-1]
    sorted_tags = [i for i in sorted_tags if i[1] > 100/len(url_list)]
    avg_score = np.nanmean([i[1] for i in sorted_tags])
    std_score = np.nanstd([i[1] for i in sorted_tags])
    sorted_tags = [(i,(j-avg_score)/std_score) for i,j in sorted_tags]

    tag_info = []
    for i in range(len(sorted_tags)):
        tag_info.append((sorted_tags[i][0],tag_dict[sorted_tags[i][0]],sorted_tags[i][1]))

    avg_num_tags = np.nanmean([len(ls) for ls in tag_lists])
    std_num_tags = np.nanstd([len(ls) for ls in tag_lists])

    path = get_path()
    tag_file = open(f'{path}/{tag_filename}.txt', 'w')
    print(f'Number of tags μ,σ,95% C.I.: {avg_num_tags:.1f},{std_num_tags:.1f},[{avg_num_tags + 2 * std_num_tags:.1f},{avg_num_tags - 2 * std_num_tags:.1f}]\n')
    print(f'Number of tags μ,σ,95% C.I.: {avg_num_tags:.1f},{std_num_tags:.1f},[{avg_num_tags + 2 * std_num_tags:.1f},{avg_num_tags - 2 * std_num_tags:.1f}]\n',file=tag_file)
    print(tabulate(tag_info, headers=[f'Tags ({len(sorted_tags)} from {len(url_list)} videos)', 'Frequency (%)', 'Score'], floatfmt='.1f'), file=tag_file)
    print(tabulate(tag_info, headers=[f'Tags ({len(sorted_tags)} from {len(url_list)} videos)', 'Frequency (%)', 'Score'], floatfmt='.1f'))
    [labels, freqs, scores] = zip(*tag_info)
    print(f'\nSuggested tag list: ',end='')
    print(f'\nSuggested tag list: ',file=tag_file,end='')
    for i in labels[0:int(avg_num_tags)]:
        print(f'{i}, ', end='')
        print(f'{i}, ',file=tag_file,end='')
    print('',file=tag_file)
    print('')
    tag_file.close()

def get_vids_for_tags(query,number,mute=True,headless=True):
    get = getme(mute=mute,headless=headless)
    get.site("https://www.youtube.com/results?search_query=" + query)
    links = set()
    while len(links) < number:
        elems = get.by_ids('video-title')
        links.update([elem.get_attribute('href') for elem in elems])
        get.web.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
    get.close()
    return links

def tag_analyzer(query,number_vids,mute=True,headless=False):
    url_list = get_vids_for_tags(query,number_vids,mute=mute,headless=headless)
    print('Collected urls')
    analyze_tags(url_list,tag_filename=query.replace(' ','-')+f'-{number_vids}',mute=mute,headless=headless)

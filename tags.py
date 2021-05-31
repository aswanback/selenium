import re
import time
import nltk
import string
import numpy as np
import operator
from misc import getme, get_path, set_dir
from tabulate import tabulate
from selenium.webdriver.common.keys import Keys
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.util import ngrams

def get_vids(queries,number,mute=True,headless=True):
    get = getme(mute=mute,headless=headless)
    links_master = set()
    for query in queries:
        links = set()
        get.site("https://www.youtube.com/results?search_query=" + query+'&sp=CAMSAhAB')
        while len(links) < number:
            elems = get.by_ids('video-title')
            links.update([elem.get_attribute('href') for elem in elems])
            get.web.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        links_master.update(links)
        print(f'Query "{query}" collected')
    get.close()
    return links_master

def get_metadata(url_list,mute=True,headless=True):
    get = getme(mute=mute,headless=headless)
    tagmat = []
    view_list = []
    title_list = []
    description_list = []

    kill_list = ['https://www.youtube.com/watch?v=rExLI6CZRvg','https://www.youtube.com/watch?v=906uFf1E-9s','https://www.youtube.com/watch?v=FwJIlmP4soE','https://www.youtube.com/watch?v=RiCG2ToRVjQ','https://www.youtube.com/watch?v=2GSCzz7gTl4','https://www.youtube.com/watch?v=c4fRX8JoXFg','https://www.youtube.com/watch?v=rExLI6CZRvg','https://www.youtube.com/watch?v=qe8YmfOphzk']
    for shit in kill_list:
        if shit in url_list:
            url_list.remove(shit)

    for url in url_list:
        get.site(url)
        page_src = get.web.page_source

        try:
            title = re.findall('<meta name="title" content="(.*?)">',page_src)[0]
        except IndexError:
            title = ''
        title_list.append(title)

        try:
            description = re.findall('"description":{"simpleText":"(.*?)"},',page_src)[0]
        except IndexError:
            description = ''
        description_list.append(description)

        try:
            tags = re.findall('<meta name="keywords" content="(.*?)"',page_src)[0]
            #taglist = tags.split(', ')
        except IndexError:
            tags = ''
        tagmat.append(tags)

        view_match = re.findall('{"viewCount":{"simpleText":"(.*?) view',page_src)
        if not view_match:
            view_list.append(0)
        else:
            views_str = view_match[0]
            if views_str == 'No':
                view_list.append(0)
            else:
                views = int(views_str.replace(',',''))
                view_list.append(views)
    get.close()
    return tagmat,view_list, description_list, title_list

def clean_and_make_ngrams(text,ngram_count, lowercase=False,stem=True):
    text = text.replace('\\n', '')
    text = text.replace('\\\\n', '')
    text = text.replace('/', '')
    text = text.translate(str.maketrans('', '', string.punctuation))
    if lowercase:
        text = text.lower()
    n_gram_obj = ngrams(nltk.word_tokenize(text), ngram_count)
    n_grams = [' '.join(grams) for grams in n_gram_obj]
    if ngram_count == 1:
        if stem:
            stemmer = PorterStemmer()
            n_grams = [stemmer.stem(i) for i in n_grams]
        n_grams = [i for i in n_grams if i not in stopwords.words('english')]
    n_grams = [i for i in n_grams if 'https' not in i]
    return n_grams

def analyze_text(text_list,view_list,ngram_count,filename,num_displayed=50,stem=True,all_lowercase=False,debug=False):
    assert len(text_list) == len(view_list)

    path = get_path()
    titlefile = open(f'{path}/{filename}.txt', 'w')
    n_grams_1 = []
    for text in text_list:
        n_grams_1.append(clean_and_make_ngrams(text,1,stem=stem,lowercase=all_lowercase))
    avg_text_length = np.nanmean([len(n_gram) for n_gram in n_grams_1])
    std_text_length = np.nanstd([len(n_gram) for n_gram in n_grams_1])
    print(f'ngram_count = {ngram_count}, total {len(text_list)} videos, average {np.nanmean(view_list):.0f} views',file=titlefile)
    print(f'length μ,σ,95% C.I.: {avg_text_length:.1f}, {std_text_length:.1f}, [{avg_text_length - 2 * std_text_length:.1f}, {avg_text_length + 2 * std_text_length:.1f}]\n',file=titlefile)
    if debug:
        print(f'ngram_count = {ngram_count}, total {len(text_list)} videos, average {np.nanmean(view_list):.0f} views',file=titlefile)
        print(f'Length μ,σ,95% C.I.: {avg_text_length:.1f}, {std_text_length:.1f}, [{avg_text_length - 2 * std_text_length:.1f}, {avg_text_length + 2 * std_text_length:.1f}]\n')


    for n_count in range(ngram_count,0,-1):
        n_grams = []
        for text in text_list:
            n_grams.append(clean_and_make_ngrams(text,n_count,stem=stem,lowercase=all_lowercase))
        n_grams_flat = list(set([item for sublist in n_grams for item in sublist]))
        n_dict = {gram:ind for ind,gram in enumerate(n_grams_flat)}

        n_grams_views = [0] * len(n_grams_flat)
        n_grams_freqs = [0] * len(n_grams_flat)
        n_grams_count = [0] * len(n_grams_flat)
        for gram_list,views in zip(n_grams,view_list):
            for gram in gram_list:
                i = n_dict[gram]
                n_grams_views[i] += views
                n_grams_freqs[i] += 1
                if n_grams_count[i] == 0:
                    n_grams_count[i] += 1
        if sum([i for i in n_grams_freqs if i > 1]) == 0:
            print(f'\tNo ngrams of size {n_count} found. Skipping...')
        else:
            mean_views = np.nanmean([i for i,j in zip(n_grams_views,n_grams_freqs) if j > 1])
            std_views = np.nanstd([i for i,j in zip(n_grams_views, n_grams_freqs) if j > 1])
            if std_views == 0:
                std_views = 1
            matr = [[k,(i-mean_views)/std_views,j] for i,j,k,l in zip(n_grams_views, n_grams_freqs, n_grams_flat,n_grams_count) if j > 1]
            words_sorted = sorted(matr, key=operator.itemgetter(1))[::-1][0:num_displayed]

            if debug:
                print(tabulate(words_sorted,headers=[f'Top n_grams size {n_count}', 'Score', 'Frequency'],floatfmt=['.3f','.1f','.0%']))
                print('\n')
            print(tabulate(words_sorted,headers=[f'Top n_grams size {n_count}', 'Score', 'Frequency'],floatfmt=['.3f','.1f','.0%']), file=titlefile)
            print('\n',file=titlefile)
    titlefile.close()

def metadata_analyzer(queries,number_vids_each,ngram_count,foldername,debug=False,mute=True,headless=False):
    path = get_path()
    url_set = get_vids(queries,number_vids_each,mute=mute,headless=headless)
    url_list = [i for i in url_set if i is not None]
    print('Collected urls')
    tag_lists, view_list, description_list, title_list = get_metadata(url_list, mute=mute, headless=headless)
    print('Collected metadata')

    f = set_dir(foldername)
    file = open(f'{path}/{foldername}/raw-metadata.txt','w')
    file.write(str(tag_lists))
    file.write(str(view_list))
    file.write(str(description_list))
    file.write(str(title_list))
    file.close()

    t_file = open(f'{path}/{foldername}/ordered-titles.txt','w')
    t_v = [(i,j) for i,j in zip(title_list,view_list)]
    t_v_sorted = sorted(t_v,key=operator.itemgetter(1))[::-1]
    print(tabulate(t_v_sorted,('Title','Views')),file=t_file)
    if debug:
        print(tabulate(t_v_sorted, ('Title', 'Views')))
    t_file.close()

    print('Analyzing tags...')
    analyze_text(tag_lists,view_list,1,f'{foldername}/tags-{number_vids_each}',debug=debug)
    print('Analyzing titles...')
    analyze_text(title_list, view_list, ngram_count,f'{foldername}/titles-{number_vids_each}',debug=debug)
    print('Analyzing descriptions...')
    analyze_text(description_list, view_list, ngram_count,f'{foldername}/descriptions-{number_vids_each}',debug=debug)

    return tag_lists,view_list,description_list,title_list

# def analyze_tags(tag_lists,view_list,tag_filename,num_displayed,debug=False):
#     assert len(tag_lists) == len(view_list)
#
#     flat_list = []
#     for list in tag_lists:
#         flat_list.extend(list)
#     tag_dict = dict.fromkeys(flat_list, 0)
#     for i in range(len(flat_list)):
#         tag_dict[flat_list[i]] += 1
#
#     score_dict = dict.fromkeys(flat_list,0)
#     for j in range(len(tag_lists)):
#         for i in range(len(tag_lists[j])):
#             score_dict[tag_lists[j][i]] += tag_dict[tag_lists[j][i]]*view_list[j]
#
#     _sorted_tags = sorted(score_dict.items(), key=operator.itemgetter(1))[::-1]
#     sorted_tags = [(i,j) for i,j in _sorted_tags if j > 1]
#
#     avg_score = np.nanmean([i[1] for i in sorted_tags])
#     std_score = np.nanstd([i[1] for i in sorted_tags])
#     sorted_tags = [(i,(j-avg_score)/std_score) for i,j in sorted_tags]
#
#     tag_info = []
#     for i in range(len(sorted_tags)):
#         tag_info.append((sorted_tags[i][0],tag_dict[sorted_tags[i][0]]/len(tag_lists),sorted_tags[i][1]))
#
#     avg_num_tags = np.nanmean([len(ls) for ls in tag_lists])
#     std_num_tags = np.nanstd([len(ls) for ls in tag_lists])
#
#     path = get_path()
#     tag_file = open(f'{path}/{tag_filename}.txt', 'w')
#     [labels, freqs, scores] = zip(*tag_info)
#     if debug:
#         print(f'Number of tags μ,σ,95% C.I.: {avg_num_tags:.1f},{std_num_tags:.1f},[{avg_num_tags - 2 * std_num_tags:.1f},{avg_num_tags + 2 * std_num_tags:.1f}]\n')
#         print(tabulate(tag_info,headers=[f'Tags ({len(sorted_tags)} from {len(tag_lists)} videos)', 'Frequency', 'Score'],floatfmt=['.1f', '.0%', '.1f']))
#         print(f'\nSuggested tag list: ', end='')
#         for i in labels[0:int(avg_num_tags)]:
#             print(f'{i}, ', end='')
#         print('')
#     print(f'Number of tags μ,σ,95% C.I.: {avg_num_tags:.1f},{std_num_tags:.1f},[{avg_num_tags - 2 * std_num_tags:.1f},{avg_num_tags + 2 * std_num_tags:.1f}]\n',file=tag_file)
#     print(tabulate(tag_info, headers=[f'Tags ({len(sorted_tags)} from {len(tag_lists)} videos)', 'Frequency', 'Score'], floatfmt=['.1f','.0%','.1f']), file=tag_file)
#     print(f'\nSuggested tag list: ',file=tag_file,end='')
#     for i in labels[0:int(avg_num_tags)]:
#         print(f'{i}, ',file=tag_file,end='')
#     print('',file=tag_file)
#     tag_file.close()
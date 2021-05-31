import re
import time
from misc import getme, get_path, set_dir
import numpy as np
import operator
from tabulate import tabulate
from selenium.webdriver.common.keys import Keys
import nltk
import string
#nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer


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

        title = re.findall('<meta name="title" content="(.*?)">',page_src)[0]
        title_list.append(title)

        description = re.findall('"description":{"simpleText":"(.*?)"},',page_src)[0]
        description_list.append(description)

        tags = re.findall('<meta name="keywords" content="(.*?)"',page_src)[0]
        taglist = tags.split(', ')
        tagmat.append(taglist)

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

def analyze_tags(tag_lists,view_list,tag_filename):
    assert len(tag_lists) == len(view_list)

    flat_list = []
    for list in tag_lists:
        flat_list.extend(list)
    tag_dict = dict.fromkeys(flat_list, 0)
    for i in range(len(flat_list)):
        tag_dict[flat_list[i]] += 1

    score_dict = dict.fromkeys(flat_list,0)
    for j in range(len(tag_lists)):
        for i in range(len(tag_lists[j])):
            score_dict[tag_lists[j][i]] += tag_dict[tag_lists[j][i]]*view_list[j]

    _sorted_tags = sorted(score_dict.items(), key=operator.itemgetter(1))[::-1]
    sorted_tags = [i for i in _sorted_tags if i[1] > 1]
    avg_score = np.nanmean([i[1] for i in sorted_tags])
    std_score = np.nanstd([i[1] for i in sorted_tags])
    sorted_tags = [(i,(j-avg_score)/std_score) for i,j in sorted_tags]

    tag_info = []
    for i in range(len(sorted_tags)):
        tag_info.append((sorted_tags[i][0],tag_dict[sorted_tags[i][0]]/len(tag_lists),sorted_tags[i][1]))

    avg_num_tags = np.nanmean([len(ls) for ls in tag_lists])
    std_num_tags = np.nanstd([len(ls) for ls in tag_lists])

    path = get_path()
    tag_file = open(f'{path}/{tag_filename}.txt', 'w')
    print(f'Number of tags μ,σ,95% C.I.: {avg_num_tags:.1f},{std_num_tags:.1f},[{avg_num_tags - 2 * std_num_tags:.1f},{avg_num_tags + 2 * std_num_tags:.1f}]\n')
    print(f'Number of tags μ,σ,95% C.I.: {avg_num_tags:.1f},{std_num_tags:.1f},[{avg_num_tags - 2 * std_num_tags:.1f},{avg_num_tags + 2 * std_num_tags:.1f}]\n',file=tag_file)
    print(tabulate(tag_info, headers=[f'Tags ({len(sorted_tags)} from {len(tag_lists)} videos)', 'Frequency', 'Score'], floatfmt=['.1f','.0%','.1f']), file=tag_file)
    print(tabulate(tag_info, headers=[f'Tags ({len(sorted_tags)} from {len(tag_lists)} videos)', 'Frequency', 'Score'], floatfmt=['.1f','.0%','.1f']))
    [labels, freqs, scores] = zip(*tag_info)
    print(f'\nSuggested tag list: ',end='')
    print(f'\nSuggested tag list: ',file=tag_file,end='')
    for i in labels[0:int(avg_num_tags)]:
        print(f'{i}, ', end='')
        print(f'{i}, ',file=tag_file,end='')
    print('',file=tag_file)
    print('')
    tag_file.close()

def analyze_titles(title_list,view_list,filename,num_displayed=500,stem=True,remove_punctuation=True,all_lowercase=False,sort_method='score'):

    title_matrix = []
    for title in title_list:
        title = title.replace('\n', '')
        title = title.replace('\\n','')
        title = title.replace('\\\\n','')
        title = title.translate({ord(i): None for i in '\\\n'})
        title_words = nltk.word_tokenize(title)
        bad_words = ['http','.com','.net',"'",'.ly','.gl']
        for j in bad_words:
            title_words = [i for i in title_words if j not in i]

        title_no_stopwords = [w for w in title_words if w.lower() not in stopwords.words('english')]

        if all_lowercase and remove_punctuation:
            title = [w.lower() for w in title_no_stopwords if w not in string.punctuation]
        elif all_lowercase and not remove_punctuation:
            title = [w.lower() for w in title_no_stopwords]
        elif not all_lowercase and remove_punctuation:
            title = [w for w in title_no_stopwords if w not in string.punctuation]
        elif not all_lowercase and not remove_punctuation:
            title = title_no_stopwords
        if stem:
            stemmer = PorterStemmer()
            title = [stemmer.stem(i) for i in title]
        title_matrix.append(title)

    word_list = []
    for title in title_matrix:
        for word in title:
            if word not in word_list:
                word_list.append(word)
    print(word_list)

    doc_word = []
    doc_word_norm = []
    for i in range(len(title_matrix)):
        doc_vec = [0] * len(word_list)
        doc_vec_norm = [0] * len(word_list)
        doc_vec_no_rep = [0] * len(word_list)
        for word in title_matrix[i]:
            ind = word_list.index(word)
            doc_vec[ind] += view_list[i]
            if doc_vec_norm[ind] == 0:
                doc_vec_norm[ind] += 1
        doc_word.append(doc_vec)
        doc_word_norm.append(doc_vec_norm)
    doc_word = np.array(doc_word)
    doc_word_norm = np.array(doc_word_norm)

    word_raw_views = [sum(i) for i in doc_word.T]
    mean_views = np.nanmean(word_raw_views)
    std_views = np.nanstd(word_raw_views)
    word_view_score = [(i-mean_views)/std_views for i in word_raw_views]

    word_raw_freq = [sum(i) for i in doc_word_norm.T]
    word_freq_frac_of_titles = [i/len(title_list) for i in word_raw_freq]
    word_freq_frac_of_words = [i/sum(word_raw_freq) for i in word_raw_freq]
    word_matrix = [[word_list[i],word_view_score[i],word_freq_frac_of_titles[i],word_freq_frac_of_words[i]] for i in range(len(word_list))]

    word_matrix = [word_matrix[i] for i in range(len(word_matrix)) if word_raw_freq[i] > 1]

    if sort_method == 'score':
        words_sorted = sorted(word_matrix, key=operator.itemgetter(1))[::-1]
    elif sort_method == 'word freq':
        words_sorted = sorted(word_matrix, key=operator.itemgetter(2))[::-1]
    elif sort_method == 'title freq':
        words_sorted = sorted(word_matrix, key=operator.itemgetter(3))[::-1]
    else:
        print("Unsupported sort_method, choose 'score', 'word freq', or 'title freq'. Auto-choosing 'score'")
        words_sorted = sorted(word_matrix, key=operator.itemgetter(1))[::-1]
    words_sorted = words_sorted[0:num_displayed]

    avg_title_length = np.nanmean([len(title) for title in title_matrix])
    std_title_length = np.nanstd([len(title) for title in title_matrix])

    path = get_path()
    titlefile = open(f'{path}/{filename}.txt', 'w')
    print(f'Length μ,σ,95% C.I.: {avg_title_length:.1f}, {std_title_length:.1f}, [{avg_title_length - 2 * std_title_length:.1f}, {avg_title_length + 2 * std_title_length:.1f}]\n')
    print(f'Length μ,σ,95% C.I.: {avg_title_length:.1f}, {std_title_length:.1f}, [{avg_title_length - 2 * std_title_length:.1f}, {avg_title_length + 2 * std_title_length:.1f}]\n',file=titlefile)
    print(f'Sorted by {sort_method}')
    print(tabulate(words_sorted,headers=[f'Top {num_displayed} words from {len(title_list)} videos', 'Score', 'Freq per video', 'Freq per word'],floatfmt=['.3f','.1f','.0%','.0%']))
    print(tabulate(words_sorted,headers=[f'Top {num_displayed} words from {len(title_list)} videos', 'Score', 'Freq per video', 'Freq per word'],floatfmt=['.3f','.1f','.0%','.0%']), file=titlefile)
    titlefile.close()


def metadata_analyzer(queries,number_vids_each,foldername,mute=True,headless=False):
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

    analyze_tags(tag_lists, view_list, tag_filename=f'{foldername}/tags-{number_vids_each}')
    analyze_titles(title_list, view_list, f'{foldername}/titles-{number_vids_each}')
    analyze_titles(description_list, view_list, f'{foldername}/descriptions-{number_vids_each}')

    return tag_lists,view_list,description_list,title_list





# Builds a term-frequency matrix
# Takes in a doc word matrix (as built in buildDocWordMatrix)
# Returns a term-frequency matrix, which should be a 2-dimensional numpy array
# with the same shape as docword
def build_jank_TFMatrix(docword):
    # fill in
    tf = np.zeros((len(docword), len(docword[0])))
    for i in range(len(docword)):
        sm = sum(docword[i])
        for j in range(len(docword[i])):
            tf[i][j] = docword[i][j]
    return tf


# Builds an inverse document frequency matrix
# Takes in a doc word matrix (as built in buildDocWordMatrix)
# Returns an inverse document frequency matrix (should be a 1xW numpy array where
# W is the number of words in the doc word matrix)
# Don't forget the log factor!
def buildIDFMatrix(docword):
    idf = np.zeros((1, len(docword.T)))
    for i in range(len(docword.T)):
        num_docs_word_in = (sum([1 for j in docword.T[i] if j != 0]))
        idf[0][i] = np.log10(len(docword) / num_docs_word_in)
    return np.array(idf)


# Builds a tf-idf matrix given a doc word matrix
def build_jank_TFIDFMatrix(docword):
    # fill in
    tf = build_jank_TFMatrix(docword)
    idf = buildIDFMatrix(docword)
    tfidf = np.zeros((len(tf), len(idf.T)))

    for i in range(len(tf)):
        for j in range(len(idf.T)):
            tfidf[i][j] = idf.T[j] * tf[i][j]
    return np.array(tfidf)
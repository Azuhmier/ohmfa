"""parse_threads.py
"""




import os
import sys
import time
import datetime
from bs4 import BeautifulSoup




class ParseThreads():
    def __init__(self, db_name, config, mode='update', dry_run=False, verbose=False):
        if not verbose :
            sys.stdout = open(os.devnull, 'w')
        REL_DIR_THREAD_HTMLS   = '../../threads/html'
        REL_DIR_OP_TEXTS   = '../../threads/ops'

def get_thread_nums(dir_thread_htmls):
    for file_name_thread_html in os.listdir(dir_thread_htmls):
        if not file_name_thread_html.startswith('.'):
            thread_num = file_name_thread_html[:-5]
            yield thread_num

def get_meta_text (article) :
    meta_text=''
    meta = article.find_all("div", class_="pull-right")[0].text
    list_meta_values = meta[1:-1].split(' / ')
    list_meta_keys = ['posts ','images','ip    ']
    list_meta = ['    '.join(z) for z in zip(list_meta_keys, list_meta_values)]
    meta_text = meta_text + '\n'.join(list_meta)
    date_time_of_thread_creation = article.find_all("span", class_="time_wrap")[0].text
    format_string = " %a %d %b %Y %H:%M:%S "
    time_stamp_of_thread_creation = time.mktime(datetime.datetime.strptime(date_time_of_thread_creation, format_string).timetuple())
    meta_text = meta_text + '\ntime      '+str(time_stamp_of_thread_creation)
    return meta_text

def get_op_text(article):
    div = article.find_all("div", class_="text")[0]
    for elem in div.find_all(["a", "span", "div", "br"]):
        if elem.name == 'br':
            elem.replace_with("\n")
        else :
            elem.replace_with(elem.text)
    op_text = div.get_text()
    return op_text


list_thread_nums = get_thread_nums(dir_thread_htmls)
i = 0
for thread_num in list_thread_nums :
    if folder.exists() :
        if text.exists() :
            if text.stat().st_size != 0 :
                if meta.isfile() :
                    continue
    elif html.stat().st_size == 0 :
        continue
    i = i + 1
    soup = BeautifulSoup(open(file_path_thread_html), 'html.parser')
    article = soup.body.find_all("article", id=thread_num)[0]
    op_text = get_op_text(article)
    meta_text = get_meta_text(article)
    if not folder.exists()
        os.mkdir()
    text.write()
    meta.write()

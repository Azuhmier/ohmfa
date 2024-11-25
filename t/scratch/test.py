
import sys
sys.path.append(  '/home/azuhmier/progs/ohmfa/t/scratch/lib' )
from lib.ohmfa.main import Main
from lib.ohmfa.fetcher import Fetcher

OHMFA_DIR = '/home/azuhmier/progs/ohmfa/t/scratch/empty_dir'
URLS_FILE = '/home/azuhmier/hmofa/hmofa/.ohm/output/paged_lists/objs/plain/url.txt'




o = Main()
o.select_ohmfa_dir(OHMFA_DIR)
o.load_urls(URLS_FILE)
f = Fetcher('/home/azuhmier/progs/ohmfa/t/scratch/lib/frameworks/domains_config.yml')
oslds = [
    #'ghostbin',
    #'hardbin',
    #'git',
    #'githubusercontent',
    #'itch',
    #'catbox',
    #'pastebin',
    'archiveofourown',
    'sofurry',
    #'fiction',
    #'poneb',
    #'fanfiction',
    #'literotica',
    #'furaffinity',
    #'mega',
    #'google',
    #'fiction',
    #'rentry',
    #'blokfort',
    #'snekguy',
    #'snootgame',
    #'google',
    #'reddit',
    #'psstaudio',
    #'pastefs',
    #'mcstories',
]
test_urls = [
    'https://archiveofourown.org/works/60729490',
    #'https://baron03.sofurry.com/',
    'https://baron03.sofurry.com/stories',
    'https://www.sofurry.com/browse/user/stories?by=213418&stories-page=3',
    'https://www.sofurry.com/browse/folder/stories?by=213418&folder=21225',
    #'https://archiveofourown.org/users/Azuhmier',
    #'https://archiveofourown.org/series/3278830',
    #'https://archiveofourown.org/users/PapaDelta/pseuds/PapaDelta',
    #'https://archiveofourown.org/users/PapaDelta/series',
    #'https://archiveofourown.org/users/PapaDelta/pseuds/PapaDelta/series',
    #'https://archiveofourown.org/users/PapaDelta/profile',
]
#o.urls = test_urls + o.urls
o.urls = test_urls
f.load_urls(o.urls,slds=oslds,verbose=1,mx=2,prnt=False)
#f.load_urls(o.urls,verbose=1)
#f.get_passwords('/home/azuhmier/.pwds')
#f.start_session()
#f.check_urls(no_domain=True)
#f.check_urls(slds=oslds)

#f.d.quit()
#f.delete_all_sessions()
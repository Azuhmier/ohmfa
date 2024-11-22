
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
slds = [
    #'ghostbin',
    #'hardbin',
    #'git',
    #'githubusercontent',
    #'itch',
    #'catbox',

    #'pastebin',
    #'archiveofourown',

    'sofurry',
    'blokfort',
    'google',
    'fiction',
    'snekguy',
    'poneb',
    'snootgame',
    'fanfiction',
    'google',
    'reddit',
    'fiction',
    'rentry',
    'psstaudio',
    'pastefs',
    'mega',
    'mcstories',
    'literotica',
    'furaffinity',
]
refresh = False
f.load_urls(o.d_urls)
f.get_passwords('/home/azuhmier/.pwds')
#f.check_urls(no_domain=True)
if not refresh:
    f.check_urls(oslds=slds,no_domain=True)

f.d.quit()
cmd     = "sessions.list"
headers = {"Content-Type": "application/json"}
fs_data = { "cmd": cmd}
r = f.s.post(f.s_url, headers=headers, json=fs_data)
import json
fs_r_json     = json.loads(r.content)
session_list = fs_r_json['sessions']
for session_id in session_list:
    cmd     = "sessions.destroy"
    headers = {"Content-Type": "application/json"}
    fs_data = { "cmd": cmd,"session":session_id}
    r = f.s.post(f.s_url, headers=headers, json=fs_data)
    fs_r_json     = json.loads(r.content)
    status = fs_r_json['status']
    print(status)
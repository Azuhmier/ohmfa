"""
## File Sytems
https://realpython.com/working-with-files-in-python/
https://docs.python.org/3/library/os.html#os.makedirs

os
    .mkdir()
        .mkdirs(dir1/dir2/dir3)
            mode=0o770
            - gives owner and group uerse r,w,and x prems
            - default is 0o777
    .listdir()
    .scandir()
    .walk()
        RETURNS [,[dirpath, dirnames,files]]
        - topdown=False
    .stat()
        .st_mtime
    .remove()
        - remove file
    .unlink()
    path
        .join()
        .is_file()
        .is_dir()
        .exists()
        .rmdir()
glob
    .iglob(pat)
        RETURNS: iterator
        recursive=True
    .glob(pat)
        recursive=True
pathlib
    Path
        .mkdir(dir)
            exists_ok=True
        .iterdir()
        .glob()
            RETURNS: generator
        .joinpath()
        .is_file()
        .is_dir()
        .name
        .stat()
            .st_mtime
        .rmdir()
        .mkdir()
            exist_ok=True
            parents=True
            - create parents if no exists
        .rename()
time
    ctime(entry.mtime)
datime
    .utcfromtimestamp(ppath.stat().st_mtime)
    .strftime('%d %b %Y)
tarfile
    .open()
        ..add(file)
        ..extract()
        ..extractfile()
        ..extractall()
            path=path
        ..getnames()
        ..getmembers()
            ..name
            ..size
zipfile
    .ZipFile
        RETURNS File i/o
        .namelist()
        .extract()
        .write()
        .extractall()
            path = dir
            pwd = pwd
        .getinfo
            .file_size
            .filename
            .compress_size
sys
    .argv
fileinput
    .input()
        ..isfirstline()
        ..filename()
        ..lineno()
shutil
    .make_archive(base_name, format, root_dir)
    .unpack_archive()
    .rmtree()
    .copy()
        - content, meta
    .copy2()
        - content, meta, attribs
    .copytree()
    - for non empty directories
    .move()
    .rename()

__str__
    .endswith()
    .startswith()
fnmatch
    .fnmatch(fname, '*.txt')
tempfile.TempraryFile()
    RETURNS: File i/o
    .write()
    .seek()
    .read()
    .close()
io.
    TextIOWrapper
        .name
        .mode
        .encoding
    BytesIO
    StringIO

urllib
    parse
        urlparse
            .scheme
            .netloc
            .path
            .params
            .query
            .fragment
FileExistsError
OSError
IsADirectoryError

pastebin.com
    /[a-zA-Z0-9]{8}

archiveofourown.com
    /works/\d+
        /chapters/\d{8}
    /series/\d+
    view_full_work=true
catbox.moe
    /c/[a-z0-9]{6}
files.catbox.moe
    /[a-z0-9].ext
docs.google.com
    /d/e/2PACX.+/PUB
    /d/.+
        /edit
drive.google.com
   /file/d/.+/view 
fiction.live
    /title/.+
ghostbin.com
    /.+
        /.+
    /paste/.+
        /.+
            /.+
    
hardbin.com
    /ipfs/.+/#.+
"""
import re
import sys
import copy
sys.path.append(  '/home/azuhmier/progs/ohmfa/t/scratch/lib' )
from lib.ohmfa.main import Main

OHMFA_DIR = '/home/azuhmier/progs/ohmfa/t/scratch/empty_dir'
URLS_FILE = '/home/azuhmier/hmofa/hmofa/.ohm/output/paged_lists/objs/plain/url.txt'




o = Main()
o.select_ohmfa_dir(OHMFA_DIR)
o.load_urls(URLS_FILE)
o.analyze_urls()

import scrapy
import selenium
import requests
import time
from bs4 import BeautifulSoup

from socket import gethostbyname,gaierror
from requests.exceptions import ConnectionError, Timeout, ConnectTimeout
from urllib3.exceptions import NewConnectionError
from http.client import RemoteDisconnected

s = requests.session()
#s.auth = ('user', 'pass')
#s.headers.update({'x-test': 'true'})
timeout = 5
header = {
    
}
def fetch(url,timeout=5,params={},headers={},wait=1):
    soup = None
    time.sleep(wait)
    try:
        r = s.get('https://'+domain,timeout=timeout,params=params,headers=headers)
        value = 'unkown status'
        if r.status_code == 200:
            value = 'Success'
            soup = BeautifulSoup(r.content,'html.parser')
        elif r.status_code == 410:
            value = 'GONE'
        elif r.status_code == 406:
            value = 'Not Acceptable'
        elif r.status_code == 404:
            value = 'Not Found'
        elif r.status_code == 504:
            value = 'Success'
        elif r.status_code == 403:
            value = 'Forbidden'
        print("    ",url," status: ", r.status_code," ",value)
    except (ConnectionError,ConnectTimeout):
        exc_type, value, traceback = sys.exc_info()
        name = exc_type.__name__
        value = str(value)
        if name == 'ConnectionError':
            if 'RemoteDisconnected' in value:
                value = 'RemoteDisconnected'
            elif '[Errno -2]' in value:
                value = 'Name or service not known'
            elif '[Errno -3]' in value:
                value = 'Temporary failer in name resolution'
            elif '[Errno 113]' in value:
                value = 'No route to host'
        elif name == 'ConnectTimeout':
            if 'Max retries exceeded' in value:
                value = 'Max retries exceeded'
        print("        ",url," ", name," ",value)

    return soup

soups = []
for key,domains in o.c_urls.items():
    print(key)
    for domain,plens in domains.items(): 
        soups.append(fetch('https://'+domain))
        for plen,urls in plens.items(): 
            soups.append(fetch(urls[0].geturl()))
soups = [x for x in soups if x]
"""
head:
    csrf-param
    csrf-token
body
    div id:inner class ['wrapper']
"""
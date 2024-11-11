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
import sys
sys.path.append(  '/home/azuhmier/progs/ohmfa/t/scratch/lib' )
from lib.ohmfa.main import Main
from lib.ohmfa.fetcher import Fetcher

OHMFA_DIR = '/home/azuhmier/progs/ohmfa/t/scratch/empty_dir'
URLS_FILE = '/home/azuhmier/hmofa/hmofa/.ohm/output/paged_lists/objs/plain/url.txt'




o = Main()
o.select_ohmfa_dir(OHMFA_DIR)
o.load_urls(URLS_FILE)
f = Fetcher()
f.load_urls(o.d_urls,test=True)

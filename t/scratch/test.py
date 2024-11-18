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
breakpoint 9267
6773
8666| function Animation( elem, properties, options ) {
868  | jQuery.ready.promise = function( obj ) {
9263 | jQuery.timers = [];
8651 | function createTweens( animation, props ) {
11   | function showTOSPrompt()
VM626
//<![CDATA[

  $j(document).ready(function() {
    var container = $j("#tos_prompt");
    var outer = $j("#outer");
    var button = $j("#accept_tos");

    setTimeout(showTOSPrompt, 1500);

    function showTOSPrompt() {
      $j.when(container.fadeIn(500)).done(function() {
        outer.addClass("hidden").attr("aria-hidden", "true");
      });

      $j("#tos_agree").on("click", function() {
        button.attr("disabled", !this.checked);
        if (this.checked) {
          button.on("click", function() {
            acceptTOS();
            outer.removeClass("hidden").removeAttr("aria-hidden");
            $j.when(container.fadeOut(500)).done(function() {
              container.remove();
            });
          });
        };
      }).change();
    };
  });

//]]]]><![CDATA[>

    https://archiveofourown.org/token_dispenser.json
    https://archiveofourown.org/works/33232534/hit_count.json
    meta, name='csrf-param', content='authenticity_token'
    meta, name='csrf-token', content
sec-fetch-data=style,priority=u=0,accept=text/css,*/*;q=0.1
accept=*/*
    .js,sef-fetch-data=script,priority=u=1
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
f = Fetcher('/home/azuhmier/progs/ohmfa/t/scratch/lib/frameworks/domains_config.yml')
slds = [
    #'archiveofourown',
    #'sofurry',
    #'blokfort',
    #'catbox',
    #'google',
    #'fiction',
    #'pastebin',
    #'snekguy',
    #'poneb',
    #'snootgame',
    #'itch',
    'fanfiction',
    #'google',
    #'reddit',
    #'hardbin',
    #'fiction',
    #'git',
    #'rentry',
    #'githubusercontent',
    #'psstaudio',
    #'pastefs',
    #'mega',
    #'mcstroies',
    #'literotica',
    #'furaffinity',
    #'ghostbin',
    ]
bad_shit = [
    'Privacy error',
    'Just a moment...',
]
f.load_urls(o.d_urls)
f.get_passwords('/home/azuhmier/.pwds')
#f.check_urls(oslds=slds)
f.check_urls(oslds=slds,no_domain=True)
f.driver.quit()
import sys
import os
from pathlib import Path
from urllib.parse import urlparse
import copy


class Main():
    ohmfa_dir = None
    ohmfa_dot_dir = None
    archive = None
    db_name = None
    db = None
    urls = None
    d_urls = None
    c_urls = None
    url_groups = None


    def __init__(self,*args,**kwargs):
        pass


    def select_ohmfa_dir(self,dirpath):
        self.ohmfa_dir=Path(dirpath)
        self.ohmfa_dir.mkdir(exist_ok=True)
        self.ohmfa_dot_dir = self.ohmfa_dir.joinpath('.ohmfa')
        self.ohmfa_dot_dir.mkdir(exist_ok=True)
        self.archive = self.ohmfa_dir.joinpath('archive')
        self.archive.mkdir(exist_ok=True)
        self.select_db(db_name='_default')


    def select_db(self,db_name):
        self.db_name = db_name
        self.db = self.archive.joinpath(self.db_name)
        self.db.mkdir(exist_ok=True)
    

    def rm_db(self):

        for root, dirs, files in os.walk(self.db, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.db)

        self.db_name       = None
        self.db            = None

    def analyze_urls(self):
        """_summary_

        
        

        vars = [
            ?*=
            _a_*
            _x_*
            _f_*
            _s_*
            _p_*
            _c_*
            *_uid


        path
        flash
        splash

        author
            author
            alias
        collection
            collection
                series
                group
        content
            work
                title
                chrono
                edition
                _tag
                _description
            part
                title
                chrono
                edition
                _tag
                _description
            page
            num
                chroni
        util
            iter
            domain
            fext
        




        dead
        specfic


        """
        substrings = [
            'itch.io',
            'catbox.moe',
            'google.com',
            'rentry',
        ]j
        bp={
            'dead':       False,
            'specfic':    False,
            'path':       { '_*':['_*']},
            'splash':     { '_*':[]},
            'flash':      { '_*':[]},
            'collection': { '_*':['_*']},
            'author':{
                '_alias_*':[],
                '_author_*':[]},
            'content':{
                'page_*':[],
                'page':[],
                'part_*':[],
                'part':[],
                'work_*':[],
                'work':[]},
        }

        dspt = {
            'docs.google.com':[{
                'dead':False,
                'content':{
                    '_work_pub':['document','d','e','_work_uid_','pub'],
                    '_work':['document','d','_work_uid_']}}],
            'drive.google.com':[{
                'dead':False,
                'content':{
                    '_work':['file','d','_work_uid_']}}],
            'mega.nz':[{
                'dead':False,
                'path':{ 
                    '_folder':['folder','_folder_uid_']},
                'content':{
                    '_work':['_p_folder','file','_work_uid_']}}],
            'catbox.moe':[{
                'specfic': True,
                'dead':False,
                'collection':{
                    '_collection':['c','_collection_uid_']},
                'content':{
                    'part':[['files','.','_domain_'],['_work_uid_','.','_fext_']],
                    'work':['_c_collection']}}],
            'raw.githubusercontent.com':[{
                'dead':False,
                'path':{
                    '_folder':['folder_']},
                'author':{
                    '_author':['_author_']},
                'collection':{
                    '_repo':['_author_','repo_','version_'] },
                'content':{
                    'work':['c_repo_','p_folder_','_work_uid_']}}],
            'www.reddit.com':[{
                'dead':False,
                'specfic':True,
                'collection':{
                    '_sub':['r','sub_']},
                'author':{
                    '_author':['user','_author_']},
                'content':{
                    '_work':['c_sub_','_author_','comments', '_work_uid_','_work_']}}],

            'www.blokfort.com':[{
                'dead':False,
                'splash':{
                    '_works':['nsfw-comics']}, 
                'author':'Blokfort',
                'content':{
                    '_work':['_work_']}}],
            'snekguy.com':[{
                'dead':False,
                'author':'Snekguy',
                'path':{
                    '_group':['group_']}, 
                'splash':{
                    '_work':['stories']}, 
                'content':{
                    '_work_edition': ['stories','p_group_','_work_','edition_'],
                    '_work': ['stories','p_group_','_work_']}}], 
            'snootgame.xyz':[{
                'dead':False,
                'specfic':True,
                'splash':{
                    '_downloads':['en','download','.html']},
                'content':{
                    '_work':['en','bin','_work_uid_','.zip']}}],
            'itch.io':[{
                'dead':False,
                'author':{
                    'author':['_author_','._domain_']},
                'content':{
                    '_work':['author_','_work_uid_']}}],
            'ghostbin.com':[{
                'dead':True,
                'path':{
                    '_folder':['folder_uid_']},
                'content':{
                    '_work':['p_folder_','_work_uid_']}}],
            'hardbin.com':[{
                'dead':True,
                'content':{
                    '_work':['ipfs','_work_uid_']}}],
            'pasterefs.com':[{
                'dead':False,
                'content':{
                    '_work':['pid','_work_uid_']}}],
            'pastes.psstaudio.com':[{
                'dead' : False,
                'content':{
                    '_work':['post','_work_uid_']}}],
            'rentry':[{
                'dead':False,
                'content':{
                    '_work':['_work_uid_']}}],
            'git.io':[{
                'dead' : False,
                'work':{
                    '_work':['_work_uid_']}}],
            'pastebin.com':[{
                'dead':False,
                'author':{
                    '_author':['u','_author_']},
                'splash':{
                    '_work':['_author_']},
                'content':{
                    '_work':['_work_uid_']} }],
            'poneb.in':[{
                'dead' :False,
                'author':{
                    '_author':['u','_author_']},
                'splash':{
                    '_work':['_author_']},
                'content':{
                    '_work':['_work_uid_']}}],
            'mcstories.com':[{
                'dead':False,
                'authors':{
                    '_author':['Authors','index','.html']},
                'flash':{
                    '_work':['_work_','index','.html']},
                'author':{
                    '_author':['Authors','_author_']},
                'content':{
                    '_work':['_work_','_work_','.fext_']}}],
            'fiction.live':[{
                'dead':False,
                'author':{
                    '_author':['user','_author_']},
                'content':{
                    '_part':['stories','_work_','_work_uid_','_part_','_part_uid_']}}],
            'www.literotica.net':[{
                'dead' : False,
                'author':{
                    '_author':['authors','_author_']},
                'splash':{
                    '_work':['_author_','works','stories','all']},
                'content':{
                    '_page':['s','_work_','?page=','page_']}}],
            'www.fanction.net':[{
                'dead' : False,
                'author':{
                    '_author':['u','_author_uid','_author_']},
                'content':{
                    '_part':['s','_work_uid_','_part_','_work_']}}],
            'archiveofourown.org':[{
                'dead':False,
                'author':{
                    '_alias':['user','_author_','pseuds','alias_'],
                    '_author':['user','_author_']},
                'splash':{
                    '_series':['_author_','series','?page=','iter_'],
                    '_work':['_author_','works','?page=','iter_']},
                'collection':{
                    '_series':['series','series_uid_']},
                'content':{
                    '_part':['works','_work_uid_','chapters','_part_uid_'],
                    '_work':['works','_work_uid_']}}],
            'www.furaffinity.net':[{
                'dead' : False,
                'author':{
                    '_author':['user','_author_']},
                'splash':{
                    '_work':['gallery','_author_','iter_','\?']},
                'content':{
                    '_work':['view','_work_uid_']}}],
            'www.sofurry.com':[{
                'dead':False,
                'author':{
                    '_author':['_author_','._domain_']},
                'splash':{
                    '_*':['browse','user','stories','?uid=','_author_uid_','?stories-page=','iter_']},
                'collection':{
                    '_folder':['browse','folder','stories','?by=_author_uid_','?folder=folder_uid_']},
                'content':{
                    '_work':['view','_work_uid_']}}],
        }

        self.c_urls = {}

        for url in self.d_urls:
            domain = url.netloc
            key = domain
            for substring in substrings:
                if substring in key:
                    key = substring
                    break

            if key not in self.c_urls:
                self.c_urls[key]={}
            if domain not in self.c_urls[key]:
                self.c_urls[key][domain]={}
            path = url.path.split('/')
            path = [x for x in path if x]

            plen = str(len(path))
            if plen not in self.c_urls[key][domain]:
                self.c_urls[key][domain][plen]=[]
            self.c_urls[key][domain][plen].append(url)

    def rm_ohmfa_dir(self):
        for root, dirs, files in os.walk(self.ohmfa_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.ohmfa_dir)

        self.ohmfa_dir     = None
        self.ohmfa_dot_dir = None
        self.archive       = None
        self.config        = None
        self.db_name       = None
        self.db            = None


    def load_urls(self,urls_file_path=None):
        infile =  open(urls_file_path,'r', encoding='utf-8')
        self.urls = infile.readlines()
        self.d_urls = [urlparse(x) for x in self.urls]
        infile.close()


    @classmethod
    def classmethod(cls):
        return 'class method called', cls


    @staticmethod
    def staticmethod():
        return 'static method called'

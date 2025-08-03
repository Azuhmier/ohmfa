import os
from pathlib import Path
from urllib.parse import urlparse


class Main():
    ohmfa_dir     = None
    ohmfa_dot_dir = None
    archive       = None
    db_name       = None
    db            = None
    urls          = None


    def __init__(self,*args,**kwargs):
        pass

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



    def load_urls(self,urls_file_path=None):
        infile =  open(urls_file_path,'r', encoding='utf-8')
        self.urls = infile.readlines()
        infile.close()


    @classmethod
    def classmethod(cls):
        return 'class method called', cls


    @staticmethod
    def staticmethod():
        return 'static method called'

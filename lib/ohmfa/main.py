## MASTER
import os
import yaml
from ohmfa.ohmfa_url import OhmfaUrl
from ohmfa.ohmfa import Ohmfa
from ohmfa.fetcher import Fetcher

REL_DCNFG_PATH = '../../configs/domain_configs.yml'
file_dir = os.path.dirname(__file__) #<-- absolute dir the script is in
dcnfg_path = os.path.join(file_dir, REL_DCNFG_PATH)

class Main(Ohmfa):
    odir       = None
    oddir      = None
    general    = None
    gdir       = None
    sdir       = None
    tdir       = None
    durls      = []


    def __init__(self,log_level=0):
        super().__init__(log_level=log_level)
        self.logger.debug(f"Main.__init__()")
        self.logger.debug(f"...Logger has been set with log level of {log_level}")
        with open(dcnfg_path, mode='r',encoding='utf-8' ) as infile:
            self.dcnfg.update(yaml.safe_load(infile))

    def load_urls(self, urls_file_path=None, lst=False):
        urls = None
        if not lst:
            infile =  open(urls_file_path,'r', encoding='utf-8')
            urls = infile.readlines()
            infile.close()
        else:
            urls = urls_file_path
        for url in urls:
            durl = OhmfaUrl(url)
            self.durls.append(durl)

    def create_fetcher(self, archive_path=None):
        self.fetcher = Fetcher(self.dcnfg, archive_path)
        self.fetcher.durls = self.durls


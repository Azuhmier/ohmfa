import os
import sys
import yaml
from pathlib import Path
from urllib.parse import urlparse
from ohmfa.url.ohmfa_url import OhmfaUrl
from ohmfa.ohmfa import Ohmfa

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


    def __init__(self,*args,**kwargs):
        super().__init__()
        with open(dcnfg_path, mode='r',encoding='utf-8' ) as infile:
            self.dcnfg = yaml.safe_load(infile)
        print(f"dcnfg loaded from '{dcnfg_path}'")

    def load_urls(self,urls_file_path=None):
        infile =  open(urls_file_path,'r', encoding='utf-8')
        urls = infile.readlines()
        infile.close()
        for url in urls:
            self.durls.append(OhmfaUrl(url))

        print(f"urls loaded from '{urls_file_path}'")

    def ohm(self, cmd, odir):
        odir  =Path(odir)
        oddir = odir.joinpath('.ohm')
        if cmd == 'create':
            if not oddir.exists() :
                odir.mkdir(exist_ok=True)
                oddir.mkdir(exist_ok=True)
                print(f"ohm '{odir}' created")
            else: 
                print(f"ohm '{odir}' already exists")
        elif cmd == 'select':
            if (self.oddir is not None
                and
                self.oddir.absolute() == oddir.absolute()
            ):
                print(f"ohm '{self.odir}' is already selected")
            elif oddir.exists() :
                self.odir = odir
                self.oddir = oddir
                print(f"ohm '{self.odir}' selected")
            elif odir.exists() :
                print(f"'{odir}' is not an ohm dir")
            else:
                print(f"'{odir}' does not exists")
        elif cmd == 'rm':
            if oddir.exists() :
                for root, dirs, files in os.walk(odir, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(odir)
                print(f"ohm '{odir}' removed")
                if (self.oddir is not None
                    and
                    self.oddir.absolute() == oddir.absolute()
                ):
                    self.odir       = None
                    self.oddir      = None
                    self.general    = None
                    self.gdir       = None
                    self.sdir       = None
                    self.tdir       = None
            else:
                print(f"'{odir}' is not an ohm dir")
        else:
            sys.exit("ERROR")

    def gohm(self,cmd,general):
        if self.odir is not None:
            gdir = self.odir.joinpath(general)
            if cmd == "create":
                if not gdir.exists() :
                    gdir.mkdir(exist_ok=True)

                    sdir = gdir.joinpath("scrapes")
                    sdir.mkdir(exist_ok=True)

                    tdir = gdir.joinpath("threads")
                    tdir.mkdir(exist_ok=True)
                    print(f"gohm '{gdir}' created")
                else:
                    print(f"gohm '{gdir}' already exists")
            elif cmd == "select":
                if (self.gdir is not None
                    and
                    self.gdir.absolute() == gdir.absolute()
                ):
                    print(f"gohm '{self.gdir}' already selected")
                elif gdir.exists() :
                    self.gdir = gdir
                    self.sdir = self.gdir.joinpath("scrapes")
                    self.tdir = self.gdir.joinpath("threads")
                    print(f"gohm dir '{self.gdir}' selected")
                else:
                    print(f"gohm '{gdir}' does not exists")

            elif cmd == "rm":
                for root, dirs, files in os.walk(self.gdir, topdown=False):
                    for name in files:
                        os.remove(os.path.join(root, name))
                    for name in dirs:
                        os.rmdir(os.path.join(root, name))
                os.rmdir(gdir)
                print(f"gohm dir '{gdir}' removed")
                if (self.gdir is not None
                    and
                    self.gdir.absolute() == gdir.absolute()
                ):
                    self.general    = None
                    self.gdir       = None
                    self.sdir       = None
                    self.tdir       = None
            else:
                sys.exit("ERROR")
        else:
                print(f"ohm not selected!")


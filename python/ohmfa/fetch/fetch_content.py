"""fetch_content.py
"""
import sys
import re
import time
import requests
import copy
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from requests_html import HTMLSession
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import InvalidCookieDomainException
from selenium.common.exceptions import ElementNotInteractableException
from ohmfa.fetch.fetcher import Fetcher
from ohmfa.utils.pather import Pather,SinglePather




class triggered(Exception):
    pass




class FetchContent(Fetcher,Pather):
    domain_config = None
    ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'
    running = False
    urls = None
    wfl = None
    actions = None
    action = None
    wfl_name = None
    GET = None
    pwds = None
    VARS = None
    domain_key = None
    list_meta = None
    url_path = None
    archive_path = None
    archive_config = None
    html = None
    list = None
    config = None
    meta = None
    re_io = re.compile(".+(io|live|xyz)$")


    def __init__(self):
        self.actions = []
        self.Get = {}
        self.urls = []
        pass


    def Next(self):
        self.url = self.urls.pop(0)
        self.get_domain_config()
        while self.do_wfl() :
            if not self.running:
                break


    def get_domain_config(self) :
        pos = self.url.netloc.index('.')
        self.domain_key = self.url.netloc[pos:]
        if self.url.netloc in self.domain_config :
            retu = self.domain_config[self.url.netloc]
        elif self.domain_key in self.domain_config :
            retu = self.domain_config[self.domain_key]
        else :
            sys.exit()
        return retu


    def do_wfl(self) :
        try :
            # default worflow
            self.actions=[]
            self.wfl_name = 'default' 
            copy.deepcopy(self.domain_config["workflows"][self.wfl_name])

            for action_name in self.wfl["do"] :
                self.action = copy.deepcopy(self.domain_config["actions"][action_name])
                self.action["name"] = action_name
                self.actions.append(action)
                if not self.do_action() :
                    return 0
        except triggered:
            return 0
        self.running = False


    def do_action(self) :
        # request
        if self.action["method"] == "requests" :
            if not self.do_action_requests() :
                return 0
        # parse
        if self.action["parse"] :
            if not self.do_parse() :
                return 0


    def do_action_requests(self) :
        # ----- Options ------- #
        # - headers
        for k,v in action["header"].items() :
            self.action["header"][k] = self.get_value(v)
        # - url
        for i in a["url"]:
            self.action["url"] = self.action["url"] + self.get_value(i)
        # - cookie
        cookie={}
        if 'cookie' in self.action["headers"]:
            self.action["cookies"] = self.action["headers"].pop('Cookie')
        # ------- Requests -------#
        # - get
        if self.action["type"] == 'get' :
            if not self.do_action_requests_get():
                return 0
        # - post
        elif self.action["type"] == 'post' :
            if not self.do_action_requests_post() :
                return 0


    def do_action_requests_post(self) :
        # payload
        for k,v in self.action["payload"].items() :
            self.action["payload"][k]=self.get_value(v)
        self.action["r"] = self.s.post(
            self.action["url"],
            headers=self.action["headers"],
            data=self.action["payload"],
            cookies=self.action["cookies"]
        )


    def do_action_requests_get(self) :
        self.action["r"] = self.s.get(
            self.action["url"],
            headers=self.action["headers"],
            cookies=self.action["cookies"]
        )


    def do_parse(self) :
        # parse
        if self.action["parse"] :
            self.action['soup'] = bs(self.action['r'].content,'html.parser')
        # get
        if "get" in self.action :
            for get_name in self.action["get"] :
                if not self.get(get_name):
                    print('Error:')
                    return 0


    def get(self,get_name) :
        get_value = None
        
        if get_name in self.GET :
            get_value = self.GET[get_name]

        elif get_name in self.domain_config["get"]
            get_arg_array = self.domain_config["get"][get_name][0]
            inter_value_name = get_arg_array[0]
            if isinstance(inter_value_name,list) :
                dictionary=self.get_value(inter_value_name)
                try:
                    key = get_arg_array[1]
                    get_value = dictionary[key]
                except KeyError:
                    
                    self.trigger(type=get_value, val=get_name)
                inter_value_name = inter_value_name[0]
                self.GET[inter_value_name] = get_value
            else :
                ele = self.domain_config["elements"][inter_value_name]
                attr=get_arg_array[1]
                tag = ele[0]
                clss = ele[1]
                val = ele[2]
                res = self.sp[0].find_all(tag,{clss:val})
                get_value = res[0][attr]
                self.GET[get_name] = get_value
        if not get_value :
            print('Error:')
            self.trigger(type=get_name, val=get_value)
        return get_value
        

    def get_value(self,arg) :
        value = None
        if isinstance(arg,list) :
            if len(arg) == 1 :
                arg = arg[0]
                if arg.isupper() :
                    value = self.get(arg)
                elif arg[0] == '_' :
                    
                    if arg[-1] == '_':
                        value = self.get_special(arg)
                    else :
                        value= self.VARS[arg[1:]]
        elif isinstance(arg,dict):
            value = arg
        else :
            value=str(value)
        return value


    def get_special(self,arg) :
        value = None
        if arg == '_cookies_' :
            value = self.s.cookies.get_dict(domain=self.domain_key)
        else:
            name = arg[1:-1]
            for action in self.actions :
                if action["name"] == name :
                    dictionary = json.loads(action["r"].text)
                    value = dictionary
        return value


    def trigger(self, type=None, **kwargs) :
        trgs = self.domain_config["triggers"]
        for trg in trgs:
            if trg["type"] == type :
                for k,v in trg["criteria"].items():
                    if kwargs[k] != v[k] :
                        break
                else :
                    continue
                self.do(trg["do"])
                self.triggered = True
                raise triggered()


    def do(self, dothese) :
        for dothis in dothese :
            this = dothis[0]
            if this == 'wfl' :
                wfl = dothis[1]
                self.wfl = wfl

    def get_nodes(self):
            e_head_title: [[head, title], [_text_]]
            e_dscr_raw: [div, class, formatted_description user_formatted]
            _AUTHOR_: [[e_head_title, [_text_], [till, by]]]
            _TITLE_: [[e_head_title, [_text_], [after, by] ]] 
            _DSCR_: [[e_dscr_raw, [1, p]]]
            _CONTENT_: [[]]

    def check_env (self, tgt_dir,bp) :
        # ARCHIVE
        # meta
        am,am_data = self.get_fileobj('meta.json',          tgt_dir, no_exist="make", bp_in=bp["archive_meta"],  clear=True )
        ac,ac_data = self.get_fileobj('config.yml',         tgt_dir, no_exist="make", bp_in=bp["archive_config"],           )
        dc,dc_data = self.get_fileobj('domains_config.yml', tgt_dir, no_exist="make", bp_in=domains_config,                 )
        al,al_data = self.get_fileobj('lists.json',         tgt_dir, no_exist="make", bp_in=bp["archive_lists"],  clear=True)
        # URLPATHS
        for up in self.iter_dir('archive', tgt_dir) :
            urlpath = self.get_urlpath_from_dir(up.name)
            al_data["domains"].append(url_obj.netloc)
            al_data["urlpaths"].append(urlpath)
            uc, uc_data = self.get_fileobj('config.yml', up.absolute(), no_exist="make",  bp_in=bp["urlpath_config"],           )
            um, um_data = self.get_fileobj('meta.json',  up.absolute(), no_exist="make",  bp_in=bp["urlpath_meta"],   clear=True)
            ul, ul_data = self.get_fileobj('lists.json', up.absolute(), no_exist="make",  bp_in=bp["urlpath_lists"],  clear=True)
            um_data["domain"] = url_obj.netloc
            um_data["urlpath"] = urlpath
            # STRTIMES
            for st in up.iter_dir() :
                if st.name not in ["config.yml", "meta.json", "lists.json"]:
                    ht, ht_data = self.get_fileobj(up.name + '.html', st.absolute())
                    sm, sm_data = self.get_fileobj("meta.json",       st.absolute())
                    ul_data["codes"].append(sm_data["code"])
                    am_data["size"]        = am_data["size"] + sm_data["size"]
                    am_data["total_files"] = am_data["total_files"] + 1
            m = self.re_io.match(str(um_data["domain"]))
            if ul_data["codes"][-1] != "200" :
                al_data["failed"].append(urlpath)
                if  um_data["domain"] == "archiveofourown.org" :
                    um_data["state"] = "deleted"
                else :
                    um_data["state"] = "error"
            elif  m:
                um_data["state"] = "unsatisfactory"
            else :
                um_data["state"] = "satisfactory"
            with um.open(mode="w+", encoding="utf-8") as outfile :
                json.dump(um_data,outfile)
            with ul.open(mode="w+", encoding="utf-8") as outfile :
                json.dump(ul_data,outfile)
        # Archive Post Processing
        # lists
        al_data["domains"]            = list(set(al_data["domains"]))
        with al.open(mode="w", encoding="utf-8") as outfile :
            json.dump(al_data,outfile)
        # meta
        #al_data["failed"].sort()
        am_data["failed"]    = len(al_data["failed"])
        am_data["total_url_paths"]    = len(al_data["urlpaths"])
        am_data["total_domains"]      = len(al_data["domains"])
        with am.open(mode="w", encoding="utf-8") as outfile :
            json.dump(am_data,outfile)



    def scrape_urls (self, tgt_dir) :
        self.import_pwds()
        self.import_urls()
        self.login()
        for url in urls :
            self.get_urlpath_from_dir()
            if self.url.netloc in [ 'git.io','raw.githubusercontent.com'] :
                continue
            if self.url_path.is_dir() :
                latest = self.get_latest_strtime_dir(self.url_path)
                if self.list_meta.content["code"] == "200" :
                    continue
            ## An authorised request.
            try :
                r = self.s.get(url, headers=self.archive_config.content["header"])
            except requests.exceptions.ConnectionError:
                
                self.meta.content["code"] = 666
                continue
            self.meta.content["code"] = r.status_code
            self.html.write()
            self.meta.write()

    def import_urls (self) :
        # Initialized return value as an empty list
        retu = []
        # Get file extension to dertermine if valid
        fext = self.path_to_urls.suffix
        # Supported file extensions
        if fext in [".txt", ".json"] :
            with open(self.path_to_urls, encoding="utf-8") as infile:
                # txt file
                if fext == ".txt":
                    for line in infile:
                        retu.append(line)
                # json file
                if fext == ".json":
                    json_dict = json.load(infile)
                    if "objs" in json_dict :
                        if "url" in json_dict["objs"] :
                            for obj in json_dict["objs"]["url"] :
                                retu.append(obj["val"])
                        else :
                            sys.exit("ERROR: json dict key(s) 'objs' does not exists at '" + path_to_urls + "'")
                    else :
                        sys.exit("ERROR: json dict key(s) 'objs.url' does not exists at '" + path_to_urls + "'")
        # Non supported file extension
        else :
            sys.exit("ERROR: '" + file_ext + "' is not a valid file extension at '" + path_to_urls + "'")
        return retu


    def get_urlpath_from_dir(self):
        #urlpath = url_obj.netloc+url_obj.path.replace("/","_")
        retu = self.urlpath.absolute().replace('__','/',1)
        retu = retu.replace('_','/')
        return retu
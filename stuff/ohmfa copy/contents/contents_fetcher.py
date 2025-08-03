""" contents_fetch.py
"""
import sys
import json
import copy
from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
from ohmfa.contents.contents_main import ContentsMain
from ohmfa.jobs.fetcher import Fetcher
from requests.exceptions import ConnectionError

#from requests_html import HTMLSession
#import re
#import time
#import requests

class ContentsFetcher(ContentsMain,Fetcher):
    """
    SYNTAX:
        VALUES:
            {ACTION_RESULT_KEY} %
            {STRING}            %
            {ATTR}              %
            ELEMENT_NAME        e_%
            ACTION_NAME         a_%
            SPECIAL_NAME        _%_
            VAR_NAME            _%
            GET_NAME            g_%
            ELEMENET            [{attr},{attr},{attr}]
        SINGLE VAR:
            $SPECIAL            [_%_]   
            $VAR                [_% ]   
            $GET                [g_%]  
        MULTI VAR
            $ACTION_VALUE   [ACTION_NAME, {ACTION_RESULT_KEY}]
            $VAR_CONCAT     [,($VAR / {STRING})] 
            $ELEMENT_VALUE  [ELEMENT_NAME, {ATTR}]

    CONFIG:
        GET
            - $ELEMENT_VALUE
            - $ACTION_VALUE
        ELEMENT (LIST)
            - ELEMENT
        ACTION (DICT)
            type:
                - {STR}
                    - post
                    - get
            method:
                - {STR}
                    - requests
                    - selenium
            parse:
                - {BOOL}
                    - True
                    - False
            get: (list)
                - GET_NAME
            payload: (DICT) 
                - $GET
            url:  
                - {STR}
                - $VAR_CONCAT
            header:
                Cookie:
                    - $SPECIAL
                User-Agent:
                    - {STR}
                    - $VAR_CONCAT
                Referer: 
                    - {STR}
                    - $VAR_CONCAT
                Host:      
                    - {STR}
                    - $VAR_CONCAT
                origin:
                    - {STR}
                    - $VAR_CONCAT
                Content-Length:
                    - {STR}
                        - 98
                        - 102
                DNT:
                    - {STR}
                        - 1
                Upgrade-Insecure-Requests:
                    - {STR}
                        - 1
                Accept-Encoding:
                    - {STR}
                        - gzip, deflate, br, zstd
                Accept-Language:
                    - {STR}
                        - 'en-US,en;q=0.5'
                Accept:
                    - {STR}
                        - '*/*'
                        - text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/png,image/svg+xml,*/*;q=0.8
                Connection:
                    - {STR}
                        - keep-alive
                Content-Type:
                    - {STR}
                        - application/x-www-form-urlencoded; charset=UTF-8
                Priority:
                    - {STR}
                        - u=4
                        - u=0
                        - u=0, i
                Sec-Fetch-Site:
                    - {STR}
                        - cross-site
                        - none
                        - same-origin
                Sec-Fetch-Dest:
                    - {STR}
                        - document
                        - empty
                        - iframe
                Sec-Fetch-Mode:
                    - {STR}
                        - navigate
                Sec-Fetch-User:
                    - {STR}
                        - '?1'
                X-Requested-With:
                    - {STR}
                        - XMLHttpRequest

    Args:
        BatchIter (_type_): _description_
        SinglePather (_type_): _description_

    Returns:
        _type_: _description_
    """


    url = None
    o = None
    domain_key = None
    wkfl_name = None
    wkfl = None
    action = None


    def __init__(self, **unconf):
        conf = {
            'read_only' : False,
            'session' : None,
            '_domain_configs' : {},
            '_login_pwds': {},
        }
        self.config.resolv_conf(conf,unconf)
        self.read_only      = conf['read_only']
        self.session        = conf['session']
        self.domain_configs = conf['_domain_configs']
        self.login_pwds     = conf['_login_pwds']

        self.actions = []
        self.domain_config = {}
        self.wkfl_vars = {}
        self.vars = {
            "url": None, 
            "ua": None, 
            "domain": None, 
        }


    def load_url(self, surl):
        self.actions=[]
        self.url = 'https://' + surl
        self.o = urlparse(self.url)
        self.get_domain_config()


    def load_wkfl(self, wkfl_name = None) :
        self.wkfl_name = wkfl_name
        if not wkfl_name :
            self.wkfl_name = 'default' 
        self.wkfl = copy.deepcopy(self.domain_config["workflows"][self.wkfl_name])


    def load_next_action(self):
        action_name = self.wkfl["do"].pop(0) :
        self.action = copy.deepcopy(self.domain_config["actions"][action_name])
        self.action['name'] = action_name
        self.actions.append(self.action)

        # ----- Config ------- #
        # - headers
        self.gen_header(self.action)
        for k,v in self.action["header"].items() :
            self.action["header"][k] = self.get_value(v)
        # - url
        self.action["url"] = self.get_value(self.action["url"])
        # - cookie
        if 'cookie' in self.action["headers"]:
            self.action["cookies"] = self.action["headers"].pop('Cookie')


    def do_action(self) :
        if self.action["method"] == "requests" :
            try 
            # ------- Requests -------#
            # - get
                if self.action["type"] == 'get' :
                    self.action["result"] = self.s.get(
                        self.action["url"],
                        headers=self.action["headers"],
                        cookies=self.action["cookies"]
                    )
                # - post
                elif self.action["type"] == 'post' :
                    for k,v in self.action["payload"].items() :
                        self.action["payload"][k]=self.get_value(v)
                    self.action["result"] = self.s.post(
                        self.action["url"],
                        headers=self.action["headers"],
                        cookies=self.action["cookies"]
                        data=self.action["payload"],
                    )

            except ConnectionError:
                self.trigger()

    def do_parse(self) :
        # parse
        if self.action["parse"] :
            # parse
            if self.action["parse"] :
                self.action['soup'] = bs(self.action['result'].content,'html.parser')
            # wkfl_vars
            if "wkfl_vars" in self.action :
                for wkfl_var_name in self.action["wkfl_vars"] :
                    self.get_wkfl_var(wkfl_var_name):




###################################################
# Utils
###################################################
    def gen_header(self, action):
        """_summary_

        Args:
            action (_type_): _description_
        """
        if action['pre_header']:
            key = action['pre_header']
            pre_header = copy.deepcopy(self.domains_config['headers'][key])
            action['header'] = action['header'] + pre_header


    def get_domain_config(self) :
        """_summary_
        """
        self.get_domain_key()
        if self.domain_key in self.domain_configs :
            self.domain_config = self.domain_configs[self.domain_key]
        else :
            sys.exit()


    def get_domain_key(self) :
        """_summary_
        """
        pos = self.o.netloc.index('.')
        self.domain_key = self.o.netloc[pos:]




############################################
# Value Methods
############################################
    def get_wkfl_var(self,wkfl_var_name) :
        wfkl_var_value = None
        
        #Already Have It
        if wkfl_var_name in self.wkfl_vars :
            wfkl_var_value = self.wkfl_vars[wkfl_var_name]

        #Don't Have it
        elif wkfl_var_name in self.domain_config["wkfl_vars"]:
            wkfl_args = self.domain_config["wkfl_vars"][wkfl_var_name]

            #ACTION_RESULT_VALUE
            wfkl_var_value = self.get_value(wkfl_args)
            self.wkfl_vars[wkfl_var_name] = wfkl_var_value

        if not wfkl_var_value :
            raise triggered(self, self.domain_config, type='a', val='a')

        return wfkl_var_value


    def get_value(self,arg) :
        value = None
        # VAR
        if isinstance(arg,list) :
            #Single
            if len(arg) == 1 :
                arg = arg[0]
                if arg[:1] == 'g_' :
                    value = self.get_wkfl_var(arg)
                elif arg[0] == '_' :
                    if arg[-1] == '_':
                        value = self.get_special(arg)
                    else :
                        value= self.vars[arg[1:]]
            # Multi
            else :
                #ACTION_RESULT_VALUE
                if arg[0][:1] == 'a_' :
                    value = self.value_from_action_result(arg[1:],arg[1])

                #ELEMENT_VALUE
                elif arg[0][:1] == 'e_' :
                    ele = self.domain_config["elements"][arg[0][0]]
                    attr = arg[0][1]
                    tag = ele[0]
                    clss = ele[1]
                    val = ele[2]
                    res = self.action['soup'].find_all(tag,{clss:val})
                    value = res[0][attr]

                #VAR_CONCAT_VALUE
                else:
                    value = ''
                    for part in arg:
                        value += str(self.get_value(part))
        # VALUE
        else :
            value=str(value)

        return value


    def get_special(self,arg) :
        """_summary_

        Args:
            arg (_type_): _description_

        Returns:
            _type_: _description_
        """
        value = None
        if arg == '_cookies_' :
            value = self.s.cookies.get_dict(domain=self.domain_key)
        return value


    def value_from_action_result(self,action_name,value_name):
        """_summary_

        Args:
            action_name (_type_): _description_
            value_name (_type_): _description_

        Returns:
            _type_: _description_
        """
        for action in self.actions:
            if action['name'] == action_name:
                dictionary = json.loads(action["result"].text)
                return dictionary[value_name]


            self.meta.data["code"] = 666
        self.meta.data["code"] = r.status_code



############################################
# Triggers
############################################
class Triggered(Exception):
    def __init__ (self, name:str, message:str)->None:
        super().__init__(message)
        self.name=name
    def trigger(self, obj, domain_config, type=None, **kwargs) :
        trgs = domain_config["triggers"]
        for trg in trgs:
            if trg["type"] == type :
                for k,v in trg["criteria"].items():
                    if kwargs[k] != v[k] :
                        break
                else :
                    continue
                self.do(trg["do"], obj)
                raise triggered()


    def do(self, dothese, obj) :
        for dothis in dothese :
            this = dothis[0]
            if this == 'wfl' :
                wfl = dothis[1]
                obj.wfl = wfl
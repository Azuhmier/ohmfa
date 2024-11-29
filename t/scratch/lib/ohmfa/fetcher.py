import os
import csv
import sys
import json
import time
import yaml

from lib.ohmfa.ohmfa_url import OhmfaUrl
from bs4 import BeautifulSoup

# ------- requests
import requests
# - Exceptions
from requests.exceptions import HTTPError
from requests.auth import HTTPBasicAuth

# ------- selenium
from selenium.webdriver.support.ui import WebDriverWait
# - Chrome
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
# - Exceptions
from selenium.common.exceptions import (WebDriverException,NoSuchWindowException)

# ------- seleniumbase
from seleniumbase import Driver

class Fetcher():
    s            = None
    s_url        = None
    s_fs_timeout = None
    def __init__(self, config_file, d_page_wait=20,):

        self.durls       = {}
        self.pwds        = {}
        self.fs_domains  = []
        self.cookie_jar  = {}
        self.crawl_db    = {}
        self.db_url      = {
            'tree': {},
            'values':{},
        }
        self.db_fetch    = {
            'tree': {},
            'values':{},
        }
        self.d_page_wait = d_page_wait

        with open(config_file, mode='r',encoding='utf-8' ) as infile:
            self.dspt = yaml.safe_load(infile)


    def start_session(self):

        # --------- request
        self.s            = requests.session()
        self.s_url        = "http://localhost:8191/v1"
        self.s_fs_timeout = 6000

        # --------- fs
        cmd     = "sessions.create"
        headers = {"Content-Type": "application/json"}
        fs_data = { "cmd": cmd}
        r=self.s.post(self.s_url, headers=headers, json=fs_data)
        response_data    = json.loads(r.content)
        status           = response_data["status"]

        r = self.s_fs('https://www.google.com')
        response_data    = json.loads(r.content)
        user_agent       = response_data["solution"]["userAgent"]

        # --------- driver
        self.d = Driver(
            agent=user_agent,
            browser="chrome",
            #devtools=True,
            do_not_track=True,
            headless=True,
            no_sandbox=True,
            uc=True,
            #uc_cdp_events=True,
            undetectable=True,
            #uc_subprocess=True,
            #version_main = 130,
            )
        self.d.set_page_load_timeout(self.d_page_wait)




    def delete_all_sessions(self):
        cmd     = "sessions.list"
        headers = {"Content-Type": "application/json"}
        fs_data = { "cmd": cmd}
        r = self.s.post(self.s_url, headers=headers, json=fs_data)
        fs_r_json     = json.loads(r.content)
        session_list = fs_r_json['sessions']
        for session_id in session_list:
            cmd     = "sessions.destroy"
            headers = {"Content-Type": "application/json"}
            fs_data = { "cmd": cmd,"session":session_id}
            r = self.s.post(self.s_url, headers=headers, json=fs_data)
            fs_r_json     = json.loads(r.content)
            status = fs_r_json['status']
            print(status)




    def fetch(self,u):
        fs_all = False
        url      = u.url.geturl()

        r  = None
        page_title    = None

        fs_used = False
        fs_page_title  = None
        fs_cookies     = None
        fs_user_agent  = None

        bad_page_titles = [
            'Reddit - Dive into anything',
            'Fiction.live',
        ]

        print(url)
        print(u.dmn)

        # ------- FlareSolverr
        if u.dmn not in self.fs_domains or fs_all:
            # - flags
            if not fs_all:
                self.fs_domains.append(u.dmn)
            fs_used = True
            # - fetch
            fs_r = self.s_fs(url)
            # - response
            fs_r_json     = json.loads(fs_r.content)
            fs_user_agent       = fs_r_json["solution"]["userAgent"]
            fs_cookies          = fs_r_json["solution"]["cookies"]
            fs_status           = fs_r_json["status"]
            fs_soup             = BeautifulSoup(fs_r.content,'html.parser')
            # - update driver
            fs_cookies = sorted(fs_cookies, key=lambda d: d['name'])
            self.d.execute_cdp_cmd('Network.enable',{})
            for fs_cookie in fs_cookies:
                fs_cookie.update({'domain': u.dmn})
                res = self.d.execute_cdp_cmd('Network.setCookie', fs_cookie)

            self.d.execute_cdp_cmd('Network.disable', {})
            # - page title check
            try:
                fs_page_title = fs_soup.head.title.text
                if not fs_page_title:
                    raise(AttributeError)
                elif page_title in bad_page_titles:
                    raise(AttributeError)
            except AttributeError: 
                print('        Bad fs_Title: ', fs_page_title)
            else:
                print('        fs_Title: ', fs_page_title)

        # -------- Driver
        # - fetch
        self.d.get(url)
        time.sleep(5)
        # - response
        cookies = self.d.get_cookies()
        cookies = sorted(cookies, key=lambda d: d['name'])
        user_agent = self.d.execute_script("return navigator.userAgent;")
        # page title check
        try :
            page_title = self.d.title
            if not page_title:
                raise(Exception)
            elif page_title in bad_page_titles:
                raise(Exception)
        except Exception:
            print('        Bad Page_Title: ', page_title)
        else:
            print('        Page_Title: ', self.d.title)

        # ------ diffs
        if fs_used:
            print('        Diff-----------')
        # - UA
            if fs_user_agent != user_agent:
                print('        UA: ',fs_user_agent)
        # - CKS
            cks_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            fs_cks_dict = {fs_cookie['name']: fs_cookie['value'] for fs_cookie in fs_cookies}
            uniq_cks    = list(set(cks_dict.keys()) - set(fs_cks_dict.keys()))
            for k in uniq_cks:
                print('            >',k)
            shared_cks  = list(set(cks_dict.keys()).intersection(fs_cks_dict.keys()))
            for k in shared_cks: 
                v = cks_dict[k]
                fs_v = fs_cks_dict[k]
                if v != fs_v:
                    print('            !',k)
            uniq_fs_cks = list(set(fs_cks_dict.keys()) - set(cks_dict.keys()))
            for k in uniq_fs_cks:
                print('            <',k)
        else:
            print('        Diff-----------')
            old_cks_dict = self.cookie_jar[u.dmn] 
            cks_dict = {cookie['name']: cookie['value'] for cookie in cookies}
            uniq_cks    = list(set(cks_dict.keys()) - set(old_cks_dict.keys()))
            for k in uniq_cks:
                print('            >',k)
            shared_cks  = list(set(cks_dict.keys()).intersection(old_cks_dict.keys()))
            for k in shared_cks: 
                v = cks_dict[k]
                old_v = old_cks_dict[k]
                if v != old_v:
                    print('            !',k)
            uniq_old_cks = list(set(old_cks_dict.keys()) - set(cks_dict.keys()))
            for k in uniq_old_cks:
                print('            <',k)
        if u.dmn not in self.cookie_jar:
            self.cookie_jar[u.dmn] = {}
        self.cookie_jar[u.dmn].update(cks_dict)

        # ------ actions
        print('        ACTIONS-----------')

        if u.fcnfg['params']['enabled']:
            wkfl = u.fcnfg['workflows']['w']
            for action in wkfl:
                u.actions.append([action,[]])
                print("            ",action)
                a = u.fcnfg['actions'][action]
                for do in a['do']:
                    res = self.do_action(do,u)
                    u.actions[-1][1].append([do,res])
                    print("               ",res," ",do)
        # ------ url vars
        print('        VARS-----------')
        return r





    def do_action(self,do,u): 
        retu = None
        res = None
        status = False
        arg_ar = None
        no_soup = False
        for arg in do:
            if arg[:2] == 'e_':
                arg_ar = u.fcnfg['elements'][arg]
                if not no_soup:
                    soup = BeautifulSoup(self.d.page_source,'html.parser')
                    retu, res, retu_type = self.eval_element(arg_ar,u,soup)
                    if not retu_type:
                        status=False
                    else:
                        status=True
                        if retu_type != 'list':
                            retu = retu[0]
            if arg[0] == '_':
                if arg[:6] == '_click':
                    if not no_soup:
                        selector = self.get_element_path(retu)
                    else:
                        selector = arg_ar[1]
                    wait_time = arg[7:-1]
                    if wait_time:
                        time.sleep(int(wait_time))
                    self.d.click(selector, by="css selector")
                if arg == '_exists':
                    retu = status
                if arg[:5] == '_wait':
                    wait_time = arg[6:-1]
                    if wait_time:
                        time.sleep(int(wait_time))
                if arg == '_len':
                    retu = len(res)
                if arg == '_no_soup':
                    no_soup=True
                if arg[:7] == '_skipif':
                    act = -1
                    nop=True
                    ele = arg[8:-1]
                    if ele[0] == '!':
                        ele=ele[1:]
                        nop=False
                    if ',' in ele:
                        act, ele = ele.split(',')
                    cond = u.actions[int(act)][1][int(ele)][1]
                    if not ( nop ^ cond ):
                        retu='skipped!'
                        return retu
        return retu




    def get_element_path(self, element):
        path = []
        while element.parent:
            parent = element.parent
            siblings = parent.find_all(element.name, recursive=False)
            index = siblings.index(element) + 1 if siblings else 1
            path.insert(0, f'{element.name}:nth-of-type({index})')
            element = parent
        return ' > '.join(path)




    def eval_element(self,arg_ar,u,given_soup):

        retu, res, retu_type = [[],[], None]
        tag, qtxt            = [None,None]
        where                = False
        tgts, tgt_params     = [[],[]]
        query, setty         = [{},{}]
        opts  = {
            '_css':    {'enabled':False, 'val':None, 'used':False},
            '_exists': {'enabled':False, 'val':None, 'used':False},
            '_for':    {'enabled':False, 'val':None, 'used':False},
            '_join':   {'enabled':False, 'val':None, 'used':False},
            '_in':     {'enabled':False, 'val':None, 'used':False},
            '_not':    {'enabled':False, 'val':None, 'used':False},
            '_slice':  {'enabled':False, 'val':None, 'used':False},
            '_hash':  {'enabled':False, 'val':None, 'used':False},
        }
        tgt_idx = -1

        for item in arg_ar:

            # arg_var tgt
            if isinstance(item,list):
                tgts.append(item)
                tgt_params.append([])
                tgt_idx+=1

            #css
            elif opts['_css']['enabled']:
                where=True
                tag=item
                opts['_css']['val']     = tag
                opts['_css']['enabled'] = False

            # attribs ops 
            elif '=' in item:
                key, value = item.split('=',1)

                # _var_=attr
                if key[0] == '_':
                    tgts.append(value)
                    tgt_params.append([])
                    tgt_idx+=1
                    setty[key] = value

                # attr=attr_value
                else:
                    if key == 'txt':
                        qtxt=value
                    else:
                        query.update({key: value})
            # ops
            elif item[0] == '_':
                if item == '_in':
                    opts[item]['enabled'], opts[item]['used'] = True,True

                elif item == '_for':
                    opts[item]['enabled'], opts[item]['used']=True,True

                elif item == '_css':
                    opts[item]['enabled'], opts[item]['used']=True,True

                elif item == '_hash':
                    opts[item]['enabled'], opts[item]['used']=True,True
                    opts[item]['val']=[]

                elif item == '_not':
                    opts[item]['enabled'], opts[item]['used']=True,True

                elif item == '_exists':
                    opts[item]['enabled'], opts[item]['used']=True,True

                elif item == '_split':
                    opts[item]['enabled'], opts[item]['used']=True,True

            # element
            elif item[:2] == 'e_':
                if opts['_in']['enabled']:
                    where=True
                    opts['_in']['val'] = item
                    opts['_in']['enabled'] =False
                else:
                    sys.exit('ERROR: _in is not enabled for ', item, ' in ',arg_ar)
            elif ':' in item:
                tgt_params[tgt_idx].append(['slice',item])

            # tag
            elif not where:
                tag = item
                where = True

            # tgt
            else:
                tgts.append(item)
                tgt_idx+=1
                tgt_params.append([])

        #------ pre soup
        # - _in
        if opts['_in']['used']: 
            ele_name = opts['_in']['val'] 
            if ele_name not in u.soups:
                ele = u.fcnfg['elements'][ele_name]
                given_soup = self.eval_element(ele,u,given_soup)[0]
                if not len(given_soup):
                    print('                ...bad given_batch',ele)
                    return [],[],None
                if isinstance(given_soup[0],list):
                    sys.exit("given_soup cant be list: ",ele_name)
            else:
                given_soup = u.soups[ele_name]


        # ----- get soup
        soup_batch = None
        # - CSS
        if opts['_css']['used']:
            selector = opts['_css']['val']
            soup_batch = given_soup.select(selector)
            if not len(soup_batch):
                print('                ...bad soup_batch',arg_ar)
                return [],[],None
        # - QUERY
        elif not opts['_in']['used']:
            if qtxt: 
                soup_batch = given_soup.find_all(tag, attrs=query, string=qtxt) 
                if not len(soup_batch):
                    print('                ...bad soup_batch',arg_ar)
                    return [],[],None
            else:
                soup_batch = given_soup.find_all(tag, attrs=query) 
                if not len(soup_batch):
                    print('                ...bad soup_batch',arg_ar)
                    return [],[],None
        else:
            soup_batch = [given_soup[0]]

        if not opts['_for']['used']:
            retu_type = 'scalar'
            soup_batch = [soup_batch[0]]
        else:
            retu_type = 'list'

        if isinstance(soup_batch[0],list):
            sys.exit("soup_batch items cant be list")

        # ----- get tgt
        for soup in soup_batch:
            if not opts['_hash']['used']:
                if not len(tgts):
                    retu.append(soup)
                else:
                    tgt = tgts[0]
                    if isinstance(tgt,list):
                        child_soup, child_res, child_soup_type = self.eval_element(tgt,u,soup)

                        if not len(child_soup):
                            print('                ...bad child_batch',tgt)
                            return [],[],None
                        if child_soup_type == 'list':
                            if isinstance(child_soup[0],list):
                                sys.exit('child soup list items cant be list :'+str(tgt))
                            if opts['_for']['used']:
                                sys.exit('only 1 list')
                            else:
                                if len(soup_batch) > 1:
                                    sys.exit('once again, only 1 list')
                                retu=child_soup
                                res=child_res
                                retu_type = list
                                break
                        else:
                            retu.append(child_soup[0])
                            if len(child_res):
                                res.append(child_res[0])
                    else:
                        tgt_param = tgt_params[0]
                        if tgt in ['text','txt']:
                            retu.append(soup)
                            res.append(soup.text)
                            for key in setty:
                                u.vrs[key] = soup.text
                        else:
                            sys.exit('only text')
            else:
                sys.exit('no hash')


        if len(retu):
            if isinstance(retu[0],list):
                print('tgts: '+str(tgts))
                sys.exit('retu elements cant be list: '+str(arg_ar))
        return retu, res, retu_type      





    def s_fs(self,url,post=False):
        r = None
        cmd     = "request.post" if post else "request.get"
        headers = {"Content-Type": "application/json"}
        fs_data = { 
                    "cmd": cmd, 
                    "url": url,
                    "waitInSeconds": 20,
                    "maxTimeout": 60000,
                    }
        try:
            r = self.s.post(self.s_url, headers=headers, json=fs_data)
        except Exception as err:
            exc_type, value, traceback = sys.exc_info()
            name = exc_type.__name__
            print(f"Other error occurred: {err}")
        return r





    def get_payload (self,d_config, pwds, domain) :
        usr = d_config["usr"]
        pwd = d_config["pwd"]
        payload = None
        if usr  is not None and pwd is not None :
            payload = {
                usr : pwds[domain]["usr"],
                pwd : pwds[domain]["pwd"],
            }
        return payload




    def get_token (self,d_config, r):
        soup  = BeautifulSoup( r.content, 'html.parser' )
        token = soup.find('input', attrs={'name': d_config["token"]})
        return token




    def login (self, dc_data, pwds, header ) :
        s = requests.Session()
        for domain in dc_data :
            d_config = dc_data[domain]
            payload = self.get_payload(d_config, pwds, domain)
            if payload is not None :
                r = s.get( d_config["login"], headers=header )
                if d_config["token"] is not None :
                    token = self.get_token(d_config, r)
                    if token is None:
                        sys.exit("ERROR: could not find `authenticity_token` on login form for '" + domain )
                    else :
                        payload.update(
                            { d_config["token"] : token.get('value').strip() }
                        )
                login_url = d_config["login"]
                s.post( login_url , data=payload, headers=header)
        return s




    def get_passwords(self, pwds_file):
        with open(pwds_file, mode='r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader( csv_file, delimiter=' ')
            line_count = 0
            for row in csv_reader :
                if line_count == 0:
                    reff = ['domain','usr','pwd']
                    line_count += 1
                    continue
                else:
                    line_count += 1
                    domain = row[0]
                    usr = row[1]
                    pwd = row[2]
                    self.pwds[domain] = {'usr':usr, 'pwd':pwd}




    def load_urls(self, urls, slds=[],verbose=0, mx=1,prnt=False):
        qc_batch = []
        for url in urls:
            u = OhmfaUrl(url,self.dspt,verbose,prnt)
            if len(slds) and not u.sld in slds:
                del u
                continue
            u.process()
            if u.sld not in self.durls:
                self.durls[u.sld]={}
            if u.node_type not in self.durls[u.sld]:
                self.durls[u.sld][u.node_type]={}
            if u.path_type not in self.durls[u.sld][u.node_type]:
                self.durls[u.sld][u.node_type][u.path_type]=[]
            self.durls[u.sld][u.node_type][u.path_type].append(u)
            if len(self.durls[u.sld][u.node_type][u.path_type]) < mx:
                qc_batch.append(u)
        for u in qc_batch:
            for line in u.log:
                print(line)




    def check_urls(self, slds=[],max=1):
        for sld, groups in self.durls.items():
            if not len(slds) or (sld in slds):
                for url_types in groups.values(): 
                    for us in url_types.values(): 
                        for idx, u in enumerate(us):
                            if idx > max:
                                break
                            self.fetch(u)

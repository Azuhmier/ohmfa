
import copy
import os
import requests
import scrapy
import csv
import sys
import time
import yaml
from bs4 import BeautifulSoup
from pathlib import Path
from socket import gethostbyname,gaierror
from urllib.parse import urlparse
from requests.exceptions import ConnectionError, Timeout, ConnectTimeout
from urllib3.exceptions import NewConnectionError
from http.client import RemoteDisconnected

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options




class Fetcher():
    """_summary_
    {property} = r.{property}

    in
    for
    where
    is

    V
        [e_*, attr]
        e_*
            [,in, 'url/soup']
        attr
            ['tag'>, *]
            [for, *]
            [where, *]


    """
    def __init__(self,config_file):
        self.pwds = {}

        #self.dspt = yaml.safe_load(config_file)

        # Selinium
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_binary_path = os.path.join('/usr/bin/google-chrome')
        chromedriver_path = os.path.join('/usr/bin/chromedriver')
        chrome_options.binary_location = chrome_binary_path
        service = Service(chromedriver_path)
        self.browser = webdriver.Chrome(service=service, options=chrome_options)

        # Requests
        self.s = requests.session()

        self.durls = {}
        self.sdspt={}
        self.timeout = 5
        self.substrings = [
            'itch.io',
            'catbox.moe',
            'literotica',
            'rentry', ]

        self.header = {
            'User-Agent':[],
            'Referer':[],
            'Host':[],      
            'origin':[],
            'Content-Length':[98,102],
            'DNT':[1],
            'Upgrade-Insecure-Requests':[1],
            'Accept-Encoding':[
                'gzip',
                'deflate',
                'br',
                'zstd'],
            'Accept-Language':[
                'en-US',
                'en',
                {
                    'q': [
                        0.5]}],
            'Accept':[
                '*/*',
                'text/html',
                'application/xhtml+xml'
                'application/xml',
                'image/avif',
                'image/webp',
                'image/png'
                'image/svg+xml',
                {
                    'q': [
                        0.8,0.9]}],
            'Connection':[
                'keep-alive' ],
            'Content-Type':[
                'application/x-www-form-urlencoded',
                {
                    'charset':[
                        'UTF-8']}],
            'Priority':[
                'u=4',
                'u=0',
                'i'],
            'Sec-Fetch-Site':[
                'cross-site',
                'none',
                'same-origin' ],
            'Sec-Fetch-Dest':[
                'document',
                'empty',
                'iframe' ],
            'Sec-Fetch-Mode':[
                'navigate'],
            'Sec-Fetch-User':[
                '?1' ],
            'X-Requested-With':[
                'XMLHttpRequest'],
        }
        self.dspt = {
            'archiveofourown.org':[{
                'login': {
                    'url':  'https://archiveofourown.org/users/login',
                    'pwd': 'pass',
                    'usr': 'name',
                    'tos': False,
                    'captcha': False,
                    'token': None},
                'dead':       False,
                'bin':        { '_series':['series','_series_uid_'] },
                'splash':{
                    '_series':['u_user','series','?page=','_iter_'],
                    '_work':['u_user','works','?page=','_iter_']},
                'user':{
                    '_user_alias':['user','_user_','pseuds','_alias_'],
                    '_user':['user','_user_']},
                'content':{
                    '_part':['works','_work_uid_','chapters','_part_uid_'],
                    '_work':['works','_work_uid_']}}],
            'docs.google.com':[{
                'dead':       False,
                'content':{
                    '_work_pub':['document','d','e','_work_uid_','pub'],
                    '_work_edit':['document','d','_work_uid_','edit'],
                    '_work':['document','d','_work_uid_']}}],
            'snekguy.com':[{
                'dead':       False,
                '_author_':   'snekguy',
                'path':       { '_group':['_group_']}, 
                'splash': {
                    '_work':['stories']}, 
                'content':{
                    '_work_edition': ['stories','p_group','_work_','_edition_'],
                    '_work': ['stories','p_group','_work_']}}], 
            'drive.google.com':[{
                'dead':       False,
                'content':    { 
                    '_work_view':['file','d','_work_uid_','view'],
                    '_work':['file','d','_work_uid_']}}],
            'mega.nz':[{
                'dead':       False,
                'path':       { '_folders':['folder','_folder_uid_']},
                'bin':        { '_work'   :['p_folders']},
                'content':    { '_work'   :['p_folders','file','_work_uid_']}}],
            'raw.githubusercontent.com':[{
                'dead':       False,
                'path':       { '_folders':['_folders_']},
                'bin':        { '_repo':['_user_','_repo_','_version_'] },
                'user':       { '_user':['_user_']},
                'content':    { 
                    'work_nofolers':['b_repo','_work_uid_'],
                    'work':['b_repo','p_folders','_work_uid_']}}],
            'www.reddit.com':[{
                'dead':       False,
                'bin':        { '_sub':['r','_sub_']},
                'user':       { '_user':['user','_user_']},
                'content':    { '_work':['b_sub','comments', '_work_uid_','_work_']}}],
            'blokfort.com':[{
                'dead':       False,
                'splash':     {'_works':['nsfw-comics']}, 
                'user':       {'_user':['Blokfort']},
                'content':    {'_work':['_work_']}}],
            'snootgame.xyz':[{
                'dead':       False,
                'specfic':    True,
                'flash':      { '_flash':[]},
                'splash':     { '_downloads':['en','download','.html']},
                'content':    { '_work':['en','bin','_work_uid_','.zip']}}],
            'itch.io':[{
                'dead':       False,
                'user':       { '_user':['_user_','._domain_']},
                'content':    { '_work':['u_user','_work_uid_']}}],
            'ghostbin.com':[{
                'dead':       True,
                'path':       { '_folder':['_folder_uid_']},
                'content':    {
                    '_work_nofolder':['_work_uid_'],
                    '_work':['p_folder','_work_uid_']}}],
            'hardbin.com':[{
                'dead':       True,
                'content':    { '_work':['ipfs','_work_uid_']}}],
            'pastefs.com':[{
                'dead':       False,
                'content':    { '_work':['pid','_work_uid_']}}],
            'pastes.psstaudio.com':[{
                'dead' :      False,
                'content':    { '_work':['post','_work_uid_']}}],
            'rentry':[{
                'dead':       False,
                'content':    { '_work':['_work_uid_']}}],
            'git.io':[{
                'dead':       False,
                'content':    { '_work':['_work_uid_']}}],
            'catbox.moe':[{
                'dead':       False,
                'bin':        { '_bin':['c','_bin_uid_']},
                'content':    { '_work':['files','._domain_','_work_uid_','._fext_']}}],
            'pastebin.com':[{
                'dead':       False,
                'user':       { '_user':['u','_user_']},
                'splash':     { '_work':['u_user']},
                'content':    { '_work':['_work_uid_']} }],
            'poneb.in':[{
                'dead':       False,
                'splash':     { '_work':['u_user']},
                'user':       { '_user':['u','_user_']},
                'content':    { '_work':['_work_uid_']}}],
            'mcstories.com':[{
                'dead':       False,
                'flash':      { '_work':['_work_','index','.html']},
                'splash':     { '_user':['users','index','.html']},
                'user':       { '_user':['users','_user_']},
                'content':    { '_work':['_work_','_work_','._fext_']}}],
            'fiction.live':[{
                'dead':       False,
                'user':       { '_user':['user','_user_']},
                'flash':      { '_flash':['stories','_work_','_work_uid_']},
                'content':    { '_part':['stories','_work_','_work_uid_','_part_','_part_uid_']}}],
            'literotica':[{
                'dead' :      False,
                'splash':     { '_work':['_user_','works','stories','all']},
                'user':       { '_user':['users','_user_']},
                'content':    {
                    '_page_none':['s','_work_'],
                    '_page':['s','_work_','?page=','page_']}}],
            'www.fanfiction.net':[{
                'dead' :      False,
                'user':       { '_user':['u','_user_uid_','_user_']},
                'content':    { '_part':['s','_work_uid_','_part_','_work_']}}],
            'www.furaffinity.net':[{
                'login': {
                    'url':  'https://www.furaffinity.net/login',
                    'pwd': 'pass',
                    'usr': 'name',
                    'tos': False,
                    'captcha': False,
                    'token': None},
                'dead' :      False,
                'splash':     { '_work':['gallery','_author_','iter_','\?']},
                'user':       { '_user':['user','_user_']},
                'content':    { '_work':['view','_work_uid_']}}],
            'www.sofurry.com':[{
                'login': {
                    'url': 'https://www.sofurry.com/user/login',
                    'pwd': 'LoginForm[sfLoginPassword]',
                    'usr': 'LoginForm[sfLoginUsername]',
                    'tos': False,
                    'captcha': False,
                    'token': None},
                'dead':       False,
                'bins':       { '_folder':['browse','folder','stories','?by=_user_uid_','?folder=_folder_uid_']},
                'splash':     { '*':['browse','user','stories','?uid=','_user_uid_','?stories-page=','_iter_']},
                'user':       { '_user':['_user_','._domain_']},
                'content':    { '_work':['view','_work_uid_']}}],
        }
        pppath = '/home/azuhmier/progs/ohmfa/t/scratch/lib/frameworks/domains_config.yml'
        with open(pppath,'w+',encoding='utf-8') as outfile:
            yaml.dump(self.dspt, outfile)


    def load_urls(self,urls,test=False):
        dspt = {
            'u':'user',
            'b':'bin',
            'c':'content',
            's':'splash',
            'f':'flash',
            'p':'path', }
        orders = [
            'content', 
            'bin',
            'splash',
            'flash',
            'user',
        ]


        def split_domain(domain,dot=False):
            num_dots = len(domain.split('.'))
            if num_dots >= 2:
                #res   = domain.split('.',1)
                res   = domain.split('.')
                res   = [x for x in res if x]
                xx = res.pop(0)
                nres = []
                for r in res:
                    nres.append('.')
                    nres.append(r)
                #nres[0:0] = ['.']
                if not dot:
                    nres[0:0] = [xx]
                res = nres
            else :
                res = ['.', domain]
            return res

        def expand_dpath(dpath,domain):
            expanded_dpath = []
            for dpart in dpath:
                try:
                    if dpart[0] == '.':
                        dpart     = dpart[1:]
                        if dpart == '_domain_':
                            dpart = split_domain(domain,dot=True)
                            expand_dpath.domain_used = True
                        else:
                            dpart = ['.', dpart]
                    elif len(dpart) > 1 and dpart[1] == '_':
                        var   = dpart[1:]
                        key   = dspt[dpart[0]]
                        try:
                            if key != 'path':
                                dpart = expand_dpath(self.sdspt[key][var],domain)
                            else:
                                dpart = [dpart]
                        except KeyError:
                            print('domain: ',domain)
                            print('dpart: ',dpart)
                            print('Key: ',key)
                            print('var: ',var)
                            sys.exit('259!!!')
                    else:
                        dpart = [dpart]
                except IndexError:
                    print('dpath: ',dpath)
                    print('domain: ',domain)
                    print('dpart: ',dpart)
                    sys.exit('266!!!')
                try:    
                    expanded_dpath = expanded_dpath+ dpart
                except TypeError:
                    print('dpath: ',dpath)
                    print('domain: ',domain)
                    print('dpart: ',dpart)
                    sys.exit('277!!!')
            return  expanded_dpath
        expand_dpath.domain_used = False


        for url in urls:
            _url = copy.deepcopy(url)
            dvars = {'_iter_':False}

            domain = url.netloc
            key    = domain
            for substring in self.substrings:
                if substring in key:
                    key = substring
                    break

            if key not in self.durls:
                self.durls[key]={}
            if domain not in self.durls[key]:
                self.durls[key][domain]={}

            patho = url.path.split('/')
            patho = [x for x in patho if x]
            patho[0:0] = split_domain(domain)
            _path = copy.deepcopy(patho)
            _dpaths = []

            match=False
            dkey = None
            _vars = []
            for order in orders:
                self.sdspt=self.dspt[key][0]
                if order not in self.sdspt:
                    continue
                dpaths = self.sdspt[order]
                for k,dpath in dpaths.items():

                    dpath = expand_dpath(dpath,domain)
                    if not expand_dpath.domain_used:
                        dpath[0:0] = split_domain(domain)
                    expand_dpath.domain_used = False
                    _dpaths.append(copy.deepcopy(dpath))

                    idx = -1
                    path_active = False

                    path = copy.deepcopy(patho)
                    npath = []
                    for p in path:
                        if len(p) > 1 and '.' in p:
                            res = p.split('.',1)
                            res = [x for x in res if x]
                            res[1:1] = ['.']
                            npath = npath + res
                        else:
                            npath.append(p)
                    path = npath
                    _npath = copy.deepcopy(npath)

                    path_idx = 0
                    path_var = None
                    pre_parts = []
                    while len(path):
                        match = False
                        idx += 1

                        if (idx+1) > len(dpath):
                            if path_active and idx >= path_idx:
                                dpath[path_idx:path_idx] = [path_var]
                                path = pre_parts[path_idx:] + path
                                idx = path_idx - 1
                                continue
                            else:
                                break
                        self.fromatify(_vars,[idx,copy.deepcopy(dpath),match,copy.deepcopy(path),path_active,path_idx])
                        part = path.pop(0)
                        pre_parts.append(part)
                        # _var_
                        try:
                            # path
                            if dpath[idx][:2] == 'p_':
                                path_var = copy.deepcopy(dpath[idx])
                                res = copy.deepcopy(self.sdspt['path'][dpath[idx][1:]])
                                _res = copy.deepcopy(res)
                                dpath[idx:(idx+1)] = res
                                path_idx = len(res) + idx
                                path_active=True

                            if dpath[idx][0] == '_':
                                dvars[dpath[idx]] = part
                            # match
                            elif part != dpath[idx]:
                                if path_active and idx >= path_idx:
                                    dpath[path_idx:path_idx] = [path_var]
                                    path = pre_parts[path_idx:] + path
                                    idx = path_idx - 1
                                    continue
                                else:
                                    break
                        except IndexError:
                            print('path',path)
                            print('dPath',dpath)
                            print('domain',domain)
                            print('domain',domain)
                            print('idx',idx)
                            sys.exit('344!!!')
                        match=True
                    
                    if match and (idx+1) == len(dpath):
                        match=True
                        dkey=k
                        break
                    else:
                        match = False
                if match:
                    break

            if dkey not in self.durls[key][domain]:
                self.durls[key][domain][dkey]=[]
                if test and ((not match) or 1):
                    print('=========================')
                    print(_url.geturl())
                    print(domain)
                    print('path',_path)
                    for _var in _vars:
                        if not _var[0]:
                            print('')
                        print("  ",_var[0],_var[1],_var[2],_var[3],_var[4],_var[5])
                    print(match)
                    print('')
            self.durls[key][domain][dkey].append(url)

    def fromatify(self,vars,arg):
        a_idx = arg[0]
        a_dpath = arg[1]
        a_match = arg[2]
        a_path = arg[3]
        a_path_idx = arg[4]
        a_path_active = arg[5]
        a_dpath[a_idx] = '<<' + a_dpath[a_idx] + '>>'
        a_path[0] = '<<' + a_path[0] + '>>'
        vars.append([a_idx,a_dpath,a_match,a_path,a_path_active,a_path_idx])


    def fetch(self,url,timeout=5,params={},headers={},wait=1):
        soup = None
        time.sleep(wait)
        try:
            r = self.s.get(url,timeout=timeout,params=params,headers=headers)
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

    def check_urls(self):
        """
        a b c p_path d e f
        
        """
        soups = []
        for key, domains in self.durls.items():
            for domain,dkeys in domains.items(): 
                print(domain)
                soups.append(self.fetch('https://'+domain))
                for dkey,urls in dkeys.items(): 
                    url = urls[0].geturl()
                    soups.append(self.fetch(url))
        soups = [x for x in soups if x]

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
        csv_reader = csv.reader( pwds_file)
        csv_list = [ tuple(row) for row in csv_reader ]
        columns = csv_list.pop(0)
        #for row in csv_list :
        #    key = row.pop(0)
        #    for idx,item in enumerate(row):
        #        pdata[key][columns[idx]] = item
        for row in csv_list :
            domain = row.pop(0)
            usr = row.pop(0)
            pwd = row.pop(0)
            self.pwds[domain] = {'usr':usr, 'pwd':pwd}



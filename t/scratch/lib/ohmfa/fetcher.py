import os
import csv
import sys
import time
import yaml

# -------- Requests
import requests
# -------- Selenium
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
# - Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
# - Exceptions
from selenium.common.exceptions import (WebDriverException,NoSuchWindowException)
# - Undetected Chrome
#import undetected_chromedriver as uc
# - Selenium Base
from seleniumbase import Driver

from lib.ohmfa.ohmfa_url import OhmfaUrl
from bs4 import BeautifulSoup

class Fetcher():
    def __init__(self,config_file):
        self.pwds = {}

        with open(config_file, mode='r',encoding='utf-8' ) as infile:
            self.dspt = yaml.safe_load(infile)

        # -------- driver
        chrome_options = Options()
        #chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_binary_path = os.path.join('/usr/bin/google-chrome')
        chromedriver_path = os.path.join('/usr/bin/chromedriver')
        chrome_options.binary_location = chrome_binary_path
        chrome_service = Service(chromedriver_path)

        self.driver = Driver(
            uc=True,
            #headless=True,
            agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36 AVG/112.0.21002.139",
            undetectable=True,
            do_not_track=True,
            no_sandbox=True,
            #devtools=True,
            #browser="chrome",
            uc_cdp_events=True,
            
            )
        #self.driver.set_page_load_timeout(5)
        #self.driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
        res=self.driver.execute_cdp_cmd('Page.enable', {})
        print(res)
        res=self.driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': """
        Element.prototype._as = Element.prototype.attachShadow;
        Element.prototype.attachShadow = function (params) {
        return this._as({mode: "open"})
        };
        """
        })
        print(res)
        #self.driver.execute_cdp_cmd('Network.enable', {})

        # Requests
        self.s = requests.session()

        self.durls = {}
        self.sdspt={}
        #self.timeout = 5


    def load_urls(self,urls, slds=[]):
        for url in urls:
            u = OhmfaUrl(url,self.dspt)
            if len(slds) and not u.sld in slds:
                del u
                continue
            u.process()
            if u.sld not in self.durls:
                self.durls[u.sld]={}
            if u.domain not in self.durls[u.sld]:
                self.durls[u.sld][u.domain]={}
            if u.bp_key not in self.durls[u.sld][u.domain]:
                self.durls[u.sld][u.domain][u.bp_key]=[]
            self.durls[u.sld][u.domain][u.bp_key].append(u)





    def fetch_request(self,url,timeout=5,params={},headers={},wait=1):
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
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout):
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

    def fetch_selenium(self,url,timeout=5,params={},headers={},wait=1,page_wait=2000):
        retu = {
            'current_url':None,
            'page_title':None,
            'response': None,
            'elapsed_time': None,
            'success': False,
            'status_code': None,
            'status_code_meaning': None,
            'error': {
                'name': None,
                'msg': None,
                'tldr': None,
            },
        }
        try:
            self.driver.uc_open(url)
            retu['current_url'] = self.driver.current_url
            retu['page_title']  = self.driver.title
            retu['response']    = self.driver.page_source
        except (WebDriverException, NoSuchWindowException):
            exc_type, value, traceback = sys.exc_info()
            name = exc_type.__name__
            retu['error']['name'] = name
            retu['error']['msg'] = value


        cur_url  = retu['current_url']
        title    = retu['page_title']
        code     = retu['status_code']
        success  = retu['success']
        err_name = retu['error']['name']
        err_value = retu['error']['msg']
        print('        CurURL:  ',cur_url)
        print('        Title:   ',title)
        print('        Code:    ',code)
        print('        Error:   ',err_name)
        #print('        Erval:   ',err_value)
        print('        Success: ',success)


        return retu


    def check_urls(self, oslds=[],no_domain=False):
        for slds, domains in self.durls.items():
            self.sdspt=self.dspt[slds]
            if not len(oslds) or (slds in oslds):
                for domain, url_types in domains.items(): 
                    print(domain)
                    print("    ",'https://'+domain)
                    if not no_domain:
                        retu = self.fetch_selenium('https://'+domain)

                    for urls in url_types.values(): 
                        u = urls[0]
                        print("    ",u.url.geturl())
                        print("        type: ",u.url_type)
                        retu = self.fetch_selenium(u.url.geturl())


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



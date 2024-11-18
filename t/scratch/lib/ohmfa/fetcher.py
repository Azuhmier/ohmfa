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
    def __init__(self,config_file):
        self.durls = {}
        self.sdspt={}
        self.pwds = {}

        with open(config_file, mode='r',encoding='utf-8' ) as infile:
            self.dspt = yaml.safe_load(infile)

        # -------- requests
        self.s = requests.session()

        # -------- selenium
        # - paths
        chrome_binary_path = os.path.join('/usr/bin/google-chrome')
        chromedriver_path  = os.path.join('/usr/bin/chromedriver')
        # - options
        options = webdriver.ChromeOptions()
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.binary_location = chrome_binary_path
        # - driver
        chrome_service = Service(chromedriver_path)
        self.s_driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

        # -------- seleniumBase
        # - driver
        self.sb_driver = Driver(
            uc=True,
            headless=True,
            agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36 AVG/112.0.21002.139",
            undetectable=True,
            do_not_track=True,
            no_sandbox=True,
            devtools=True,
            browser="chrome",
            uc_cdp_events=True,
            
            )
        # - options
        self.sb_driver.set_page_load_timeout(5)
        # - CDP
        self.sb_driver.execute_cdp_cmd('Page.enable', {})
        self.sb_driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': """
            Element.prototype._as = Element.prototype.attachShadow;
            Element.prototype.attachShadow = function (params) {
            return this._as({mode: "open"})
            }; """
        })
        self.sb_driver.execute_cdp_cmd('Network.enable', {})




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


    def fetch(self,url):
        codes = {
            200:'Success',
            410:'GONE',
            406:'Not Acceptable',
            404:'Not Found',
            504:'Success',
            403:'Forbidden',
        }

        # -------- Requests
        # - config
        rq_cookies = {cookie["name"]: cookie["value"] for cookie in original_cookies}
        self.s.cookies.update(rq_cookies)
        self.s.headers.update({"User-Agent": rq_user_agent})
        # - fetch
        try:
            rq_r = self.s.get(url)
        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.ConnectTimeout):
            rq_exc_type, rq_value, rq_traceback = sys.exc_info()
            rq_name = rq_exc_type.__name__
            rq_value = str(value)
            if rq_name == 'ConnectionError':
                if 'RemoteDisconnected' in rq_value:
                    rq_value = 'RemoteDisconnected'
                elif '[Errno -2]' in rq_value:
                    rq_value = 'Name or service not known'
                elif '[Errno -3]' in rq_value:
                    rq_value = 'Temporary failer in name resolution'
                elif '[Errno 113]' in rq_value:
                    rq_value = 'No route to host'
            elif rq_name == 'ConnectTimeout':
                if 'Max retries exceeded' in rq_value:
                    rq_value = 'Max retries exceeded'
            print("        ",url," ", rq_name," ",rq_value)
        # - response
        rq_resp = rq_r.content 
        rq_code = rq_r.status_code

        # -------- Selinium
        # - config
        # - fetch
        try:
            self.s_driver
        except (WebDriverException, NoSuchWindowException):
            s_exc_type, s_value, s_traceback = sys.exc_info()
            s_name = s_exc_type.__name__
        # - response
        s_url    = self.s_driver.current_url
        s_title  = self.s_driver.title
        s_resp   = self.s_driver.page_source
        
        # -------- SeliniumBase
        # - config
        # - fetch
        try:
            self.sb_driver.us_open(url)
        except (WebDriverException, NoSuchWindowException):
            sb_exc_type, sb_value, sb_traceback = sys.exc_info()
            sb_name = sb_exc_type.__name__
        # - response
        sb_url    = self.sb_driver.current_url
        sb_title  = self.sb_driver.title
        sb_resp   = self.sb_driver.page_source

        # -------- Flare_Solver
        # - config
        fs_url = "http://localhost:8191/v1"
        fs_headers = {"Content-Type": "application/json"}
        fs_data = {
            "cmd": "request.get",
            "url": fs_url,
            "maxTimeout": fs_timeout
        }
        # - fetch 
        try:
            fs_r = self.s.post(fs_url, headers=fs_headers, json=fs_data)
        except:
            pass
        # - response
        fs_soup = BeautifulSoup(fs_r.content,'html.parser')
        try:
            fs_title = fs_soup.head.title.text)
        except AttributeError:
            pass
        fs_js = json.loads(fs_r.content)
        original_cookies = fs_js["solution"]["cookies"]
        fs_ua = fs_js["solution"]["userAgent"]




    def fetchh(self,url):
        durl = "http://localhost:8191/v1"
        headers = {"Content-Type": "application/json"}
        data = {
            "cmd": "request.get",
            "url": url,
            "maxTimeout": 60000
        }
        r = self.s.post(durl, headers=headers, json=data)
        print("    ",r.status_code)


    def check_urls(self, oslds=[],no_domain=False):
        for slds, domains in self.durls.items():
            self.sdspt=self.dspt[slds]
            if not len(oslds) or (slds in oslds):
                for domain, url_types in domains.items(): 
                    print(domain)
                    print("    ",'https://'+domain)
                    if not no_domain:
                        self.fetch('https://'+domain)

                    for urls in url_types.values(): 
                        u = urls[0]
                        print("    ",u.url.geturl())
                        print("     type: ",u.url_type)
                        self.fetch(u.url.geturl())


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




import copy
import os
import requests
import scrapy
import csv
import sys
import time
import yaml

from lib.ohmfa.ohmfa_url import OhmfaUrl
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
    def __init__(self,config_file):
        self.pwds = {}

        with open(config_file, mode='r',encoding='utf-8' ) as infile:
            self.dspt = yaml.safe_load(infile)

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





    def fetch(self,url,timeout=5,params={},headers={},wait=1):
        soup = None
        time.sleep(wait)
        r = None
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
        return [r, soup]


    def check_urls(self, groups=[], raw=False):
        retu = []
        for group, domains in self.durls.items():
            self.sdspt=self.dspt[group]
            if not len(groups) or (group in groups):
                for domain, url_types in domains.items(): 
                    print(domain)
                    if raw:
                        retu.append(self.fetch('https://'+domain))
                    else:
                        self.browser.get('https://'+domain)
                        print('https://'+domain)
                        print("    ", self.browser.current_url)
                        print("    ", self.browser.title)
                    for url_type, urls in url_types.items(): 
                        url = urls[0]
                        if raw:
                            retu.append(self.fetch(url.geturl()))
                        else:
                            self.browser.get(url.geturl())
                            print(url_type)
                            print(url.geturl())
                            print("    ", self.browser.current_url)
                            print("    ", self.browser.title)
                    x = self.sdspt['_purl']['content']['_work']
        retu = [x for x in retu if x]
        return retu


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



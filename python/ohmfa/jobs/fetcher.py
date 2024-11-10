"""fetcher.py
"""



import sys
import requests
from bs4 import BeautifulSoup
from ohmfa.ohmfa import Ohmfa
from urllib.parse import urlparse
from ohmfa.utils.pather import Pather




class Fetcher(Ohmfa,Pather):
    # Iter Vars
    s      = None

    # Fetch Args
    psoup  = None 
    url    = None

    # Fetch Results
    r      = None
    content   = None
    soup   = None
    p      = None

    mode        = 'update'
    max_iter    = 0
    timeout     = 10
    wait        = 1
    

    def __init__(self):
        pass

    def start_session(self,**opts):
        self.s = requests.Session()

    def strip_scheme(self,url):
        parsed = urlparse(url)
        scheme = "%s://" % parsed.scheme
        return parsed.geturl().replace(scheme, '', 1)


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
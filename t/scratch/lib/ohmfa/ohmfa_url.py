"""_summary_
TODO
- only verbose on every uniq url structure like queries
- gen urls for testing
- put resl_path log into function

"""
import copy
import sys
import urllib
from urllib.parse import urlparse, parse_qs
from .url_processor import UrlProcessor
from .ohmfa import Ohmfa




class OhmfaUrl(Ohmfa):
    # domain
    dmn_type    = None
    hstn        = None
    tld         = None
    sld         = None


    node_type   = None

    path_type    = None

    uproc = None
    query  = None


    def __init__(self, url, sld_configs, verbose=0,prnt=0):
        self.url       = urlparse(url)
        self.dmn       = self.url.netloc
        self.log       = []
        self.verbose   = verbose
        self.prnt      = prnt

        # Determine sld
        domain_frags = self.dmn.split('.')
        self.sld = domain_frags[1]
        if len(domain_frags) == 2:
            self.sld = domain_frags[0]

        #get config
        self.cnfg  = sld_configs[self.sld]
        super().__init__(verbose,prnt)

    def process(self):
        self.logthis(1,'#'*80)
        self.logthis(1,f"url: {self.url.geturl()}")

        # domain
        self.uproc = UrlProcessor(self,self.verbose,self.prnt)
        self.uproc.resl_dmn()
        self.uproc.resl_path()

        self.logthis(1,f"dmn: {self.dmn}")
        self.logthis(1,f"sld: {self.sld}")
        self.logthis(1,f"bp:  {self.uproc.bp[0]}")
        self.logthis(1,f"ar:  {self.uproc.ar[0]}")
        self.logthis(1,f"ar:  {self.uproc.bp_hold}")

        #self.resl_query()
        #self.update_url()

"""_summary_
TODO
- only verbose on every uniq url structure like queries
- gen urls for testing
- put resl_path log into function

"""
import copy
import urllib
from urllib.parse import urlparse, parse_qs
from ohmfa.config_parser import (process_item)
from ohmfa.ohmfa import Ohmfa
from ohmfa.path_resolver import PathResolver
from ohmfa.path_resolver2 import PathResolver2




class OhmfaUrl(Ohmfa):
    # domain
    hstn        = None
    sld         = None
    tld         = None
    port        = None
    query       = None
    frag        = None
    cnfg        = None
    bp          = None
    ar          = None
    vrs         = None
    node_type  = None
    url_type   = None
    bp_type    = None

    def __init__(self, url):
        super().__init__()
        self.logger.debug(f"OhmfaUrl.__init__()")
        self.logger.debug(f"...url = {url}")
        self.url       = urlparse(url)
        self.pr = PathResolver2()
        self.ws = {}
        self.actions=[]
        dmn_frags = self.url.netloc.split('.')
        self.sld = dmn_frags[1]
        if len(dmn_frags) == 2:
            self.sld = dmn_frags[0]
        cnfgs  = [v for k,v in self.dcnfg.items() if k == self.sld]
        if len(cnfgs) > 0:
            for cnfg in cnfgs:
                if self.resl_dmn(dmn_frags, cnfg['dmns']):
                    self.cnfg = cnfg
                    if self.resl_path():
                        if self.resl_query():
                            self.update_url()
                        break
            self.pcnfg = self.dcnfg[self.sld]

    def resl_dmn(self, dmn_frags, dmn_cnfgs):
        self.logger.debug(f"OhmfaUrl.resl_dmn()")
        hstn, sld, tld   = None,None,None
        dmn_type         = None
        if len(dmn_frags) == 2:
            dmn_frags = [''] + dmn_frags
        hstn, sld, tld = dmn_frags
        for dmn_type, cnfg in dmn_cnfgs.items():
            if tld not in cnfg['tlds']:
                continue
            new_tld  = cnfg['tlds'][0]
            self.tld = new_tld 
            if not cnfg['hstn_var']:
                if hstn not in cnfg['hstns']:
                    continue
                new_hstn  = cnfg['hstns'][0]
                self.hstn = new_hstn
            else:
                self.hstn = hstn
            self.dmn_type = dmn_type
            break
        else:
            return False
        new_dmn_frags   = [self.hstn, self.sld, self.tld]
        new_dmn_frags   = [x for x in new_dmn_frags if x]
        self.dmn = '.'.join(new_dmn_frags)
        return True

    def resl_path(self): 
        self.logger.debug(f"OhmfaUrl.resl_path()")
        for node_type, node_cnfg in self.cnfg['nodes'].items():
            for url_type, url_cnfg in node_cnfg.items():
                bp_dmn_type = url_cnfg['domain_type']
                bp_cnfg = url_cnfg['bp_cnfg']
                if bp_dmn_type != self.dmn_type:
                    continue
                ar = [self.url.path]
                bp   = copy.deepcopy(bp_cnfg)
                if ar[0][-1] == '/':
                    if len(ar[0]) > 1:
                        ar[0] = ar[0][:-1]
                    else:
                        ar.pop(0)
                if len(ar): 
                    if ar[0][0] == '/':
                        if len(ar[0]) > 1:
                            ar[0] = ar[0][1:]
                        else:
                            ar.pop(0)
                res, bp, nar = self.pr.start_recursion(bp,ar)
                if res:
                    self.fcnfg = url_cnfg 
                    self.node_type  = node_type
                    self.url_type = url_type
                    self.bp  = bp
                    self.ar  = ar
                    break
            else:
                continue
            break
        else:
            return False
        return True

    def uid(self):
        a = self.cnfg["site_key"]

    def update_url(self):
        self.logger.debug(f"OhmfaUrl.update_url()")
        newquery = urllib.parse.urlencode(self.query,doseq=True)
        self.url = self.url._replace(query=newquery)
        self.url = self.url._replace(netloc=self.dmn)

    def resl_query(self):
        self.logger.debug(f"OhmfaUrl.resl_query()")
        ccfg = self.cnfg['nodes'][self.node_type][self.url_type]
        if 'query' in ccfg:
            query_bp  = self.cnfg['nodes'][self.node_type][self.url_type]['query']
            query     = self.url.query
            query     =  parse_qs(query)
            new_query = {}
            for k,v in query_bp.items():
                vrnm, item_type, arg_ar = process_item(v)
                if item_type not in ['bool', 'ltrl']: 
                    if k not in query:
                        if len(arg_ar[0]) == 3:
                            new_query[k] = arg_ar[0]['set']
                else :
                    new_query[k] = v
            self.query = new_query
            return True
        else: 
            self.query = {}
            return True
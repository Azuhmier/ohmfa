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
from ohmfa.url.processor import Processor
from ohmfa.ohmfa import Ohmfa
from ohmfa.url.path_resolver import PathResolver




class OhmfaUrl(Ohmfa):
    # domain
    hstn        = None
    sld         = None
    tld         = None
    port        = None
    query       = None
    frag        = None

    node_name  = None
    url_name   = None


    def __init__(self, url, verbose=0,prnt=0):
        super().__init__(verbose,prnt)
        self.url       = urlparse(url)
        self.pr = PathResolver(verbose=verbose,prnt=prnt)

        # Determine sld
        dmn_frags = self.url.netloc.split('.')
        self.sld = dmn_frags[1]
        if len(dmn_frags) == 2:
            self.sld = dmn_frags[0]

        # Resolve Domain
        cnfgs  = [v for k,v in self.dcnfg.items() if v['sld'] == self.sld]
        if len(cnfgs) > 0:
            for cnfg in cnfgs:
                if self.resl_dmn(dmn_frags, cnfg):
                    if self.resl_path():
                        if self.resl_query():
                            self.update_url()

    def resl_dmn(self, dmn_frags, dmn_cnfgs):
        hstn, sld, tld   = None,None,None
        dmn_type         = None

        # For domains that omit the hostname when it is 'www'
        if len(dmn_frags) == 2:
            dmn_frags = [''] + dmn_frags

        hstn, sld, tld = dmn_frags
        for dmn_type, cnfg in dmn_cnfgs.items():

            #TLD
            if tld not in cnfg['tlds']:
                continue

            # First tld in list is preffered
            new_tld  = cnfg['tlds'][0]
            self.tld = new_tld 

            #HSTN
            if not cnfg['hstn_var']:
                if hstn not in cnfg['hstns']:
                    continue
                # First hstnm in list is preffered
                new_hstn  = cnfg['hstns'][0]
                self.hstn = new_hstn
            else:
                self.hstn = hstn
            self.dmn_type = dmn_type
            break
        else:
            return False

        new_dmn_frags   = [self.u.hstn, self.u.sld, self.u.tld]
        new_dmn_frags   = [x for x in new_dmn_frags if x]
        self.cnfg = dmn_cnfgs
        return True



    def resl_path(self): 

        self._gen_path_bps()
        for node_type, nd_cnfg in self.cnfg['urls'].items():
            for path_type, url_cnfg in nd_cnfg.items():
                bp_cnfg     = url_cnfg['bp_cnfg']
                bp_dmn_type = url_cnfg['domain_type']
                if bp_dmn_type != self.dmn_type:
                    continue
                ar = [self.u.url.path]
                bp   = copy.deepcopy(bp_cnfg['bp'])
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
                res, bp, nar, nvrs = self.pr.start_recursion(bp,ar)
                if res:
                    self.vrs = nvrs
                    self.node_name  = node_type
                    self.url_name = path_type
                    break
            else:
                continue
            break
        else:
            return False
        return True


    def _gen_path_bps(self): 
        """_summary_
        """
        for node_type, node_cnfg in self.u.cnfg['urls'].items(): 
            for path_type, path_cnfg in node_cnfg.items():
                if isinstance(path_cnfg['bp_cnfg'],dict):
                    break
                path_bp = path_cnfg['bp_cnfg']
                query       = {}
                if len(path_bp) and isinstance(path_bp[-1],dict):
                    query   = path_bp[-1]
                    path_bp = path_bp[:-1]
                self.u.cnfg['urls'][node_type][path_type]['bp_cnfg'] = {
                    'bp':       path_bp,
                    'query':    query,
                    'cnfg':     path_cnfg,
                }
            else:
                continue
            break




    def _split_by_dot(self, arg):
        arg_items = arg.split('.')
        arg_ar = []
        for idx, item in enumerate(arg_items):
            if idx:
                arg_ar.append('.')
            arg_ar.append(item)
        arg_ar   = [x for x in arg_ar if x]
        return arg_ar
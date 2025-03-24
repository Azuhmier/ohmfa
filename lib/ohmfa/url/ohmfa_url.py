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
    cnfg        = None
    bp          = None
    ar          = None
    vrs         = None

    node_type  = None
    url_type   = None
    bp_type    = None


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
                if self.resl_dmn(dmn_frags, cnfg['dmns']):
                    self.cnfg = cnfg
                    if self.resl_path():
                        break
                        #if self.resl_query():
                            #self.update_url()
                            #break

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

        new_dmn_frags   = [self.hstn, self.sld, self.tld]
        new_dmn_frags   = [x for x in new_dmn_frags if x]
        return True



    def resl_path(self): 
        for node_type, node_cnfg in self.cnfg['nodes'].items():
            for url_type, url_cnfg in node_cnfg['urls'].items():
                for bp_type,bp_cnfg in url_cnfg["bps"].items():
                    bp_dmn_type = bp_cnfg['domain_type']
                    if bp_dmn_type != self.dmn_type:
                        continue
                    ar = [self.url.path]
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
                        self.node_type  = node_type
                        self.url_type = url_type
                        self.bp_type = bp_type
                        self.bp  = bp
                        self.ar  = ar
                        self.vrs = nvrs
                        break
                else:
                    continue
                break
            else:
                continue
            break
        else:
            return False
        return True

    def uid(self):

        a = self.cnfg["site_key"]
        print(f"{a}.{self.node_type}.{self.url_type}.{self.bp_type}")





    #def resl_query(self):
    #    self.logthis(1,f"{'':>4}>resl_query()")

    #    query_bp  = self.cnfg['urls'][self.u.node_type][self.u.path_type]['cnfg']['query']
    #    query     = self.u.url.query
    #    query     =  parse_qs(query)

    #    self.logthis(1,f"{'':>8}bp_query: {query_bp}")
    #    self.logthis(1,f"{'':>8}query: {query}")
    #    
    #    new_query = {}

    #    self.logthis(2,f"{'':>8}...resolving queries: {query}")
    #    for k,v in query_bp.items():
    #        self.logthis(2,f"{'':>8}?{k}={v}")
    #        vrnm, item_type, arg_ar = self.process_item(v)
    #        if vrnm: 
    #            self.logthis(2,f"{'':>12}bp value  '{v}' is var '{vrnm}'")
    #            #if 'subclass' in vr and vr['subclass'] == 'iter':
    #            if  vr['subclass'] == 'iter':
    #                start_iter=vr['val']
    #                self.logvar(12,vrnm,start_iter)
    #                self.set_vr(vr,start_iter)

    #            if k not in query:
    #                self.logthis(1,f"{'':>12}!Warning: bp key '{k}' is not in query")
    #                if vrnm not in self.vrs:
    #                    string = f"{'':>12}!ERROR: Bp var '{vrnm}' not in vrs"
    #                    sys.exit(string)
    #                self.logthis(2,f"{'':>12}Bp var    '{vrnm}' is in vrs")
    #                v = self.vrs[vrnm]['val']
    #                self.logthis(2,f"{'':>12}query key '{k}' created")
    #            else:
    #                self.logthis(2,f"{'':>12}bp key    '{k}' is in query")
    #                if vrnm in self.vrs:
    #                    self.logthis(2,f"{'':>12}bp var    '{vrnm}' is in vrs")
    #                    if query[k] != self.vrs[vrnm]['val']:
    #                        if vr['subclass'] == 'iter':
    #                            string = f"{'':>12}!WARNING: Query mismatch at '{k}' bp: '{self.vrs[vrnm]['val']}' url: '{query[k][0]}'"
    #                            self.logthis(1,string)
    #                        else:
    #                            string = f"{'':>12}!ERROR: Query mismatch at '{k}' bp: '{self.vrs[vrnm]['val']}' url: '{query[k][0]}'"
    #                            sys.exit(string)
    #                    else:
    #                        self.logthis(2,f"{'':>12}key '{k}' have identical values in both bp and query")
    #                else:
    #                    self.logthis(2,f"{'':>12}bp var    '{vrnm}' is not in vrs")
    #                    self.logvar(12,vrnm,query[k])
    #                    self.set_vr(vr,query[k])
    #                    v = query[k] 
    #        else:
    #            self.logthis(1,f"{'':>12}bp value  '{v}' is constant")
    #            if k not in query:
    #                self.logthis(1,f"{'':>12}!Warning: bp key '{k}' is not in query")
    #            self.logthis(2,f"{'':>12}query key '{k}' created")
    #        self.logthis(2,f"{'':>12}query key '{k}' value is now '{v}'")
    #        new_query[k] = v
    #    self.u.query = new_query
    #    self.logthis(1,f"{'':>8}new_query: {self.u.query}")
"""_summary_
"""
from urllib.parse import urlparse, parse_qs
from ohmfa.url.path_resolver import PathResolver
from ohmfa.ohmfa import Ohmfa
import sys
import copy


class Processor(Ohmfa):
    """_summary_

    Args:
        CnfgProcessor (_type_): _description_
    """
    vrs = None
    bp  = None
    ar  = None

    def __init__(self,u,verbose=0,prnt=0):
        """_summary_
        """
        super().__init__(verbose,prnt)
        self.u = u
        self.pr = PathResolver(verbose=verbose,prnt=prnt)


    def resl_dmn(self):
        """_summary_
        """
        self.logthis(2,f"{'':>4}>resl_dmn()")

        hstn, sld, tld   = None,None,None
        dmn_type         = None
        dmn_frags        = self.u.dmn.split('.')
        dmn_cnfgs        = self.u.cnfg['dmns']

        if len(dmn_frags) == 2:
            dmn_frags = [''] + dmn_frags

        self.logthis(2,f"{'':>8}dmn_frags:     ['{dmn_frags[0]}', '{dmn_frags[1]}', '{dmn_frags[2]}']")

        hstn, sld, tld = dmn_frags
        self.logthis(3,f"{'':>8}...looping through domain configs")

        for dmn_type, cnfg in dmn_cnfgs.items():
            self.logthis(3,f"{'':>8}dmn_type: {dmn_type}")

            #TLD
            self.logthis(3,f"{'':>12}...searching for tld '{tld}' in {cnfg['tlds']}")
            if tld not in cnfg['tlds']:

                self.logthis(3,f"{'':>12}!tld '{tld}' not found")
                self.logthis(3,f"{'':>12}continue")
                continue

            new_tld  = cnfg['tlds'][0]

            if new_tld != tld:
                self.logthis(1,f"{'':>12}tld changed from '{tld}' to '{new_tld}")

            self.u.tld = new_tld 

            #HSTN
            self.logthis(3,f"{'':>12}...searching for hstn '{hstn}' in {cnfg['hstns']}")
            if not cnfg['hstn_var']:

                if hstn not in cnfg['hstns']:

                    self.logthis(3,f"{'':>12}hstn '{hstn}' not found")
                    self.logthis(3,f"{'':>12}continue")
                    continue
                
                new_hstn  = cnfg['hstns'][0]
                if new_hstn != hstn:
                    self.logthis(1,f"{'':>12}hstn changed from '{hstn}' to '{new_hstn}")

                self.u.hstn = new_hstn

            else:
                self.u.hstn = hstn

            self.u.dmn_type = dmn_type
            self.logthis(3,f"{'':>8}SUCESS! at domain_type '{dmn_type}'")
            break

        else:
            self.dump()
            sys.exit('ERROR: Domain "',self.u.dmn,'" Could not Be Resoled!')

        new_dmn_frags   = [self.u.hstn, self.u.sld, self.u.tld]
        self.logthis(3,f"{'':>8}new_dmn_frags: {new_dmn_frags}")

        new_dmn_frags   = [x for x in new_dmn_frags if x]

        self.logthis(3,f"{'':>8}new_dmn_frags: {new_dmn_frags}")
        self.logthis(2,f"{'':>8}dmn_type:      {self.u.dmn_type}")


    def resl_path(self): 
        """_summary_

        Returns:
            _type_: _description_
        """

        self.logthis(2,f"{'':>4}>resl_path()")

        self._gen_path_bps()


        for node_type, nd_cnfg in self.u.cnfg['urls'].items():

            self.logthis(2,f"{'':>4}node_type: {node_type}")
            for path_type, url_cnfg in nd_cnfg.items():

                self.logthis(2,f"{'':>8}path_type: {path_type}")
                bp_cnfg     = url_cnfg['bp_cnfg']
                bp_dmn_type = url_cnfg['domain_type']

                if bp_dmn_type != self.u.dmn_type:

                    self.logthis(3,f"{'':>12}!dmn_type doesn't match bp's")

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
                self.logthis(2,f"{'':>16}ar: {ar}")
                self.logthis(2,f"{'':>16}bp: {bp}")
                res, bp, nar, nvrs = self.pr.start_recursion(bp,ar)
                self.log.extend(self.pr.log)
                self.logthis(2,f"{'':>16}{res}")

                
                if res:

                    self.vrs = nvrs
                    self.bp = bp
                    self.ar = nar
                    self.logthis(2,f"{'':>8}node_type:    {node_type}")
                    self.logthis(2,f"{'':>8}path_type:    {path_type}")
                    self.logthis(2,f"{'':>8}bp:           {bp}")
                    self.logthis(2,f"{'':>8}ar:           {nar}")

                    self.u.node_type  = node_type
                    self.u.path_type = path_type

                    break

            else:
                continue

            break

        else:
            self.dump()
            sys.exit('ERROR: Could not resolv url "'+str(self.u.url.geturl())+'"')


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


    def url_from_cnfg(self, group, path_type):
        cnfg = self.u.cnfg['urls'][group][path_type]['cnfg']
        url = self.url_from_bp(cnfg['bp'])
        return url


    def url_from_bp(self,url_bp):
        url_ar = []
        for item in url_bp:
            item = self.process_item(item)
            url_ar.append(item)
        url = ''.join(url_ar)
        return url


    def _gen_path_bps(self): 
        """_summary_
        """

        self.logthis(3,f"{'':>8}>gen_url_bp()")
        self.logthis(4,f"{'':>8}...generating bps")

        for node_type, node_cnfg in self.u.cnfg['urls'].items(): 
            for path_type, path_cnfg in node_cnfg.items():
                if isinstance(path_cnfg['bp_cnfg'],dict):
                    self.logthis(4,f"{'':>8}...alrady done!")
                    break

                path_bp = path_cnfg['bp_cnfg']

                self.logthis(4,f"{'':>12}node_type:  {node_type}")
                self.logthis(4,f"{'':>16}path_type:  {path_type}")

                query       = {}
                if len(path_bp) and isinstance(path_bp[-1],dict):
                    query   = path_bp[-1]
                    path_bp = path_bp[:-1]

                self.logthis(4,f"{'':>20}new_path_bp: {path_bp}")
                self.logthis(4,f"{'':>20}query:       {query}")

                self.u.cnfg['urls'][node_type][path_type]['bp_cnfg'] = {
                    'bp':       path_bp,
                    'query':    query,
                    'cnfg':     path_cnfg,
                }
            else:
                continue
            break



    def _process_ar(self,ar):

        new_ar = []
        ar = [x for x in ar if x]
        for idx, item in enumerate(ar):

            if len(item) > 1 and '.' in item:
                item = self._split_by_dot(item)

            if idx:
                new_ar.append('/')
            new_ar.append(item)
        return new_ar


    def _split_by_dot(self, arg):
        arg_items = arg.split('.')
        arg_ar = []
        for idx, item in enumerate(arg_items):
            if idx:
                arg_ar.append('.')
            arg_ar.append(item)
        arg_ar   = [x for x in arg_ar if x]
        return arg_ar
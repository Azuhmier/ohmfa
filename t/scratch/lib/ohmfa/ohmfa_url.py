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
import warnings




class OhmfaUrl():
    action_idx  = 0
    action      = None
    action_name = None
    wkfl_name   = None
    wkfl        = None

    ck_dmn      = None

    hstn        = None
    tld         = None
    group       = None
    dmn_type    = None
    url_type    = None
    dmn_ar      = None
    path_ar     = None
    ar          = None
    bp          = None
    query       = None




    def __init__(self, url, sld_configs, verbose=0,prnt=0):
        self.url       = urlparse(url)
        self.dmn       = self.url.netloc
        self.actions   = []
        self.log       = []
        self.soups     = {}
        self.node      = None
        self.vrs       = {}
        self.iters     = {}
        self.db_url    = {
            'tree': {},
            'values':{}
        }
        self.db_fetch    = {
            'tree': {},
            'values':{}
        }
        self.verbose   = verbose
        self.prnt     = print

        # Determine sld
        domain_frags = self.dmn.split('.')
        self.sld = domain_frags[1]
        if len(domain_frags) == 2:
            self.sld = domain_frags[0]

        #get config
        self.cnfg  = sld_configs[self.sld]




    def process(self):
        self.logthis(1,'#'*80)
        self.logthis(1,f"url: {self.url.geturl()}")
        self.logthis(1,f"dmn: {self.dmn}")
        self.logthis(1,f"sld: {self.sld}")

        # domain
        self.resl_dmn()
        self.gen_dmn_bps()
        self.gen_url_bps()
        self.resl_path()
        self.resl_query()
        self.update_url()




    def resl_query(self):
        self.logthis(1,f"{'':>4}>resl_query()")

        query_bp  = self.cnfg['urls'][self.group][self.url_type]['cnfg']['query']
        query     = self.url.query
        query     =  parse_qs(query)

        self.logthis(1,f"{'':>8}bp_query: {query_bp}")
        self.logthis(1,f"{'':>8}query: {query}")
        
        new_query = {}

        self.logthis(2,f"{'':>8}...resolving queries: {query}")
        for k,v in query_bp.items():
            self.logthis(2,f"{'':>8}?{k}={v}")
            vrnm, vr = self.get_vr(v)
            if vrnm: 
                self.logthis(2,f"{'':>12}bp value  '{v}' is var '{vrnm}'")
                #if 'subclass' in vr and vr['subclass'] == 'iter':
                if  vr['subclass'] == 'iter':
                    start_iter=vr['val']
                    self.logvar(12,vrnm,start_iter)
                    self.set_vr(vr,start_iter)

                if k not in query:
                    self.logthis(1,f"{'':>12}!Warning: bp key '{k}' is not in query")
                    if vrnm not in self.vrs:
                        string = f"{'':>12}!ERROR: Bp var '{vrnm}' not in vrs"
                        sys.exit(string)
                    self.logthis(2,f"{'':>12}Bp var    '{vrnm}' is in vrs")
                    v = self.vrs[vrnm]['val']
                    self.logthis(2,f"{'':>12}query key '{k}' created")
                else:
                    self.logthis(2,f"{'':>12}bp key    '{k}' is in query")
                    if vrnm in self.vrs:
                        self.logthis(2,f"{'':>12}bp var    '{vrnm}' is in vrs")
                        if query[k] != self.vrs[vrnm]['val']:
                            if vr['subclass'] == 'iter':
                                string = f"{'':>12}!WARNING: Query mismatch at '{k}' bp: '{self.vrs[vrnm]['val']}' url: '{query[k][0]}'"
                                self.logthis(1,string)
                            else:
                                string = f"{'':>12}!ERROR: Query mismatch at '{k}' bp: '{self.vrs[vrnm]['val']}' url: '{query[k][0]}'"
                                sys.exit(string)
                        else:
                            self.logthis(2,f"{'':>12}key '{k}' have identical values in both bp and query")
                    else:
                        self.logthis(2,f"{'':>12}bp var    '{vrnm}' is not in vrs")
                        self.logvar(12,vrnm,query[k])
                        self.set_vr(vr,query[k])
                        v = query[k] 
            else:
                self.logthis(1,f"{'':>12}bp value  '{v}' is constant")
                if k not in query:
                    self.logthis(1,f"{'':>12}!Warning: bp key '{k}' is not in query")
                self.logthis(2,f"{'':>12}query key '{k}' created")
            self.logthis(2,f"{'':>12}query key '{k}' value is now '{v}'")
            new_query[k] = v
        self.query = new_query
        self.logthis(1,f"{'':>8}new_query: {self.query}")




    def update_url(self):
        newquery = urllib.parse.urlencode(self.query,doseq=True)
        self.url = self.url._replace(query=newquery)
        self.url = self.url._replace(netloc=self.dmn)
        

    def resl_dmn(self):
        self.logthis(1,f"{'':>4}>resl_dmn()")
        hstn, sld, tld   = None,None,None
        dmn_type         = None
        dmn_frags        = self.dmn.split('.')
        dmn_cnfgs        = self.cnfg['dmns']
        if len(dmn_frags) == 2:
            dmn_frags = [''] + dmn_frags
        self.logthis(1,f"{'':>8}dmn_frags:     ['{dmn_frags[0]}', '{dmn_frags[1]}', '{dmn_frags[2]}']")
        hstn, sld, tld = dmn_frags
        self.logthis(2,f"{'':>8}...looping through domain configs")

        for dmn_type, cnfg in dmn_cnfgs.items():
            self.logthis(2,f"{'':>8}dmn_type: {dmn_type}")

            #TLD
            self.logthis(2,f"{'':>12}...searching for tld '{tld}' in {cnfg['tlds']}")
            if tld not in cnfg['tlds']:

                self.logthis(2,f"{'':>12}!tld '{tld}' not found")
                self.logthis(2,f"{'':>12}continue")
                continue

            new_tld  = cnfg['tlds'][0]

            if new_tld != tld:
                self.logthis(1,f"{'':>12}tld changed from '{tld}' to '{new_tld}")

            self.tld = new_tld 

            #HSTN
            self.logthis(2,f"{'':>12}...searching for hstn '{hstn}' in {cnfg['hstns']}")
            if not cnfg['hstn_var']:

                if hstn not in cnfg['hstns']:

                    self.logthis(2,f"{'':>12}hstn '{hstn}' not found")
                    self.logthis(2,f"{'':>12}continue")
                    continue
                
                new_hstn  = cnfg['hstns'][0]
                if new_hstn != hstn:
                    self.logthis(1,f"{'':>12}hstn changed from '{hstn}' to '{new_hstn}")

                self.hstn = new_hstn

            else:
                vrnm, vr  = self.get_vr(cnfg['hstn_var'])
                self.logthis(2,f"{'':>12}hstn in config is var '{vrnm}' ")

                self.logvar(12,vrnm,hstn) 
                self.set_vr(vr,hstn)
                self.hstn = hstn

            self.dmn_type = dmn_type
            self.logthis(2,f"{'':>8}SUCESS! at domain_type '{dmn_type}'")
            break
        else:
            sys.exit('ERROR: Domain "',self.dmn,'" Could not Be Resoled!')

        new_dmn_frags   = [self.hstn, self.sld, self.tld]
        self.logthis(2,f"{'':>8}new_dmn_frags: {new_dmn_frags}")
        new_dmn_frags   = [x for x in new_dmn_frags if x]
        self.dmn        = '.'.join(new_dmn_frags)
        self.dmn_ar     = self.split_by_dot(self.dmn) 
        self.logthis(2,f"{'':>8}new_dmn_frags: {new_dmn_frags}")
        self.logthis(1,f"{'':>8}dmn_type:      {self.dmn_type}")
        self.logthis(1,f"{'':>8}dmn:           {self.dmn}")
        self.logthis(1,f"{'':>8}dmn_ar:        {self.dmn_ar}")




    def resl_path(self): 
        self.logthis(1,f"{'':>4}>resl_path()")

        def _log(ind):
            log_str = copy.deepcopy(_m.bp)
            log_str2 = copy.deepcopy(_m.ar)
            if not ((_m.idx+1) > len(_m.bp)):
                log_str[_m.idx] = "<<"+log_str[_m.idx]+">>"
            if len(log_str2):
                log_str2[0] = "<<"+log_str2[0]+">>"
            self.logthis(2,f"{'':>{ind}}{log_str}{log_str2}")

        def _m(ar,  bp):
            self.logthis(2,f"{'':>20}>!_m()")

            _m.idx         = -1
            _m.ar          = ar
            _m.bp          = bp
            _m.pre_items   = []
            end_reached    = False
            vrs = {}

            def _r():
                is_r = False

                self.logthis(2,f"{'':>32}>>_r()")
                self.logthis(2,f"{'':>36}_r.active: {_r.active}")
                self.logthis(2,f"{'':>36}_r.end:    {_r.end}")
                self.logthis(2,f"{'':>36}_m.idx:    {_m.idx}")
                self.logthis(2,f"{'':>36}_m.val:    {_r.val}")

                if _r.active:

                    if _r.end == 0:

                        if _r.start >= (len(_m.bp)):
                            self.logthis(2,f"{'':>36}!_r.start '{_r.start}' exceeds bp_len '{len(_m.bp)}'")

                            _m.bp[_r.start:_r.start] = _r.val
                            self.logthis(2,f"{'':>36}...returning path val without '/'")

                            _log(32)

                        else:
                            self.logthis(2,f"{'':>36}!_r.start '{_r.start}' does exceeds bp_len '{len(_m.bp)}'")

                            _m.bp[_r.start:_r.start] = _r.val + ['/']
                            self.logthis(2,f"{'':>36}...returning path val without '/'")

                            _log(32)

                        _m.ar = _m.pre_items[_r.start:] + _m.ar
                        self.logthis(2,f"{'':>36}...returning pre_items")

                        _log(32)

                        del _m.pre_items[_r.start:]

                        self.logthis(2,f"{'':>36}...deincrementing idx")
                        self.logthis(2,f"{'':>36}old_idx {_m.idx}")

                        _m.idx = _r.start - 1
                        self.logthis(2,f"{'':>36}new_idx {_m.idx}")

                        _log(32)

                        _r.end = len(_r.val) + _m.idx
                        self.logthis(2,f"{'':>36}_r.end {_r.end}")

                        _m.is_r = True
                        is_r = True

                    elif _m.idx >= _r.end:

                        if _r.end >= (len(_m.bp)):
                            self.logthis(2,f"{'':>36}!_r.end '{_r.end}' exceeds bp_len '{len(_m.bp)}'")

                            _m.bp[_r.end:_r.end] = _r.val
                            self.logthis(2,f"{'':>36}...returning path val without '/'")

                            _log(32)


                        else:
                            self.logthis(2,f"{'':>36}!_r.end '{_r.end}' does not exceeds bp_len '{len(_m.bp)}'")
                            _m.bp[_r.end:_r.end] = _r.val + ['/']
                            _log(32)


                        _m.ar = _m.pre_items[_r.end:] + _m.ar
                        self.logthis(2,f"{'':>36}...returning pre_items")
                        _log(32)


                        del _m.pre_items[_r.start:]

                        self.logthis(2,f"{'':>36}...deincrementing idx")
                        self.logthis(2,f"{'':>36}old_idx {_m.idx}")
                        _m.idx = _r.end - 1

                        self.logthis(2,f"{'':>36}new_idx {_m.idx}")

                        _log(32)

                        is_r = True
                #if is_r:
                    #self.logthis('_r<<<<',_m.idx,len(_m.bp),_r.start,_r.end,_r.active,_m.bp,_m.ar)
                return is_r

            ### _m() ##################################
            _r.val    = None
            _r.start  = 0
            _r.end    = 0
            _r.active = False

            self.logthis(2,f"{'':>24}idx:         {_m.idx}")
            self.logthis(2,f"{'':>24}pre_items:   {_m.pre_items}")
            self.logthis(2,f"{'':>24}end_reached: {end_reached}")
            self.logthis(2,f"{'':>24}_r.val:      {_r.val}")
            self.logthis(2,f"{'':>24}_r.start:    {_r.start}")
            self.logthis(2,f"{'':>24}_r.end:      {_r.end}")
            self.logthis(2,f"{'':>24}_r.active:   {_r.active}")
            self.logthis(2,f"{'':>24}...starting matching")
            idd = 0
            while len(_m.ar):
                idd += 1
                #if(idd > 15):
                #    sys.exit('ERROR')
                _m.idx += 1
                end_reached = False

                self.logthis(2,f"{'':>28}idx: {_m.idx}")
                self.logthis(2,f"{'':>32}pre_items: {_m.pre_items}")

                _log(28)

                #bp array exhausted
                if (_m.idx+1) > len(_m.bp):
                    self.logthis(2,f"{'':>32}!idx_len '{_m.idx+1}' exceeds bp_len '{len(_m.bp)}'")
                    if _r():
                        self.logthis(2,f"{'':>32}continue'")
                        continue
                    self.logthis(2,f"{'':>32}break'")
                    break
                item      = _m.ar.pop(0)
                bp_item   = _m.bp[_m.idx]
                self.logthis(2,f"{'':>32}bp_item: '{bp_item}' item: '{item}'")
                _m.pre_items.append(item)

                if bp_item[:2] == 'p_':
                    self.logthis(2,f"{'':>32}!path_var")

                    _r.start               = _m.idx
                    _r.active              = True

                    _r.val                 = self.cnfg['urec'][bp_item]
                    self.logthis(2,f"{'':>32}_r.val:    {_r.val}")

                    _r.val                 = self.process_ar(_r.val)
                    _m.bp.pop(_m.idx)

                    self.logthis(2,f"{'':>32}_r.val:    {_r.val}")
                    self.logthis(2,f"{'':>32}_r.active: {_r.active}")
                    self.logthis(2,f"{'':>32}_r.start:  {_r.start}")
                    self.logthis(2,f"{'':>32}...poping bp at {_m.idx}")

                    _log(28)
                    if (_m.idx+1) > len(_m.bp):
                        self.logthis(2,f"{'':>32}!idx_len '{_m.idx+1}' exceeds bp_len '{len(_m.bp)}'")

                        if _r():

                            self.logthis(2,f"{'':>32}continue")
                            continue

                        self.logthis(2,f"{'':>32}break")
                        break

                    else:

                        if _m.bp[_m.idx] == '/':

                            _m.bp.pop(_m.idx)
                            self.logthis(2,f"{'':>32}...poping bp at {_m.idx}")
                            _log(28)

                        bp_item  = _m.bp[_m.idx]
                        self.logthis(2,f"{'':>32}!new_bp_item: {bp_item}")

                vrnm, vr = self.get_vr(bp_item)

                if vrnm:
                    del vr['name']
                    vr['val'] = item
                    vrs[vrnm] = vr
                    self.logthis(2,f"{'':>32}!bp_item is var - {vrnm}: {item}")

                elif item != bp_item:
                    if _r():

                        self.logthis(2,f"{'':>32}continue")
                        continue

                    self.logthis(2,f"{'':>32}break")
                    break

                end_reached=True
                self.logthis(2,f"{'':>32}!end_reached")
            self.logthis(2,f"{'':>28}end_reached: {end_reached}")
            suc = False
            if not (end_reached and (_m.idx+1) == len(_m.bp)):
                self.logthis(2,f"{'':>28}!idx_len '{_m.idx+1}' is not equal '{len(_m.bp)}'")
                vrs = {}
            else:
                self.logthis(2,f"{'':>28}!idx_len '{_m.idx+1}' is equal '{len(_m.bp)}'")
                self.logthis(2,f"{'':>24}RESOLUTION FOUND!")
                suc = True
            return suc, vrs

        ### .resl_path() ##################################
        url_groups = [
            '_content',
            '_flash',
            '_bin',
            '_listing',
            '_usr',
            '_misc',
        ]

        self.logthis(2,f"{'':>8}...starting url resolving")
        for group in url_groups:
            self.logthis(2,f"{'':>12}group: {group}")
            if group not in self.cnfg['urls']:
                self.logthis(2,f"{'':>12}!not found in ucnfg")
                continue
            url_cnfgs = self.cnfg['urls'][group]
            for url_type, cnfg in url_cnfgs.items():
                cnfg = cnfg['cnfg']
                self.logthis(2,f"{'':>16}url_type: {url_type}")
                self.logthis(2,f"{'':>20}dmn_type:      {self.dmn_type}")
                self.logthis(2,f"{'':>20}cnfg_dmn_type: {cnfg['dmn_type']}")
                if cnfg['dmn_type'] != self.dmn_type:
                    self.logthis(2,f"{'':>20}!dmn_type doesn't match cnfgs")
                    continue
                path_ar = self.process_ar(self.url.path.split('/'))
                ar0 = self.dmn_ar + ['/'] + path_ar
                ar = copy.deepcopy(ar0)
                bp = copy.deepcopy(cnfg['bp'])

                self.logthis(2,f"{'':>20}path_ar:       {path_ar}")
                self.logthis(2,f"{'':>20}ar0:           {ar0}")
                self.logthis(2,f"{'':>20}ar:            {ar}")
                self.logthis(2,f"{'':>20}bp:            {bp}")

                suc, vrs = _m(ar, bp)
                if suc:

                    self.logthis(1,f"{'':>8}group:    {group}")
                    self.logthis(1,f"{'':>8}url_type: {url_type}")
                    self.logthis(1,f"{'':>8}bp:       {bp}")
                    self.logthis(1,f"{'':>8}ar:       {ar0}")
                    self.logthis(2,f"{'':>8}path_ar:  {path_ar}")

                    self.group    = group
                    self.url_type = url_type
                    self.ar       = ar0
                    self.path_ar  = path_ar
                    self.bp       = bp
                    for k,v in vrs.items():
                        val = v['val']
                        self.logvar(8,k,val)
                    self.vrs.update(vrs)

                    break
            else:
                continue
            break
        else:
            #self.dump()
            sys.exit('ERROR: Could not resolv url "'+str(self.url.geturl())+'"')





    def process_item(self, item):
        retu = None
        vrnm = self.get_vr(item)[0]
        if vrnm in self.vrs:
            retu = self.vrs[vrnm]['val']
        else:
            retu = item
        return retu



    def url_from_cnfg(self, group, url_type):
        cnfg = self.cnfg['urls'][group][url_type]['cnfg']
        url = self.url_from_bp(cnfg['bp'])
        return url




    def url_from_bp(self,url_bp):
        url_ar = []
        for item in url_bp:
            item = self.process_item(item)
            url_ar.append(item)
        url = ''.join(url_ar)
        return url




    def gen_dmn_bps(self):
        self.logthis(2,f"{'':>4}>gen_dmn_bps()")
        dmn_cnfgs = self.cnfg['dmns']
        if 'bp' not in dmn_cnfgs['d']:
            self.logthis(2,f"{'':>8}...generating bps")
            for dmn_type, cnfg in dmn_cnfgs.items():
                #TLD
                tld = cnfg['tlds'][0]
        
                #HSTN
                if not cnfg['hstn_var']:
                    hstn = cnfg['hstns'][0]
                else:
                    hstn = cnfg['hstn_var']

                self.logthis(2,f"{'':>12}dmn_type:     '{dmn_type}'")
                self.logthis(2,f"{'':>12}tld:          '{tld}'")
                self.logthis(2,f"{'':>12}hstn:         '{hstn}'")
        
                dmn_bp_frags   = [hstn, self.sld, tld]
                self.logthis(2,f"{'':>12}dmn_bp_frags: {dmn_bp_frags}")
                dmn_bp_frags   = [x for x in dmn_bp_frags if x]
                dmn_bp_str     = '.'.join(dmn_bp_frags)
                dmn_bp         = self.split_by_dot(dmn_bp_str)
                cnfg['bp'] = dmn_bp

                self.logthis(2,f"{'':>12}dmn_bp_frags: {dmn_bp_frags}")
                self.logthis(2,f"{'':>12}dmn_bp_str:   {dmn_bp_str}")
                self.logthis(2,f"{'':>12}dmn_bp:       {dmn_bp}")
        else:
            self.logthis(2,f"{'':>8}Already Done!")




    def gen_url_bps(self): 
        self.logthis(2,f"{'':>4}>gen_url_bp()")
        self.logthis(2,f"{'':>8}...generating bps")
        for group in self.cnfg['urls']: 
            for url_type, cnfg in self.cnfg['urls'][group].items():
                cnfg = cnfg['cnfg']
                if isinstance(cnfg,dict):
                    self.logthis(2,f"{'':>8}Already Done!")
                    break
                dmn_type    = cnfg[0]
                url_bp      = cnfg[1:]
                query       = {}


                if len(url_bp) and isinstance(url_bp[-1],dict):
                    query=url_bp[-1]
                    url_bp = url_bp[:-1]

                self.logthis(2,f"{'':>12}group:      {group}")
                self.logthis(2,f"{'':>16}url_type:   {url_type}")
                self.logthis(2,f"{'':>20}dmn_type:   {dmn_type}")
                self.logthis(2,f"{'':>20}url_bp:     {url_bp}")
                self.logthis(2,f"{'':>20}query:      {query}")

                new_url_bp = self.process_ar(url_bp)
                domain_bp = self.cnfg['dmns'][dmn_type]['bp']
                self.logthis(2,f"{'':>20}new_url_bp: {new_url_bp}")
                self.logthis(2,f"{'':>20}domain_bp:  {domain_bp}")
                new_url_bp = domain_bp + ['/'] + new_url_bp
                self.logthis(2,f"{'':>20}new_url_bp: {new_url_bp}")
                self.cnfg['urls'][group][url_type]['cnfg'] = {
                    'bp':       new_url_bp,
                    'query':    query,
                    'dmn_type': dmn_type,
                    'cnfg':     cnfg,
                }
            else:
                continue
            break




    def process_ar(self,ar):
        new_ar = []
        ar = [x for x in ar if x]
        for idx, item in enumerate(ar):
            if len(item) > 1 and '.' in item:
                item = self.split_by_dot(item)
            else:
                item = [item]
            if idx:
                new_ar = new_ar + ['/'] + item
            else:
                new_ar = new_ar + item
        return new_ar




    def split_by_dot(self, arg):
        arg_items = arg.split('.')
        arg_ar = []
        for idx, item in enumerate(arg_items):
            if idx:
                arg_ar.append('.')
            arg_ar.append(item)
        arg_ar   = [x for x in arg_ar if x]
        return arg_ar




    def get_vr(self, string):
        vrnm = None
        var = {}

        if isinstance(string,str):
            if string[0] == '_' and string[-1] == '_':
                vrnm = string[1:-1]
                if not vrnm:
                    sys.exit('ERROR: Varible Name but be of nonzero length "'+string+'"')
                else:
                    if vrnm[-1] == ')':
                        z        = vrnm.find('(')
                        arg      = vrnm[(z+1):-1]
                        vrnm     = vrnm[:z]
                        arg_ar   = arg.split(';')
                        if arg_ar[0] in ['node','parent','child','attr']:
                            var['class']     = 'tree'
                            var['subclass'] = arg_ar[0]
                            var['node_type'] = arg_ar[1]
                            if arg_ar[0] == 'node':
                                var['type']      = arg_ar[0]
                            else:
                                var['type']      = arg_ar[2]
                        else:
                            var['class'] = arg_ar[0]
                            var['subclass'] = arg_ar[1]
                            var['val'] = arg_ar[2]
                        var['name'] = vrnm
                        var['val']  = None
        return vrnm, var









    def logthis(self,lvl,string):
        if self.verbose >= lvl:
            self.log.append(string)
            if self.prnt :
                print(string)

    def dump(self):
        for line in self.log:
            print(line)

    def logvar(self,ind,name,value,ind2=0):
                
                if name not in self.vrs:
                    self.logthis(1,f"{'':>{ind}}_{name}_: '{value}'")
                else: 
                    self.logthis(1,f"{'':>{ind}}_{name}_: '{self.vrs[name]}' -> '{value}'")
    
    def set_vr(self, vr:dict, val):
        vrnm = vr['name']
        del vr['name']
        vr['val']=val
        self.vrs[vrnm] = vr

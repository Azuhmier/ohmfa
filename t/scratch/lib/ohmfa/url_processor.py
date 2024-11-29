"""_summary_
"""
from .cnfg_processor import CnfgProcessor
from urllib.parse import urlparse, parse_qs
import sys
import copy


class UrlProcessor(CnfgProcessor):
    """_summary_

    Args:
        CnfgProcessor (_type_): _description_
    """
    idx      = None
    bp       = None
    ar       = None
    arbf     = None
    r_e      = None
    r_active = None
    r_val    = None
    item     = None
    bp_item  = None

    def __init__(self,u,verbose=0,prnt=0):
        """_summary_
        """
        super().__init__(u.cnfg,verbose,prnt)
        self.u = u


    def gen_dmn_bps(self):
        self.logthis(3,f"{'':>4}>gen_dmn_bps()")


        if 'bp' not in self.cnfg['dmns']['d']:

            self.logthis(3,f"{'':>8}...generating bps")

            for dmn_type, cnfg in self.cnfg['dmns'].items():

                #TLD
                tld = cnfg['tlds'][0]

                #HSTN
                if not cnfg['hstn_var']:
                    hstn = cnfg['hstns'][0]

                else:
                    hstn = cnfg['hstn_var']

                self.logthis(3,f"{'':>12}dmn_type:     '{dmn_type}'")
                self.logthis(3,f"{'':>12}tld:          '{tld}'")
                self.logthis(3,f"{'':>12}hstn:         '{hstn}'")
        
                dmn_bp_frags   = [hstn, self.u.sld, tld]
                self.logthis(3,f"{'':>12}dmn_bp_frags: {dmn_bp_frags}")

                dmn_bp_frags   = [x for x in dmn_bp_frags if x]
                dmn_bp_str     = '.'.join(dmn_bp_frags)
                dmn_bp         = self.split_by_dot(dmn_bp_str)
                cnfg['bp']     = dmn_bp

                self.logthis(3,f"{'':>12}dmn_bp_frags: {dmn_bp_frags}")
                self.logthis(3,f"{'':>12}dmn_bp_str:   {dmn_bp_str}")
                self.logthis(3,f"{'':>12}dmn_bp:       {dmn_bp}")

        else:
            self.logthis(2,f"{'':>8}Already Done!")


    def resl_dmns(self):
        self.logthis(1,f"{'':>4}>resl_dmn()")

        hstn, sld, tld   = None,None,None
        dmn_type         = None
        dmn_frags        = self.u.dmn.split('.')
        dmn_cnfgs        = self.cnfg['dmns']

        if len(dmn_frags) == 2:
            dmn_frags = [''] + dmn_frags

        self.logthis(1,f"{'':>8}dmn_frags:     ['{dmn_frags[0]}', '{dmn_frags[1]}', '{dmn_frags[2]}']")

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
            sys.exit('ERROR: Domain "',self.u.dmn,'" Could not Be Resoled!')

        new_dmn_frags   = [self.u.hstn, self.u.sld, self.u.tld]
        self.logthis(3,f"{'':>8}new_dmn_frags: {new_dmn_frags}")

        new_dmn_frags   = [x for x in new_dmn_frags if x]

        self.logthis(3,f"{'':>8}new_dmn_frags: {new_dmn_frags}")
        self.logthis(1,f"{'':>8}dmn_type:      {self.u.dmn_type}")


    def gen_url_bps(self): 
        self.logthis(3,f"{'':>4}>gen_url_bp()")

        self.logthis(3,f"{'':>8}...generating bps")
        for node_type in self.cnfg['urls']: 


            for url_type, cnfg in self.cnfg['urls'][node_type].items():

                cnfg = cnfg['bp_cnfg']

                if isinstance(cnfg,dict):
                    self.logthis(3,f"{'':>8}Already Done!")
                    break

                self.logthis(3,f"{'':>16}url_type:   {url_type}")
                self.logthis(3,f"{'':>12}node_type:  {node_type}")

                path_bp     = cnfg[1:]
                query       = {}

                nmstr, item_type, arg_ar = self.process_item(cnfg[0])
                dmn_type    = arg_ar[0]

                if len(path_bp) and isinstance(path_bp[-1],dict):
                    query=path_bp[-1]
                    path_bp = path_bp[:-1]

                new_path_bp = self.process_ar(path_bp)

                self.logthis(3,f"{'':>20}new_path_bp: {new_path_bp}")
                self.logthis(3,f"{'':>20}dmn_type:    {dmn_type}")
                self.logthis(3,f"{'':>20}query:       {query}")

                self.cnfg['urls'][node_type][url_type]['bp_cnfg'] = {
                    'bp':     new_path_bp,
                    'query':    query,
                    'dmn_type': dmn_type,
                    'cnfg':     cnfg,
                }

            else:
                continue

            break


    def resl_url(self): 
        """_summary_

        Returns:
            _type_: _description_
        """

        self.logthis(2,f"{'':>4}>resl_url()")

        for ndnm, nd_cnfg in self.cnfg['urls'].items():

            for url_type, url_cnfg in nd_cnfg.items():

                bp_cnfg     = url_cnfg['bp_cnfg']
                bp_dmn_type = bp_cnfg['dmn_type']

                if bp_dmn_type != self.u.dmn_type:

                    self.logthis(3,f"{'':>20}!dmn_type doesn't match bp's")

                    continue

                self.ar   = []
                self.arbf = self.process_ar(self.u.url.path.split('/'))
                self.bp   = copy.deepcopy(bp_cnfg['bp'])

                self.logthis(2,f"{'':>24}url_type: {url_type}")

                suc = self.m()

                if suc:

                    self.logthis(1,f"{'':>8}node_type:    {ndnm}")
                    self.logthis(1,f"{'':>8}url_type: {url_type}")
                    self.logthis(1,f"{'':>8}bp:       {self.bp}")
                    self.logthis(1,f"{'':>8}ar:       {self.ar}")

                    self.u.node_type  = ndnm
                    self.u.url_type = url_type

                    break

            else:
                continue

            break

        else:
            sys.exit('ERROR: Could not resolv url "'+str(self.u.url.geturl())+'"')


    def m(self):
        ### m() ##################################
        #self.logthis(2,f"{'':>20}>!_m()")

        retu=False
        last_match_was_sucessful = False
        self.r_val    = None
        self.r_e      = None
        self.r_active = False
        self.idx      = -1

        while len(self.arbf):
            self.idx += 1
            last_match_was_sucessful = False

            self.logars(28)

            #if (len(arbf) + len(ar)) < (len(bp)):
            #    break
            #self.logars(28)

            # if the idx has gone out of range of the bp, we need to check if we can
            # append the '_try' items to the bp, before breaking the loop.
            if (len(self.bp) - self.idx) < 1:
                if self.r():
                    continue
                break

            # If remaing bp items exceed that of the ar, then we need to break. Appending more
            # '_try' items will not help
            #if len(arbf) < (len(bp) - self.idx):
            #    break

            self.bp_item = self.bp[self.idx]
            self.item    = self.arbf.pop(0)
            self.ar.append(self.item)

            self.logars(28,where='POSTCHECKS')


            nmstr, item_type, arg_ar = self.process_item(self.bp_item)

            # _try(*arg_ar)
            if item_type == 'op':
                if nmstr == 'try':
                    self.logthis(2,f"{'':>36}try op found!")
                    self.process_op_routine(nmstr,arg_ar)
                    continue

            if item_type == 'vr':
                pass

            elif self.item != self.bp_item:
                self.logthis(2,f"{'':>36}{self.item} != {self.bp_item}")
                # items from bp and ar at the current idx did not match. We need to see if we can backtrack
                # and append '_try' items for a better match
                if self.r():
                    continue
                break
            #self.logars(28)
            last_match_was_sucessful=True
            if not len(self.arbf):
                if self.idx != (len(self.bp)-1):
                    self.logthis(2,f"{'':>36}arbf exhausted!")

        # Sucess
        if last_match_was_sucessful and (self.idx) == (len(self.bp)-1):
            self.logthis(2,f"{'':>32}Sucess!")
            retu = True

        # Failure
        else:
            self.logthis(2,f"{'':>32}Failure!")

        return retu


    def r(self):
        """_summary_
        ['/', _try(*), '/']
        ['/', _try(*)]

        [_try(*), '/']
        [_try(*)]

        len(bp)-1 - idx = 0 = last_bp_indx
        len(bp)-1 - idx > 0 = bp_indx
        len(bp)-1 - idx < 0 = out of range



        Returns:
            _type_: _description_
        """
        #self.logthis(2,f"{'':>32}>r()")

        retu = False
        bp   = self.bp
        ar   = self.ar
        arbf = self.arbf

        if self.r_active and self.idx >= self.r_e:

            rval = self.r_val
            rval_len = len(self.r_val)

            if self.r_e >= len(self.bp):
                rval = ['/'] + rval
            else:
                rval = rval + ['/']

            self.bp[self.r_e:self.r_e] = rval
            self.arbf = self.ar[self.r_e:] + self.arbf
            del self.ar[self.r_e:]

            # Idx is incremented at the start of each loop. To repeat the current index
            # the idx is deincremented before the next loop is started.
            self.idx = self.r_e - 1

            # The try value array will be inserted before the "forward end" of the last insert.
            # The next forward end is found by adding the rval len to the last "forward end"
            # index.
            self.r_e += rval_len


            retu = True
            #self.logars(28)
        #else:
            #self.logthis(2,f"{'':>36}r_active: {self.r_active} idx: {self.idx} < r_e: {self.r_e}")

        return retu


    #def resl_query(self):
    #    self.logthis(1,f"{'':>4}>resl_query()")

    #    query_bp  = self.cnfg['urls'][self.u.node_type][self.u.url_type]['cnfg']['query']
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


    def logars(self,ind:int,where:str='START') -> None:
        """_summary_

        Args:
            ind (int): _description_
            where (str, optional): _description_. Defaults to 'START'.
        """
        bp        = copy.deepcopy(self.bp)
        bp_len    = len(bp)
        arbf      = copy.deepcopy(self.arbf)
        ar        = copy.deepcopy(self.ar)
        idx       = self.idx
        r_e       = self.r_e

        if where == 'START':
            self.logthis(2,f"{'':>{ind}}----------------------------")

        if not ((idx+1) > len(bp)):
            bp[idx] = "<<"+bp[idx]+">>"
        if where == 'START':
            if len(arbf):
                arbf[0] = "<<"+arbf[0]+">>"
        else:
            if len(ar):
                ar[-1] = "<<"+ar[-1]+">>"

        nind = ind + 4
        ind += 8
        self.logthis(2,f"{'':>{nind}}{where}")
        self.logthis(2,f"{'':>{ind}}idx: {idx}, or_bp{bp_len-idx}, r_e{r_e}")
        self.logthis(2,f"{'':>{ind}}{bp}")

        if len(ar):
            self.logthis(2,f"{'':>{ind}}{ar}{arbf}")
        else:
            self.logthis(2,f"{'':>{ind}}{arbf}")


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


    def process_vr(self,vrnm:str,args:list):
        """_summary_

        Args:
            vrnm (str): _description_
            args (list): _description_
        """


    def process_op_routine(self,opnm:str,arg_ar:list):
        """_summary_

        Args:
            opnm (str): _description_
            arg_ar (list): _description_
        """
        if opnm == 'try':

            bp = self.bp

            self.r_e                   = self.idx
            self.r_active              = True
            self.r_val                 = self.process_ar(arg_ar)

            # remove the opstr           
            self.bp.pop(self.idx)

            # make sure the idx has not gone out of range of the bp before
            # attempting access it.          
            if self.idx != (len(self.bp)):

                # remove trailing '/' in bp array if one exists          
                if bp[self.idx] == '/':
                    self.bp.pop(self.idx)
                if bp[-1] == '/':
                    self.bp.pop(-1)
                


            # The idx should not be greater than the bp's length by design, this happening
            # means something is wrong. 
            elif self.idx > (len(self.bp)):
                sys.exit(f"ERROR: idx '{self.idx}' exceeds length of the bp '{len(self.bp)-1}'")

            else:
                if bp[self.idx-1] == '/':
                    self.bp.pop(self.idx - 1)

            self.arbf = self.ar[self.r_e:] + self.arbf
            del self.ar[self.r_e:]

            # Idx is incremented at the start of each loop. To repeat the current index
            # the idx is deincremented before the next loop is started.
            self.idx -= 1


    def get_op_ar_val(self,opnm:str,arg_ar:list) -> list:
        """_summary_

        Args:
            opnm (str): _description_
            arg_ar (list): _description_

        Returns:
            list: _description_
        """
        ar_val = None
        if opnm == 'dmns':
            if len(arg_ar) != 1:
                sys.exit(f"ERROR: arg length for dmns is not 1 '{arg_ar}'")
            dmn_type = arg_ar[0]
            try:
                dmn_bp = self.cnfg['dmns'][dmn_type]['bp']
            except KeyError:
                sys.exit(f"ERROR: dmn_type '{dmn_type}' does not exist")
            ar_val = dmn_bp
        else:
            sys.exit(f"ERROR: opnm '{opnm}' is not valid")
        return ar_val

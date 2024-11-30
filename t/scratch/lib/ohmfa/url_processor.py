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
    depth    = -1
    idx      = None
    bp       = None
    ar       = None
    arbf     = None
    r_e      = None
    r_active = None
    r_val    = None
    item     = None
    bp_item  = None
    abrf     = None
    delim    = None
    bp_hold  = None

    def __init__(self,u,verbose=0,prnt=0):
        """_summary_
        """
        super().__init__(u.cnfg,verbose,prnt)
        self.u = u


    def resl_dmn(self):
        """_summary_
        """
        self._gen_dmn_bps()
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


    def resl_path(self): 
        """_summary_

        Returns:
            _type_: _description_
        """

        self.logthis(2,f"{'':>4}>resl_path()")

        self._gen_path_bps()


        for node_type, nd_cnfg in self.cnfg['urls'].items():

            for path_type, url_cnfg in nd_cnfg.items():

                bp_cnfg     = url_cnfg['bp_cnfg']
                bp_dmn_type = bp_cnfg['dmn_type']

                if bp_dmn_type != self.u.dmn_type:

                    self.logthis(3,f"{'':>20}!dmn_type doesn't match bp's")

                    continue

                arbf = self._process_ar(self.u.url.path.split('/'))
                bp   = copy.deepcopy(bp_cnfg['bp'])

                self.logthis(2,f"{'':>24}path_type: {path_type}")
                self.ar       = []
                self.bp       = []
                self.arbf     = []
                self.r_val    = []
                self.r_e      = []
                self.r_active = []
                self.idx      = []
                self.delim    = []

                self.logthis(2,f"{'':>24}bp: {bp}")
                self.logthis(2,f"{'':>24}arbf: {arbf}")
                suc = self._m(bp,arbf,'/')
                if suc:

                    self.logthis(1,f"{'':>8}node_type:    {node_type}")
                    self.logthis(1,f"{'':>8}path_type:    {path_type}")
                    self.logthis(1,f"{'':>8}bp:           {self.bp[0]}")
                    self.logthis(1,f"{'':>8}ar:           {self.ar[0]}")

                    self.u.node_type  = node_type
                    self.u.path_type = path_type

                    break

            else:
                continue

            break

        else:
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
        cnfg = self.cnfg['urls'][group][path_type]['cnfg']
        url = self.url_from_bp(cnfg['bp'])
        return url


    def url_from_bp(self,url_bp):
        url_ar = []
        for item in url_bp:
            item = self.process_item(item)
            url_ar.append(item)
        url = ''.join(url_ar)
        return url


    def process_op_routine(self,opnm:str,arg_ar:list):
        """_summary_

        Args:
            opnm (str): _description_
            arg_ar (list): _description_
        """
        if opnm == 'try':

            bp   = self.bp[self.depth]
            ar   = self.ar[self.depth]
            arbf = self.arbf[self.depth]
            idx = self.idx[self.depth]
            delim = self.delim[self.depth]

            self.r_e[self.depth]      = idx
            self.r_active[self.depth] = True
            self.r_val[self.depth]    = self._process_ar(arg_ar)

            r_e = self.r_e[self.depth]
            r_active = self.r_active[self.depth]
            r_val = self.r_val[self.depth]
            # remove the opstr           
            bp.pop(idx)

            # make sure the idx has not gone out of range of the bp before
            # attempting access it.          
            if idx != (len(bp)):

                # remove trailing '/' in bp array if one exists          
                if bp[idx] == delim:
                    bp.pop(idx)
                if bp[-1] == delim:
                    bp.pop(-1)
                


            # The idx should not be greater than the bp's length by design, this happening
            # means something is wrong. 
            elif idx > (len(bp)):
                sys.exit(f"ERROR: idx '{idx}' exceeds length of the bp '{len(bp)-1}'")
            else:
                if len(bp):
                    if (len(bp)-idx) >= 0:
                        if bp[idx-1] == delim:
                            bp.pop(idx - 1)

            arbf[0:0] = ar[r_e:]
            del ar[r_e:]

            # Idx is incremented at the start of each loop. To repeat the current index
            # the idx is deincremented before the next loop is started.
            self.idx[self.depth] -= 1


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


    def _gen_dmn_bps(self):
        """_summary_
        """
        self.logthis(2,f"{'':>4}>gen_dmn_bps()")


        if 'bp' not in self.cnfg['dmns']['d']:

            self.logthis(3,f"{'':>8}...generating bps")

            for dmn_type, dmn_cnfg in self.cnfg['dmns'].items():

                #TLD
                tld = dmn_cnfg['tlds'][0]

                #HSTN
                if not dmn_cnfg['hstn_var']:
                    hstn = dmn_cnfg['hstns'][0]

                else:
                    hstn = dmn_cnfg['hstn_var']

                self.logthis(3,f"{'':>12}dmn_type:     '{dmn_type}'")
                self.logthis(3,f"{'':>12}tld:          '{tld}'")
                self.logthis(3,f"{'':>12}hstn:         '{hstn}'")
        
                dmn_bp_frags   = [hstn, self.u.sld, tld]
                self.logthis(3,f"{'':>12}dmn_bp_frags: {dmn_bp_frags}")

                dmn_bp_frags    = [x for x in dmn_bp_frags if x]
                dmn_bp_str      = '.'.join(dmn_bp_frags)
                dmn_bp          = self._split_by_dot(dmn_bp_str)
                dmn_cnfg['bp']  = dmn_bp

                self.logthis(3,f"{'':>12}dmn_bp_frags: {dmn_bp_frags}")
                self.logthis(3,f"{'':>12}dmn_bp_str:   {dmn_bp_str}")
                self.logthis(3,f"{'':>12}dmn_bp:       {dmn_bp}")

        else:
            self.logthis(2,f"{'':>8}Already Done!")


    def _gen_path_bps(self): 
        """_summary_
        """

        self.logthis(2,f"{'':>8}>gen_url_bp()")

        self.logthis(3,f"{'':>8}...generating bps")
        for node_type, node_cnfg in self.cnfg['urls'].items(): 

            for path_type, path_cnfg in node_cnfg.items():

                path_bp_cnfg = path_cnfg['bp_cnfg']

                if isinstance(path_bp_cnfg,dict):
                    self.logthis(3,f"{'':>8}Already Done!")
                    break

                self.logthis(2,f"{'':>12}node_type:  {node_type}")
                self.logthis(2,f"{'':>16}path_type:   {path_type}")

                nmstr, item_type, arg_ar = self.process_item(path_bp_cnfg[0])
                dmn_type    = arg_ar[0]

                path_bp     = path_bp_cnfg[1:]
                query       = {}
                if len(path_bp) and isinstance(path_bp[-1],dict):
                    query   = path_bp[-1]
                    path_bp = path_bp[:-1]

                new_path_bp = self._process_ar(path_bp)

                self.logthis(3,f"{'':>20}new_path_bp: {new_path_bp}")
                self.logthis(3,f"{'':>20}dmn_type:    {dmn_type}")
                self.logthis(3,f"{'':>20}query:       {query}")

                self.cnfg['urls'][node_type][path_type]['bp_cnfg'] = {
                    'bp':       new_path_bp,
                    'query':    query,
                    'dmn_type': dmn_type,
                    'cnfg':     path_bp_cnfg,
                }

            else:
                continue

            break


    def _logars(self,ind:int,where:str='START') -> None:
        """_summary_

        Args:
            ind (int): _description_
            where (str, optional): _description_. Defaults to 'START'.
        """
        bp   = self.bp[self.depth]
        ar   = self.ar[self.depth]
        arbf = self.arbf[self.depth]
        r_active = self.r_active[self.depth]
        r_val = self.r_val[self.depth]
        r_e = self.r_e[self.depth]
        idx = self.idx[self.depth]
        delim = self.delim[self.depth]

        bp        = copy.deepcopy(bp)
        bp_len    = len(bp)
        arbf      = copy.deepcopy(arbf)
        ar        = copy.deepcopy(ar)

        if where == 'START':
            self.logthis(2,f"{'':>{ind}}----------------------------")

        if not ((idx+1) > len(bp)):
            bp[idx] = "<<"+str(bp[idx])+">>"
            if r_e is not None and (len(bp) - r_e) >= 1:
                bp[r_e] = "||"+str(bp[r_e])+"||"
        if where == 'START':
            if len(arbf):
                arbf[0] = "<<"+str(arbf[0])+">>"
        else:
            if len(ar):
                ar[-1] = "<<"+str(ar[-1])+">>"


        nind = ind + 4
        ind += 8
        self.logthis(2,f"{'':>{nind}}{where}")
        self.logthis(2,f"{'':>{ind}}depth: {self.depth}")
        self.logthis(2,f"{'':>{ind}}idx:{idx}, orbp:{bp_len-idx}, r_e:{r_e}")
        self.logthis(2,f"{'':>{ind}}{bp}")

        if len(ar):
            self.logthis(2,f"{'':>{ind}}{ar}{arbf}")
        else:
            self.logthis(2,f"{'':>{ind}}{arbf}")


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


    def _m(self,bp,arbf,delim):
        ### m() ##################################
        #self.logthis(2,f"{'':>20}>!_m()")
        self.depth +=1
        retu=False
        last_match_was_sucessful = False
        self.r_val.append(None)
        self.r_e.append(None)
        self.r_active.append(False)
        self.idx.append(-1)
        self.delim.append(delim)

        idx = self.idx[self.depth]

        self.bp.append(bp)
        self.arbf.append(arbf)
        self.ar.append([])
        bp = self.bp[self.depth]
        ar =  self.ar[self.depth]
        arbf = self.arbf[self.depth]
        delim = self.delim[self.depth]
        if not len(bp) and not len(arbf):
            retu = True
            return retu
        while len(arbf):
            self.idx[self.depth] += 1
            idx = self.idx[self.depth]
            last_match_was_sucessful = False

            self._logars(28)

            #if (len(arbf) + len(ar)) < (len(bp)):
            #    break
            #self._logars(28)

            # if the idx has gone out of range of the bp, we need to check if we can
            # append the '_try' items to the bp, before breaking the loop.
            if (len(bp) - idx) < 1:
                self.logthis(2,f"{'':>36}orbp({len(bp)-idx}) < 1")
                if self._r():
                    continue
                break

            # If remaing bp items exceed that of the ar, then we need to break. Appending more
            # '_try' items will not help
            #if len(arbf) < (len(bp) - self.idx):
            #    break

            bp_item = bp[idx]
            item    = arbf.pop(0)
            ar.append(item)

            self._logars(28,where='POSTCHECKS')


            nmstr, item_type, arg_ar = self.process_item(bp_item)

            # _try(*arg_ar)
            if item_type == 'op':
                if nmstr == 'try':
                    self.logthis(2,f"{'':>36}try op found!")
                    self.process_op_routine(nmstr,arg_ar)
                    continue

            elif item_type == 'ar':
                tbp_item = copy.deepcopy(bp_item)
                op = tbp_item.pop(0)
                nmstr, item_type, arg_ar = self.process_item(op)
                mm = False
                tbp_item = '.'.join(tbp_item)
                tbp_item = self._split_by_dot(tbp_item)
                
                if not isinstance(item,list):
                    mm = self._m(tbp_item, [item],arg_ar[0])
                else:
                    mm = self._m(tbp_item, item,arg_ar[0])
                if isinstance(item,list):
                    item[0:0] = self.ar[self.depth+1]
                self.bp_hold = copy.deepcopy(self.bp[self.depth-1])
                self.r_val.pop(-1)
                self.r_e.pop(-1)
                self.r_active.pop(-1)
                self.idx.pop(-1)
                self.bp.pop(-1)
                self.arbf.pop(-1)
                self.ar.pop(-1)
                if not mm:
                    if self.r_active[self.depth]:
                        if self._r():
                            continue
                        break
                    break

            elif item_type == 'vr':
                pass

            elif item != bp_item:
                self.logthis(2,f"{'':>36}{item} != {bp_item}")

                # items from bp and ar at the current idx did not match. We need to see if we can backtrack
                # and append '_try' items for a better match
                if self._r():
                    continue
                break


            self._logars(28,where='POSTPROCESS')
            if not len(arbf):
                if idx != (len(bp)-1):
                    if (len(bp) - idx) > 2:
                        if bp[idx +1] == delim:
                            next_item = bp[idx +2]
                            nmstr,item_type,arg_ar =  self.process_item(next_item)
                            if nmstr == 'try' and item_type == 'op':
                                bp.pop(idx+1)
                                bp.pop(idx+1)
                                arbf[0:0] = [ar[-1]]
                                del ar[-1]
                                self.idx[self.depth] -= 1
                                idx = self.idx[self.depth]
                                continue
                                

                    self.logthis(2,f"{'':>36}arbf exhausted!")

            self._logars(28,where='FINAL')
            last_match_was_sucessful=True

        # Sucess
        if last_match_was_sucessful and (self.idx[self.depth]) == (len(self.bp[self.depth])-1):
            self.logthis(2,f"{'':>32}Sucess! Depth:{self.depth}")
            retu = True

        # Failure
        else:
            self.logthis(2,f"{'':>32}Failure! Depth:{self.depth}")



        self.depth -= 1

        return retu


    def _r(self):
        """_summary_
        

        Returns:
            _type_: _description_
        """
        #self.logthis(2,f"{'':>32}>r()")

        retu = False
        bp   = self.bp[self.depth]
        ar   = self.ar[self.depth]
        arbf = self.arbf[self.depth]
        r_active = self.r_active[self.depth]
        r_val    = self.r_val[self.depth]
        r_e      = self.r_e[self.depth]
        idx      = self.idx[self.depth]
        delim    = self.delim[self.depth]

        if r_active and idx >= r_e:

            if r_e >= len(bp) and len(bp) is not 0:
                r_val = [delim] + r_val

            elif len(bp) is not 0:
                r_val = r_val + [delim]

            rval_len = len(r_val)

            bp[r_e:r_e] = r_val
            arbf[0:0]   = ar[r_e:]
            del ar[r_e:]

            # Idx is incremented at the start of each loop. To repeat the current index
            # the idx is deincremented before the next loop is started.
            self.idx[self.depth] = r_e - 1

            # The try value array will be inserted before the "forward end" of the last insert.
            # The next forward end is found by adding the rval len to the last "forward end"
            # index.
            self.r_e[self.depth] += rval_len


            retu = True
            #self._logars(28)
        #else:
            #self.logthis(2,f"{'':>36}r_active: {self.r_active} idx: {self.idx} < r_e: {self.r_e}")

        return retu

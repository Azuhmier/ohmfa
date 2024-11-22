
import copy
import sys
import urllib
from urllib.parse import urlparse
class OhmfaUrl():
    ops = {
        'special':{
            'z:e': None,
            '[]': None,
        },
        '__': {
            '_domain_': None,
        },
        '_': {
            '_in': None,
            '_css': None,
            '_for': None,
            '_exists': None,
            '_hash=''': None,
            '_not=''': None,
        }
    }
    url_types  = [
        'content', 
        'series',
        'flash',
        'listing',
        'bin',
        'author',
        'misc',
        ]
    action_idx = 0
    action = None
    action_name = None
    wkfl_name = None
    wkfl = None
    url_type = None
    bp_key = None
    domain_type = None
    bp_domain = None


    def __init__(self,url,sld_configs):
        self.url = url
        self.domain = url.netloc
        self.ck_domain = None
        self.actions = []
        self.ws = {}
        self.log = []
        self.soups = {}

        # Determine sld
        domain_frags = self.domain.split('.')
        self.sld = domain_frags[1]
        if len(domain_frags) == 2:
            self.sld = domain_frags[0]

        # Determine Group
        # Get Config
        self.reff        =sld_configs[self.sld]['reffs']
        self.fetch_config=sld_configs[self.sld]['fetch']


    def process(self):
        # domain
        self.domain_type = self.resolve_domain()
        if not self.domain_type:
            sys.exit('Error: domain resolution failed!')

        url_ar0 = self.url.path
        url_ar0 = url_ar0.split('/')
        url_ar0 = [x for x in url_ar0 if x]
        url_ar0 = self.process_url_ar(url_ar0)
        res = self.resolve_url(url_ar0)

        if not res['url_type']:
            print(self.url.geturl())
            print(self.domain)
            for line in self.log:
                print(line)
            sys.exit('ERROR: url resolution failed!')

        self.url_type=res['url_type']
        self.bp_key=res['bp_key']
        self.ws.update(res['vars'])
        if res['query']:
            newquery = urllib.parse.urlencode(res['query'],doseq=True)
            self.url = self.url._replace(query=newquery)


    def resolve_domain(self):
        domain_type  = 'd'
        domain_reffs = self.reff['domain']
        domain_reff  = domain_reffs[domain_type]
        hostname, sld, tld = [None, None, None]

        domain_frags = self.domain.split('.')

        if len(domain_frags) == 2:
            sld,tld = domain_frags
            hostnames = domain_reff['hostname']
            if hostname in hostnames:
                hostname = hostnames[0]
            else:
                sys.exit('Error: invalid hostname at length of 2 "'+str(hostname)+'"')
        else :
            hostname,sld,tld = domain_frags
            hostnames  = domain_reff['hostname']
            if not hostname in hostnames:
                for domain_type,domain_reff in domain_reffs.items():
                    if domain_type not in ['u','d']:
                        if hostname == domain_reff['hostname'][0]:
                            break
                else:
                    if 'u' in domain_reffs:
                        domain_type = 'u'
                        domain_reff = domain_reffs[domain_type]
                        hostname_var = domain_reff['hostname'][0]
                        self.ws[hostname_var] = hostname
            else:
                hostname = hostnames[0]

        if tld not in domain_reff['tld']: 
            sys.exit('Error: invalid tld "'+str(tld)+'"')
        #else:
        #    tld = domain_reff['tld'][0]

        if hostname:
            self.domain = '.'.join([hostname,sld,tld])
        else:
            self.domain = '.'.join([sld,tld])

        self.bp_domain = self.domain
        if domain_type == 'u':
            hostname_var = domain_reff['hostname'][0]
            self.bp_domain = '.'.join([hostname_var,sld,tld])
        return domain_type


    def logthis(self,*args):
        nargs=[]
        for arg in args:
            if isinstance(arg,list):
                nargs.append(copy.deepcopy(arg))
            elif isinstance(arg,dict):
                nargs.append(copy.deepcopy(arg))
            else:
                nargs.append(arg)
        self.log.append(nargs)

    def resolve_url(self,url_ar0): 
        retu = {
            'query':    None,
            'url_type': None,
            'bp_key':   None,
            'vars': {},
        }


        def is_match(url_ar,bp_ar):

            is_match.idx         = -1
            is_match.url_ar      = url_ar
            is_match.bp_ar       = bp_ar
            is_match.pre_items   = []
            success     = False
            _log = []


            def rept():
                is_rept = False
                if rept.active:
                    self.logthis('REPT????',is_match.idx,len(is_match.bp_ar),rept.start,rept.end,rept.active,is_match.bp_ar,is_match.url_ar)
                    if rept.end == 0:
                        is_match.bp_ar[rept.start:rept.start] = rept.val
                        is_match.url_ar = is_match.pre_items[rept.start:] + is_match.url_ar
                        del is_match.pre_items[rept.start:]
                        is_match.idx = rept.start - 1
                        rept.end = len(rept.val) + is_match.idx
                        is_match.is_rept = True
                        is_rept = True
                    elif is_match.idx >= rept.end:
                        is_match.bp_ar[rept.end:rept.end] = rept.val
                        is_match.url_ar = is_match.pre_items[rept.end:] + is_match.url_ar
                        del is_match.pre_items[rept.start:]
                        is_match.idx = rept.end - 1
                        is_rept = True

                if is_rept:
                    self.logthis('REPT<<<<',is_match.idx,len(is_match.bp_ar),rept.start,rept.end,rept.active,is_match.bp_ar,is_match.url_ar)
                return is_rept


            rept.val    = None
            rept.start  = 0
            rept.end    = 0
            rept.active = False

            while len(is_match.url_ar):
                success = False
                is_match.idx += 1
                self.logthis('START===',is_match.idx,len(is_match.bp_ar),rept.start,rept.end,rept.active,is_match.bp_ar,is_match.url_ar)
                if len(is_match.url_ar) > 10:
                    for line in self.log:
                        print(line)
                    sys.exit('ERROR! Iteration Depth Reached at "'+str(is_match.idx)+'"')
                #reff exhausted
                if (is_match.idx+1) > len(is_match.bp_ar):
                    if rept():
                        continue
                    break

                item      = is_match.url_ar.pop(0)
                reff_item = is_match.bp_ar[is_match.idx]
                is_match.pre_items.append(item)

                self.logthis('POPPED  ',is_match.idx,len(is_match.bp_ar),rept.start,rept.end,rept.active,is_match.bp_ar,is_match.url_ar,rept.active)
                if reff_item[:2] == 'p_':
                    rept.start               = is_match.idx
                    rept.active              = True
                    rept.val                 = self.reff['path'][reff_item[2:]]
                    is_match.bp_ar.pop(is_match.idx)
                    if len(is_match.bp_ar) < (is_match.idx+1):
                        if rept():
                            continue
                        break
                    else:
                        reff_item  = is_match.bp_ar[is_match.idx]


                self.logthis('VALIDATE',is_match.idx,len(is_match.bp_ar),rept.start,rept.end,rept.active,is_match.bp_ar,url_ar)
                if reff_item[0] == '_':
                    retu['vars'][reff_item] = item
                elif item != reff_item:
                    if rept():
                        continue
                    break

                self.logthis('SUCCESS ',is_match.idx,len(is_match.bp_ar),rept.start,rept.end,rept.active,is_match.bp_ar,is_match.url_ar)
                success=True

            if not (success and (is_match.idx+1) == len(is_match.bp_ar)):
                success = False
            return success


        for url_type in self.url_types:
            self.logthis(url_type)
            bps_key = 'bp_'+url_type

            if bps_key not in self.reff:
                self.logthis('not_found!')
                continue

            bps = self.reff[bps_key]
            for bp_key, bp in bps.items():
                self.logthis(bp_key[0],self.domain_type)

                if bp_key[0] != self.domain_type:
                    self.logthis('no_match!')
                    continue

                bp_ar0 = copy.deepcopy(bp)
                if len(bp_ar0) and isinstance(bp_ar0[-1],dict):
                    retu['query']=bp_ar0.pop(-1)
                bp_ar0 = self.process_url_ar(bp_ar0)

                bp_ar    = copy.deepcopy(bp_ar0)
                url_ar       = copy.deepcopy(url_ar0)

                if is_match(url_ar,bp_ar):
                    retu['bp_key']=bp_key
                    break

            if retu['bp_key']:
                retu['url_type'] = url_type
                break

        return retu


    def process_url_ar(self,ar,keep_vars=True):
        new_ar = []
        for item in ar:
            if len(item) > 1 and '.' in item:
                item_ar = self.split_by_dot(item)
                new_ar = new_ar + item_ar
            # Scalar, process value
            else:
                if not keep_vars:
                    item = self.process_item(item)
                new_ar.append(item)
        domain_ar = self.split_by_dot(self.domain)

        new_ar[0:0] = domain_ar
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


    def process_item(self,item):
        retu = None
        if item[0] == '_':
            if item[-1] == '_':
                retu = self.get_var(item)
        else:
            retu = item
        return retu

    def get_var(self,var):
        value=None
        if var in self.ws:
            value = self.ws[var]
        return value

    #def process_get_ar(self,ele_ar):
    #    'e_'
    #    'g_
    #    'a_'
    #    'w_'
    #def process_ele_ar(self,ele_ar):
    #    '_css'
    #    '_in'
    #    '_hash'
    #    '_any'
    #    '_not'
    #    '_for'
    #    '.'
    #    '='
    #    'txt'
    #    'e_'
    #    ':'
    
    #def resolve_fetch(self):
    #    self.load_wkfl('w0')
    #    self.load_next_action()


    #def load_wkfl(self, wkfl_name=None) :
    #    if not wkfl_name :
    #        wkfl_name = 'w1' 
    #    self.wkfl = self.fetch_config['workflows'][wkfl_name]
    #    return wkfl_name


    #def load_next_action(self):
    #    self.action_idx += 1
    #    self.action_name = self.wkfl[self.action_idx]
    #    self.action = self.fetch_config['actions'][self.action_name]
    #    self.actions.append(self.action)
    #    self.gen_header()
    #    url = self.process_item([self.action["url"]])

    #def gen_header(self):
    #    pass












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
    slds = [
        'itch.io',
        'literotica',
        'rentry', 
        'sofurry',
        'archiveofourown' ]

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
        self.actions = []
        self.ws = {}

        # Determine Group
        for sld in self.slds:
            if sld in self.domain:
                self.sld = sld
                break
        else:
            self.sld = self.domain

        # Determine Group
        # Get Config
        self.reff=sld_configs[self.sld]['reffs']
        #self.fetch_config=sld_configs[self.sld]['fetch']


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
        hostname, sld, tld = [None, None,None]

        domain_frags = self.domain.split('.')

        if len(domain_frags) == 2:
            sld,tld = domain_frags
            hostnames = domain_reff['hostname']
            if hostname in hostnames:
                hostname = hostnames[1]
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
                if hostnames[0]:
                  hostname = hostnames[0]
                else:
                  hostname = hostnames[1]

        if tld not in domain_reff['tld']: 
            sys.exit('Error: invalid tld "'+str(tld)+'"')
        else:
            tld = domain_reff['tld'][0]

        self.domain = '.'.join([hostname,sld,tld])
        self.bp_domain = self.domain
        if domain_type == 'u':
            hostname_var = domain_reff['hostname'][0]
            self.bp_domain = '.'.join([hostname_var,sld,tld])
        return domain_type


    def resolve_url(self,url_ar0): 
        retu = {
          'query':    None,
          'url_type': None,
          'bp_key':   None,
          'vars': {},
        }


        def is_match(url_ar,bp_ar):

            idx         = -1
            pre_items   = []
            success     = False


            def rept(url_ar,bp_ar,idx):
                is_rept = False
                if rept.active:
                  if not rept.end:
                      bp_ar[rept.start:rept.start] = rept.val
                      url_ar = pre_items[rept.start:] + url_ar
                      idx = rept.start - 1
                      rept.end = len(rept.val) + idx
                      is_rept = True
                  elif idx >= rept.end:
                      bp_ar[rept.end:rept.end] = rept.val
                      url_ar = pre_items[rept.end:] + url_ar
                      idx = rept.end - 1
                      is_rept = True
                return is_rept


            rept.val    = None
            rept.start  = 0
            rept.end    = 0
            rept.active = False

            while len(url_ar):
                success = False

                idx += 1
                #reff exhausted
                if (idx+1) > len(bp_ar):
                    if rept(url_ar,bp_ar,idx):
                        continue
                    break

                item      = url_ar.pop(0)
                reff_item = bp_ar[idx]
                pre_items.append(item)

                if reff_item[:2] == 'p_':
                    rept.start               = idx
                    rept.active              = True
                    rept.val                 = self.reff['path'][reff_item[1:]]
                    bp_ar.pop(idx)
                    reff_item                = bp_ar[idx]


                if reff_item[0] == '_':
                    retu['vars'][reff_item] = item
                elif item != reff_item:
                    if rept(url_ar,bp_ar,idx):
                        continue
                    break

                success=True

            if not (success and (idx+1) == len(bp_ar)):
                success = False
            return success


        for url_type in self.url_types:
            bps_key = 'bp_'+url_type

            if bps_key not in self.reff:
                continue

            bps = self.reff[bps_key]
            for bp_key, bp in bps.items():

                if bp_key[0] != self.domain_type:
                    continue

                bp_ar0 = copy.deepcopy(bp)
                if isinstance(bp_ar0[-1],dict):
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











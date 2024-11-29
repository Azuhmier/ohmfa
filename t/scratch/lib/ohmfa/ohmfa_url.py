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
import warnings




class OhmfaUrl(Ohmfa):
    # domain
    dmn_type    = None
    hstn        = None
    tld         = None
    sld         = None


    url_type    = None
    query  = None
    node_type   = None
    uproc = None


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
        self.logthis(1,f"dmn: {self.dmn}")
        self.logthis(1,f"sld: {self.sld}")

        # domain
        self.uproc = UrlProcessor(self,self.verbose,self.prnt)


        self.uproc.resl_dmns()
        self.uproc.gen_dmn_bps()
        self.uproc.gen_url_bps()
        self.uproc.resl_url()
        #self.resl_query()
        #self.update_url()

    def update_url(self):
        newquery = urllib.parse.urlencode(self.query,doseq=True)
        self.url = self.url._replace(query=newquery)
        self.url = self.url._replace(netloc=self.dmn)
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
    def logvar(self,ind,name,value,ind2=0):
                
                if name not in self.vrs:
                    self.logthis(1,f"{'':>{ind}}_{name}_: '{value}'")
                else: 
                    self.logthis(1,f"{'':>{ind}}_{name}_: '{self.vrs[name]}' -> '{value}'")
    def set_vr(self, vr:dict, val):
        """_summary_

        Args:
            vr (dict): _description_
            val (_type_): _description_
        """
        vrnm = vr['name']
        del vr['name']
        vr['val']=val
        self.vrs[vrnm] = vr

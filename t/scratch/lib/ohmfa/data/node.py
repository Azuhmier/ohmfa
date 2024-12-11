from ohmfa.ohmfa import Ohmfa
from ohmfa.utils.config_parser import (validate_item, process_item)
import copy
import sys
import yaml

class Table(Ohmfa):
    cnfg = None
    def __init__(self,cnfg_file=None,verbose=0,prnt=False):
        super().__init__(verbose,prnt)
        if cnfg_file:
            with open(cnfg_file, mode='r',encoding='utf-8' ) as infile:
                self.cnfg = yaml.safe_load(infile)
        self.ntbls = {}
        self.atbls = {}
        self.ptbls = {}
        self.utbls = []
        self.tree = {}

    def load_cnfg(self,cnfg_file):
        with open(cnfg_file, mode='r',encoding='utf-8' ) as infile:
            self.cnfg = yaml.safe_load(infile)

    def process_cnfg(self):
            new_cnfg = copy.deepcopy(self.cnfg)
            node_sbcls_list    = [sbcls for sbcls,sbcls_cnfg in new_cnfg.items() if sbcls_cnfg['superclass'] == 'node']
            attr_sbcls_list    = [sbcls for sbcls,sbcls_cnfg in new_cnfg.items() if sbcls_cnfg['superclass'] == 'attr']
            prop_sbcls_list    = [sbcls for sbcls,sbcls_cnfg in new_cnfg.items() if sbcls_cnfg['superclass'] == 'prop']

            for sbcls in self.cnfg.items():
                self.cnfg[sbcls]['attr'] = {}
                self.cnfg[sbcls]['prop'] = {}
                self.cnfg[sbcls][-1] = {}
                self.cnfg[sbcls][1] = {}

            for sbcls, sbcls_cnfg in self.cnfg.items():


                
                # enable_for
                for item in sbcls_cnfg['enable_for']:
                    retu, res = validate_item(item, desired_item_type='op',desired_namestr='mi',err=True,cnfg=self.cnfg)
                    m = res[0]
                    i = res[1]
                    res  = res[2]
                    # Parent
                    if m[1] == '1' and i == 0: 
                        if sbcls_cnfg['superclass'] == 'node':
                            for key in list(res.keys()):
                                sbcls_cnfg['parents'][key] = []
                        elif sbcls_cnfg['class'] == 'value':
                            if sbcls_cnfg['superclass']== 'prop':
                                for v in res.values():
                                    v['prop'][sbcls] = sbcls_val 
                            else:
                                for v in res.values():
                                    v['attr'][sbcls] = sbcls_val 
                        else: 
                            pass
                    # Child
                    elif m == '1':
                        if sbcls_cnfg['superclass'] == 'node':
                            for k,v in res.items():
                                if v['superclass'] == 'node':
                                    v['parents'][sbcls] = []
                                else:
                                    sys.exit('ERROR')

                # val type
                carrier = sbcls_cnfg['carrier']
                sbcls_val = carrier
                if sbcls_val is not None:
                    if isinstance(sbcls_val,dict) and len(list(sbcls_val.keys())):
                        for k,v in sbcls_val.items():
                            retu, new_v = validate_item(
                                v,
                                desired_item_type='op',
                                desired_namestr='type')
                            sbcls_val[k] = new_v

                    if sbcls_cnfg['val']['type'] != 'predefined':
                        if isinstance(sbcls_val,list):
                            pass
                        elif isinstance(sbcls_val,dict):
                            pass
                else:
                    retu, sbcls_val = validate_item(
                        sbcls_cnfg['val']['type'],
                        desired_item_type='op',
                        desired_namestr='type')
                if (sbcls_cnfg['superclass'] == 'node'):
                    tscope = sbcls_cnfg['val']['tscope']
                    for item in tscope:
                        retu,res = validate_item(item, desired_item_type='op',desired_namestr='mi',err=True,cnfg=self.cnfg)
                        m = res[0]
                        i = res[1]
                        res  = res[2]
                        if m == '-m' and i == 'i': 
                            if sbcls_cnfg['superclass'] == 'prop':
                                self.ptbls[sbcls] = {'name':sbcls, 'table':[]}
                                for k in eres[0].keys():
                                    utbl = {
                                        'tbls_used': [k,sbcls],
                                        'tbl': []
                                    }
                                    self.utbls.append(utbl)
                            elif sbcls_cnfg['superclass'] == 'attr':
                                self.atbls[sbcls] = {'name':sbcls, 'table':[]}
                                for k in eres[0].keys():
                                    utbl = {
                                        'tbls_used': [k,sbcls],
                                        'tbl': []
                                    }
                                    self.utbls.append(utbl)
                        elif m == '-1' and i == '0': 
                            if sbcls_cnfg['superclass'] == 'prop':
                                for k in eres[0].keys():
                                    self.ntbls[k]['ptables'] = {'name':sbcls, 'table':[]}
                                    utbl = {
                                        'tbls_used': [k,sbcls],
                                        'tbl': []
                                    }
                                    self.utbls.append(utbl)
                            elif sbcls_cnfg['superclass'] == 'attr':
                                for k in eres[0].keys():
                                    self.ntbls[k]['utables'] = {'name':sbcls, 'table':[]}
                                    utbl = {
                                        'tbls_used': [k, sbcls],
                                        'tbl': []
                                    }
                                    self.utbls.append(utbl)

                    tuniq = sbcls_cnfg['val']['tscope']
                    for item in tuniq:
                        retu,res = validate_item(item, desired_item_type='op',desired_namestr='mi',err=True,cnfg=self.cnfg)
                elif (sbcls_cnfg['class'] == 'use'):
                    uscope = sbcls_cnfg['val']['uscope']
                    rez = []
                    m = []
                    i = []
                    for item in tscope:
                        retu,res = validate_item(item[0], desired_item_type='op',desired_namestr='mi',err=True,cnfg=self.cnfg)
                        m.append(res[0])
                        i.append(res[1])
                        rez.append(res[2])
                        retu,res = validate_item(item[1], desired_item_type='op',desired_namestr='mi',err=True,cnfg=self.cnfg)
                        m.append(res[0])
                        i.append(res[1])
                        rez.append(res[2])
                        if m[0] == '-1' and i[0] == 'i': 
                            if m[1] == '1' and i[1] == 'i': 
                                    self.ntbls[eres[0]['subclass']]['utables'].append({'name':sbcls, 'table':[]})
                                    for k in eres[0].keys():
                                        utbl = {
                                            'tbls_used': [k,sbcls],
                                            'tbl': []
                                        }
                                        self.utbls.append(utbl)

                    tuniq = sbcls_cnfg['val']['tscope']
                    for item in tuniq:
                        retu,res = validate_item(item, desired_item_type='op',desired_namestr='mi',err=True,cnfg=self.cnfg)
                elif (sbcls_cnfg['class'] == 'value'):
                    uscope = sbcls_cnfg['val']['tscope']
                    for item in uscope:
                        retu,res = validate_item(item, desired_item_type='op',desired_namestr='mi',err=True,cnfg=self.cnfg)
                        m = res[0]
                        i = res[1]
                        res  = res[2]
                        if m == '-m' and i == 'i': 
                            if sbcls_cnfg['superclass'] == 'prop':
                                self.ptbls[sbcls] = {'name':sbcls, 'table':[]}
                                for k in eres[0].keys():
                                    utbl = {
                                        'tbls_used': [k,sbcls],
                                        'tbl': []
                                    }
                                    self.utbls.append(utbl)
                            elif sbcls_cnfg['superclass'] == 'attr':
                                self.atbls[sbcls] = {'name':sbcls, 'table':[]}
                                for k in eres[0].keys():
                                    utbl = {
                                        'tbls_used': [k,sbcls],
                                        'tbl': []
                                    }
                                    self.utbls.append(utbl)
                        elif m == '-1' and i == '0': 
                            if sbcls_cnfg['superclass'] == 'prop':
                                for k in eres[0].keys():
                                    self.ntbls[k]['ptables'] = {'name':sbcls, 'table':[]}
                                    utbl = {
                                        'tbls_used': [k,sbcls],
                                        'tbl': []
                                    }
                                    self.utbls.append(utbl)
                            elif sbcls_cnfg['superclass'] == 'attr':
                                for k in eres[0].keys():
                                    self.ntbls[k]['utables'] = {'name':sbcls, 'table':[]}
                                    utbl = {
                                        'tbls_used': [k, sbcls],
                                        'tbl': []
                                    }
                                    self.utbls.append(utbl)

                uuniq = sbcls_cnfg['val']['tscope']
                for item in uuniq:
                    retu,res = validate_item(item, desired_item_type='op',desired_namestr='mi',err=True,cnfg=self.cnfg)





class Node(Ohmfa):
    def __init__(self,cnfg, verbose=0,prnt=False):
        super().__init__(verbose,prnt)
        self.cnfg = cnfg
        self.data = {}
    def update_node(self,vr):
        pass



# Main ##################################################
if __name__ == '__main__':
    cnfg_file = '/home/azuhmier/progs/ohmfa/t/scratch/lib/frameworks/node_config.yml'
    t = Table(cnfg_file,verbose=3,prnt=True)
    t.process_cnfg()
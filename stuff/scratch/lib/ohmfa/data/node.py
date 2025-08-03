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
                self.cnfg = self.cnfg['uwu']
        self.ntbls = {}
        self.atbls = {}
        self.ptbls = {}
        self.utbls = []
        self.tree = {}
        self.cnt = 0
        self.mem = {}

    def load_cnfg(self,cnfg_file):
        with open(cnfg_file, mode='r',encoding='utf-8' ) as infile:
            self.cnfg = yaml.safe_load(infile)
            self.cnfg = self.cnfg['uwu']

    def process_cnfg(self):
        new_cnfg = copy.deepcopy(self.cnfg)
        node_sbcls_list    = {k:v for k,v in new_cnfg.items() if v['superclass'] == 'node'}
        attr_sbcls_list    = {k:v for k,v in new_cnfg.items() if v['superclass'] == 'attr'}
        prop_sbcls_list    = {k:v for k,v in new_cnfg.items() if v['superclass'] == 'prop'}

        for k,v in node_sbcls_list.items():
            v['parents'] = {}
            v['childs'] = {}
        for k,v in new_cnfg.items():
            v['attr'] = {}
            v['prop'] = {}
            v['mi']={0:{0:{k:v}}}
            for m in range(-100,100,1):
                v['mi'][m]={}
                for i in range(0,100,1):
                    v['mi'][m][i]={}
        new_cnfg = self.connect(new_cnfg)
        new_cnfg = self.connect(new_cnfg)
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
        for sbcls_cnfg in new_cnfg.values():
            self.mem = {}
            print('&&&&&&&&&&&&&&&&&&&&&&&&&&&&')
            print(f"sbcls: {sbcls_cnfg['subclass']}")
            self.fill_mi(sbcls_cnfg,sbcls_cnfg)
        print(self.cnt)
        #for k,v in new_cnfg.items():
        #    print(k)
        #    if v['superclass'] == 'node':
        #        print('    parents: ',list(v['parents'].keys()))
        #        print('    childs: ',list(v['childs'].keys()))
        #    print('    attr: ',list(v['attr'].keys()))
        #    print('    prop: ',list(v['prop'].keys()))
        #    print('    1: ',list(v['mi'][1][0].keys()))
        #    print('    0: ',list(v['mi'][0][0].keys()))
        #    print('    -1: ',list(v['mi'][-1][0].keys()))



    def connect(self,new_cnfg):
        for sbcls, sbcls_cnfg in new_cnfg.items():
            # enable_for
            print('%%%%%%%%%%%%%%%%%%%%%%')
            print(sbcls)
            for item in sbcls_cnfg['enabled_for']:
                print('    ======================')
                retu, res = validate_item(item, desired_item_type='op',desired_namestr='mi',err=True,cnfg=new_cnfg)
                if res is None:
                    continue
                m    = res[0][0]
                mp   = res[0][1]
                i    = res[1][0]
                ip   = res[1][1]
                res  = res[2]

                print('        ----------------------')
                print('        res: ',list(res.keys()))
                print('        m: ',m)
                print('        i: ',i)
                print('        mp: ',mp)
                print('        ip: ',ip)


                for k,v in res.items():
                    sprcls   = sbcls_cnfg['superclass']
                    cls      = sbcls_cnfg['class']
                    v_sprcls = v['superclass']
                    v_cls    = v['class']

                    if sprcls == 'node':
                        if v_sprcls == 'node':

                            #nc[nr]
                            if m == -1:
                                sbcls_cnfg['mi'][m][i][k] = v
                                sbcls_cnfg['parents'][k] = []
                                v['childs'][sbcls] = []
                                v['mi'][-m][i][sbcls] = sbcls_cnfg

                            #nr[nc]
                            else:
                                v['mi'][-m][i][sbcls] = sbcls_cnfg
                                v['parents'][sbcls] = []
                                sbcls_cnfg['childs'][k] = []
                                sbcls_cnfg['mi'][m][i][k] = v

                        else:

                            #nc[xr]
                            if m == -1:
                                sys.exit('ERROR')

                            #xr[nc]
                            else:
                                v['mi'][-m][i][sbcls] = sbcls_cnfg
                                sbcls_cnfg[v_sprcls][k] = []
                                sbcls_cnfg['mi'][m][i][k] = v
                    else:
                        if v_sprcls == 'node':

                            #xc[nr]
                            if m == -1:
                                sbcls_cnfg['mi'][m][i][k] = v
                                v[sprcls][sbcls] = sbcls_cnfg
                                v['mi'][-m][i][sbcls] = sbcls_cnfg

                            #nr[xc]
                            else:
                                sys.exit('ERROR')
                        else:

                            #xc[xr]
                            if m == -1:
                                sbcls_cnfg['mi'][m][i][k] = v
                                v[sprcls][sbcls] = sbcls_cnfg

                            #xr[xc]
                            else:
                                v['mi'][-m][i][sbcls] = sbcls_cnfg
                                sbcls_cnfg[v_sprcls][k] = v
        return new_cnfg

    def fill_mi(self,sbcls_cnfg,r0_cnfg,i=0,m=0,locked=[None,False,0]):
        self.cnt += 1
        if m < -20:
            sys.exit('ERROR')
        if m > 20:
            sys.exit('ERROR')
        i = int(i)
        m = int(m)
        sbcls     = sbcls_cnfg['subclass']
        mi        = sbcls_cnfg['mi']
        r0_mi    = r0_cnfg['mi']

        if sbcls_cnfg['subclass'] == r0_cnfg['subclass'] and locked[1]:
            return True
        if locked[1]:
            i +=1

        if not locked[0] or locked[0] == 'up':
            if not locked[0]:
                locked[0] = 'up'
            for p,pv in r0_mi[-1][0].items():
                m -= 1
                print(f"{'    '*abs(m)}r- {sbcls_cnfg['subclass']} {m},{i} {pv['subclass']} {locked}")
                if not (m == 0 and i==0):
                    mi[m][i][p] = pv
                    pv['mi'][-m][i][sbcls] = sbcls_cnfg

                old_locked = copy.deepcopy(locked)
                if not locked[1]:
                    locked = ['down',True,locked[2]]
                    for k,v in pv['mi'][1][i].items():
                        m+=1
                        print(f"{'    '*abs(m)}r+ {sbcls_cnfg['subclass']} {m},{i+1} {v['subclass']} {locked}")
                        mi[m][i+1][k] = v
                        v['mi'][-m][i+1][sbcls] = sbcls_cnfg
                        self.fill_mi(sbcls_cnfg,v,i+1,m,locked=locked)
                        m-=1
                locked = old_locked
                self.fill_mi(sbcls_cnfg,pv,i,m,locked=locked)
                m+=1



            #for sbcls, sbcls_cnfg in self.cnfg.items():
            #    self.fill_mi(sbcls_cnfg,sbcls_cnfg)

                ## val type
                #carrier = sbcls_cnfg['carrier']
                #sbcls_val = carrier
                #if sbcls_val is not None:
                #    if isinstance(sbcls_val,dict) and len(list(sbcls_val.keys())):
                #        for k,v in sbcls_val.items():
                #            retu, new_v = validate_item(
                #                v,
                #                desired_item_type='op',
                #                desired_namestr='type')
                #            sbcls_val[k] = new_v

                #    if sbcls_cnfg['val']['type'] != 'predefined':
                #        if isinstance(sbcls_val,list):
                #            pass
                #        elif isinstance(sbcls_val,dict):
                #            pass
                #else:
                #    retu, sbcls_val = validate_item(
                #        sbcls_cnfg['val']['type'],
                #        desired_item_type='op',
                #        desired_namestr='type')
                #if (sbcls_cnfg['superclass'] == 'node'):
                #    tscope = sbcls_cnfg['val']['tscope']
                #    for item in tscope:
                #        retu,res = validate_item(item, desired_item_type='op',desired_namestr='mi',err=True,cnfg=self.cnfg)
                #        m = res[0]
                #        i = res[1]
                #        res  = res[2]
                #        if m == '-m' and i == 'i': 
                #            if sbcls_cnfg['superclass'] == 'prop':
                #                self.ptbls[sbcls] = {'name':sbcls, 'table':[]}
                #                for k in eres[0].keys():
                #                    utbl = {
                #                        'tbls_used': [k,sbcls],
                #                        'tbl': []
                #                    }
                #                    self.utbls.append(utbl)
                #            elif sbcls_cnfg['superclass'] == 'attr':
                #                self.atbls[sbcls] = {'name':sbcls, 'table':[]}
                #                for k in eres[0].keys():
                #                    utbl = {
                #                        'tbls_used': [k,sbcls],
                #                        'tbl': []
                #                    }
                #                    self.utbls.append(utbl)
                #        elif m == '-1' and i == '0': 
                #            if sbcls_cnfg['superclass'] == 'prop':
                #                for k in eres[0].keys():
                #                    self.ntbls[k]['ptables'] = {'name':sbcls, 'table':[]}
                #                    utbl = {
                #                        'tbls_used': [k,sbcls],
                #                        'tbl': []
                #                    }
                #                    self.utbls.append(utbl)
                #            elif sbcls_cnfg['superclass'] == 'attr':
                #                for k in eres[0].keys():



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
##MASTER
import copy
import sys
from ohmfa.config_parser import (is_desired_item, process_item)
from ohmfa.ohmfa import Ohmfa

class PathResolver2(Ohmfa):

    def __init__(self,debug=False):
        super().__init__()
        self.debug=True

    def start_recursion(self, bp:list, ar:list):  
        self.o = None
        return self._m(bp, ar)

## UTILITES ##########################################################

    def _get_curr_idx(self):
        return self.o['ida'][-1]

    def _get_lvl(self):
        return (len(self.o['ida'])-1)

    def _get_prev_ida(self):
        if not self._get_lvl():
            sys.exit()
        p_ida = copy.deepcopy(self.o['ida'])
        if self.o['ws'][-2]['lvl'] > self._get_lvl():
            p_ida[-1] -= 1
            p_ida.append(self.o['ws'][-2]['idx'])
            return p_ida
        elif self.o['ws'][-2]['lvl'] < self._get_lvl():
            p_ida.pop(-1)
            p_ida[-1] -= 1
            return p_ida

    def _get_parent_array(self,key):
        if self._get_lvl() == 0:
            sys.exit()
        parent_array = self.o[key]
        for n in range(0,self._get_lvl() - 1, 1 ):
            parent_array = parent_array[self.o['ida'][n]]
        return parent_array

## SETTERS ##########################################################

    def _get_cur(self):
        args = [self.o['a'], self.o['b']]
        for n in range(0,self._get_lvl(),1):
            args = [arg[self.o['ida'][n]] for arg in args]
        self.o['ws'][-1]['a'] = args[0]
        self.o['ws'][-1]['b'] = args[1]

    def _get_delims(self):
        if len(self.o['ws'][-1]['b']):
            #get delims
            nmstr, item_type, args = process_item( copy.deepcopy(self.o['ws'][-1]['b'][0]) )
            if item_type == 'op' and nmstr == 'delims':
                self.o['ws'][-1]['delims'] = args[0][0]
                self.o['ws'][-1]['b'].pop(0)
            elif self._get_lvl() == 0:
                self.o['ws'][-1]['delims'] = '/'
            else:
                sys.exit('Error: missing delims')
            #apply delims
            if not isinstance(self.o['ws'][-1]['a'],list):
                if self._get_lvl() > 0:
                    arg = self.o['a']
                    parent_array = self._get_parent_array('a')
                    parent_array[self.o['ida'][-2]] =self.o['ws'][-1]['a'].split(self.o['ws'][-1]['delims'])
                    self.o['ws'][-1]['a'] = parent_array[self.o['ida'][-2]]
                else:
                    self.o['a'] = self.o['ws'][-1]['a'].split(self.o['ws'][-1]['delims'])
                    self.o['ws'][-1]['a'] = self.o['a']

    def _gen_ze(self):
        if self.o['ws'][-1]['z'] is not None:
            sys.exit()
        if self._get_lvl():
            p_ida = self._get_prev_ida()
            if self.o['ws'][-2]['lvl'] > self._get_lvl():
                if self.o['ida'][-1]  -1 != p_ida[-2]:
                    sys.exit()
            elif self.o['ws'][-2]['lvl'] < self._get_lvl():
                if self.o['ida'][-2] -1 != p_ida[-1]:
                    sys.exit()
        self.o['ws'][-1]['z']=self.o['ida'][-1]+1 if not self.o['ws'][-1]['z'] else self.o['ws'][-1]['z']
        self.o['ws'][-1]['e']=next((n+self.o['ws'][-1]['z'] for n,bp_item in enumerate(iter(self.o['ws'][-1]['b'][self.o['ws'][-1]['z']:])) if isinstance(bp_item,list)),len(self.o['ws'][-1]['b']))

    def _set_r(self):
        i = self.o['ws'][-1]['z']
        while (i < self.o['ws'][-1]['e']):
            nmstr, item_type, args = process_item(copy.deepcopy(self.o['ws'][-1]['b'][i]))
            if item_type == 'op' and nmstr == 'try':
                r = {'e':i,'z0':i,'val':args[0],'ph':self.o['ws'][-1]['b'][i]}
                self.o['ws'][-1]['e'] -= 1
                self.o['ws'][-1]['r_ar'].append(r)
                self.o['ws'][-1]['b'].pop(i)
            else:
                i += 1

    def _check_empty(self) :
        if not len(self.o['ws'][-1]['b']) and not len(self.o['ws'][-1]['a']): 
            return True
        elif not len(self.o['ws'][-1]['a']): 
            return False
        else:
            return None

## MISC ##########################################################

    def _descend(self):
        retu = None
        self.o['k'] += 1
        self.o['ida'].append(-1)
        self.o['ws'].append({'delims':None,'e':None,'z':None,'a':None,'b':None,'r_ar':[],'lvl':self._get_lvl(),'idx':None,})
        self._get_cur()
        self._get_delims()
        self._gen_ze()
        self._set_r()
        retu = self._check_empty()
        if self.o['k'] == 0:
            if retu is not None:
                return retu
        return retu

    def _r(self) -> bool:
        retu=False
        for n,r in enumerate(self.o['ws'][-1]['r_ar'][::-1]):
            if  r['e'] <= self.o['ida'][-1]:
                self.o['ws'][-1]['b'][r['e']:r['e']] = r['val']
                self.o['ida'][self._get_lvl()] = r['e'] -1
                r['e'] += len(r['val'])
                self.o['ws'][-1]['e'] += len(r['val'])
                retu = True
                break
            else:
                if r['z0'] != r['e']:
                    self.o['ws'][-1]['e'] -= (r['e'] - r['z0'])
                    if not (len(self.o['ws'][-1]['r_ar']) > n+1 and self.o['ws'][-1]['r_ar'][::-1][n+1]['z0'] ==  r['z0']):
                        self.o['ida'][-1] = r['z0']-1 
                    del self.o['ws'][-1]['b'][r['z0']:r['e']]
                    r['e'] = r['z0']
        if retu:
            self.o['backtrack'] = False
        return retu

    def _ascend(self):
        self.o['k'] += 1
        self.o['ws'][-1]['idx'] = self.o['ida'][-1]

        if 0:
            if self._get_lvl() >= 0:
                if self._get_lvl() > 0:
                    if len(self.o['ws'][-1]['a']) > 1:
                        self._get_parent_array('a')[self.o['ida'][-2]] = self.o['ws'][-1]['delims'].join(self.o['ws'][-1]['a'])
                    else:
                        self._get_parent_array('a')[self.o['ida'][-2]] = self.o['ws'][-1]['a'][0]
                else:
                    if len(self.o['ws'][-1]['a']) > 1:
                        self.o['a'] = self.o['ws'][-1]['delims'].join(self.o['ws'][-1]['a'])
                        self.o['ws'][-1]['a']= self.o['a']
                    else:
                        self.o['a'] = self.o['ws'][-1]['a'][0]
                        self.o['ws'][-1]['a'] = self.o['a']

        self.o['ida'].pop(-1)
        if self._get_lvl() >= 0:
            self.o['ws'].append({'a':None,'b':None,'e':None,'z':None,'r_ar':[],'lvl':self._get_lvl(),'delims':self.o['ws'][-2]['delims']})
            self._get_cur()
            self._gen_ze()
            self._set_r()

    def _backtrack(self):
        self.o['backtrack'] = True
        if self.o['k'] != 0:
            if self.o['ws'][-2]['lvl'] > self._get_lvl():
                self.o['ida'][-1] -= 1
                self.o['ws'].pop(-1)
                self.o['ws'][-1]['idx'] -= 1
                self.o['ida'].append(self.o['ws'][-1]['idx'])
            elif self.o['ws'][-2]['lvl'] < self._get_lvl():
                for r in self.o['ws'][-1]['r_ar']: 
                    self.o['ida'][-1] = r['z0']-1 
                    del self.o['ws'][-1]['b'][r['z0']:r['e']]
                    self.o['ws'][-1]['b'][r['z0']:r['z0']] = [r['ph']]
                    self.o['ws'][-1]['r_ar'].pop(-1)
                self.o['ws'][-1]['b'].insert(0,f"_delims({self.o['ws'][-1]['delims']})")
                if len(self.o['ws'][-1]['a']) > 1:
                    self.o['ws'][-2]['a'][self.o['ida'][-2]] = self.o['ws'][-1]['delims'].join(self.o['ws'][-1]['a'])
                else:
                    self.o['ws'][-2]['a'][self.o['ida'][-2]] = self.o['ws'][-1]['a'][0]
                self.o['ida'].pop(-1)
                self.o['ida'][-1] -= 1
                self.o['ws'].pop(-1)
        else:
            self.o['ida'] = []
        self.o['k'] -= 1

## MAIN ##########################################################
    def _m(self,b,a) -> bool:
        self.o={'k':-1,'a':a,'b':b,'ida':[],'ws':[],'backtrack':False}
        dres = self._descend()
        if dres is not None:
            self.logger.debug(f"{dres}")
            return dres
        while(self._get_lvl() > -1):
            self.logger.debug(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            self._logthis()
            while( self.o['ida'] and self.o['ida'][-1] < self.o['ws'][-1]['e']):
                #c_idx < e
                self.o['ida'][-1] += 1
                self.logger.debug(f"=========")
                self._logthis()
                if self.o['ida'][-1] == len(self.o['ws'][-1]['a']):
                    #c_idx == len(c_ar)
                    if len(self.o['ws'][-1]['b']) > self.o['ida'][-1]:
                        #len(c_bp) > c_idx
                        if not self._r():
                            self._backtrack()
                    elif self.o['backtrack']:
                        if not self._r():
                            self._backtrack()
                    else:
                        self._ascend()
                elif self.o['ida'][-1] == self.o['ws'][-1]['e']: 
                    #c_idx == e
                    if self.o['ws'][-1]['e'] == len(self.o['ws'][-1]['b']):
                        #len(c_bp) == e
                        if not self._r():
                            self._backtrack()
                    elif self.o['backtrack']:
                        if not self._r():
                            self._backtrack()
                    else:
                        self._descend()
                else:
                    nmstr,item_type,args = process_item(copy.deepcopy(self.o['ws'][-1]['b'][self.o['ida'][-1]]))
                    if item_type == 'vr':
                        retu=True
                    elif self.o['ws'][-1]['a'][self.o['ida'][-1]] != self.o['ws'][-1]['b'][self.o['ida'][-1]]:
                        if not self._r():
                            self._backtrack()
        if self.o['k'] >= 0:
            return True
        else:
            return False

## VERBOSE ##########################################################

    def print_nested_list(self, nested_list):
        output = []
        for item in nested_list:
            if isinstance(item, list):
                output.append(self.print_nested_list(item))
            elif isinstance(item, str):
                output.append(item.replace("'", "").replace('"', ''))
            else:
                output.append(str(item))
        return '[' + ', '.join(output) + ']'

    def _logthis(self):
        if self.debug:
            o = copy.deepcopy(self.o)
            wsk = o['ws'][-1]
            c_bp = wsk['b']
            c_ar = wsk['a']
            z = wsk['z']
            e = wsk['e']
            i = self._get_curr_idx()
            lvl = self._get_lvl()
            self.logger.debug(f"~ {o['k']}@{lvl} [{z} {i} {e}] BACKTRACK: {self.o['backtrack']}")
            if c_bp:
                if i - z == -1:
                    #PRE
                    if e == z:
                        if len(c_bp) == e:
                            c_bp[z-1] = str(c_bp[z-1]) + '!<>'
                        else:
                            c_bp[z] = '!<>' + str(c_bp[z])
                    else:
                        c_bp[z] = '!<' + str(c_bp[z])
                        c_bp[e-1] = str(c_bp[e-1]) + '>'
                elif i >= z and e > i:
                    #INDEXING
                    c_bp[i]   = '{' + str(c_bp[i]) + '}'
                    c_bp[z]   = '<' + str(c_bp[z])
                    c_bp[e-1] = str(c_bp[e-1]) + '>'
                elif i == e:
                    #EXHAUSTION
                    if e == z:
                        if len(c_bp) == e:
                            c_bp[z-1] = str(c_bp[z-1]) + '<>!'
                        else:
                            c_bp[z] = '<>!' + str(c_bp[z])
                    else:
                        c_bp[z] = '<' + str(c_bp[z])
                        c_bp[e-1] = str(c_bp[e-1]) + '>!'
            else:
                if i - z == -1:
                    c_bp.append('!<>')
                elif i == e:
                    c_bp.append('<>!')
            if c_ar:
                if len(c_ar) < e:
                    e = len(c_ar)
                    if i - z == -1:
                        #PRE
                        if e == z:
                            if len(c_ar) == e:
                                c_ar[z-1] = c_ar[z-1] + '!<$'
                            else:
                                c_ar[z] = '!<$' + c_ar[z]
                        else:
                            c_ar[z] = '!<' + c_ar[z]
                            c_ar[e-1] = c_ar[e-1] + '$'
                    elif i >= z and e > i:
                        #INDEXING
                        c_ar[i]   = '{' + c_ar[i] + '}'
                        c_ar[z]   = '<' + c_ar[z]
                        c_ar[e-1] = c_ar[e-1] + '$'
                    elif i == e:
                        #EXHAUSTION
                        if e == z:
                            if len(c_ar) == e:
                                c_ar[z-1] = c_ar[z-1] + '<$!'
                            else:
                                c_ar[z] = '<$!' + c_ar[z]
                        else:
                            c_ar[z] = '<' + c_ar[z]
                            c_ar[e-1] = c_ar[e-1] + '$!'

                elif len(c_ar) >= e:
                    if i - z == -1:
                        #PRE
                        if e == z:
                            if len(c_ar) == e:
                                c_ar[z-1] =  str(c_ar[z-1]) + '!<>'
                            else:
                                c_ar[z] = '!<>' + c_ar[z]
                        else:
                            c_ar[z] = '!<' + c_ar[z]
                            c_ar[e-1] = c_ar[e-1] + '>'
                    elif i >= z and e > i:
                        #INDEXING
                        c_ar[i]   = '{' + c_ar[i] + '}'
                        c_ar[z]   = '<' + c_ar[z]
                        c_ar[e-1] = c_ar[e-1] + '>'
                    elif i == e:
                        #EXHAUSTION
                        if e == z:
                            if len(c_ar) == e:
                                c_ar[z-1] = str(c_ar[z-1]) + '<>!' 
                            else:
                                c_ar[z] = '<>!' + c_ar[z]
                        else:
                            c_ar[z] = '<' + c_ar[z]
                            c_ar[e-1] = c_ar[e-1] + '>!'
            else:
                if len(c_ar) < e:
                    e = len(c_ar)
                    if i - e == -1:
                        c_ar.append('!<$')
                    elif i == e:
                        c_ar.append('<$!')
                elif len(c_ar) >= e:
                    if i - e == -1:
                        c_ar.append('!<>')
                    elif i == e:
                        c_ar.append('<>!')

            self.logger.debug(f"~ AR: {self.print_nested_list(o['a'])}")
            self.logger.debug(f"~ BP: {self.print_nested_list(o['b'])}")

## TESTS ##########################################################

if __name__ == "__main__":
    from ohmfa.main import Main
    o = Main(log_level=10)
    pr = PathResolver2()
    res = []
    args = [
        [[],     [],                 True],
        [['a'],  [],                 False],
        [[],     ['b'],              False],
        [['a'],  ['b'],              False],
        [['b'],  ['b'],              True],
        [[],     ['_delims(/)'],     True],
        [['a'],  ['_delims(/)'],     False],
        [[],     ['_delims(/)','b'], False],
        [['a'],  ['_delims(/)','b'], False],
        [['b'],  ['_delims(/)','b'], True],
        [[],     ['_try(b)'],        True],
        [['a'],  ['_try(b)'],        False],
        [['b'],  ['_try(b)'],        True],
        [['1', '2', '2.3', 'v'], ['1', '_try(2)', ['_delims(.)', '2', '_try(3)'], '_try(_val()_)'], True],
        [
            [ 'b', 'c',             'c',            'd',                  'iuua.b.b',                                                     'e',                           'c'], 
            [ 'b', '_try(_val()_)', 'c', '_try(f)', 'd', [ '_delims(uu)', 'i', [ '_delims(.)', 'a', 'b', '_try(b)', ], ], [ '_delims(.)', '_val()_', '_try(_val()_)', ], 'c', ],
            True,
        ],
        [['b', 'c', 'c', 'd', 'iuua.b.b', 'e', 'c'], [ 'b', '_try(_val()_)', 'c', '_try(c)','_try(f)', 'd', [ '_delims(uu)', 'i', [ '_delims(.)', 'a', 'b', '_try(b)', ], ], [ '_delims(.)', '_val()_', '_try(_val()_)', ], 'd', ], False, ],
        [['a', 'b.c'],['a', ['_delims(.)', 'b', 'c']],True],
        [['a', 'b.c'],[['_delims(.)', 'b', 'c']],False],
        [['b.c','a'],[['_delims(.)', 'b', 'c']],False],
        [['folder1','folder2','folder3','fname.html'],['_try(_val()_)',['_delims(.)','_val(a)_','_try(_val(b)_)']],True],
        [['folder1','folder2','folder3','fname'],['_try(_val()_)',['_delims(.)','_val(a)_','_try(_val(b)_)']],True],
        [['folder1','folder2','folder3','fname'],['_try(_val()_)',['_delims(,)','_val(a)_','_try(_val(b)_)']],True],
        [['folder1','folder2','folder3','fname.html'],['_try(_val()_)',['_delims(,)','_val(a)_','_try(_val(b)_)']],True],
        [['folder1','folder2','folder3','fname.html'],['_try(_val()_)','_try(_val()_)',['_delims(.)','_val(a)_']],False],
        [['folder1','folder2','folder3','fname.html'],['_try(_val()_)',['_delims(.)','_try(_val(a)_)']],True],
        [['folder1','folder2','folder3','fname.html'],['_try(_val()_)','_try(_val()_)',['_delims(.)','_try(_val(a)_)']],True],
        [['a','b','c'],['a','_try(b;c)'],True],
        [['a','b','c'],['a','_try(b;d)'],False],
        [['a','b','c'],['a','_try(b;d)'],False],
        [['b'],['_try(a)','b','_try(c)'],True],
        [['a'],['_try(a)','_try(b)'],True],
        [['a'],['_try(a)','_try(b)','_try(c)'],True],
        [['a'],['_try(a)','_try(b)','_try(c)', '_try(d)'],True],
        [['y','a'],['y','_try(a)','_try(b)'],True],
        [['y','a'],['y','_try(a)','_try(b)','_try(c)'],True],
        [['y','a'],['_try(a)','_try(b)','_try(c)','y','_try(a)','_try(b)','_try(c)'],True],
    ]
    args2 = copy.deepcopy(args)
    r = []
    v = []
    for arg in args:
        ar = arg[0]
        bp = arg[1]
        print('')
        print('')
        print('')
        print('')
        print('>%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
        print(f"ar({ar})")
        print(f"bp({bp})")
        retu = pr.start_recursion(bp,ar)
        r.append(retu)
        v.append(pr.o['a'])

    res = []
    for i,arg in enumerate(args2):
        ar = arg[0]
        bp = arg[1]
        if r[i]==arg[2]:
            res.append(1)
            print(f"    Pass {ar} || {bp}")
        else:
            print(f"    Fail {ar} || {bp}")
            res.append(0)
        print(f"    {v[i]}")
        print("")
    if 0 in res:
        print(f"FAIL")
    else:
        print(f"PASS")



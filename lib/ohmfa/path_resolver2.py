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



    def _get_lvl(self):
        return (len(self.o['ida'])-1)



    def _get_wsk(self,key):
        wsk = self.o['ws'][-1]
        return wsk[key]



    def _get_curr_idx(self):
        ida = self.o['ida']
        lvl = self._get_lvl()
        i = ida[lvl]
        return i


    def print_nested_list(self, nested_list):
        output = []
        for item in nested_list:
            if isinstance(item, list):
                # If it's a nested list, recursively call the function
                output.append(self.print_nested_list(item))
            elif isinstance(item, str):
                # If it's a string, remove quotes and append
                output.append(item.replace("'", "").replace('"', ''))
            else:
                # For other data types, convert to string and append
                output.append(str(item))
        # Join the elements with a comma and space, and enclose in brackets
        return '[' + ', '.join(output) + ']'



    def _get_cur(self) ->list:
        ida = self.o['ida'] 
        wsk = self.o['ws'][-1]
        args = [self.o['a'], self.o['b']]
        for n in range(0,len(ida)-1,1):
            args = [arg[ida[n]] for arg in args]
        wsk['a'] = args[0]
        wsk['b'] = args[1]



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



    def _r(self) -> bool:
        retu=False
        r_ar = self._get_wsk('r_ar')
        c_bp = self._get_wsk('b')
        lvl  = self._get_lvl()
        ida  = self.o['ida']
        wsk  = self.o['ws'][-1]
        for r in r_ar[::-1]:
            if  r['e'] <= self._get_curr_idx():
                c_bp[r['e']:r['e']] = r['val']
                new_idx = r['e'] -1
                r['e'] += len(r['val'])
                self.o['ws'][-1]['e'] += len(r['val'])
                ida[lvl] = new_idx
                retu = True
                break
            else:
                if r['z0'] != r['e']:
                    span = (r['e'] - r['z0'])
                    self.o['ws'][-1]['e'] -= span
                    #self.o['ws'][-1]['e'] += 1
                    self.o['ida'][-1] = r['z0']-1 
                    del c_bp[r['z0']:r['e']]
        if retu:
            self.o['backtrack'] = False
        return retu
        


    def _get_delims(self):
        lvl  = self._get_lvl()
        wsk  = self.o['ws'][-1]
        c_bp = wsk['b']
        c_ar = wsk['a']
        ida  = self.o['ida'] 
        if len(c_bp):
            nmstr, item_type, args = process_item( copy.deepcopy(c_bp[0]) )
            if item_type == 'op' and nmstr == 'delims':
                wsk['delims'] = args[0][0]
                c_bp.pop(0)
            elif lvl == 0:
                wsk['delims'] = '/'
            else:
                sys.exit('Error: missing delims')
            if not isinstance(c_ar,list):
                delims = wsk['delims']
                new_wsk_a = c_ar.split(delims)
                if len(ida) == 1:
                    self.o['a'] = new_wsk_a
                    wsk['a'] = self.o['a']
                else:
                    arg = self.o['a']
                    for n in range(0,len(ida)-1,1):
                        if n == len(ida)-2:
                            arg[ida[n]] = new_wsk_a
                            wsk['a'] = arg[ida[n]]
                        else:
                            arg = arg[ida[n]]



    def _check_empty(self) :
        wsk = self.o['ws'][self.o['k']]
        c_bp = wsk['b']
        c_ar = wsk['a']
        lvl = self._get_lvl()
        retu = None
        if not len(c_bp) and not len(c_ar): 
            retu=True
        elif not len(c_ar): 
            retu=False
        return retu



    def _get_virtual(self):
        wsk = self.o['ws'][-1]
        i   = self._get_curr_idx()
        z   = self._get_wsk('z')
        # Determin z if not defined
        if z is None:
            wsk['z'] = i + 1
            z        = self._get_wsk('z')
        # Determin e of BP sliced at "z:""
        e = z
        if wsk['b']:
            bp_slice = wsk['b'][z:]
            for bp_item in bp_slice:
                if isinstance(bp_item, list):
                    break
                else:
                    e += 1
        wsk['e'] = e
        # Sanity Checks
        if e < z:
            sys.exit(f"ERROR: z({z}) exceeds e({e})!")


    def _backtrack(self):
        self.o['backtrack'] = True
        retu = False
        if self.o['k'] != 0:
            retu = True
            ida = self.o['ida']
            # current
            wsk    = self.o['ws'][-1]
            delims = wsk['delims']
            lvl    = self._get_lvl()
            c_bp   = wsk['b']
            c_ar   = wsk['a']
            # new
            new_wsk  = self.o['ws'][-2]
            nlvl     = new_wsk['l']
            new_c_ar = new_wsk['a']
            if nlvl > lvl:
                # current
                ida[-1] -= 1
                self.o['ws'].pop(-1)
                # new
                new_wsk['i'] -= 1
                new_i = new_wsk['i']
                ida.append(new_i)
            elif nlvl < lvl:
                # restor _r
                r_ar = wsk['r_ar']
                for r in r_ar: 
                    span = (r['e'] - r['z0'])
                    self.o['ida'][-1] = r['z0']-1 
                    del c_bp[r['z0']:r['e']]
                    c_bp[r['z0']:r['z0']] = [r['ph']]
                    r_ar.pop(-1)
                # restor delims
                c_bp.insert(0,f"_delims({delims})")
                j = self.o['ida'][nlvl]
                if len(c_ar) > 1:
                    new_item = delims.join(c_ar)
                else:
                    new_item = c_ar[0]
                new_c_ar[j] = new_item
                # finalize
                ida.pop(-1)
                ida[-1] -= 1
                self.o['ws'].pop(-1)
            self.o['k'] -= 1
        return retu



    def _ascend(self):
        self.o['k'] += 1
        i = self._get_curr_idx()
        wsk = self.o['ws'][-1]
        wsk['i'] = i
        ida = self.o['ida']
        ida.pop(-1)
        lvl = self._get_lvl()
        if lvl >= 0:
            prev_wsk = self.o['ws'][-2]
            delims = prev_wsk['delims'],
            self.o['ws'].append({
                    'delims': delims,
                    'a': None,
                    'b': None,
                    'e' : None,
                    'z' : None,
                    'r_ar': [],
                    'l': lvl
                })
            self._get_cur()
            self._get_virtual()
            self._set_r()



    def _descend(self):
        retu = None
        self.o['k'] += 1
        ida = self.o['ida']
        ida.append(-1)
        lvl = self._get_lvl()
        self.o['ws'].append({
                'delims': None,
                'e' : None,
                'z' : None,
                'a': None,
                'b': None,
                'r_ar': [],
                'l' : lvl,
            })
        self._get_cur()
        self._get_delims()
        self._get_virtual()
        self._set_r()
        retu = self._check_empty()
        if self.o['k'] == 0:
            if retu is not None:
                return retu
        return retu



    def _set_r(self):
        wsk = self.o['ws'][-1]
        c_bp = wsk['b']
        ida = self.o['ida']
        e = wsk['e']
        z = wsk['z']
        c_bp_slice = c_bp[e:]

        i = z
        while (i < e):
            bp_item = c_bp[i]
            nmstr, item_type, args = process_item(copy.deepcopy(bp_item))
            if item_type == 'op' and nmstr == 'try':
                r_val = args[0]
                r = {
                    'e':   i,
                    'z0':  i,
                    'val': r_val,
                    'ph':  bp_item
                }
                wsk['e'] -= 1
                e = wsk['e']
                wsk['r_ar'].append(r)
                c_bp.pop(i)
            else:
                i += 1



    def _m(self,b,a) -> bool:
        self.o = {
            'k': -1,
            'a': a,
            'b': b,
            'ida': [],
            'ws': [],
            'backtrack': False
        }
        dres = self._descend()
        if dres is not None:
            self.logger.debug(f"{dres}")
            return dres

        while(self._get_lvl() > -1):
            retu = False
            self.logger.debug(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            self._logthis()
            i = self._get_curr_idx()
            e = self._get_wsk('e')

            while( self._get_curr_idx() < e):
                self.logger.debug(f"=========")
                retu=False
                ida  = self.o['ida']
                wsk  = self.o['ws'][-1]
                e    = wsk['e']
                C_AR = wsk['a']
                C_BP = wsk['b']
                ida[-1] += 1
                i    = self._get_curr_idx()
                self._logthis()


                if i == len(C_AR):
                    g = i
                    if g < e:
                        if not self._r():
                            break
                        continue
                    elif g == e:
                        if len(C_BP) > e:
                            if not self._r():
                                break
                            continue
                        elif self.o['backtrack']:
                            if not self._r():
                                break
                            continue
                        else:
                            retu = True
                            break
                    else:
                        sys.exit(f"ERROR ar")

                elif i == e: 
                    if e == len(C_BP):
                        if not self._r():
                            break
                        continue
                    elif e < len(C_BP):
                        if self.o['backtrack']:
                            if not self._r():
                                break
                            continue
                        else:
                            retu = True
                            break
                    else:
                        sys.exit('ERROR bp')

                bp_item = C_BP[i]
                item    = C_AR[i]
                nmstr,item_type,args = process_item(copy.deepcopy(bp_item))
                if item_type == 'vr':
                    retu=True
                    continue
                if item != bp_item:
                    if not self._r():
                        break
                    continue
                else:
                    retu = True

            if retu:
                if i >= len(C_BP):
                    self._ascend()
                elif isinstance(C_BP[i],list):
                    self._descend()
                else:
                    sys.exit('Error end')
            else:
                if not self._backtrack():
                    break

        self.logger.debug(f"{retu}")
        return retu



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
        [['b', 'c', 'c', 'd', 'iuua.b.b', 'e', 'c'], [ 'b', '_try(_val()_)', 'c', '_try(f)', 'd', [ '_delims(uu)', 'i', [ '_delims(.)', 'a', 'b', '_try(b)', ], ], [ '_delims(.)', '_val()_', '_try(_val()_)', ], 'd', ], False, ],
        [['a', 'b.c'],['a', ['_delims(.)', 'b', 'c']],True],
        [['a', 'b.c'],[['_delims(.)', 'b', 'c']],False],
        [['b.c','a'],[['_delims(.)', 'b', 'c']],False],
        [['folder1','folder2','folder3','fname.html'],['_try(_val()_)',['_delims(.)','_val(a)_','_try(_val(b)_)']],True],
        [['folder1','folder2','folder3','fname'],['_try(_val()_)',['_delims(.)','_val(a)_','_try(_val(b)_)']],True],
        [['folder1','folder2','folder3','fname'],['_try(_val()_)',['_delims(,)','_val(a)_','_try(_val(b)_)']],True],
        [['folder1','folder2','folder3','fname.html'],['_try(_val()_)',['_delims(,)','_val(a)_','_try(_val(b)_)']],True],
        [['folder1','folder2','folder3','fname.html'],['_try(_val()_)',['_delims(.)','_val(a)_']],False],
        [['folder1','folder2','folder3','fname.html'],['_try(_val()_)',['_delims(.)','_try(_val(a)_)']],True],
        [['folder1','folder2','folder3','fname.html'],['_try(_val()_)','_try(_val()_)',['_delims(.)','_try(_val(a)_)']],True],
        [['a','b','c'],['a','_try(b;c)'],True],
        [['a','b','c'],['a','_try(b;d)'],False],
        [['a','b','c'],['a','_try(b;d)'],False],
        [[],[],True],
    ]
    args2 = copy.deepcopy(args)
    r = []
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

    for i,arg in enumerate(args2):
        ar = arg[0]
        bp = arg[1]
        if r[i]==arg[2]:
            print(f"Pass {ar} || {bp}")
        else:
            print(f"Fail {ar} || {bp}")
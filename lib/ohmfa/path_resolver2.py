##MASTER
import copy
import sys
from ohmfa.config_parser import (is_desired_item, process_item)
from ohmfa.ohmfa import Ohmfa

class PathResolver2(Ohmfa):


    final = False
    def __init__(self,debug=False):
        super().__init__()
        self.logger.debug(f"PathResolver.__init__()")
        self.debug=True


    def start_recursion(self, b:list, a:list):  
        self.logger.debug(f"PathResolver.start_recursion()")
        self.o = None
        self.final = False
        return self._m(b,a)


    def _logthis(self):
        if self.debug:
            o = copy.deepcopy(self.o)
            wsk = o['ws'][self.o['k']]
            z = wsk['z']
            e = wsk['e']
            iv = None



            ######### Item
            if self._get_curr_idx() != -1:
                # Virtual A
                iv = self._get_curr_idx() - self._get_wsk('z')
                if self._get_curr_idx != -1:
                    if iv < self._get_virt_len():
                        wsk['a'][iv] = str('{'+wsk['a'][iv] + '}')
                    else:
                        wsk['a'].append('!!')
                if self._get_curr_idx != -1:
                    if iv < self._get_virt_len():
                        wsk['b'][iv] = str('{'+wsk['b'][iv] + '}')
                    else:
                        wsk['b'].append('!!')

            ######### Virtual
            if z is not None:

                if z >= len(wsk['b']):
                    wsk['b'].append('<z')
                else:
                    wsk['b'][z] = '<' + str(wsk['b'][z])

                if self._get_virt_len():
                    if (e-1) >= len(wsk['b']):
                        wsk['b'].append('e>')
                    else:
                        wsk['b'][e-1] = str(wsk['b'][e-1] + '>')
                else:
                    if z >= len(wsk['b']):
                        wsk['b'][-1] = wsk['b'][-1] + 'e>'
                    else:
                        wsk['b'][z] = '>' + str(wsk['b'][z])

                # Virtual A
                if z >= len(wsk['a']):
                    wsk['a'].append('<z')
                else:
                    wsk['a'][z] = '<' + str(wsk['a'][z])

                if self._get_virt_len():
                    if (e-1) >= len(wsk['a']):
                        wsk['a'].append('e>')
                    else:
                        wsk['a'][e-1] = str(wsk['a'][e-1] + '>')
                else:
                    if z >= len(wsk['a']):
                        wsk['a'][-1] = wsk['a'][-1] + 'e>'
                    else:
                        wsk['a'][z] = '>' + str(wsk['a'][z])


            ######### CUrrent
            # Current A
            if len(wsk['a']):
                wsk['a'][0] = '|' + str(wsk['a'][0])
                wsk['a'][-1] = str(wsk['a'][-1] + '|')
            else:
                wsk['a'].append('||')

            # Current B
            if len(wsk['b']):
                wsk['b'][0] = '|' + str(wsk['b'][0])
                wsk['b'][-1] = str(wsk['b'][-1] + '|')
            else:
                wsk['b'].append('||')

            self.logger.debug(f"...i:{self._get_curr_idx()} k:{o['k']} z:{z} e:{e} iv:{iv} lvl:{self._get_lvl()}")
            self.logger.debug(f"...ar: {o['a']}")
            self.logger.debug(f"...bp: {o['b']}")


    def _r(self) -> bool:
        """_summary_
        [1  2 <|t|> 4  5 6]
        [1 <2>     |3| 4, 5]

        [1   2      |3|  4 <5>]
        [1   2   t  |4|  5 <6>]
        [1   2   t  |4|  5 <6>]
        [1  <2>  t  |4|  5  6]

        [1 2   t     |4|  5  <6>]
        [1 2   t   t |5|  6  <7>]
        [1 2  <t>  t |5|  6  <7>]
        """
        self.logger.debug(f"PathResolver._r()")
        retu=False
        r_ar = self._get_wsk('r_ar')
        c_bp = self._get_wsk('b')
        lvl = self._get_lvl()
        ida = self.o['ida']
        while(len(r_ar)):
            r = r_ar[-1] 
            self.logger.debug(f"r:{r}")
            if  r['e'] <= self._get_curr_idx():
                self.logger.debug(f"r['e']:{r['e']} <= ida[lvl]:{self._get_curr_idx()}")
                c_bp[r['e']:r['e']] = r['val']
                new_idx = r['e'] -1
                r['e'] += len(r['val'])
                self.o['ws'][-1]['e'] += len(r['val'])
                ida[lvl] = new_idx
                retu = True
                break
            else:
                span = (r['e'] - r['z0'])
                self.o['ws'][-1]['e'] -= span
                self.o['ida'][-1] = r['z0']-1 
                del c_bp[r['z0']:r['e']]
                c_bp[r['z0']:r['z0']] = [r['ph']]
                r_ar.pop(-1)

        self._logthis()

        if retu:
            self.o['backtrack'] = False
        return retu
        

    def _get_cur(self) ->list:
        self.logger.debug(f"PathResolver.get_cur()")

        ida = self.o['ida'] 
        wsk = self.o['ws'][self.o['k']]
        args = [self.o['a'], self.o['b']]

        for n in range(0,len(ida)-1,1):
            args = [arg[ida[n]] for arg in args]

        wsk['a'] = args[0]
        wsk['b'] = args[1]


    def _get_delims(self):
        self.logger.debug('PathResolver.get_delims()')
        lvl = self._get_lvl()
        wsk = self.o['ws'][-1]

        # - CHECK INVALID CURRENT ARRAYS ---------------------------------------------------------
        #if lvl > 0 and self.o['ida'] == 0:
        #    if len(c_bp) < 2:
        #        sys.exit('ERROR: bp subarrays must be of length 2 or greater')

        # Make sure not empty
        if len(wsk['b']):

            # If delims operator get delims else use default
            nmstr,item_type,args = process_item(copy.deepcopy(wsk['b'][0]))
            if item_type == 'op' and nmstr == 'delims':
                wsk['delims'] = args[0][0]
                wsk['b'].pop(0)
            elif lvl == 0:
                wsk['delims'] = '/'
            else:
                sys.exit('Error: missing delims')

            # apply the delims if not already applied
            if not isinstance(wsk['a'],list):
                wsk = self.o['ws'][-1]
                new_wsk_a = wsk['a'].split(wsk['delims'])
                arg = self.o['a']
                ida = self.o['ida'] 

                if len(ida)-1 == 0:
                    self.o['a'] = new_wsk_a
                    wsk['a'] = self.o['a']
                        
                else:
                    for n in range(0,len(ida)-1,1):
                        if n == len(ida)-1:
                            arg[ida[n]] = new_wsk_a
                            wsk['a'] = arg[ida[n]]
                        else:
                            arg = arg[ida[n]]



    def _check_empty(self) :
        self.logger.debug('PathResolver.check_empty()')
        wsk = self.o['ws'][self.o['k']]
        lvl = self._get_lvl()
        retu = None

        if not len(wsk['b']) and not len(wsk['a']): 
            if lvl == 0:
                retu=True
            else:
                sys.exit('ERROR: subarrays cannot be empty')
        elif not len(wsk['b']):
            if lvl == 0:
                retu=False
            else:
                sys.exit('ERROR: subarrays cannot be empty')
        elif not len(wsk['a']): 
            if lvl == 0:
                retu=False
            else:
                sys.exit('ERROR: subarrays cannot be empty')

        self.logger.debug(f"...{retu}")
        return retu


    def _get_virtual(self):
        self.logger.debug(f"PathResolver.get_virtual()")

        # get z if not defined
        wsk=self.o['ws'][-1]
        z = self._get_wsk('z')
        self.logger.debug(f"...z: {z}")
        if wsk['z'] is None:
            wsk['z'] = self._get_curr_idx() + 1
            self.logger.debug(f"...z: {wsk['z']}")

        # e 
        e = None
        for a_idx, bp_item in enumerate(wsk['b']):
            e = a_idx
            if isinstance(bp_item,list):
                break
        wsk['e'] = e+1
        self.logger.debug(f"...e: {wsk['e']}")


    def _get_virt_len(self):
        e = self._get_wsk('e')
        z = self._get_wsk('z')
        return (e-z)


    def _get_wsk(self,key):
        k = self.o['k']
        wsk = self.o['ws'][k]
        return wsk[key]


    def _get_curr_idx(self):
        ida = self.o['ida']
        lvl = self._get_lvl()
        curr_idx = ida[lvl]
        return curr_idx


    def _backtrack(self):

        """_summary_
        [0 1 2 [0 1 [[0 1]]] 0] 4 [0]]
        0
        1
        2
        3<>
        30     ida.pop()
        31
        32<>
        320<>  ida.pop()
        3200   ida.pop()
        3201
        3202!
        321!   ida[-1] -= 1, i-=1
        33     ida[-1] -= 1, i-=1
        34!
        4      ida[-1] -= 1, i-=1
        5<>
        50     ida.pop()
        51!
        6!     ida[-1] -= 1, i-=1
        """
        self.logger.debug(f"PathResolver._backtrack()")
        self.o['backtrack'] = True
        retu = False

        # Can we Brack Track Further?
        if self.o['k'] != 0:
            retu = True

            wsk = self.o['ws'][-1]
            old_wsk = self.o['ws'][-2]
            lvl = self._get_lvl()
            nlvl = old_wsk['l']        # set on each descent

            # Back Tracking to higher level
            if nlvl > lvl:
                self.o['ida'][-1] -= 1

                self.o['k'] -= 1
                self.o['ws'].pop(-1)

                i = self.get_wsk('i') - 1
                self.o['ida'].append(i)

            # Back Tracking to lower level
            elif nlvl < lvl:
                wsk['b'].insert(0,f"_delims({delims})")
                j = self.o['ida'][lvl-1]
                delims = self.get_wsk('delims')
                if len(self.get_wsk(a)) > 1:
                    old = delims.join(self.get_wsk('a'))
                else:
                    old = self.get_wsk('a')[0]

                self.o['ida'].pop(-1)
                self.o['k'] -= 1
                self.o['ws'].pop(-1)
                a = self.get_wsk('a')
                a[j] = old

        return retu



    def _ascend(self):
        self.logger.debug(f"PathResolver._ascend()")
        self.o['k'] += 1
        self.o['ws'][-1]['i'] = self._get_curr_idx()
        self.o['ida'].pop(-1)
        if self._get_lvl() > 0:
            self.o['ws'].append({
                    'delims': self.o['ws'][-2]['delims'],
                    'a': self.o['ws'][-2]['a'],
                    'b': self.o['ws'][-2]['b'],
                    'e' : None,
                    'z' : None,
                    'r_ar': None,
                    'l': self.o['ws'][-2]['l']
                })
            self._get_virtual()
            self._logthis()


    def _descend(self):
        self.logger.debug(f"PathResolver._descend()")
        retu = None

        self.o['k'] += 1
        self.o['ida'].append(-1)
        self.o['ws'].append({
                'delims': None,
                'e' : None,
                'z' : None,
                'a': None,
                'b': None,
                'r_ar': [],
                'l' : self._get_lvl(),
            })

        self._get_cur()
        self._logthis()
        self._get_delims()
        self._logthis()
        retu = self._check_empty()
        self._logthis()
        if retu is not None:
            return retu
        self._get_virtual()
        self._logthis()
        return retu


    def _get_virt_len(self) -> int:
        z = self._get_wsk('z')
        e = self._get_wsk('e')
        virt_len =  e-z
        return virt_len


    def _get_vi(self) -> int:
        i = self._get_curr_idx()
        z = self._get_wsk('z')
        e = self._get_wsk('e')
        vi = i - z
        return vi


    def _get_lvl(self):
        return (len(self.o['ida'])-1)


    def _m(self,b,a) -> bool:
        self.logger.debug(f"PathResolver._m()")

        # nested array variables
        self.o = {
            'k': -1,    # index of flat array
            'a':a,     # arg array
            'b':b,     # boiler plate
            'ida':[], # index of nexted array
            'ws': [],
            'backtrack': False
        }

        # Initial Descend and check for empty initial arrays
        dres = self._descend()
        if dres is not None:
            self.logger.debug(f"Exiting with dres:{dres}")
            return dres

        retu = False
        while(self._get_lvl() > -1):
            self.logger.debug(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            self.logger.debug(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            self.logger.debug(f"Begin Loop 1 ")
            self._logthis()
            while( self._get_curr_idx() < self._get_wsk('e')):
                retu=False
                self.o['ida'][-1] += 1
                self.logger.debug(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                self.logger.debug(f"Begin Loop 2 ")
                self.logger.debug(f"...vi:{self._get_vi()}")
                self._logthis()


                # ar Exhaustion
                # ida[lvl]         3 = z-va
                # va        <0 1 2>
                if self._get_curr_idx() >= self._get_wsk('e'):
                    self.logger.debug(f"i:{self._get_curr_idx()} >= e:{self._get_wsk('e')}")

                    # c_bp was not long enouph
                    if False:
                        self.logger.debug(f"e:{self._get_wsk('e')} >= lva:{len(self._get_wsk('b'))}")
                        if not self._r():
                            break
                        continue

                    # c_bp just right, meaning this mus a 'legal' exhaustion
                    else:
                        if self.o['backtrack']:
                            if not self._r():
                                break
                            continue
                        else:
                            self.logger.debug(f"e:{self._get_wsk('e')} == lva:{len(self._get_wsk('b'))}")
                            retu = True
                            break

                #b exhaustion
                elif self._get_curr_idx() >= len(self._get_wsk('b')): 
                    self.logger.debug(f"i:{self._get_curr_idx()} >= lvb:{len(self._get_wsk('b'))}") 
                    c_bp = self._get_wsk('b')

                    if not self._r():
                        break
                    continue

                i = self._get_curr_idx()
                bp_item = self._get_wsk('b')[i]
                item    = self._get_wsk('a')[i]
                self.logger.debug(f"=====================")
                self.logger.debug(f"...item: {item}")
                self.logger.debug(f"...bp_item: {item}")

                # PRE MATCHING #########################################################
                nmstr,item_type,args = process_item(copy.deepcopy(bp_item))

                # - TRY ---------------------------------------------------------
                if item_type == 'op':
                    self.logger.debug(f"...OP => {item}")
                    r_ar = self._get_wsk('r_ar')
                    if len(r_ar) and r_ar[-1]['e'] == self._get_curr_idx():
                        sys.exit("ERROR: Consecuitve Try ops not supported")
                    r = {
                        'e': self._get_curr_idx(),
                        'z0': self._get_curr_idx(),
                        'val': args[0],
                        'ph': bp_item}
                    r_ar.append(r)
                    self.o['ws'][-1]['b'].pop(self._get_curr_idx())
                    lvl = self._get_lvl()
                    self.o['ida'][lvl] -= 1
                    self.o['ws'][-1]['e'] -= 1
                    self._logthis()
                    continue

                # MATCHING #########################################################
                # - VAR ---------------------------------------------------------
                elif item_type == 'vr' and not isinstance(item,list):
                    self.logger.debug(f"vr is item:{item}")
                    retu=True

                # - LITERAL ---------------------------------------------------------
                elif item != bp_item:
                    self.logger.debug(f"item:{item} != bp_item: {bp_item}")
                    r_res = self._r()
                    if not r_res:
                        b_res = self._backtrack()
                        if not b_res:
                            break
                else:
                    retu = True

                self.logger.debug(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                self.logger.debug(f"END LOOP 1")
                self.logger.debug(f"retu:{retu}")
                self._logthis()


            self.logger.debug(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            self.logger.debug(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            self.logger.debug(f"END LOOP 2")
            self.logger.debug(f"retu:{retu}")
            self._logthis()
            if retu:
                self.logger.debug(f"retu is True")
                wsk = self.o['ws'][self.o['k']]
                i = self._get_curr_idx()
                if i >= len(wsk['b']):
                    self._ascend()
                elif isinstance(wsk['b'][i],list):
                    self._descend()
                else:
                    sys.exit('Error')
            else:
                self.logger.debug(f"retu is False")
                if not self._backtrack():
                    break
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

        [[],     [],                 True],
        [['a'],  [],                 False],
        [[],     ['_try(b)'],              False],
        [['a'],  ['_try(b)'],              False],
        #[['b'],  ['_try(b)'],              True],
        #[['b', '_try(_val()_)', 'c', '_try(f)', 'd',['_delims(uu)', 'i', ['_delims(.)', 'a', 'b', '_try(b)']],['_delims(.)','_val()_','_try(_val()_)'], 'c'],
        # ['b', 'c', 'c', 'd','iuua.b.b',                                               'e','c']],
    ]
    args2 = copy.deepcopy(args)
    print('%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%')
    r = []
    for arg in args:
        ar = arg[0]
        bp = arg[1]
        print(f"ar:{ar}")
        print(f"bp:{bp}")
        retu = pr.start_recursion(bp,ar)
        r.append(retu)

    for i,arg in enumerate(args2):
        ar = arg[0]
        bp = arg[1]
        if r[i]==arg[2]:
            print(f"Pass {ar} || {bp}")
        else:
            print(f"Fail {ar} || {bp}")

"""_summary_

[0, '_try(1)', [1 '_try(2)'], '_try(_val())']
[0, 1]           => [0,    [1]           ]
[0, 1, 1]        => [0,    [1],    v(1)  ]
[0, 1, 1.2]      => [0,    [1],    v(1.2)]
[0, 1, 1.2, 'v'] => [0, 1, [1,2],  v(v) ]
[0, 1, 1, 'v']   => [0, 1, [1],    v(v) ]
[0, 1.2]         => [0,    [1, 2]       ]
[0, 1.2 'v']     => [0,    [1,2],  v(v) ]
[0, 1, 'v']      => [0,    [1],    v(v) ]

[0, '_try(1,1,1)', [1 '_try(2,1)'], '_try(_val(),1)']
[0, 1]           => [0,    [1]          ]
[0, 1, 1]        => [0, 1, [1]          ]
[0, 1, 1.2]      => [0, 1, [1.2],       ]
[0, 1, 1.2, 'v'] => [0, 1, [1,2],  v(v) ]
[0, 1, 1, 'v']   => [0, 1, [1],    v(v) ]
[0, 1.2]         => [0,    [1, 2]       ]
[0, 1.2 'v']     => [0,    [1,2],  v(v) ]
[0, 1, 'v']      => [0,    [1],    v(v) ]


[a try(b) [b try(c)] try(v)]
[a b b.c f]

    a [b] b.c f
    a [b] 

    a [b] b.c f
    a [b] v

    a b [b c] f
    a b [b]

    a b [b c] f
    a b [b c] f

[a try(b) [b try(c)] try(v)]
[a b b.c]

    a [b] b.c
    a [b] 

    a [b] b.c
    a [b] v

[a try(b) [b try(c)] try(v)]
[a b .c]

    a [null, c]
    a [b] 


"""
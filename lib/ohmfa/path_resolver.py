"""
CAVEATS:
- All Try block items are scalars
- Default lvl 0 delim is '/'
- Default lvl 1 delim is '.'
- Non Default Delim strs must be indicated at beginning of array via "_delim({delim_str})"
- '_try' ops can not be consecutive
- all bp arrays with lvls greater that 0, must contain 2 or more items

MODEL CHARACTERISTICS:
- all 'r' values are stored and are unique to each recursion or depth as arrays to account for 
  multiple try blocks
- [x, "x", [x, "x"]] == [x, x, [x, "x"]]

"""
import copy
import sys
from lib.config_parser import (validate_item, process_item)
from ohmfa.ohmfa import Ohmfa

class PathResolver(Ohmfa):

    final = False
    gen_from_vars = False
    def __init__(self,verbose=0,prnt=0):
        super().__init__(verbose,prnt)


    def start_recursion(self, bp:list, ar:list, vrs:list =None,gen_from_vars:bool=False ):  
        self.final = False
        if vrs is None:
            vrs = []
        depth = 0
        lvl   = 0
        ida   = []
        delims = []
        if gen_from_vars:
            self.gen_from_vars = True
            ar = bp
        retu, bp, ar, vrs, delims = self._m(bp,ar,depth,ida,lvl,delims,vrs)
        self.gen_from_vars = False
        return [retu,bp,ar, vrs]


    def _m(self, bp_in:list, ar_in:list, depth:int, ida:list, lvl:int, delims:list, vrs:list) -> list:


        # _logars() ##############################################
        def _logars(ind:int, border:str, header:str, bp:list, ar:list, ida:int, lvl:int, depth:int, retu:bool, r_ar:list,v_ard,v_bpd) -> None:
            ind = 24
            r_e = None
            if len(r_ar):
                r_e = r_ar[-1]['e']
            bp = copy.deepcopy(bp)
            ar = copy.deepcopy(ar)
            c_bp, c_ar = get_cur(ida,lvl,[bp,ar])

            if ida[lvl] < len(c_bp):
                c_bp[ida[lvl]] = "<<" + str(c_bp[ida[lvl]]) + ">>"
            elif len(c_bp):
                c_bp[-1] = "((" + str(c_bp[-1]) + "))"

            if ida[lvl] < len(c_ar):
                c_ar[ida[lvl]] = "<<" + str(c_ar[ida[lvl]]) + ">>"
            elif len(c_ar):
                c_ar[-1] = "((" + str(c_ar[-1]) + "))"

            self.logthis(4,f"{'':>{ind}}{border*40}")
            self.logthis(4,f"{'':>{ind}}{header}")
            self.logthis(4,f"{'':>{ind+4}}DPTH: {depth} LVL: {lvl} orlo: {ida[lvl]+1-len(c_ar)} bporlo: {ida[lvl]+1-len(c_bp)} r_e: {r_e} retu: {retu}")
            self.logthis(4,f"{'':>{ind+4}}ar_z: {v_ard['z']} ar_e: {v_ard['e']}")
            self.logthis(4,f"{'':>{ind+4}}bp_z: {v_bpd['z']} bp_e: {v_bpd['e']}")
            self.logthis(4,f"{'':>{ind+4}}IDX:      {ida}")
            self.logthis(4,f"{'':>{ind+4}}ar:       {ar}")
            self.logthis(4,f"{'':>{ind+4}}bp:       {bp}")


        # _r() ##############################################
        def _r(c_bp,idx,r_ar,v_bpd) -> list:
            retu=False
            while(len(r_ar)):
                r = r_ar[-1] 
                if  r['e'] <= idx:
                    c_bp[r['e']:r['e']] = r['val']
                    idx = r['e']
                    r['e'] += len(r['val'])
                    idx -= 1
                    retu = True
                    break
                else:
                    del c_bp[r['z0']:r['e']]
                    c_bp[r['z0']:r['z0']] = [r['ph']]
                    r_ar.pop(-1)

            v_bpd = get_virtual(c_bp,idx,v_bpd)
            return retu, idx, r_ar,v_bpd
            

        # get_cur() ##############################################
        def get_cur(ida,lvl,args) ->list:
            for n in range(0,lvl,1):
                args = [arg[ida[n]] for arg in args]
            return args

        # get_virtual() ##############################################
        def get_virtual(c,idx,v_d=None):
            if not v_d:
                v_d = {}
                v_d['start_idx'] = idx
                v_d['z'] = idx + 1
            v_d['ar_idxs']  = [aidx+v_d['start_idx']+1 for aidx,item in enumerate(c[v_d['start_idx']+1:]) if isinstance(item,list)]

            if not len(v_d['ar_idxs']):
                v_d['e'] = len(c)
            else:
                v_d['e'] = v_d['ar_idxs'][0]
            return v_d

        # PRE LOOP #########################################################

        # - IDA ---------------------------------------------------------
        # The index array (idx_ar) is a nested array index; whose items
        # correspond to a specfic array idx at a specfic level in the nesting
        # hiearchy. The top array (ar) has a level of zero, so its current idx
        # would be idx_ar[0]
        #
        #       idx_ar = [idx_0,idx_1 ... idx_n-1, idx_n]
        #       c_ar   = ar[idx_0][idx_1]...[idx_n-1][idx_n]
        #
        # When an array in "descended" in to for the first time, the idx_ar will
        # not have indice for its index, so we must append an inital idx value
        # for that array to idx_ar.

        if len(ida)-1 < (lvl):
            ida.append(-1)

        # - GET CURRENT ARRAYS ---------------------------------------------------------
        # in order to get the current array we need only to to index the top
        # array (ar) for all the levels above the current level, unless the
        # current level. If the current level is 0, then the the current array
        # is simply the top array (ar)

        bp  = copy.deepcopy(bp_in)
        ar  = copy.deepcopy(ar_in)
        c_bp, c_ar = get_cur(ida,lvl,[bp,ar])

        # - DELIMS ---------------------------------------------------------
        if len(delims)-1 < (lvl):
            if lvl == 0:
                delims.append('/')
            elif lvl == 1:
                delims.append('.')
            else:
                delims.append('')

        if len(c_bp) and ida[lvl] == -1:
            nmstr,item_type,args = process_item(copy.deepcopy(c_bp[0]))
            if item_type == 'op' and nmstr == 'delim':
                delims[lvl] = args[0][0]
                c_bp.pop(0)
                c_bp = get_cur(ida,lvl,[bp])[0]

        # - APPLY DELIMS ---------------------------------------------------------
        new_c_ar = []
        child_delims = []
        for item in c_ar:
            if not isinstance(item,list):
                if delims[lvl]:
                    newitem = item.split(delims[lvl])
                    if len(newitem) > 1:
                        new_c_ar = new_c_ar + newitem
                        continue
            new_c_ar.append(item)
        c_ar[:] = new_c_ar[:]

        child_delims = []
        for item in c_bp:
            if isinstance(item,list):
                nmstr,item_type,args = process_item(copy.deepcopy(item[0]))
                if item_type == 'op' and nmstr == 'delim':
                    child_delims = args[0][0]

        new_c_ar = []
        if len(child_delims):
            for item in c_ar:
                if not isinstance(item,list):
                    newitem = None
                    for delim in child_delims:
                        newitem = item.split(delim)
                        if len(newitem) > 1:
                            new_c_ar.append(newitem)
                            break
                    else:
                        new_c_ar.append(item)
                    continue

                new_c_ar.append(item)
            c_ar[:] = new_c_ar[:]


        # - CHECK FOR EMPTY CURRENT ARRAYS ---------------------------------------------------------
        if not len(c_bp) and not len(c_ar): 
            if lvl == 0:
                return [True, bp, ar, vrs, delims]
            sys.exit('ERROR: subarrays cannot be empty')

        elif not len(c_bp):
            if lvl == 0:
                return [False, bp, ar, vrs, delims]
            sys.exit('ERROR: subarrays cannot be empty')

        elif not len(c_ar): 
            if lvl == 0:
                if validate_item(c_bp[0],'try','op')[0]:
                    return [True, bp, ar, vrs, delims]
                else:
                    return [False, bp, ar, vrs, delims]
            sys.exit('ERROR: subarrays cannot be empty')

        # - CHECK INVALID CURRENT ARRAYS ---------------------------------------------------------
        if lvl > 0 and ida[lvl] == -1:
            if len(c_bp) < 2:
                sys.exit('ERROR: bp subarrays must be of length 2 or greater')

        # - GET VIRTUAL ARRAYS AND VARS ---------------------------------------------------------
        v_ard = get_virtual(c_ar,ida[lvl])
        v_bpd = get_virtual(c_bp,ida[lvl])


        # - RECURSION STATE VARIABLES ---------------------------------------------------------
        depth += 1        

        # - LOOP VARIABLES ---------------------------------------------------------
        r_ar = []
        retu = False

        # # LOOP #########################################################
        while(ida[lvl] < len(c_ar)):

            # # PRE CHECKS #########################################################

            # - IDX ---------------------------------------------------------
            ida[lvl] += 1


            # - LOGGING ---------------------------------------------------------
            if ida[lvl] == v_ard['start_idx'] + 1:
                _logars(4,'-','START',bp,ar,ida,lvl,depth,retu,r_ar,v_ard,v_bpd)
            else:
                _logars(4,'-','NEXT',bp,ar,ida,lvl,depth,retu,r_ar,v_ard,v_bpd)


            # # CHECKS #########################################################
            # Checks: an item must exists at the current idx for both the bp
            # array and the given array. If the previous statment is not
            # satisfied, 'r' methods will be used and if unsusseful, then the
            # loop must break
            # - AR EXHAUSTION ---------------------------------------------------------
            # check if the current idex is out of range of 'ar'. When the ar is
            # exhausted it will always be at it's end so the real bp_len can be
            # used, instead of the virtual one
            if(ida[lvl] >= v_ard['e']):

                # c_bp was not long enouph
                if (v_ard['e']-v_ard['z']) > (v_bpd['e']-v_bpd['z']):
                    r_res, ida[lvl], r_ar, v_bpd = _r(c_bp, ida[lvl], r_ar, v_bpd)
                    if r_res:
                        continue
                    else:
                        retu = False
                    break

                # c_bp was too long
                elif (v_ard['e']-v_ard['z']) < (v_bpd['e']-v_bpd['z']):
                    retu=False

                    # check if the current bp_item is penultimate and if the
                    # next/last bp_item is a try_op
                    #if ida[lvl] + 1 == len(c_bp):
                    if ida[ lvl ] == ( v_bpd[ 'e' ] - 1 ):
                        nmstr,item_type,args = process_item(copy.deepcopy(c_bp[ida[lvl]]))
                        if nmstr == 'try':

                            # It's optional, so it is not needed and we can get
                            # rid of it and call the match succesfull
                            c_bp.pop(ida[lvl])
                            retu = True
                    break

                # c_bp just right, meaning this mus a 'legal' exhaustion
                else:
                    if v_ard['e'] == len(c_ar):
                        retu = True
                        break

            # - BP EXHAUSTION ---------------------------------------------------------
            #if ida[lvl] >= len(c_bp): 
            elif ida[lvl] >= v_bpd['e']: 
                if ( 
                    len(c_bp) == v_bpd['e']
                    or
                    len(v_bpd['ar_idxs']) == len(v_ard['ar_idxs'])
                ):
                    r_res, ida[lvl], r_ar, v_bpd = _r(c_bp, ida[lvl], r_ar, v_bpd)
                    if r_res:
                        continue
                    else:
                        retu = False
                        break

            # POST CHECKS #########################################################
            # - REtU ---------------------------------------------------------
            retu = False

            # - ITEMS ---------------------------------------------------------
            bp_item = c_bp[ida[lvl]]
            item    = c_ar[ida[lvl]]

            # PRE MATCHING #########################################################
            nmstr,item_type,args = process_item(copy.deepcopy(bp_item))

            # - LVL DECEND ---------------------------------------------------------
            if isinstance(bp_item,list):
                ar_copy = copy.deepcopy(ar)
                if not isinstance(item,list):
                    c_ar_copy = get_cur(ida,lvl,[ar_copy])[0]
                    c_ar_copy[ida[lvl]] = [item]
                retu, new_bp, new_ar, nvrs, ndelims = self._m(bp,ar_copy,depth,copy.deepcopy(ida),lvl+1,copy.deepcopy(delims),copy.deepcopy(vrs))
                if retu:
                    bp[:] = new_bp
                    ar[:] = new_ar
                    v_ard = get_virtual(c_ar,ida[lvl],v_ard)
                    vrs = nvrs
                    delims = ndelims
                else:
                    r_res, ida[lvl], r_ar, v_bpd = _r(c_bp, ida[lvl], r_ar, v_bpd)
                    if r_res:
                        continue
                break

            # - TRY ---------------------------------------------------------
            elif item_type == 'op':
                if len(r_ar) and r_ar[-1]['e'] == ida[lvl]:
                    sys.exit("ERROR: Consecuitve Try ops not supported")
                r = {
                    'e': ida[lvl],
                    'z0': ida[lvl],
                    'val': args[0],
                    'ph': bp_item}
                r_ar.append(r)
                c_bp.pop(ida[lvl])
                ida[lvl] -= 1
                v_bpd = get_virtual(c_bp,ida[lvl],v_bpd)
                continue

            # MATCHING #########################################################
            # - VAR ---------------------------------------------------------
            elif item_type == 'vr' and not isinstance(item,list):
                if self.gen_from_vars:
                    vrs2 = [vr for vr in vrs if vr[0] == nmstr ]
                    val = [vr[2] for vr in vrs2 if vr[1] == args[0][0] ][0]

                    c_ar[ida[lvl]] = val
                vrs.append([bp_item,item])
                retu=True

            # - LITERAL ---------------------------------------------------------
            elif item != bp_item:
                r_res, ida[lvl], r_ar,v_bpd = _r(c_bp,ida[lvl],r_ar,v_bpd)
                if r_res:
                    continue
                break
            else:
                retu = True

        # POST LOOP #########################################################
        # - LVL ASCEND ---------------------------------------------------------
        if lvl > 0 and ida[lvl] == len(c_ar) and retu:
            nidx = copy.deepcopy(ida) 
            nidx.pop(-1)
            retu, new_bp, new_ar, nvrs, ndelims = self._m(bp,ar,depth,nidx,lvl-1,copy.deepcopy(delims),copy.deepcopy(vrs))
            if retu:
                bp[:] = new_bp
                ar[:] = new_ar
                vrs = nvrs

        # FINAL ----------
        _logars(4,'-','FINAL',bp,ar,ida,lvl,depth,retu,r_ar,v_ard,v_bpd)
        if retu and (self.final or (lvl== 0 and ida[lvl] == len(c_bp))):
            self.final = True
            if len(c_ar) > v_ard['e']:
                if isinstance(c_ar[v_ard['e']],list):
                    items = c_ar[v_ard['e']]
                    c_ar[v_ard['e']] = delims[lvl+1].join(items)
            if lvl == 0 and v_ard['z'] == 0:
                items = c_ar[:]
                c_ar[:] = [delims[lvl].join(items)]

        print(vrs)
        return [retu, bp, ar, vrs, delims]